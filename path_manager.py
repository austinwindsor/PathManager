# author:		Austin Windsor

import os
import shutil
import logging

class PathManager:
	def __init__(self, root=''):
		self.root = root

	def setup_directory_system(self, directory_system=["input", "output","debug","logs"]):
		""""
		this method iterates through each brach of the input directory system and recrusively creates 
		the system.

		Parameters:
		directory_system:	(list of lists) the lsit of lists denote the hierarchical structure of the dir system
							ex: 	[	input,
											[folder1,
											folder2],
										output,
											[folder1,
											folder2,
												[folder3,
												folder4]
											],
									]
		Output:
		Completion status: 1 (success) or 0 (failure)
		"""
		self._make_dir_tree(directory_system, root=self.root)
		return 1

	def make_dir(self, folder):
		if os.path.exists(folder):
			print("folder aleady exists: %s" % folder)
		else:
			print("+++ making folder: %s" % folder)
			os.mkdir( folder )

	def make_dir_iter(self, folders, path):
		folders = folders if type(folders)==list else folders.replace("\\","/").split("/")
		for arg in folders:
			self.make_dir( os.path.join( path, arg) )
			path = os.path.join( path,  arg)
		return 1

	def _make_dir_tree(self, structure, root, spaces=1, verbose=False):
		"""private method to recursively buil the directories in directory system"""
		curr_root = os.path.join( root, structure[0])

		if not os.path.exists( curr_root ):
			print('\t'*spaces+'making dir: %s' % structure[0])
			self.make_dir_iter( str( structure[0]) , path=root)

		else:
			print('\t'*spaces+'dir already made: %s' % structure[0])

		try:
			if structure[1]:
				for i in range(1, len(structure)):
					self._make_dir_tree(structure = structure[i], root=curr_root, spaces = spaces+1)
				else:
					return 

		except IndexError as e:
			logging.error("Error: the full tree strucute and any substree should follow the format\
							[root, [subtree]], even for leaf nodes where the subtree list is an empty list [].")
			logging.error(e)

	def save_folder_paths(self, folder_dict={"input": "input", "output":"output"}):

		try:
			assert type(folder_dict)==folder_dict
		except AssertionError:
			print("ERROR: save_folder_method only accepts a dictionary (ex: {file nickname: 'relative path/to/folder'}")
			raise TypeError

		self.paths = folder_dict

	def transfer_files(self, target_path, source_path, files):
		"""
		transfer files from one path to another path. If you want to do this for different sources and 
		targets, use map(  lambda x: transfer_files(**x), [{'target_path':'','source_path':'','files':[]}])

		Parameters:
		source_path: 		(str/path object)  path to copy the file(s) from
		target_path: 		(str/path object)  path to send the file(s) to
		files:				(str/llist of str) string of simple of filenames or list of such strings

		Output:
		None
		"""
		files = files if type(files)==list else [files]
		for file in files:
			print('%s: %s ---> %s' % (files, source_path, target_path))

			if not os.path.exists(target_path):
				self.make_dir_iter( target_path )

			shutil.copy( os.path.join( source_path, file), os.path.join( target_path, file))


