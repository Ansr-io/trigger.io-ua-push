import time
import json
import os
import shutil
import zipfile
import hashlib
import sys
import subprocess
import re
from datetime import datetime

import build
import utils

def _hash_folder(hash, path, ignore=[]):
	'''Update a hash with all of the file/dirnames in a folder as well as all the file contents that aren't in ignore'''
	if not os.path.exists(path):
		return
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			full_path = os.path.join(dirpath, filename)
			relative_path = full_path[len(path)+1:]
			if not relative_path in ignore:
				hash.update(relative_path)
				with open(full_path, 'rb') as cur_file:
					hash.update(cur_file.read())
		for dirname in dirnames:
			full_path = os.path.join(dirpath, dirname)
			relative_path = full_path[len(path)+1:]
			if not relative_path in ignore:
				hash.update(relative_path)

def _update_target(target, cookies):
	"""Update the inspector app to a clean one for the current platform version

	returns the location the previous inspector app was moved to"""

	plugin_dynamic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	plugin_path = os.path.abspath(os.path.join(plugin_dynamic_path, '..'))

	if not os.path.exists(os.path.join(plugin_dynamic_path, 'cache')):
		os.makedirs(os.path.join(plugin_dynamic_path, 'cache'))

	# If we don't have an inspector build... get it
	if not os.path.exists(os.path.join(plugin_dynamic_path, 'cache', '%s.zip' % target)):

		# Do this import here so we can run without the toolkit
		from trigger import forge_tool

		with open(os.path.join(plugin_dynamic_path, 'platform_version.txt')) as platform_version_file:
			platform_version = platform_version_file.read()

		data = {}

		data['config'] = json.dumps({
			"platform_version": platform_version,
			"uuid": "0",
			"config_version": "2",
			"name": "-",
			"author": "-",
			"version": "0.1",
			"description": "-",
			"modules": {},
		})
		data['target'] = target

		build_state = {
			"state": "pending"
		}
		while build_state['state'] in ('pending', 'working'):
			build_state = forge_tool.singleton.remote._api_post('plugin/inspector_build/', data=data, cookies=cookies)
			data['id'] = build_state['id']

			if build_state['state'] in ('pending', 'working'):
				time.sleep(3)

		if build_state['state'] != 'complete':
			raise Exception('build failed: %s' % build_state['log_output'])

		forge_tool.singleton.remote._get_file(build_state['file_output'], os.path.join(plugin_dynamic_path, 'cache', '%s.zip' % target))

	# If we already have an inspector move it out of the way
	moved_to = None
	if os.path.exists(os.path.join(plugin_path, 'inspector', target)):
		moved_to = os.path.join(plugin_path, 'inspector', '%s.%s' % (target, datetime.now().isoformat().replace(":", "-") ))
		shutil.move(os.path.join(plugin_path, 'inspector', target), moved_to)

	# Extract new inspector
	with zipfile.ZipFile(os.path.join(plugin_dynamic_path, 'cache', '%s.zip' % target)) as inspector_zip:
		inspector_zip.extractall(os.path.join(plugin_path, 'inspector'))

	return moved_to

def hash_android():
	'''Get the current hash for the Android plugin files'''
	hash = hashlib.sha1()
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'android')), ['plugin.jar'])
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'tests')))
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'javascript')))
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'platform_version.txt'))) as platform_version_file:
		hash.update(platform_version_file.read())
	return hash.hexdigest()

def check_android_hash(**kw):
	current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'inspector', 'an-inspector', '.hash'))
	if not os.path.exists(current_path):
		return {'message': 'Android inspector not found.', 'type': 'error'}
	with open(current_path, 'r') as hash_file:
		if hash_android() == hash_file.read():
			return {'message': 'Android inspector up to date.', 'type': 'good'}
		else:
			return {'message': 'Android inspector out of date.', 'type': 'warning'}

def update_android(cookies, **kw):
	previous_path = _update_target('an-inspector', cookies=cookies)
	current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'inspector', 'an-inspector'))

	# If we're updating copy the plugin source from the previous inspector
	if previous_path is not None:
		shutil.rmtree(os.path.join(current_path, 'ForgeModule', 'src'))
		if os.path.exists(os.path.join(previous_path, 'src')):
			shutil.copytree(os.path.join(previous_path, 'src'), os.path.join(current_path, 'ForgeModule', 'src'))
		else:
			shutil.copytree(os.path.join(previous_path, 'ForgeModule', 'src'), os.path.join(current_path, 'ForgeModule', 'src'))

	# Prepare example module code
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'manifest.json'))) as manifest_file:
		manifest = json.load(manifest_file)
	
	plugin_name = str(manifest['name'])

	for root, dirnames, filenames in os.walk(os.path.join(current_path, 'ForgeModule')):
		for filename in filenames:
			with open(os.path.join(root, filename), 'rb') as source:
				lines = source.readlines()
			if 'templatemodule' in os.path.join(root, filename):
				os.remove(os.path.join(root, filename))
				old_dir = os.path.split(os.path.join(root, filename))[0]
				if len(os.listdir(old_dir)) == 0:
					os.removedirs(old_dir)
				new_dir = os.path.split(os.path.join(root, filename).replace('templatemodule', plugin_name))[0]
				if not os.path.isdir(new_dir):
					os.makedirs(new_dir)
			with open(os.path.join(root, filename).replace('templatemodule', plugin_name), 'wb') as output:
				for line in lines:
					output.write(line.replace('templatemodule', plugin_name))

	# Update inspector with plugin specific build details
	try:
		build.apply_plugin_to_android_project(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin')), os.path.join(current_path, 'ForgeInspector'), skip_jar=True, example_config=True, include_tests=True, local_build_steps=os.path.join(current_path, 'ForgeInspector', 'assets', 'src'))
		# In the Android inspectors case we want any libs to be attached to the ForgeModule project, not the ForgeInspector
		if os.path.exists(os.path.join(current_path, 'ForgeInspector', 'libs')):
			for file_ in os.listdir(os.path.join(current_path, 'ForgeInspector', 'libs')):
				if not file_.startswith("."):
					shutil.move(
						os.path.join(current_path, 'ForgeInspector', 'libs', file_),
						os.path.join(current_path, 'ForgeModule', 'libs'))


		if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'android', 'res'))):

			if not os.path.exists(os.path.join(current_path, 'ForgeModule', 'trigger-gen')):
				os.makedirs(os.path.join(current_path, 'ForgeModule', 'trigger-gen'))

			# Generate magic R.java
			if sys.platform.startswith('darwin'):
				aapt_exec = 'aapt_osx'
			elif sys.platform.startswith('win'):
				aapt_exec = 'aapt.exe'
			else:
				aapt_exec = 'aapt_linux'

			with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'platform_version.txt'))) as platform_version_file:
				platform_version = platform_version_file.read().strip()

			subprocess.check_call([
				utils.ensure_lib_available(cookies, platform_version, aapt_exec),
				'package', '-m',
				'-M', os.path.join(current_path, 'ForgeModule', 'AndroidManifest.xml'),
				'-S', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'android', 'res')),
				'-J', os.path.join(current_path, 'ForgeModule', 'trigger-gen'),
				'-I', utils.ensure_lib_available(cookies, platform_version, 'android-platform.apk')
				])

		
			for root, dirnames, filenames in os.walk(os.path.join(current_path, 'ForgeModule', 'trigger-gen')):
				for filename in filenames: 
					# Tweak R.java to be magic
					with open(os.path.join(root, filename)) as source:
						content = source.read()

					content = content.replace("final ", "")
 					content = content.replace("public class R", """import java.lang.reflect.Field;

public class R""")
					content = re.sub(r'\/\* AUTO-GENERATED.*?\*\/', '''/* This file was generated as part of a ForgeModule.
 *
 * You may move this file to another package if you require, however do not modify its contents.
 * To add more resources rebuild the inspector project.
 */''', content, flags=re.MULTILINE | re.DOTALL)

					content = re.sub('''    public static class (\w+) {(.*?)\n    }''', r'''    public static class \1 {\2
        static {
            try {
                Class<?> realR = Class.forName("io.trigger.forge.android.inspector.R");
                for (Class<?> c : realR.getClasses()) {
                    if (c.getSimpleName().equals("\1")) {
                        for (Field f : \1.class.getDeclaredFields()) {
                            try {
                                f.set(null, c.getDeclaredField(f.getName()).get(null));
                            } catch (IllegalArgumentException e) {
                            } catch (IllegalAccessException e) {
                            } catch (NoSuchFieldException e) {
                            }
                        }
                        break;
                    }
                }               
            } catch (ClassNotFoundException e) {
            }
        }
    }''', content, flags=re.MULTILINE | re.DOTALL)

					with open(os.path.join(root, filename), 'w') as output:
						output.write(content)

	except Exception as e:
		shutil.rmtree(current_path)
		try:
			raise
			#raise Exception("Applying build steps failed, check build steps and re-update inspector: %s" % e)
		finally:
			try:
				shutil.move(previous_path, current_path)
			except Exception:
				pass

	# Prefix eclipse project names with plugin name
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'manifest.json'))) as manifest_file:
		manifest = json.load(manifest_file)
		plugin_name = manifest['name']
	for project in ('ForgeInspector', 'ForgeModule'):
		with open(os.path.join(current_path, project, '.project')) as project_file:
			project_conf = project_file.read()
		project_conf = project_conf.replace('<name>Forge', '<name>%s_Forge' % plugin_name)
		with open(os.path.join(current_path, project, '.project'), 'w') as project_file:
			project_file.write(project_conf)

	# Create hash for inspector
	with open(os.path.join(current_path, '.hash'), 'w') as hash_file:
		hash_file.write(hash_android())

def hash_ios():
	'''Get the current hash for the iOS plugin files'''
	hash = hashlib.sha1()
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'ios')), ['plugin.a'])
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'tests')))
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'javascript')))
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'platform_version.txt'))) as platform_version_file:
		hash.update(platform_version_file.read())
	return hash.hexdigest()

def check_ios_hash(**kw):
	current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'inspector', 'ios-inspector', '.hash'))
	if not os.path.exists(current_path):
		return {'message': 'iOS inspector not found.', 'type': 'error'}
	with open(current_path, 'r') as hash_file:
		if hash_ios() == hash_file.read():
			return {'message': 'iOS inspector up to date.', 'type': 'good'}
		else:
			return {'message': 'iOS inspector out of date.', 'type': 'warning'}

def update_ios(cookies, **kw):
	if not sys.platform.startswith('darwin'):
		raise Exception("iOS inspector can only be used on OS X.")

	previous_path = _update_target('ios-inspector', cookies=cookies)
	current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'inspector', 'ios-inspector'))

	# If we're updating copy the plugin source from the previous inspector
	if previous_path is not None:
		shutil.rmtree(os.path.join(current_path, 'ForgeModule'))
		shutil.copytree(os.path.join(previous_path, 'ForgeModule'), os.path.join(current_path, 'ForgeModule'))
	else:
		# Prepare example module code
		with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'manifest.json'))) as manifest_file:
			manifest = json.load(manifest_file)
		
		plugin_name = str(manifest['name'])

		for root, dirnames, filenames in os.walk(os.path.join(current_path, 'ForgeModule')):
			for filename in filenames:
				with open(os.path.join(root, filename), 'r') as source:
					lines = source.readlines()
				if 'templatemodule' in filename:
					os.remove(os.path.join(root, filename))
				with open(os.path.join(root, filename.replace('templatemodule', plugin_name)), 'w') as output:
					for line in lines:
						output.write(line.replace('templatemodule', plugin_name))

	# Update inspector with plugin specific build details
	try:
		build.apply_plugin_to_ios_project(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin')), current_path, skip_a=True, example_config=True, include_tests=True, local_build_steps=os.path.join(current_path, 'ForgeInspector', 'assets', 'src'))
	except Exception as e:
		shutil.rmtree(current_path)
		try:
			raise
			#raise Exception("Applying build steps failed, check build steps and re-update inspector: %s" % e)
		finally:
			try:
				shutil.move(previous_path, current_path)
			except Exception:
				pass

	# Create hash for inspector
	with open(os.path.join(current_path, '.hash'), 'w') as hash_file:
		hash_file.write(hash_ios())

def hash_osx():
	'''Get the current hash for the Android plugin files'''
	hash = hashlib.sha1()
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'tests')))
	_hash_folder(hash, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', 'javascript')))
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'platform_version.txt'))) as platform_version_file:
		hash.update(platform_version_file.read())
	return hash.hexdigest()

def update_osx(cookies, **kw):
	if not sys.platform.startswith('darwin'):
		raise Exception("OSX inspector can only be used on OS X.")

	previous_path = _update_target('osx-inspector', cookies=cookies)
	current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'inspector', 'osx-inspector'))

	# If we're updating copy the plugin source from the previous inspector
	if previous_path is not None:
		shutil.rmtree(os.path.join(current_path, 'ForgeModule'))
		shutil.copytree(os.path.join(previous_path, 'ForgeModule'), os.path.join(current_path, 'ForgeModule'))

	# Update inspector with plugin specific build details
	try:
		build.apply_plugin_to_osx_project(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin')), current_path, skip_framework=True, example_config=True, include_tests=True, local_build_steps=os.path.join(current_path, 'ForgeInspector', 'assets', 'src'))
	except Exception:
		shutil.rmtree(current_path)
		try:
			raise
			#raise Exception("Applying build steps failed, check build steps and re-update inspector: %s" % e)
		finally:
			try:
				shutil.move(previous_path, current_path)
			except Exception:
				pass

	# Create hash for inspector
	with open(os.path.join(current_path, '.hash'), 'w') as hash_file:
		hash_file.write(hash_osx())