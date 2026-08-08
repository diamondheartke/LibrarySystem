# database.py

import sqlite3
import sys

class DataBase:
	def __init__(self, db_file, subjects):
		self.conn = sqlite3.connect(db_file)
		self.c = self.conn.cursor()
		
		self.subj = subjects
		
	def database_check(self):
		sys.stdout.writelines('[INFO] Performing Database Check....')
		try:
			for subj in self.subj:
				self.c.execute(f'''CREATE TABLE {subj} (
				id INTEGER PRIMARY KEY AUTOINCREMENT, 
				token INTEGER UNIQUE,
				assigned INTEGER UNIQUE,
				type TEXT
			) 
		''')  
		except sqlite3.OperationalError as e:
			sys.stderr.writelines(f'[ERROR] Error creating table: {e}')
		finally:
			sys.stdout.writelines('\n[INFO] Database Check Complete.')
			
	def insert_data(self, data):
		try:
			self.c.execute(f'''INSERT INTO {data['table']}(token, assigned, type)
			values(?, ?, ?)''', (data['token'], data['assigned'], data['type']))
		except sqlite3.IntegrityError as e:
			sys.stderr.writelines(f'[ERROR] Error inserting value: {e}')
		except sqlite3.ProgrammingError as e:
			sys.stderr.writelines(f'[ERROR] Error inserting value: {e}')
		finally:
			sys.stdout.writelines(f"[INFO] Initiated inserted data to {data['table']}")
			self.conn.commit()
			
	def remove_data(self, data):
		try:
			self.execute(f"DELETE FROM {data['table']} WHERE token{data['token']}")
		except AttributeError:
			pass
		finally:
			sys.stdout.writelines(f"[INFO] Intiated deleted data from {data['table']}")
			self.conn.commit()
			
	def display_db(self, subject):
		self.c.execute(f'SELECT * FROM {subject}')
		return self.c.fetchall()
		
	def database_search(self, data):
		try:
			self.c.execute(f"SELECT * FROM {data['table']} WHERE token=? OR assigned=? OR type=?", (data['token'], data['assigned'], data['type']))
			return self.c.fetchall()
		except AttributeError:
			pass
		finally:
			sys.stdout.writelines(f"[INFO] Initiated searched for data from {data['table']}")
			return None
			
	def update_database(self, data):
		self.c.execute()

if __name__ == '__main__':
	dummy_db = 'test.db'
	dummy_subjects = ['English', 'Math', 'Computer', 'Science', 'Other']
	dummy_data = {
		1: {'table': 'English',
		'token': 10669,
		'assigned': 'Diamond Ebenyo',
		'type': 'KLB'},
		2: {'table': 'English',
		'token': 10670,
		'assigned': 'Raymond Ebenyo',
		'type': 'KLB'},
		3: {'table': 'English',
		'token': 10668,
		'assigned': 'Roy Chirchir',
		'type': 'KLB'},
		4: {'table': 'English',
		'token': 10667,
		'assigned': 'Dancan Kibet',
		'type': 'KLB'},
		5: {'table': 'English',
		'token': 10665,
		'assigned': 'Random Person',
		'type': 'KLB'}
	}
	
	db = DataBase(dummy_db, dummy_subjects)
	
	db.database_check()
	
	for key in dummy_data.keys():
		data = dummy_data[key]
		db.insert_data(data)
	
	for subj in dummy_subjects:
		print(f"{'-'*50} \n{subj} {'-'*50}")
		for data in db.display_db(subj):
			print(data)

	db.remove_data({'table': 'English', 'token': 10668})
	check = db.database_search({'table': 'English', 'token': 10669, 'type': 'KLB', 'assigned': 'Diamond Ebenyo'}) if not None else 'Empty'
	print(check)
