from os import path
import os
import logging

from lib import task

LOG = logging.getLogger(__name__)

def _chrome_folder():
	return path.abspath(path.join(os.getcwd(), 'development', 'chrome'))

@task
def run_chrome(build):
	msg = """Currently it is not possible to launch a Chrome extension via this interface.
The required steps are:

	1) Go to chrome:extensions in the Chrome browser
	2) Make sure "developer mode" is on (top right corner)')
	3) Use "Load unpacked extension" and select the folder: {chrome_folder}""".format(chrome_folder=_chrome_folder())

	LOG.info(msg)

@task
def package_chrome(build):
	msg = """Currently it is not possible to package a Chrome extension via this interface.
The required steps are:

	1) Go to chrome:extensions in the Chrome browser
	2) Make sure "developer mode" is on (top right corner)')
	3) Use "Pack extension" and use use this for the root: {chrome_folder}

More information on packaging Chrome extensions can be found here:
	http://code.google.com/chrome/extensions/packaging.html
	""".format(chrome_folder=_chrome_folder())

	LOG.info(msg)
