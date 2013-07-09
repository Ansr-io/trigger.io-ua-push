from xml.etree import ElementTree
import json
import os
import shutil
from contextlib import contextmanager

import build_steps
import build_steps_local
import build_steps_predicates
from xcode import XcodeProject

@contextmanager
def cd(target_dir):
	'Change directory to :param:`target_dir` as a context manager - i.e. rip off Fabric'
	old_dir = os.getcwd()
	try:
		os.chdir(target_dir)
		yield target_dir
	finally:
		os.chdir(old_dir)

# Needed to prevent elementtree screwing with namespace names
ElementTree.register_namespace('android', 'http://schemas.android.com/apk/res/android')
ElementTree.register_namespace('tools', 'http://schemas.android.com/tools')

def _call_with_params(method, build_params, params):
	if isinstance(params, dict):
		return method(build_params, **params)
	elif isinstance(params, tuple):
		return method(build_params, *params)
	else:
		return method(build_params, params)

def apply_plugin_to_osx_project(plugin_path, project_path, skip_framework=False, example_config=False, include_tests=False, local_build_steps=None):
	"""Take the plugin in a specific folder and apply it to an xcode ios project in another folder"""
	with open(os.path.join(plugin_path, 'manifest.json')) as manifest_file:
		manifest = json.load(manifest_file)

	# JS
	if os.path.exists(os.path.join(plugin_path, 'javascript', 'plugin.js')):
		with open(os.path.join(plugin_path, 'javascript', 'plugin.js')) as plugin_js:
			with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'all.js'), 'a') as alljs:
				alljs.write('(function () {\n')
				alljs.write(plugin_js.read())
				alljs.write('\n})();')

	# Tests
	if include_tests:
		if os.path.exists(os.path.join(plugin_path, 'tests', 'fixtures')):
			if os.path.exists(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name'])):
				shutil.rmtree(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name']))
			if not os.path.exists(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures')):
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures'))
			shutil.copytree(os.path.join(plugin_path, 'tests', 'fixtures'), os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name']))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'automated.js')):
			try:
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'automated'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'automated.js'), os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'automated', manifest['name']+'.js'))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'interactive.js')):
			try:
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'interactive'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'interactive.js'), os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'interactive', manifest['name']+'.js'))

	# Add plugin a if we want it
	if not skip_framework:
		# TODO
		pass
		"""plugin_a = os.path.join(plugin_path, 'ios', 'plugin.a')
		if os.path.isfile(plugin_a):
			# Copy to libs
			shutil.copy2(plugin_a, os.path.join(project_path, manifest['name']+'.a'))
			
			# Add to xcode build
			xcode_project = XcodeProject(os.path.join(project_path, 'ForgeInspector.xcodeproj', 'project.pbxproj'))
			xcode_project.add_framework(manifest['name']+'.a', "<group>")
			xcode_project.save()"""

	with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'app_config.json')) as app_config_json:
		app_config = json.load(app_config_json)
	if "plugins" not in app_config:
		app_config["plugins"] = {}
	if example_config:
		# Add example config for plugin to app_config.js(on).
		if os.path.exists(os.path.join(plugin_path, 'config_example.json')):
			with open(os.path.join(plugin_path, 'config_example.json'), "r") as config_example:
				app_config['plugins'][manifest['name']] = {
					"hash": "examplehash",
					"config": json.load(config_example)
				}
		else:
			app_config['plugins'][manifest['name']] = {
				"hash": "examplehash"
			}
		with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'app_config.json'), 'w') as app_config_json:
			json.dump(app_config, app_config_json)
		with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'app_config.js'), 'w') as app_config_js:
			app_config_js.write("window.forge = {}; window.forge.config = %s;" % json.dumps(app_config))

	# frameworks
	plugin_frameworks = os.path.join(plugin_path, 'osx', 'frameworks')
	if os.path.isdir(plugin_frameworks):
		xcode_project = XcodeProject(os.path.join(project_path, 'ForgeModule', 'ForgeModule.xcodeproj', 'project.pbxproj'))
		xcode_inspector_project = XcodeProject(os.path.join(project_path, 'ForgeInspector.xcodeproj', 'project.pbxproj'))
		for framework in os.listdir(plugin_frameworks):
			if framework.endswith(".framework"):
				shutil.copytree(os.path.join(plugin_frameworks, framework), os.path.join(project_path, framework))
				xcode_project.add_framework(os.path.join('..', framework), '<group>')
				xcode_inspector_project.add_saved_framework(framework, '<group>')
			
		xcode_project.save()
		xcode_inspector_project.save()

	# build steps
	plugin_steps_path = os.path.join(plugin_path, 'osx', 'build_steps.json')
	if os.path.isfile(plugin_steps_path):
		with open(plugin_steps_path, 'r') as build_steps_file:
			plugin_build_steps = json.load(build_steps_file)
			with cd(project_path):
				build_params = {
					'app_config': app_config,
					'project_path': project_path,
					'src_path': local_build_steps
				}
				for step in plugin_build_steps:
					if "do" in step:
						for task in step["do"]:
							task_func = getattr(build_steps, task, None)
							if task_func is not None:
								_call_with_params(task_func, build_params, step["do"][task])
							elif local_build_steps is not None:
								task_func = getattr(build_steps_local, task, None)
								if task_func is not None:
									_call_with_params(task_func, build_params, step["do"][task])

def apply_plugin_to_ios_project(plugin_path, project_path, skip_a=False, example_config=False, include_tests=False, local_build_steps=None):
	"""Take the plugin in a specific folder and apply it to an xcode ios project in another folder"""
	with open(os.path.join(plugin_path, 'manifest.json')) as manifest_file:
		manifest = json.load(manifest_file)

	# JS
	if os.path.exists(os.path.join(plugin_path, 'javascript', 'plugin.js')):
		with open(os.path.join(plugin_path, 'javascript', 'plugin.js')) as plugin_js:
			with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'all.js'), 'a') as alljs:
				alljs.write('(function () {\n')
				alljs.write(plugin_js.read())
				alljs.write('\n})();')

	# Tests
	if include_tests:
		if os.path.exists(os.path.join(plugin_path, 'tests', 'fixtures')):
			if os.path.exists(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name'])):
				shutil.rmtree(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name']))
			if not os.path.exists(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures')):
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures'))
			shutil.copytree(os.path.join(plugin_path, 'tests', 'fixtures'), os.path.join(project_path, 'ForgeInspector', 'assets', 'src', 'fixtures', manifest['name']))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'automated.js')):
			try:
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'automated'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'automated.js'), os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'automated', manifest['name']+'.js'))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'interactive.js')):
			try:
				os.makedirs(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'interactive'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'interactive.js'), os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'tests', 'interactive', manifest['name']+'.js'))

	# Add plugin a if we want it
	if not skip_a:
		plugin_a = os.path.join(plugin_path, 'ios', 'plugin.a')
		if os.path.isfile(plugin_a):
			# Copy to libs
			shutil.copy2(plugin_a, os.path.join(project_path, manifest['name']+'.a'))
			
			# Add to xcode build
			xcode_project = XcodeProject(os.path.join(project_path, 'ForgeInspector.xcodeproj', 'project.pbxproj'))
			xcode_project.add_framework(manifest['name']+'.a', "<group>")
			xcode_project.save()

	with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'app_config.json')) as app_config_json:
		app_config = json.load(app_config_json)
	if "plugins" not in app_config:
		app_config["plugins"] = {}
	if example_config:
		# Add example config for plugin to app_config.js(on).
		if os.path.exists(os.path.join(plugin_path, 'config_example.json')):
			with open(os.path.join(plugin_path, 'config_example.json'), "r") as config_example:
				app_config['plugins'][manifest['name']] = {
					"hash": "examplehash",
					"config": json.load(config_example)
				}
		else:
			app_config['plugins'][manifest['name']] = {
				"hash": "examplehash"
			}
		with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'app_config.json'), 'w') as app_config_json:
			json.dump(app_config, app_config_json)
		with open(os.path.join(project_path, 'ForgeInspector', 'assets', 'forge', 'app_config.js'), 'w') as app_config_js:
			app_config_js.write("window.forge = {}; window.forge.config = %s;" % json.dumps(app_config))


	# bundles
	plugin_bundles = os.path.join(plugin_path, 'ios', 'bundles')
	if os.path.isdir(plugin_bundles):
		xcode_project = XcodeProject(os.path.join(project_path, 'ForgeInspector.xcodeproj', 'project.pbxproj'))
		for bundle in os.listdir(plugin_bundles):
			if bundle.endswith(".bundle"):
				shutil.copytree(os.path.join(plugin_bundles, bundle), os.path.join(project_path, bundle))
				xcode_project.add_resource(bundle)
			
		xcode_project.save()

	# build steps
	plugin_steps_path = os.path.join(plugin_path, 'ios', 'build_steps.json')
	if os.path.isfile(plugin_steps_path):
		with open(plugin_steps_path, 'r') as build_steps_file:
			plugin_build_steps = json.load(build_steps_file)
			with cd(project_path):
				build_params = {
					'app_config': app_config,
					'project_path': project_path,
					'src_path': local_build_steps
				}
				for step in plugin_build_steps:
					if "when" in step:
						should_continue = False
						for predicate in step["when"]:
							predicate_func = getattr(build_steps_predicates, predicate, None)
							if predicate_func is not None:
								if not _call_with_params(predicate_func, build_params, step["when"][predicate]):
									should_continue = True
									break
							else:
								should_continue = True
								break
						if should_continue:
							continue
					if "do" in step:
						for task in step["do"]:
							task_func = getattr(build_steps, task, None)
							if task_func is not None:
								_call_with_params(task_func, build_params, step["do"][task])
							elif local_build_steps is not None:
								task_func = getattr(build_steps_local, task, None)
								if task_func is not None:
									_call_with_params(task_func, build_params, step["do"][task])

def apply_plugin_to_android_project(plugin_path, project_path, skip_jar=False, example_config=False, include_tests=False, local_build_steps=None):
	"""Take the plugin in a specific folder and apply it to an eclipse android project in another folder"""
	with open(os.path.join(plugin_path, 'manifest.json')) as manifest_file:
		manifest = json.load(manifest_file)

	# JS
	if os.path.exists(os.path.join(plugin_path, 'javascript', 'plugin.js')):
		with open(os.path.join(plugin_path, 'javascript', 'plugin.js')) as plugin_js:
			with open(os.path.join(project_path, 'assets', 'forge', 'all.js'), 'a') as alljs:
				alljs.write('(function () {\n')
				alljs.write(plugin_js.read())
				alljs.write('\n})();')

	# Tests
	if include_tests:
		if os.path.exists(os.path.join(plugin_path, 'tests', 'fixtures')):
			if os.path.exists(os.path.join(project_path, 'assets', 'src', 'fixtures', manifest['name'])):
				shutil.rmtree(os.path.join(project_path, 'assets', 'src', 'fixtures', manifest['name']))
			if not os.path.exists(os.path.join(project_path, 'assets', 'src', 'fixtures')):
				os.makedirs(os.path.join(project_path, 'assets', 'src', 'fixtures'))
			shutil.copytree(os.path.join(plugin_path, 'tests', 'fixtures'), os.path.join(project_path, 'assets', 'src', 'fixtures', manifest['name']))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'automated.js')):
			try:
				os.makedirs(os.path.join(project_path, 'assets', 'forge', 'tests', 'automated'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'automated.js'), os.path.join(project_path, 'assets', 'forge', 'tests', 'automated', manifest['name']+'.js'))
		if os.path.exists(os.path.join(plugin_path, 'tests', 'interactive.js')):
			try:
				os.makedirs(os.path.join(project_path, 'assets', 'forge', 'tests', 'interactive'))
			except OSError:
				pass
			shutil.copy2(os.path.join(plugin_path, 'tests', 'interactive.js'), os.path.join(project_path, 'assets', 'forge', 'tests', 'interactive', manifest['name']+'.js'))

	# Add plugin jar if we want it
	if not skip_jar:
		plugin_jar = os.path.join(plugin_path, 'android', 'plugin.jar')
		if os.path.exists(plugin_jar):
			shutil.copy2(plugin_jar, os.path.join(project_path, 'libs', manifest['name']+'.jar'))

	with open(os.path.join(project_path, 'assets', 'app_config.json')) as app_config_json:
		app_config = json.load(app_config_json)
	if "plugins" not in app_config:
		app_config["plugins"] = {}
	if example_config:
		# Add example config for plugin to app_config.js(on).
		if os.path.exists(os.path.join(plugin_path, 'config_example.json')):
			with open(os.path.join(plugin_path, 'config_example.json'), "r") as config_example:
				app_config['plugins'][manifest['name']] = {
					"hash": "examplehash",
					"config": json.load(config_example)
				}
		else:
			app_config['plugins'][manifest['name']] = {
				"hash": "examplehash"
			}
		with open(os.path.join(project_path, 'assets', 'app_config.json'), 'w') as app_config_json:
			json.dump(app_config, app_config_json)
		with open(os.path.join(project_path, 'assets', 'forge', 'app_config.js'), 'w') as app_config_js:
			app_config_js.write("window.forge = {}; window.forge.config = %s;" % json.dumps(app_config))

	# res
	plugin_res = os.path.join(plugin_path, 'android', 'res')
	if os.path.isdir(plugin_res):
		for dirpath, _, filenames in os.walk(plugin_res):
			if not os.path.exists(os.path.join(project_path, 'res', dirpath[len(plugin_res)+1:])):
				os.makedirs(os.path.join(project_path, 'res', dirpath[len(plugin_res)+1:]))
			for filename in filenames:
				if (filename.startswith('.')):
					continue
				if os.path.exists(os.path.join(project_path, 'res', dirpath[len(plugin_res)+1:], filename)):
					raise Exception("File '%s' already exists, plugin resources may only add files, not replace them." % os.path.join('res', dirpath[len(plugin_res)+1:], filename))
				shutil.copy2(os.path.join(dirpath, filename), os.path.join(project_path, 'res', dirpath[len(plugin_res)+1:], filename))

	# libs
	plugin_res = os.path.join(plugin_path, 'android', 'libs')
	if os.path.isdir(plugin_res):
		for dirpath, _, filenames in os.walk(plugin_res):
			if not os.path.exists(os.path.join(project_path, 'libs', dirpath[len(plugin_res)+1:])):
				os.makedirs(os.path.join(project_path, 'libs', dirpath[len(plugin_res)+1:]))
			for filename in filenames:
				shutil.copy2(os.path.join(dirpath, filename), os.path.join(project_path, 'libs', dirpath[len(plugin_res)+1:], filename))

	# build steps
	if os.path.isfile(os.path.join(plugin_path, 'android', 'build_steps.json')):
		with open(os.path.join(plugin_path, 'android', 'build_steps.json')) as build_steps_file:
			plugin_build_steps = json.load(build_steps_file)
			with cd(project_path):
				build_params = {
					'app_config': app_config,
					'project_path': project_path,
					'src_path': local_build_steps
				}
				for step in plugin_build_steps:
					if "do" in step:
						for task in step["do"]:
							task_func = getattr(build_steps, task, None)
							if task_func is not None:
								_call_with_params(task_func, build_params, step["do"][task])
							elif local_build_steps is not None:
								task_func = getattr(build_steps_local, task, None)
								if task_func is not None:
									_call_with_params(task_func, build_params, step["do"][task])