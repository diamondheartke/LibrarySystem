# database.py

from utils.logger import Logger

import sqlite3
import sys

class Database:
	def __init__(self, db_file):
		self.log = Logger()
		
		self.log.event_logs('db_connect', self.log.info['sql_connection'])
		
		self.conn = sqlite3.connect(db_file)
		self.c = self.conn.cursor()
		
		self.log.event_logs('db_connect', self.log.success['sql_connection_success'])
		
		self.tables = ['book_records', 'user_records', 'borrow_records']

	def create_tables(self):
		'''Creates tables with proper foreign key constraints.'''
		
		# Enforce foreign key constraints in SQLite
		self.c.execute("PRAGMA foreign_keys = ON;")

		tables = {
			"book_records": """
				CREATE TABLE IF NOT EXISTS book_records (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					book_id INTEGER UNIQUE NOT NULL,
					title TEXT NOT NULL,
					subject TEXT,
					author TEXT,
					isbn TEXT,
					status TEXT DEFAULT 'available'
				);
			""",
			"user_records": """
				CREATE TABLE IF NOT EXISTS user_records (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					user_id INTEGER UNIQUE NOT NULL,
					user_name TEXT NOT NULL
				);
			""",
			"borrow_records": """
				CREATE TABLE IF NOT EXISTS borrow_records (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					book_id INTEGER NOT NULL,
					user_id INTEGER NOT NULL,
					borrow_date TEXT NOT NULL,
					due_date TEXT NOT NULL,
					return_date TEXT,
					status TEXT DEFAULT 'active',
					FOREIGN KEY (book_id) REFERENCES book_records(book_id) ON DELETE CASCADE,
					FOREIGN KEY (user_id) REFERENCES user_records(user_id) ON DELETE CASCADE
				);
			"""
		}

		try:
			for table_name, query in tables.items():
				self.c.execute(query)
			self.conn.commit()
			print("[INFO] All database tables created successfully.")
			
		except sqlite3.OperationalError as e:
			print(f'[ERROR] Error creating database tables: {e}', file=sys.stderr)
			
		except Exception as e:
			print(f'[ERROR] Unexpected error: {e}', file=sys.stderr)
			
	'''
	Eliminates String Manipulation Bugs: No trailing commas or invalid SQL string generation.

Readable & Maintainable: Schema changes are plain SQL and easy to inspect.

Idempotent (IF NOT EXISTS): Safe to run on app startup without crashing if tables already exist.

PRAGMA foreign_keys = ON;: Guarantees SQLite enforces relationships between borrow_records, book_records, and user_records.
	'''
			
	def insert_user_records(self, data):
		'''
		data format:
			{
				'user_name': 'TEXT',
				'user_id': 'INTEGER UNIQUE'
			}
		'''
		try:
			self.c.execute('''INSERT INTO user_records 
							(user_name, user_id)
							values(?, ?)''',
							(data['user_name'], data['user_id']))
		except sqlite3.IntegrityError as e:
			print(f'[ERROR] Error inserting value: {e}', file=sys.stderr)
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
		try:
			self.c.execute('''INSERT INTO book_records
							(book_id, title, subject, author, isbn, status)
							values(?, ?, ?, ?, ?, ?)''',
							(data['book_id'], data['title'], data['subject'], data['author'], data['isbn'], data['status'])
			)
		except sqlite3.IntegrityError as e:
			print(f'[ERROR] Error inserting value: {e}', file=sys.stderr)
		finally:
			self.conn.commit()
			
	def insert_borrow_records(self, data):
		'''
		data format:
			{
				'book_id': 'INTEGER UNIQUE',
				'user_id': 'INTEGER UNIQUE',
				'borrow_date': 'TEXT',
				'return_date': 'TEXT'
			}
		'''
		try:
			self.c.execute('''INSERT INTO borrow_records
							(book_id, user_id, borrow_date, return_date)
							values(?, ?, ?, ?)''',
							(data['book_id'], data['user_id'], data['borrow_date'], data['return_date'])
				)
		except sqlite3.IntegrityError as e:
			print(f'[ERROR] Error inserting value: {e}', file=sys.stderr)
		finally:
			self.conn.commit() 

	def delete_book_record(self, book_id):
		if not isinstance(book_id, int):
			self.log.error_logs('delete_book', self.log.use['invalid_input'])
			raise ValueError('Invalid book_id')
		try:
			self.execute(f"DELETE FROM book_records WHERE book_id=?", (book_id,))
		except Exception as e:
			print(f'[ERROR] Failed to delete book record - {book_id}: {e}', file=sys.stderr)
		finally:
			self.conn.commit()
			
	def delete_user_record(self, user_id):
		if not isinstance(user_id, int):
			self.log.error_logs('delete_book', self.log.use['invalid_input'])
			raise ValueError('Invalid book_id')
		try:
			self.c.execute(f"DELETE FROM user_records WHERE user_id=?", (user_id,))
		except Exception as e:
			print(f'[ERROR] Failed to delete book record - {user_id}: {e}', file=sys.stderr)
		finally:
			self.conn.commit()

	def get_all(self, table):
		if table not in self.tables:
			raise ValueError('Invalid table')

		self.c.execute(f'SELECT * FROM {table}')

		return self.c.fetchall()
		

	def search(self, table, column, value):
		if table not in self.tables:
			raise ValueError('Invalid table')

		allowed_columns = ['book_id', 'subject', 'author', 'isbn', 'status', 'user_id', 'user_name', 'borrow_date', 'return_date']

		if column not in allowed_columns:
			raise ValueError('Invalid search column')

		try:
			self.c.execute(f"SELECT * FROM {table} WHERE {column}=?", (value,))
			return self.c.fetchall()

		except Exception as e:
			print(f'[ERROR] Search failed: {e}')
			

	def update(self, table, column, value):
		if table not in self.tables:
			raise ValueError('Invalid table')

		allowed_columns = ['book_id', 'subject', 'author', 'isbn', 'status', 'user_id', 'user_name', 'borrow_date', 'return_date']

		if column not in allowed_columns:
			raise ValueError('Invalid search column')

		try:
			self.c.execute(f'UPDATE {table} SET {column}=?', (value,))
		except Exception as e:
			print(f'[ERROR] Failed to update {column}: {e}', file=sys.stderr)

	def close(self):
		self.conn.close()
