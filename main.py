# main.py

from core.engine import Engine
from tests.test_database import run_test

class LibrarySystem:
	def __init__(self):
		self.engine = Engine()
		
if __name__ == '__main__':
	ls = LibrarySystem()
	run_test()

