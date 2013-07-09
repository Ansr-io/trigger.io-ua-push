import json
import os
import zipfile
import tempfile

from trigger import forge_tool

def create_template(uuid, name, path, **kw):
	os.makedirs(os.path.join(path, 'plugin'))
	with open(os.path.join(path, 'plugin', 'manifest.json'), 'w') as manifest_file:
		manifest = {
			"uuid": uuid,
			"name": name,
			"version": "0.1",
			"description": "My plugin template"
		}

		with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'platform_version.txt'))) as platform_version_file:
			manifest['platform_version'] = platform_version_file.read()

		json.dump(manifest, manifest_file, indent=4, sort_keys=True)

	# Copy template module
	template_path = os.path.abspath(os.path.join(os.path.split(__file__)[0],'templatemodule'))

	for root, dirnames, filenames in os.walk(template_path):
		for filename in filenames:
			relative_path = os.path.join(root, filename)[len(template_path)+1:]
			with open(os.path.join(root, filename), 'r') as source:
				lines = source.readlines()
			new_dir = os.path.split(os.path.join(path, 'plugin', relative_path.replace('templatemodule', name)))[0]
			if not os.path.isdir(new_dir):
				os.makedirs(new_dir)
			with open(os.path.join(path, 'plugin', relative_path.replace('templatemodule', name)), 'w') as output:
				for line in lines:
					output.write(line.replace('templatemodule', name))

	return load(path, manifest)

def load(path, manifest, **kw):
	plugin_model = {}
	plugin_model['local_path'] = path
	plugin_model['plugin_dynamic_path'] = os.path.join(path, ".trigger", "plugin_dynamic")
	plugin_model['uuid'] = manifest['uuid']
	plugin_model['files'] = {
		'manifest': os.path.join(path, 'plugin', 'manifest.json'),
		'plugin_structure': os.path.join(path, ".trigger", "schema", "plugin_structure.json")
	}
	plugin_model['rawfiles'] = {
		'dynamic_platform_version': os.path.join(path, ".trigger", "platform_version.txt")
	}
	plugin_model['directories'] = {
		'plugin_directory': os.path.join(path, 'plugin')
	}
	return plugin_model

def upload(cookies, path, **kw):
	path = os.path.abspath(os.path.join(path, 'plugin'))

	manifest_path = os.path.join(path, 'manifest.json')
	with open(manifest_path, "r") as manifest_file:
		manifest = json.load(manifest_file)

		plugin_uuid = manifest['uuid']
		version = manifest['version']
		description = manifest['description']
		manifest = json.dumps(manifest)
		
		targets = []
		if os.path.exists(os.path.join(path, 'android')):
			targets.append("android")
		if os.path.exists(os.path.join(path, 'ios')):
			targets.append("ios")

		with tempfile.NamedTemporaryFile() as zip_file:
			with zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
				for dirpath, dirnames, filenames in os.walk(path):
					for filename in filenames:
						full_path = os.path.join(dirpath, filename)
						zf.write(full_path, full_path[len(path)+1:])
			zip_file.seek(0)
			return forge_tool.singleton.remote.upload_plugin_version(plugin_uuid, version, description, manifest, targets, zip_file, cookies)