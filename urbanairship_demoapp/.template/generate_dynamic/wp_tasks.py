import logging
import os
from os import path
import re
import shutil
from subprocess import PIPE, STDOUT
import tempfile
import time

import lib
from lib import task
from utils import run_shell

LOG = logging.getLogger(__name__)


class WPError(lib.BASE_EXCEPTION):
	pass

@task
def build_wp(build, new_working_dir):
	original_dir = os.getcwd()
	build_cmd = [
		'c:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe',
		'Forge.sln',
		'/t:Forge',
		'/p:Configuration=Release'
	]
        LOG.info('Changing dir to do Visual Studio build: %s, was in %s' % (new_working_dir, original_dir))
	try:
		os.chdir(new_working_dir)
		msbuild = lib.PopenWithoutNewConsole(build_cmd, stdout=PIPE, stderr=STDOUT)
		out = msbuild.communicate()[0]
		if msbuild.returncode != 0:
			build.log.error('Visual Studio build error: %s' % out)
			raise Exception('Visual Studio build error')
		else:
			build.log.debug('Visual Studio build output: %s' % out)
	finally:
		os.chdir(original_dir)


@task 
def package_wp(build):
        path_to_wp_build  = path.abspath(path.join('development', 'wp'))
        try: 
                relative_path_to_marketplace_artwork = build.config['icons']['wp']['173']
        except:
                relative_path_to_marketplace_artwork = None

        _create_xap_from_app(
                build=build,
                path_to_wp_build=path_to_wp_build,
                target='release',
                relative_path_to_marketplace_artwork=relative_path_to_marketplace_artwork,
        )


@task
def test_wp(build, device):
        _create_xap_from_app(
                build=build,
                path_to_wp_build=path.abspath('wp'), 
                target='.'
        )


@task
def run_wp(build, device):
        path_to_wp_build  = path.abspath(path.join('development', 'wp'))

        path_to_xap = _create_xap_from_app(
                build=build,
                path_to_wp_build=path_to_wp_build,
                target='development'
        )
        LOG.info('Running: %s' % path_to_xap)

        automation = path.join(path_to_wp_build, "automation", "bin", "Release", "automation.exe")
        if not path.exists(automation):
                raise WPError("Couldn't find Windows Phone deployment tool")
        
	if not device or device.lower() == 'simulator': 
		LOG.info('Running Windows Phone Emulator')
                target = 'emulator'
	else:
		LOG.info('Running on Windows Phone device: {device}'.format(device=device))
                target = 'device'

        run_shell(automation, path_to_xap, target, fail_silently=False, verbose=True, logger=LOG)


# builds the application xap file
def _create_xap_from_app(build, path_to_wp_build, target, relative_path_to_marketplace_artwork = None):
        """Create an ipa from an app

        :param build: instance of build
        :param path_to_wp_build: Absolute path to wp directory
        :param relative_path_to_marketplace_artwork: (Optional) A path to 99x99 and 173x173 png images 
               for the Windows Phone Marketplace catalog. This should be relative to the location of
               the user assets.
               """
        LOG.info('Starting package process for Windows Phone')
        
        manifest = [
		'Properties/',
                'Properties/WMAppManifest.xml',
                'build/Release/AppManifest.xaml',  
                'build/Release/Forge.dll',
		'lib/Silverlight_ZXing_Core.dll',
                'lib/Newtonsoft.Json.dll',
                'lib/Newtonsoft.Json.xml', 
                'Icons/',  # TODO lose?
                'assets/',
                'dist/',
        ]

        _create_isolated_storage_manifest(path_to_wp_build)

        temp_dir = tempfile.mkdtemp()
        for filename in manifest:
                if filename.endswith('/'):
                        shutil.copytree(path.join(path_to_wp_build, filename), path.join(temp_dir, filename))
                else:
                        shutil.copy(path.join(path_to_wp_build, filename), temp_dir)

        if target == 'release':
                prefix = "{name}-{time}"
        else:
                prefix = "{name}"
        base_name = prefix.format(
                name=re.sub("[^a-zA-Z0-9]", "", build.config["name"].lower()),
                time=str(int(time.time()))
                )

        archive = path.abspath(path.join(target, 'wp', base_name))
        shutil.make_archive(archive, 'zip', temp_dir, '.', verbose=True, logger=LOG)

        output_path_for_xap = archive + ".xap" 
        shutil.move(archive + ".zip", output_path_for_xap)

        LOG.info("created XAP: {output}".format(output=output_path_for_xap))

        return output_path_for_xap


# builds a manifest for app files destined for isolated storage
def _create_isolated_storage_manifest(path_to_wp_build):
        path_to_assets = path.join(path_to_wp_build, 'assets')

        assets = []
        for root, subfolders, files in os.walk(path_to_assets):
                for filename in files:
                        filename = os.path.join(root, filename)
                        filename = path.relpath(filename, path_to_wp_build)
                        assets.append(filename.replace('\\', '/'))

        with open(path.join(path_to_assets, 'manifest'), 'w') as manifest:
                for filename in assets:
                        manifest.write('%s\n' % filename)
