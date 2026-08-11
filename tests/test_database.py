# tests/test_database.py

import os
import sys
import datetime

today = datetime.date.today()
tomorrow = today+datetime.timedelta(days=1)
tomorrow2 = today+datetime.timedelta(days=2)

#print('today:', today)
#print('tomorrow:', tomorrow)
#print('tomorrow2:', tomorrow2)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
wdir = os.path.join(dname, '..')
os.chdir(wdir)

print('Current working directory set to:', os.getcwd())

for i in ['database', 'utils']:
	sys.path.append(os.path.join(os.getcwd(), 'database'))

from database.database import Database

DB_FILE = "tests/test_database.db"


tables = ['book_records', 'user_records', 'borrow_records']

dummy_book_data = [
	{
		'book_id': 1,
		'title': 'Science in Action',
		'subject': 'Biology',
		'author': 'Diamond Heart',
		'isbn': 'null',
		'status': 'new'
	},
	
	{
		'book_id': 2,
		'title': 'Physics 2',
		'subject': 'Physics',
		'author': 'Robert Mitei',
		'isbn': 'null',
		'status': 'old'
	}
]

dummy_user_data = [
	{
		'user_id': 10669,
		'user_name': 'Diamond Ebenyo'
	},
	
	{
		'user_id': 10670,
		'user_name': 'Raymond Ebenyo'
	},
	
	{
		'user_id': 10668,
		'user_name': 'Roy Chirchir'
	}
]

dummy_borrow_data = [
	{
		'book_id': 1,
		'user_id': 10670,
		'borrow_date': today,
		'return_date': tomorrow
	},
	
	{
		'book_id': 2,
		'user_id': 10668,
		'borrow_date': tomorrow,
		'return_date': tomorrow2
	}
]



def run_test():

	# remove old database
	if os.path.exists(DB_FILE):
		os.remove(DB_FILE)


	db = Database(DB_FILE)

	print("Creating tables...")
	db.create_tables()
	
	print("Inserting Book data...")
	for item in dummy_book_data:
		db.insert_book_records(item)

	print("Inserting User data...")
	for item in dummy_user_data:
		db.insert_user_records(item)

	print("Inserting Borrowing data...")
	for item in dummy_borrow_data:
		db.insert_borrow_records(item)

	print("\nUser table:")
	rows = db.get_all("user_records")

	for row in rows:
		print(row)
		
	print('\nBook table:')
	rows = db.get_all('book_records')
	
	for row in rows:
		print(row)
		
	print('\nBorrow table')
	rows = db.get_all('borrow_records')
	
	for row in rows:
		print(row)

	print("\nSearching user_id 10669:")
	result = db.search("user_records", "user_id", 10669)

	print(result[0])
	
	print('\nSearching book_id 1:')
	result = db.search('book_records', 'book_id', 1)
	
	print(result[0])
	
	print('\nDeleting user_id 10668:')
	db.delete_user_record(10668)
	
	rows = db.get_all("user_records")

	print('\nDisplaying user records:')
	for row in rows:
		print(row)
		
	print('\nUpdating user records - 10669:')
	db.update('user_records', 'user_name', 'Diamond Heart Ebenyo')
	
	result = db.search("user_records", "user_id", 10669)

	print(result[0])

	db.close()
	
	os.remove(DB_FILE)
	print('\nRemoved test_database.db')

if __name__ == "__main__":
	run_test()
