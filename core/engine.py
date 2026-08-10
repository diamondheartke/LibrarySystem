# engine.py

from database.database import Database
from utils.logger import Logger

import json
import os
import sys

class Engine:
	def __init__(self):
		self.log = Logger()
		
		# Log Launch Time
		self.log.event_logs('launch_time', self.log.info['launch'])
		
		self.config = self.load_config()
		if isinstance(self.config, dict):
			sys.stdout.write('[INFO] Configuration file successfully loaded.')
			self.log.event_logs('config_file', self.log.success['loading_success'])
		
		self.db = self.config['database']
		
		self.Database = Database('test.db')
	
	def load_json(self, json_file):
		with open(json_file, 'r', encoding='utf-8') as f:
			return json.load(f)
			
	def load_config(self):
		''' Loads the configuration file (config.json)'''
		config_file = 'configuration/config.json'
		
		if os.path.exists(config_file) and os.path.getsize(config_file):
			self.log.event_logs('config_file', self.log.info['load_config'])
			return self.load_json(config_file)

		else:
			self.log.event_logs('config_file', self.log.user_error['not_found'])
			sys.stderr.write('[ERROR] Configuration File \'config.json\' Is Missing or Corrupted.')
			prompt = input('\nProceed with fallback configuration file (y|n): ').lower()
			if prompt == 'y':
				with open(config_file, 'w', encoding='utf-8') as f:
					data = {'version': 'v1.0.0', 'database': 'database/database.db'}
					json.dump(data, f, ensure_ascii=False, indent=4)
					self.log.event_logs('config_file', self.log.warning['fallback'])
					sys.stdout.write('[INFO] Successfully Created Fallback Configuration File.')
					self.log.event_logs('config_file', self.log.info['load_config'])
				return self.load_json(config_file)
					
			elif prompt == 'n':
				sys.stderr.write('[ERROR] Failed To Create Fallback Configuration File.')
				self.log.event_logs('config_file', self.log.system_error['file_system_error'])
				
			else:
				sys.stdout.write('\'y\' or \'n\'')
			
if __name__ == '__main__':
	LS = LibrarySystem()
