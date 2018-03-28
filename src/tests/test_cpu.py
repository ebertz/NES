import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpu import *

class InstructionTests(unittest.TestCase):
	def setUp(self):
		self.cpu = CPU()

	def tearDown(self):
		pass

	def test_0x00(self):
		self.cpu.execute(*self.cpu.instructions[0x00])
		assert True

	def test_0x01(self):
		assert True

if __name__ == '__main__':
	unittest.main()
