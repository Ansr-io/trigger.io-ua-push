from collections import defaultdict
import socket
import time
import errno
import json
import logging
import os
from os import path
import re
import shutil
import sys
import subprocess
import threading
from urlparse import urljoin

import requests

import lib
from lib import cd, task
import utils
from utils import run_shell, ShellError


LOG = logging.getLogger(__name__)


class WebError(lib.BASE_EXCEPTION):
	pass


def _port_available(port):
	s = None
	try:
		# need to set SO_REUSEADDR, otherwise we get false positives where the
		# port is unavailable for a small period of time after closing node

		# http://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
		# http://stackoverflow.com/questions/775638/using-so-reuseaddr-what-happens-to-previously-open-socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('127.0.0.1', port))
		return True

	except socket.error:
		return False

	finally:
		if s is not None:
			s.close()

def _update_path_for_node(build):
	'''change sys.path to include the directory which holds node and npm

	:param build: :class:`Build` instance
	'''
	# configuration setting overrides all
	manual = build.tool_config.get('web.node_path')
	path_chunks = os.environ["PATH"].split(os.pathsep)
	if manual is None:
		possible_locations = defaultdict(list)
		possible_locations.update({
			'darwin': ['/usr/local/bin/']
		})

		for location in possible_locations[sys.platform]:
			path_chunks.append(location)
	else:
		# override given
		if not isinstance(manual, list):
			manual = [manual]
		for manual_path in manual:
			abs_manual_path = os.path.abspath(manual_path)
			if abs_manual_path not in path_chunks:
				path_chunks.insert(0, abs_manual_path)
	os.environ["PATH"] = os.pathsep.join(path_chunks)

def _npm(build, *args, **kw):
	if sys.platform.startswith("win"):
		npm = "npm.cmd"
	else:
		npm = "npm"
	if not utils.which(npm):
		raise WebError("""Couldn't find {tool} on your PATH or in likely locations - is it installed?

You can use the 'node_path' setting in your local configuration to set a custom install directory"""
.format(tool=npm))

	kw['check_for_interrupt'] = True
	run_shell(npm, *args, **kw)

def _node(build, *args, **kw):
	node = "node"
	if not utils.which(node):
		raise WebError("couldn't find {tool} on your PATH or in likely "
				"locations - is it installed?".format(tool=node))

	kw['check_for_interrupt'] = True
	run_shell(node, *args, **kw)

def _post_kill_signal(port):
	LOG.debug('POSTING to /kill')
	requests.post('http://localhost:%d/_forge/kill/' % port)
	time.sleep(1)


@task
def run_web(build):
	"""Run an instance of Node locally"""
	# TODO: port should be a parameter/configuration
	port = 3000
	_update_path_for_node(build)

	def show_local_server():
		LOG.info("Attempting to open browser at http://localhost:%d/" % port)
		_open_url("http://localhost:%d/" % port)

	with cd(path.join("development", "web")):
		timer = None
		try:
			# TODO: annoyingly difficult to kill npm processes on windows - npm.cmd actually
			# launches an instance of node as a subprocess which is the real thing you need to kill!
			# might be possible to kill npm.cmd in a nicer way, e.g. sending a CTRL_C event, needs
			# a bit of experimentation
			_npm(build, "install")

			attempts = 0
			while not _port_available(port):
				LOG.info('Port still in use, attempting to send a kill signal')
				#TODO: appropriate timeout and handling
				requests.post('http://localhost:%d/_forge/kill/' % port)

				time.sleep(1)

				attempts += 1
				if attempts > 5:
					raise WebError("Port %d seems to be in use, you should specify a different port to use" % port)

			timer = threading.Timer(3, show_local_server).start()
			_node(build, "./web.js", command_log_level=logging.INFO,
					check_for_interrupt=True,
					env=dict(os.environ, PORT=str(port), FORGE_DEBUG='1'))

		finally:
			if timer:
				timer.cancel()


def _git(cmd, *args, **kwargs):
	"""Runs a git command and scrapes the output for common problems, so that we can try
	to advise the user about them

	e.g. _git('push', '--all')
	"""
	try:
		output = run_shell('git', cmd, *args, **kwargs)
	except OSError as e:
		if e.errno == errno.ENOENT:
			# TODO: download portable copy of git/locate git?
			raise WebError("Can't run git commands - you need to install git and make sure it's in your PATH")
	except ShellError as e:
		def _key_problem(output):
			lines = output.split('\n')
			if len(lines) > 0:
				first = lines[0]
				return first.startswith('Permission denied (publickey)')

		if _key_problem(e.output):
			# TODO: prompt user with choice to use existing .pub in ~/.ssh
			# or create new keypair and submit to heroku
			raise WebError('Failed to access remote git repo, you need to set up key based access')

		raise WebError('Problem running git {cmd}:\n {output}'.format(cmd=cmd, output=e.output))

	return output


def _request_heroku_credentials():
	"""Prompts the user for heroku username and password and returns them"""
	call = lib.current_call()
	question_schema = {
		'title': 'Enter your heroku login details',
		'properties': {
			'username': {
				'type': 'string',
				'title': 'Username',
				'description': 'Your heroku username',
				'_order': 1,
			},

			'password': {
				'type': 'string',
				'title': 'Password',
				'description': 'Your heroku password',
				'_password': True,
				'_order': 0,
			}
		}
	}

	while True:
		event_id = call.emit('question', schema=question_schema)
		response = call.wait_for_response(event_id)
		response_data = response.get('data')

		if response_data is None:
			raise WebError("User aborted")

		heroku_username = response_data.get('username')
		heroku_password = response_data.get('password')

		if not heroku_username:
			LOG.warning("Username required")
			continue

		if not heroku_password:
			LOG.warning("Password required")
			continue

		return heroku_username, heroku_password


def _check_heroku_response(response):
	if not response.ok:
		msg = (
			"Request to Heroku API went wrong\n"
			"url: {url}\n"
			"code: {code}"
		).format(url=response.request.url, code=response.status_code)

		if response.status_code == 401:
			msg += "\n\nUnauthorized - make sure the value of web.profile.heroku_api_key is correct"

		raise WebError(msg)


def _heroku_get_api_key(username, password):
	response = requests.post(
		'https://api.heroku.com/login',
		data={
			'username': username,
			'password': password
		},
		headers={
			'Accept': 'application/json'
		}
	)

	try:
		_check_heroku_response(response)
	except WebError:
		LOG.error("Incorrect heroku details")
		return None

	#The json you get back:
	#'{"verified_at":null,"api_key":"yourapikey","id":"839828@users.heroku.com","verified":false,"email":"t.r.monks@gmail.com"}'
	return json.loads(response.content)['api_key']


# TODO: error code checking on responses
def _heroku_get(api_key, api_url):
	# see https://api-docs.heroku.com/apps
	# heroku api requires a blank user and api_key as http auth details
	auth = ('', api_key)
	headers = {
		'Accept': 'application/json',
	}
	url = urljoin('https://api.heroku.com/', api_url)
	response = requests.get(url, auth=auth, headers=headers)
	_check_heroku_response(response)
	return response


# TODO: error code checking on responses
def _heroku_post(api_key, api_url, data):
	# heroku api requires a blank user and api_key as http auth details
	auth = ('', api_key)
	headers = {
		'Accept': 'application/json',
	}
	url = urljoin('https://api.heroku.com/', api_url)
	response = requests.post(url, data=data, auth=auth, headers=headers)
	_check_heroku_response(response)
	return response


def _open_url(url):
	'''Attempt to open the provided URL in the default browser'''
	if sys.platform.startswith('darwin'):
		run_shell('open', url, fail_silently=True)
	elif sys.platform.startswith('win'):
		# 'start' seems to need shell=True to be found (probably a builtin)
		cmd = subprocess.list2cmdline(['start', url])
		subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	elif sys.platform.startswith('linux'):
		run_shell('xdg-open', url, fail_silently=True)


def _get_app_to_push_to(build, api_key):
	app = build.tool_config.get('web.profile.heroku_app_name')

	if app is not None:
		return app

	LOG.info('Querying heroku about registered apps...')
	apps = json.loads(_heroku_get(api_key, 'apps').content)
	app_names = [app['name'] for app in apps]

	create_new_heroku_app = True
	if app_names:
		message = (
			"You don't have a heroku app name specified in local_config.json."
			'You can choose either to:'
		)

		chosen_n = lib.ask_multichoice(question_text=message, choices=[
			'Create a new heroku application',
			'Push to a currently registered heroku application'
		])

		if chosen_n == 1:
			create_new_heroku_app = True
		else:
			create_new_heroku_app = False

	# either create a new heroku app, or choose an already existing app
	if create_new_heroku_app:
		LOG.info('Creating new heroku application')
		response = _heroku_post(api_key, 'apps', data='app[stack]=cedar')
		chosen_app = json.loads(response.content)['name']

	else:
		chosen_n = lib.ask_multichoice(question_text='Choose an existing heroku app to deploy to:', choices=app_names, radio=False)
		chosen_app = app_names[chosen_n - 1]

	lib.set_dotted_attributes(build, {
		'web.profile.heroku_app_name': chosen_app
	})
	return chosen_app


def _get_heroku_api_key(build):
	"""Get a heroku API key for interaction with the heroku API.

	First looks to see if we have one stored in local_config.json,
	if not then asks the user for their heroku credentials
	so we can authenticate with the service to obtain one.
	"""
	api_key = build.tool_config.get('web.profile.heroku_api_key')

	while api_key is None:
		heroku_username, heroku_password = _request_heroku_credentials()
		api_key = _heroku_get_api_key(heroku_username, heroku_password)

		if api_key is not None:
			lib.set_dotted_attributes(build, {
				'web.profile.heroku_api_key': api_key
			})

	return api_key


@task
def package_web(build):
	interactive = build.tool_config.get('general.interactive', True)
	development = lib.expand_relative_path(build, 'development/web')
	output = lib.expand_relative_path(build, 'release/web/heroku')

	# deploy to Heroku
	with cd(development):
		api_key = _get_heroku_api_key(build)
		chosen_app = _get_app_to_push_to(build, api_key)

		if not path.isdir(output):
			os.makedirs(output)

		with cd(output):
			if not path.isdir('.git'):
				LOG.debug('Creating git repo')
				_git('init')

				LOG.debug('Create dummy first commit')
				with open('.forge.txt', 'w') as forge_file:
					forge_file.write('')
				_git('add', '.')
				_git('commit', '-am', 'first commit')

		# remove all previous files/folders except for .git!
		with cd(output):
			for f in os.listdir('.'):
				if not f == '.git':
					if path.isfile(f):
						os.remove(f)

					elif path.isdir(f):
						shutil.rmtree(f)

		# copy code from development to release!
		with cd(development):
			for f in os.listdir('.'):
				if path.isfile(f):
					shutil.copy2(f, output)
				elif path.isdir(f) and path.basename(f) != '.git':
					shutil.copytree(f, path.join(output, f), ignore=shutil.ignore_patterns('.git'))

		with cd(output):
			# setup with the specified remote
			LOG.debug('Setting up git remote for %s' % chosen_app)

			# remove any previous remote
			try:
				_git('remote', 'rm', 'heroku')
			except WebError:
				pass

			_git('remote', 'add', 'heroku', 'git@heroku.com:%s.git' % chosen_app)

			# commit
			_git('add', '.')
			diff = _git('diff', 'HEAD')
			if not diff.strip():
				# not interactive basically means we're using the trigger toolkit, where 'forge build'
				# doesn't really make sense
				if interactive:
					LOG.warning("No app changes detected: did you forget to forge build?")
				else:
					LOG.warning("No app changes detected, pushing to heroku anyway")
			else:
				_git('commit', '-am', 'forge package web')

			# push
			LOG.info('Deploying to %s.herokuapp.com' % chosen_app)

			# TODO: when running a packaged up toolkit there is no commandline... need to make sure
			# we can use the ssh key earlier somehow and ask for passphrase if not
			# also provide docs on how to use ssh-agent/pageant
			if not interactive:
				LOG.warning('If the packaging process hangs here, you need to set up ssh-agent or Pageant')

			# TODO: show our own one line progress bar when running non-verbosely
			push_output = _git('push', 'heroku', '--all', '--force', command_log_level=logging.INFO)

			if push_output.startswith('Everything up-to-date'):
				remote_output = _git('remote', '-v')
				remote_pattern = re.compile(r'git@heroku.com:(.*?).git \(fetch\)')

				remote_match = remote_pattern.search(remote_output)
				if remote_match:
					app_url = 'http://%s.herokuapp.com' % remote_match.group(1)
					_open_url(app_url)
					LOG.info('Deployed at %s' % app_url)

			else:
				deploy_pattern = re.compile(r'(http://[^ ]+) deployed to Heroku')
				deploy_match = deploy_pattern.search(push_output)
				if deploy_match:
					_open_url(deploy_match.group(1))
					LOG.info('Deployed at %s' % deploy_match.group(1))


