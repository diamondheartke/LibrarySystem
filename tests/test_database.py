# tests/test_database.py

import sys
import os

path = sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import Database

DB_FILE = "test_database.db"


subjects = [
	"English",
	"Math",
	"Computer",
	"Science",
	"Other"
]


dummy_data = [
	
]



def run_test():

	# remove old database
	if os.path.exists(DB_FILE):
		os.remove(DB_FILE)


	db = Database(DB_FILE, subjects)

	print("Creating tables...")
	db.create_tables()
	

	print("Inserting data...")
	for item in dummy_data:
		db.insert_data(item)
		

	print("\nEnglish table:")
	rows = db.get_all("English")

	for row in rows:
		print(row)
		
	print('\nMath table:')
	rows = db.get_all('Math')
	
	for row in rows:
		print(row)
		
	print('\nComputer table')
	rows = db.get_all('Computer')
	
	for row in rows:
		print(row)

	print("\nSearching token 10669:")
	result = db.search("English", "token", 10669)

	print(result[0])

	db.close()

if __name__ == "__main__":
	run_test()
