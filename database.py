# database.py

import sqlite3
import sys

class Database:
	def __init__(self, db_file, subjects):
		self.subj = subjects

		self.conn = sqlite3.connect(db_file)
		self.c = self.conn.cursor()

	def create_tables(self):
		''' Creates tables if they do not exist'''
		tables = [
			{'books': {
				'id': 'INTEGER PRIMARY KEY AUTOINCREMENT, ',
				'book_id': 'INTEGER UNIQUE, ',
				'title': 'TEXT, ',
				'subject': 'TEXT, ',
				'author': 'TEXT, ',
				'isbn': 'TEXT, ',
				'status': 'TEXT'
				}

		},
			{'users': {
				'id': 'INTEGER PRIMARY KEY AUTOINCREMENT, ',
				'name': 'TEXT, ',
				'user_id': 'INTEGER UNIQUE'
				}

		},
			{'borrow_records': {
				'id': 'INTEGER PRIMARY KEY AUTOINCREMENT, ',
				'book_id': 'INTEGER UNIQUE, ',
				'user_id': 'INTEGER UNIQUE, ',
				'borrow_date': 'TEXT, ',
				'return_date': 'TEXT'
				}

		}
	]

		current_tables = []
		table_values = ''
		try:
			for i, x in enumerate(tables):
				for table, value in x.items():
					current_tables.append(table)
					for key, val in value.items():
						table_values += f'{key} {val}'
				print(table_values)
				self.c.execute(f"CREATE TABLE {table} ({table_values})")
				table_values = ''
		except sqlite3.OperationalError as e:
			print(f'[ERROR] Error creating table \'{current_tables[len(current_tables)-1]}\': {e}', file=sys.stderr)
		finally:
			self.conn.commit()

	def insert_book_records(self, data):
		'''
		data format:
			{
				'book_id': 'INTEGER UNIQUE',
				'title': 'TEXT',
				'subject': 'TEXT',
				'author': 'TEXT',
				'isbn': 'TEXT',
				'status': 'TEXT'
			}
		'''
		table = data['table']
		if table not in self.subj:
			raise ValueError('Invalid subject table')

		try:
			self.c.execute(f'''INSERT INTO {data['table']}
							(token, assigned, type)
							values(?, ?, ?)''',
							(data['token'], data['assigned'], data['type'])
			)
		except sqlite3.IntegrityError as e:
			print(f'[ERROR] Error inserting value: {e}', file=sys.stderr)
		finally:
			print(f"[INFO] Initiated inserted data to {data['table']}", file=sys.stderr)
			self.conn.commit()

	def delete_data(self, table, token):
		if table not in self.subj:
			raise ValueError('Invalid subject')
		try:
			self.execute(f"DELETE FROM {table} WHERE token=?", (token,))
		except Exception as e:
			print(f'[ERROR] Failed to delete {token}: {e}', file=sys.stderr)
		finally:
			self.conn.commit()

	def get_all(self, subject):
		if subject not in self.subj:
			raise ValueError('Invalid subject')

		self.c.execute(f'SELECT * FROM {subject}')

		return self.c.fetchall()

	def search(self, table, column, value):
		if table not in self.subj:
			raise ValueError('Invalid subject table')

		allowed_columns = ["id", "token", "assigned", "type"]

		if column not in allowed_columns:
			raise ValueError('Invalid search column')

		try:
			self.c.execute(f"SELECT * FROM {table} WHERE {column}=?", (value,))
			return self.c.fetchall()

		except Exception as e:
			print(f'[ERROR] Search failed: {e}')

	def update(self, table, column, value):
		if table not in self.subj:
			raise ValueError('Invalid subject table')

		allowed_columns = ["id", "token", "assigned", "type"]

		if column not in allowed_columns:
			raise ValueError('Invalid search column')

		try:
			self.c.execute(f'UPDATE {table} SET {column}=?', (value,))
		except Exception as e:
			print(f'[ERROR] Failed to update {column}: {e}', file=sys.stderr)

	def close(self):
		self.conn.close()
