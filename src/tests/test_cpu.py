import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpu import *

class InstructionTests(unittest.TestCase):
	def setUp(self):
		self.cpu = CPU()

	def tearDown(self):
		pass


	def test_address_zero_page(self):
		self.cpu.memory.write(0x0010, 5)
		assert self.cpu.address_zero_page(0x10) == 5

	def test_address_zero_page_x(self):
		self.cpu.memory.write(0x0015, 5)
		self.cpu.X = 5
		assert self.cpu.address_zero_page_x(0x10) == 5

	def test_address_zero_page_y(self):
		self.cpu.memory.write(0x0015, 5)
		self.cpu.Y = 5
		assert self.cpu.address_zero_page_y(0x10) == 5

	def test_address_absolute(self):
		self.cpu.memory.write(0x1000, 5)
		assert self.cpu.address_absolute(0x1000) == 5

	def test_address_absolute_x(self):
		self.cpu.memory.write(0x1005, 5)
		self.cpu.X = 5
		assert self.cpu.address_absolute_x(0x1000) == 5	

	def test_address_absolute_y(self):
		self.cpu.memory.write(0x1005, 5)
		self.cpu.Y = 5
		assert self.cpu.address_absolute_y(0x1000) == 5			

	def test_address_indirect(self):
		self.cpu.memory.write(0x1000, 0x00)
		self.cpu.memory.write(0x1001, 0x20)
		self.cpu.memory.write(0x2000, 5)
		assert self.cpu.address_indirect(0x1000) == 5

	def test_address_indirect_x(self):
		self.cpu.memory.write(0x1000, 0x00)
		self.cpu.memory.write(0x1001, 0x20)
		self.cpu.memory.write(0x2000, 5)
		self.cpu.X = 1
		assert self.cpu.address_indirect_x(0x0FFF) == 5
	
	def test_address_indirect_y(self):
		self.cpu.memory.write(0x1000, 0x00)
		self.cpu.memory.write(0x1001, 0x20)
		self.cpu.memory.write(0x2000, 5)
		self.cpu.Y = 1
		assert self.cpu.address_indirect_y(0x0FFF) == 5

	def test_address_implied(self):
		assert self.cpu.address_none(0x1000) == None

	def test_address_accumulator(self):
		self.cpu.A = 5
		assert self.cpu.address_accumulator(0x1000) == 5

	def test_address_immediate(self):
		assert self.cpu.address_immediate(0x10) == 0x10	

	def test_address_relative(self):
		assert self.cpu.address_relative(0x10) == 0x10	

	#adc
	def test_adc_immediate(self): #0x69
		self.cpu.A = 0xFF
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 1)
		self.cpu.execute(*self.cpu.instructions[0x69])
		assert self.cpu.A == 0x00
		assert self.cpu.C == 1
		assert self.cpu.N == 0
		assert self.cpu.Z == 1
		assert self.cpu.PC == 0x1002

	def test_adc_zero_page(self): #0x65
		self.cpu.A = 0xFF
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.memory.write(0x0010, 0x1)
		self.cpu.execute(*self.cpu.instructions[0x65])
		assert self.cpu.A == 0x00
		assert self.cpu.C == 1
		assert self.cpu.N == 0
		assert self.cpu.Z == 1
		assert self.cpu.PC == 0x1002		

	def test_adc_zero_page_x(self): #0x65
		self.cpu.A = 0xFF
		self.cpu.X = 0x05
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.memory.write(0x0015, 0x1)
		self.cpu.execute(*self.cpu.instructions[0x75])
		assert self.cpu.A == 0x00
		assert self.cpu.C == 1
		assert self.cpu.N == 0
		assert self.cpu.Z == 1
		assert self.cpu.PC == 0x1002

	def test_adc_absolute(self): #0x65
		self.cpu.A = 0xFF
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x00)
		self.cpu.memory.write(0x1002, 0x20)
		self.cpu.memory.write(0x2000, 0x1)
		self.cpu.execute(*self.cpu.instructions[0x6d])
		assert self.cpu.A == 0x00
		assert self.cpu.C == 1
		assert self.cpu.N == 0
		assert self.cpu.Z == 1
		assert self.cpu.PC == 0x1003

if __name__ == '__main__':
	unittest.main()
