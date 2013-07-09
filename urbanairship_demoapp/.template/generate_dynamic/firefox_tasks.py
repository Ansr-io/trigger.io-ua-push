import os
import shutil
import logging
import sys

from lib import task
from utils import run_shell, ensure_lib_available


LOG = logging.getLogger(__name__)


def _clean_firefox(build_type_dir):
	original_harness_options = os.path.join(build_type_dir, 'firefox', 'harness-options.json')
	backup_harness_options = os.path.join(build_type_dir, 'firefox', 'harness-options-bak.json')
	LOG.debug('Cleaning up after firefox run')
	if os.path.isfile(backup_harness_options):
		shutil.move(backup_harness_options, original_harness_options)


@task
def clean_firefox(build, build_type_dir):
	_clean_firefox(build_type_dir)


def _run_python_code(build, extra_path, entry_point):
	python_runner = ensure_lib_available(build, 'python_runner.py')

	if sys.platform.startswith("win"):
		runner = ensure_lib_available(build, 'python_runner_win.exe')
		run_shell(runner, extra_path, entry_point, command_log_level=logging.INFO, check_for_interrupt=True)
	elif sys.platform.startswith("darwin"):
		runner = ensure_lib_available(build, 'python_runner_darwin')
		run_shell(runner, extra_path, entry_point, command_log_level=logging.INFO, check_for_interrupt=True, create_process_group=True)
	else:
		python = sys.executable
		run_shell(python, python_runner, extra_path, entry_point, command_log_level=logging.INFO, check_for_interrupt=True)

	


@task
def run_firefox(build, build_type_dir):
	firefox_lib = ensure_lib_available(build, 'run-firefox.zip')

	try:
		_run_python_code(build, firefox_lib, 'firefox_runner.run')
	finally:
		_clean_firefox(build_type_dir)


def _generate_package_name(build):
	if "core" not in build.config:
		build.config["core"] = {}
	if "firefox" not in build.config["core"]:
		build.config["core"]["firefox"] = {}
	if "package_name" not in build.config["core"]["firefox"]:
		build.config["core"]["firefox"]["package_name"] = build.config["uuid"]
	return build.config["core"]["firefox"]["package_name"]

