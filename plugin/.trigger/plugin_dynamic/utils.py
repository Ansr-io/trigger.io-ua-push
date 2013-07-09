# XXX should consolidate this with lib
import os
import sys
import subprocess
import json
import hashlib
import urlparse
import stat
from os import path
import logging

LOG = logging.getLogger(__name__)

# # # # # # # # # # # # # # # # # # # 
#
# Data transform
# TODO XPath or similar?
#
# # # # # # # # # # # # # # # # # # # 
def transform(data, node_steps, fn, allow_set=False):
	'''Mutate an arbitrary nested dictionary/array combination with the given function.
	
	``node_steps`` is dot-separated instructions on how to arrive at the data node
	which needs changing::
	
		array_name.[]
		dictionary.key_name
		dictionary.*			   // all keys in a dictionary

	:param data: a nested dictionary / array combination
	:type data: ``dict``
	:param node_steps: dot-separated data path, e.g. my_dict.my_array.[].*.target_key
	:param fn: mutating function - will be passed the data found at the end
		``node_steps``, and should return the desired new value
	:param allow_set: if True the mutating function will be called with None for none
		existing keys - i.e. you can set new keys
	'''
	obj = data.copy()
	list(_handle_all(obj, node_steps.split('.'), fn, allow_set))
	return obj

def _yield_plain(obj, name):
	'If obj is a dictionary, yield an attribute'
	if hasattr(obj, '__contains__') and name in obj:
		yield obj[name]
def _yield_array(obj):
	'Yield all elements of an array'
	assert hasattr(obj, '__iter__'), 'Expecting an array, got %s' % obj
	for thing in obj:
		yield thing
def _yield_asterisk(obj):
	'Yield all values in a dictionary'
	if hasattr(obj, 'iteritems'):
		for _, value in obj.iteritems():
			yield value
def _yield_any(obj, name):
	'Yield a value, or array or dictionary values'
	if name == '*':
		return _yield_asterisk(obj)
	elif name == '[]':
		return _yield_array(obj)
	else:
		return _yield_plain(obj, name)

def recurse_dict(dictionary, fn):
	'''
	if the property isn't a string, recurse till it is
	'''
	for key, value in dictionary.iteritems():
		if hasattr(value, 'iteritems'):
			recurse_dict(value, fn)
		else:
			dictionary[key] = fn(value)

def _handle_all(obj, steps, fn, allow_set):
	if len(steps) > 1:
		for value in _yield_any(obj, steps[0]):
			for x in _handle_all(value, steps[1:], fn, allow_set):
				yield x
	else:
		step = steps[0]
		if step == '*':
			assert hasattr(obj, 'iteritems'), 'Expecting a dictionary, got %s' % obj
			recurse_dict(obj, fn)
		elif step == '[]':
			assert hasattr(obj, '__iter__'), 'Expecting an array, got %s' % obj
			for i, x in enumerate(obj):
				obj[i] = fn(x)
		else:
			if hasattr(obj, '__contains__') and step in obj:
				obj[step] = fn(obj[step])
			elif allow_set:
				obj[step] = fn(None)
	
# # # # # # # # # # # # # # # # # # # 
#
# End data transform
#
# # # # # # # # # # # # # # # # # # # 

class PopenWithoutNewConsole(subprocess.Popen):
	"""Wrapper around Popen that adds the appropriate options to prevent launching
	a new console window everytime we want to launch a subprocess.
	"""
	_old_popen = subprocess.Popen

	def __init__(self, *args, **kwargs):
		if sys.platform.startswith("win") and 'startupinfo' not in kwargs:
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			startupinfo.wShowWindow = subprocess.SW_HIDE
			kwargs['startupinfo'] = startupinfo

		self._old_popen.__init__(self, *args, **kwargs)

def ensure_lib_available(cookies, platform_version, file):
	plugin_dynamic_path = path.split(path.abspath(__file__))[0]

	# In case of forge-inspector check for file
	server_path = path.abspath(path.join(plugin_dynamic_path, '..', '..', '..', '..', 'generate', 'lib', file))
	if path.isfile(server_path):
		return server_path

	lib_dir = path.abspath(path.join(plugin_dynamic_path, '..', '..', '.lib'))
	hash_path = path.abspath(path.join(plugin_dynamic_path, '..', 'hash.json'))
	if not path.exists(lib_dir):
		os.makedirs(lib_dir)
		
	# Hide directory on windows
	if sys.platform == 'win32':
		try:
			PopenWithoutNewConsole(['attrib', '+h', lib_dir]).wait()
		except Exception:
			# don't care if we fail to hide the templates dir
			pass
	
	from trigger import forge_tool
	remote = forge_tool.singleton.remote

	server_details = urlparse.urlparse(remote.server)	

	if not path.exists(hash_path):
		url = "{protocol}://{netloc}/lib-static/{platform_version}/{file}".format(
			protocol=server_details.scheme,
			netloc=server_details.netloc,
			platform_version=platform_version,
			file='hash.json'
		)
		remote._get_file(url, hash_path, cookies=cookies)

	with open(hash_path, 'r') as hash_file:
		hashes = json.load(hash_file)
	
	file_path = path.join(lib_dir, file)

	if path.exists(file_path) and file in hashes:
		# Check hash
		with open(file_path, 'rb') as cur_file:
			hash = hashlib.md5(cur_file.read()).hexdigest()
			if hash == hashes[file]:
				# File exists and is correct
				LOG.debug("File: %s, already downloaded and correct." % file)
				return file_path

	# File doesn't exist, or has the wrong hash or has no known hash - download
	LOG.info("Downloading lib file: %s, this will only happen when a new file is available." % file)
	
	url = "{protocol}://{netloc}/lib-static/{platform_version}/{file}".format(
		protocol=server_details.scheme,
		netloc=server_details.netloc,
		platform_version=platform_version,
		file=file
	)
	remote._get_file(url, file_path, cookies=cookies)
	
	# Make file executable.
	os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
	
	return file_path
