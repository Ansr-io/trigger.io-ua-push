import os
import re
import validictory
import json

def json_schema(manifest, file, schema, **kw):
	file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', file))
	schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schema', 'plugin_'+schema+'_schema.json'))
	
	with open(file_path, 'rb') as file_file:
		file_json = json.load(file_file)
	
	with open(schema_path, 'rb') as schema_file:
		schema_json = json.load(schema_file)
	
	validictory.validate(file_json, schema_json)

def android_plugin(manifest, file, **kw):
	plugin_jar = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', file))
	
	with open(plugin_jar, 'rb') as plugin_jar_file:
		if re.search(re.escape('io/trigger/forge/android/modules/'+manifest['name']+'/API'), plugin_jar_file.read()) == None:
			raise Exception("File '%s' is not a valid jar file containing a Forge Android plugin with name '%s'." % (file, manifest['name']))


def ios_plugin(manifest, file, **kw):
	plugin_a = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', file))
	
	with open(plugin_a, 'rb') as plugin_a_file:
		if re.search(re.escape(manifest['name']+'_API.m'), plugin_a_file.read()) == None:
			raise Exception("File '%s' is not a valid static library file containing a Forge iOS plugin with name '%s'." % (file, manifest['name']))

def valid_bundle(manifest, file, **kw):
	bundle_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'plugin', file))

	if not bundle_path.endswith(".bundle"):
		raise Exception("Folder '%s' is not a valid bundle, bundle names always end '.bundle'" % (file))