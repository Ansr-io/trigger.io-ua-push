import logging
import os
import subprocess
import shutil
import time

from lib import task
from utils import run_shell

LOG = logging.getLogger(__name__)

@task
def run_osx(build):
	args = [os.path.join('development', 'osx', 'Forge.app', 'Contents', 'MacOS', 'ForgeTemplate')]
	# Bring app to foreground after 1 second
	subprocess.Popen(["osascript", "-e", "delay 1", "-e", 'tell application "%s" to activate' % build.config['name']])
	run_shell(*args, command_log_level=logging.INFO, check_for_interrupt=True)

def _generate_package_name(build):
	if "core" not in build.config:
		build.config["core"] = {}
	if "osx" not in build.config["core"]:
		build.config["core"]["ios"] = {}
	if "package_name" not in build.config["core"]["osx"]:
		build.config["core"]["osx"]["package_name"] = "io.trigger.forge"+build.config["uuid"]
	return build.config["core"]["osx"]["package_name"]


@task
def package_osx(build):
	timedir = str(int(time.time()))
	os.makedirs(os.path.join('release', 'osx', timedir))
	shutil.copytree(os.path.join("development", "osx", "Forge.app"), os.path.join("release", "osx", timedir, "%s.app" % build.config['name']), symlinks=True)
	LOG.info("Created .app '%s'" % os.path.join("release", "osx", timedir, "%s.app" % build.config['name']))