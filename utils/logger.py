# utils/logger.py

import os
import time
import json

class Logger:
	def __init__(self):
		self.config = self.load_log_config()
		
		self.logs_path = self.config['logs_path']
		
		self.info = self.config['status_codes']['info_process_state']
		self.success = self.config['status_codes']['successfull_ops']
		self.warning = self.config['status_codes']['warnings_recover']
		self.user_error = self.config['status_codes']['user_input_config_errors']
		
	def load_json(self, json_file):
		with open(json_file, 'r', encoding='utf-8') as f:
			return json.load(f)
	
	def load_log_config(self):
		''' Loads the configuration file (log_config.json)'''
		config_file = 'configuration/log_config.json'
		
		data = {
			'status_codes': {
				'info_process_state': {
					'launch': 100,
					'close': 101,
					'load_config': 102,
					'sql_connection': 103,
					'validate_tables': 104,
					'import_modules': 105,
					'authentication': 106,
					'database_backup': 107
				},
				
				'successfull_ops': {
					'generic_success': 200,
					'new_book': 201,
					'new_member': 202,
					'book_update': 203,
					'book_delete': 204,
					'loading_success': 205,
					'sql_connection_success': 206,
					'search_complete': 207,
					'transaction_complete': 208
				},
				
				'warnings_recover': {
					'fallback': 300,
					'missing_optional': 301,
					'duplicate_detected': 302,
					'deprecated_feature': 303,
					'partial_success': 304,
					'retry_required': 305
				},
				
				'user_input_config_errors': {
					'invalid_input': 400,
					'unauthorized': 401,
					'permission_denied': 402,
					'forbidden_action': 403,
					'not_found': 404,
					'invalid_config': 405,
					'missing_required_data': 406,
					'duplicate_entry': 407,
					'invalid_ops': 408,
					'conflict': 409
				},
				
				'system_errors': {
					'internal_error': 500,
					'not_implemented': 501,
					'database_failure': 502,
					'service_unavailable': 503,
					'file_system_error': 504,
					'memory_error': 505,
					'dependency_failure': 506,
					'corrupted_data': 507
				}
			},
			
			'logs_path': 'utils/logs'
		}
			
		if os.path.exists(config_file) and os.path.getsize(config_file):
			return self.load_json(config_file)
			
		else:
			with open(config_file, 'w', encoding='utf-8') as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
				return self.load_json(config_file)
	
	def event_logs(self, log, status_code):
		log_file = 'event_log.txt'
		path = os.path.join(self.logs_path, log_file)
		
		events = {
			'launch_time': f"Launching: status code {status_code} - {time.ctime()}\n{'-'*70}",
			'config_file': f'Loading Configuration file: status code {status_code} - {time.ctime()}'
		}
		
		for key, val in events.items():
			if key == log:
				if key == 'launch_time':
					log = f"\n\n{'-'*70}\n[Event] {key} - {val}"
				else:
					log = f'\n[Event] {key} - {val}'
			
		if os.path.exists(path):
			with open(path, 'a', encoding='utf-8') as f:
				f.write(log)
				
		else:
			with open(path, 'w', encoding='utf-8') as f:
				f.write(f'\n[Event] Created {log_file} - {time.ctime()}')
				f.write(log)
				
	def exception_logs(self, exception):
		log_file = 'exception_log.txt'
		path = os.path.join(self.logs_path, log_file)
			
		if os.path.exists(path):
			with open(path, 'a', encoding='utf-8') as f:
				f.write(exception)
				
		else:
			with open(path, 'w', encoding='utf-8') as f:
				f.write(f'\n[Event] Created {log_file} - {time.ctime()}')
				f.write(exception)
				
	def error_logs(self, log, status_code):
		log_file = 'error_log.txt'
		path = os.path.join(self.logs_path, log_file)
		
		errors = {
			'error': f'Error - status code {status_code}' # placeholder
		}
		
		for key, val in errors.items():
			if key == log:
				if key == 'launch_time':
					log = f"\n\n{'-'*70}\n[Event] {key} - {val}"
				else:
					log = f'\n[Event] {key} - {val}'
			
		if os.path.exists(path):
			with open(path, 'a', encoding='utf-8') as f:
				f.write(log)
				
		else:
			with open(path, 'w', encoding='utf-8') as f:
				f.write(f'\n[Event] Created {log_file} - {time.ctime()}')
				f.write(log)
	
