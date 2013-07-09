import shutil
import os

import pystache

import build_steps

def copy_file_from_src(build_params, filename, dest):
	filename = pystache.render(filename, build_params['app_config'])
	dest = pystache.render(dest, build_params['app_config'])
	if os.path.isfile(os.path.join(build_params['src_path'], filename)):
		if not os.path.exists(os.path.dirname(os.path.join(build_params['project_path'], dest))):
			os.makedirs(os.path.dirname(os.path.join(build_params['project_path'], dest)))
		shutil.copy2(os.path.join(build_params['src_path'], filename), os.path.join(build_params['project_path'], dest))

def icons_handle_prerendered(build_params):
	if "ios" in build_params['app_config']["plugins"]["icons"]["config"] and build_params['app_config']["plugins"]["icons"]["config"]["ios"].get("prerendered"):
		build_steps.set_in_biplist(
			filename=os.path.join(build_params['project_path'], "Info.plist"),
			key="UIPrerenderedIcon",
			value=True)
		build_steps.set_in_biplist(
			filename=os.path.join(build_params['project_path'], "Info.plist"),
			key="CFBundleIcons.CFBundlePrimaryIcon.UIPrerenderedIcon",
			value=True)