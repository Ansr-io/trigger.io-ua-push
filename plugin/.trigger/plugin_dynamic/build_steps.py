from xml.etree import ElementTree
import glob
import json
import os
import biplist
import zipfile

import pystache

import utils
import build
from xcode import XcodeProject

# Needed to prevent elementtree screwing with namespace names
ElementTree.register_namespace('android', 'http://schemas.android.com/apk/res/android')
ElementTree.register_namespace('tools', 'http://schemas.android.com/tools')

def include_dependencies(build_params, **kw):
	for plugin, properties in kw.items():
		# Download dependency
		cache_dir = os.path.abspath(os.path.join('..', '..', '.trigger', 'cache'))
		if not os.path.exists(os.path.join(cache_dir, properties['hash'])):
			from trigger import forge_tool

			forge_tool.singleton.remote._get_file('%splugin/download_hash/%s/' % (forge_tool.singleton.remote.server, properties['hash']), os.path.join(cache_dir, properties['hash']+".zip"))
			with zipfile.ZipFile(os.path.join(cache_dir, properties['hash']+".zip")) as plugin_zip:
				plugin_zip.extractall(os.path.join(cache_dir, properties['hash']))
			os.unlink(os.path.join(cache_dir, properties['hash']+".zip"))
		# Include in inspector
		if os.path.split(os.getcwd())[1] == "an-inspector": # XXX: Hacky, do something better?
			build.apply_plugin_to_android_project(os.path.join(cache_dir, properties['hash']), os.getcwd())
		elif os.path.split(os.getcwd())[1] == "ios-inspector": # XXX: Hacky, do something better?
			build.apply_plugin_to_ios_project(os.path.join(cache_dir, properties['hash']), os.getcwd())

def add_element_to_xml(build_params, file, element, to=None, unless=None):
	'''add new element to an XML file

	:param file: filename or file object
	:param element: dict containing tag and optionally attributes, text and children
	:param to: sub element tag name or path we will append to
	:param unless: don't add anything if this tag name or path already exists
	'''
	def create_element(tag, attributes={}, text=None, children=[]):
		for attribute in attributes:
			if isinstance(attributes[attribute], str) or isinstance(attributes[attribute], unicode):
				attributes[attribute] = pystache.render(attributes[attribute], build_params['app_config'])
		element = ElementTree.Element(tag, attributes)
		if text is not None:
			if isinstance(text, str) or isinstance(text, unicode):
				text = pystache.render(text, build_params['app_config'])
			element.text = text
		for child in children:
			element.append(create_element(**child))

		return element

	xml = ElementTree.ElementTree()
	xml.parse(file)
	if to is None:
		el = xml.getroot()
	else:
		el = xml.find(to, dict((v, k) for k, v in ElementTree._namespace_map.items()))
	if unless is None or xml.find(unless, dict((v, k) for k, v in ElementTree._namespace_map.items())) is None:
		new_el = create_element(**element)
		el.append(new_el)
		xml.write(file)

def add_to_json_array(build_params, filename, key, value):
	if isinstance(value, str) or isinstance(value, unicode):
		value = pystache.render(value, build_params['app_config'])
	
	found_files = glob.glob(filename)
	for found_file in found_files:
		file_json = {}
		with open(found_file, "r") as opened_file:
			file_json = json.load(opened_file)
			# TODO: . separated keys?
			file_json[key].append(value)
		with open(found_file, "w") as opened_file:
			json.dump(file_json, opened_file, indent=2, sort_keys=True)

def android_add_permission(build_params, permission):
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element={
			"tag": "uses-permission",
			"attributes": {"android:name": permission},
		},
		unless="uses-permission/[@android:name='%s']" % permission
	)

def android_add_feature(build_params, feature, required="false"):
	if required == "true":
		unless = "uses-feature/[@android:name='%s']/[@android:required='true']" % feature
	else:
		unless = "uses-feature/[@android:name='%s']" % feature

	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element={
			"tag": "uses-feature",
			"attributes": {"android:name": feature, "android:required": required},
		},
		unless=unless)

def android_add_to_application_manifest(build_params, element):
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element=element,
		to="application")

def android_add_to_activity_manifest(build_params, element):
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element=element,
		to="application/activity")

def android_add_to_manifest(build_params, element):
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element=element)

def android_add_activity(build_params, activity_name, attributes={}):
	attributes['android:name'] = activity_name
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element={
			"tag": "activity",
			"attributes": attributes,
		},
		to="application")

def android_add_service(build_params, service_name, attributes={}):
	attributes['android:name'] = service_name
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element={
			"tag": "service",
			"attributes": attributes,
		},
		to="application")

def android_add_receiver(build_params, receiver_name, attributes={}, intent_filters=[]):
	attributes['android:name'] = receiver_name
	add_element_to_xml(build_params,
		file='AndroidManifest.xml',
		element={
			"tag": "receiver",
			"attributes": attributes,
		},
		to="application")

	if len(intent_filters) != 0:
		add_element_to_xml(build_params,
			file='AndroidManifest.xml',
			element={
				"tag": "intent-filter",
			},
			to="application/receiver/[@android:name='%s']" % receiver_name)

		for intent in intent_filters:
			for tag in intent:
				add_element_to_xml(build_params,
					file='AndroidManifest.xml',
					element={
						"tag": tag,
						"attributes": {"android:name": intent[tag]},
					},
					to="application/receiver/[@android:name='%s']/intent-filter" % receiver_name)

def ios_add_url_handler(build_params, scheme, filename='ForgeInspector/ForgeInspector-Info.plist'):
	if isinstance(scheme, str) or isinstance(scheme, unicode):
		scheme = pystache.render(scheme, build_params['app_config'])
	
	found_files = glob.glob(filename)
	for found_file in found_files:
		plist = biplist.readPlist(found_file)
		if "CFBundleURLTypes" in plist:
			plist["CFBundleURLTypes"][0]["CFBundleURLSchemes"].append(scheme)
		else:
			plist["CFBundleURLTypes"] = [{"CFBundleURLSchemes": [scheme]}]
		biplist.writePlist(plist, found_file)

def ios_add_background_mode(build_params, mode, filename='ForgeInspector/ForgeInspector-Info.plist'):
	if isinstance(mode, str) or isinstance(mode, unicode):
		mode = pystache.render(mode, build_params['app_config'])
	
	found_files = glob.glob(filename)
	for found_file in found_files:
		plist = biplist.readPlist(found_file)
		if "UIBackgroundModes" in plist:
			plist["UIBackgroundModes"].append(mode)
		else:
			plist["UIBackgroundModes"] = [mode]
		biplist.writePlist(plist, found_file)

def set_in_biplist(build_params, filename, key, value):
	if isinstance(value, str) or isinstance(value, unicode):
		value = pystache.render(value, build_params['app_config'])
	
	found_files = glob.glob(filename)
	for found_file in found_files:
		plist = biplist.readPlist(found_file)
		plist = utils.transform(plist, key, lambda _: value, allow_set=True)
		biplist.writePlist(plist, found_file)

def set_in_info_plist(build_params, key, value):
	set_in_biplist(build_params, "ForgeInspector/ForgeInspector-Info.plist", key, value)

def add_ios_system_framework(build_params, framework):
	xcode_project = XcodeProject('ForgeInspector.xcodeproj/project.pbxproj')
	if framework.endswith('.framework'):
		xcode_project.add_framework("System/Library/Frameworks/"+framework, "SDKROOT")
	elif framework.endswith('.dylib'):
		xcode_project.add_framework("usr/lib/"+framework, "SDKROOT")
	else:
		raise Exception("Unsupported iOS framework type for '%s', must end in .framework or .dylib." % framework)
	xcode_project.save()

def add_osx_system_framework(build_params, framework):
	xcode_project = XcodeProject('ForgeInspector.xcodeproj/project.pbxproj')
	if framework.endswith('.framework'):
		xcode_project.add_framework("System/Library/Frameworks/"+framework, "SDKROOT")
	elif framework.endswith('.dylib'):
		xcode_project.add_framework("usr/lib/"+framework, "SDKROOT")
	else:
		raise Exception("Unsupported OSX framework type for '%s', must end in .framework or .dylib." % framework)
	xcode_project.save()