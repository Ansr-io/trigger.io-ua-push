import subprocess
import uuid
import plistlib
import json

class XcodeProject:
	def __init__(self, path):
		# Make sure the file is converted to json (could be xml or openstep)
		pbxproj_json = subprocess.check_output(['plutil', '-convert', 'json', '-o', '-', path])
		self.path = path
		self.pbxproj = json.loads(pbxproj_json)

	def add_file(self, path, sourceTree, settings=None):
		"""Add a file to the xcode project for ios, return build ref for file"""
		
		for possible_file in self.pbxproj['objects']:
			if "path" in self.pbxproj['objects'][possible_file] and self.pbxproj['objects'][possible_file]["path"] == path and possible_file.endswith("file"):
				return possible_file[:-4]+'build'

		file_uuid = str(uuid.uuid4())
		
		# Add file ref (A reference to an actual file on the disk)
		self.pbxproj['objects'][file_uuid+'file'] = {
			"isa": "PBXFileReference",
			"path": path,
			"sourceTree": sourceTree
		}
		# Add build ref (A reference to a file ref to be used during builds)
		self.pbxproj['objects'][file_uuid+'build'] = {
			"isa": "PBXBuildFile",
			"fileRef": file_uuid+"file"
		}
		# Add the file to the structure of the project (so it actually shows up in xcode)
		for key in self.pbxproj['objects']:
			if isinstance(self.pbxproj['objects'][key], dict) and self.pbxproj['objects'][key]['isa'] == 'PBXGroup' and "name" in self.pbxproj['objects'][key] and self.pbxproj['objects'][key]['name'] == 'Frameworks':
				self.pbxproj['objects'][key]['children'].append(file_uuid+'file')
				break

		if settings:
			self.pbxproj['objects'][file_uuid+'build']['settings'] = settings

		return file_uuid+'build'

	def add_framework(self, path, sourceTree):
		"""Add a framework to the xcode project for ios"""
		
		ref = self.add_file(path, sourceTree, {'ATTRIBUTES': ('Weak',)})
	
		# Add build ref to list of linked frameworks
		for key in self.pbxproj['objects']:
			if isinstance(self.pbxproj['objects'][key], dict) and self.pbxproj['objects'][key]['isa'] == 'PBXFrameworksBuildPhase':
				if ref not in self.pbxproj['objects'][key]['files']:
					self.pbxproj['objects'][key]['files'].append(ref)
				break
	
	def add_resource(self, path):
		"""Add a resource to the xcode project for ios"""

		ref = self.add_file(path, "<group>")

		# Add build ref to list of resources
		for key in self.pbxproj['objects']:
			if isinstance(self.pbxproj['objects'][key], dict) and self.pbxproj['objects'][key]['isa'] == 'PBXResourcesBuildPhase':
				self.pbxproj['objects'][key]['files'].append(ref)
				break

	def add_saved_framework(self, path, sourceTree):
		"""Add a saved framework to xcode build output"""
		
		ref = self.add_file(path, sourceTree)
	
		# Add build ref to list of linked frameworks
		for key in self.pbxproj['objects']:
			if isinstance(self.pbxproj['objects'][key], dict) and self.pbxproj['objects'][key]['isa'] == 'PBXCopyFilesBuildPhase':
				if ref not in self.pbxproj['objects'][key]['files']:
					self.pbxproj['objects'][key]['files'].append(ref)
				break

	def save(self):
		# Save the output result (as xml)
		plistlib.writePlist(self.pbxproj, self.path)