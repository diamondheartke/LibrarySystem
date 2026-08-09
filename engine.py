# engine.py

from database import DataBase

import json
import os
import sys
import time

class LibrarySystem:
	def __init__(self):
		self.event_logs('launch_time', 500)
		self.config = self.load_config()
		
		self.db = self.config['database']
		self.subjects = self.config['subjects']
		
		self.DataBase = DataBase('test.db', self.subjects)
		
		self.search = self.DataBase.database_search({'table': 'English', 'token': 10669})
		
	def event_logs(self, log, status_code):
		actions = {
			'launch_time': f"Launching: status code {status_code} - {time.ctime()}\n{'-'*70}",
			'config_file': f'Loading: status code {status_code} - {time.ctime()}'
		}
		
		for key, val in actions.items():
			if key == log:
				if key == 'launch_time':
					log = f"\n\n{'-'*70}\n[Event] {key} - {val}"
				else:
					log = f'\n[Event] {key} - {val}'
			
		if os.path.exists('event_log.txt'):
			with open('event_log.txt', 'a', encoding='utf-8') as f:
				f.write(log)
				
		else:
			with open('event_log.txt', 'w', encoding='utf-8') as f:
				f.write(f'\n[Event] Created log.txt - {time.ctime()}')
				f.write(log)
			
	def load_config(self):
		''' Loads the configuration file (config.json)'''
		config_file = 'config.json'
		if os.path.exists(config_file) and os.path.getsize(config_file):
			self.event_logs('config_file', 500)
			with open(config_file, 'r', encoding='utf-8') as f:
				sys.stdout.writelines('[INFO] Successfully Loaded Configuration File.')
				return json.load(f)

		else:
			self.write_logs('config_file', 404)
			sys.stderr.writelines('[ERROR] Configuration File \'config.json\' Is Missing or Corrupted.')
			prompt = input('\nProceed with fallback configuration file (y|n): ').lower()
			if prompt == 'y':
				self.event_logs('config_file', 200)
				with open(config_file, 'w', encoding='utf-8') as f:
					data = {'version': 'v1.0.0', 'database': 'data/database.db', 'subjects': ['English', 'Math', 'Computer', 'Science', 'Other']}
					json.dump(data, f, ensure_ascii=False, indent=4)
					sys.stdout.writelines('[INFO] Successfully Created Fallback Configuration File.')
					
			elif prompt == 'n':
				sys.stderr.writelines('[ERROR] Failed To Create Fallback Configuration File.')
				self.event_logs('config_file', 100) # I don't know the exact status codes, but this are placeholders
				
			else:
				sys.stdout.writelines('\'y\' or \'n\'')
			
if __name__ == '__main__':
	LS = LibrarySystem()
