import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cpu import *

class InstructionTests(unittest.TestCase):
	def setUp(self):
		self.cpu = CPU()

	def tearDown(self):
		pass

	def test_memory_read16(self):
		self.cpu.memory.write(0x1000, 0x34)
		self.cpu.memory.write(0x1001, 0x12)
		assert self.cpu.memory.read16(0x1000) == 0x1234

	def test_memory_write16(self):
		self.cpu.memory.write16(0x1000, 0x1234)
		assert self.cpu.memory.read(0x1000) == 0x34
		assert self.cpu.memory.read(0x1001) == 0x12

	def test_address_zero_page(self):
		self.cpu.memory.write(0x0010, 5)
		assert self.cpu.zeroPage.read(0x10) == 5

	def test_address_zero_page_x(self):
		self.cpu.memory.write(0x0015, 5)
		self.cpu.X = 5
		assert self.cpu.zeroPageX.read(0x10) == 5

	def test_address_zero_page_y(self):
		self.cpu.memory.write(0x0015, 5)
		self.cpu.Y = 5
		assert self.cpu.zeroPageY.read(0x10) == 5

	def test_address_absolute(self):
		self.cpu.memory.write(0x1000, 5)
		assert self.cpu.absolute.read(0x1000) == 5

	def test_address_absolute_x(self):
		self.cpu.memory.write(0x1005, 5)
		self.cpu.X = 5
		assert self.cpu.absoluteX.read(0x1000) == 5	

	def test_address_absolute_y(self):
		self.cpu.memory.write(0x1005, 5)
		self.cpu.Y = 5
		assert self.cpu.absoluteY.read(0x1000) == 5			

	def test_address_indirect(self):
		self.cpu.memory.write(0x1000, 0x00)
		self.cpu.memory.write(0x1001, 0x20)
		self.cpu.memory.write(0x2000, 5)
		assert self.cpu.indirect.read(0x1000) == 5

	def test_address_indirect_x(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write(0x2000, 5)
		self.cpu.X = 1
		assert self.cpu.indirectX.read(0x0FFF) == 5
	
	def test_address_indirect_y(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write(0x2001, 5)
		self.cpu.Y = 1
		assert self.cpu.indirectY.read(0x1000) == 5

	def test_address_implied(self):
		assert self.cpu.implied.read(0x1000) == None

	def test_address_accumulator(self):
		self.cpu.A = 5
		assert self.cpu.accumulator.read(0x1000) == 5

	def test_address_immediate(self):
		assert self.cpu.immediate.read(0x10) == 0x10	

	def test_address_relative(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		assert self.cpu.relative.read(0x1001) == 0x1010	

	def test_adc(self): #0x69
		self.cpu.A = 0xFF
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 1)
		self.cpu.execute(*self.cpu.instructions[0x69])
		assert self.cpu.A == 0x00
		assert self.cpu.C == 1
		assert self.cpu.N == 0
		assert self.cpu.Z == 1
		assert self.cpu.PC == 0x1002

	def test_branch_fail(self):
		initCycles = self.cpu.cycles
		self.cpu.PC=0x1000
		self.cpu.C = 1
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.execute(*self.cpu.instructions[0x90])
		assert self.cpu.PC == 0x1002
		assert self.cpu.cycles == initCycles + 2

	
	def test_branch_successful(self):
		initCycles = self.cpu.cycles
		self.cpu.PC=0x1000
		self.cpu.C = 0
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.execute(*self.cpu.instructions[0x90])
		assert self.cpu.PC == 0x1012
		assert self.cpu.cycles == initCycles + 3


	def test_branch_page_cross(self):
		initCycles = self.cpu.cycles
		self.cpu.PC= 0x10F0
		self.cpu.C = 0
		self.cpu.memory.write(0x10F1, 0x10)
		self.cpu.execute(*self.cpu.instructions[0x90])
		assert self.cpu.PC == 0x1102
		assert self.cpu.cycles == initCycles + 4

if __name__ == '__main__':
	unittest.main()
