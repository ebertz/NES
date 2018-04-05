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

	def test_address_zero_page_read(self):
		self.cpu.memory.write(0x10, 5)
		self.cpu.memory.write(0x1000, 0x10)
		assert self.cpu.zeroPage.read(0x1000) == 5

	def test_address_zero_page_x_read(self):
		self.cpu.memory.write(0x15, 5)
		self.cpu.memory.write(0x1000, 0x10)
		self.cpu.X = 5
		assert self.cpu.zeroPageX.read(0x1000) == 5

	def test_address_zero_page_y_read(self):
		self.cpu.memory.write(0x15, 5)
		self.cpu.memory.write(0x1000, 0x10)
		self.cpu.Y = 5
		assert self.cpu.zeroPageY.read(0x1000) == 5

	def test_address_absolute_read(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write(0x2000, 5)
		assert self.cpu.absolute.read(0x1000) == 5

	def test_address_absolute_x_read(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write(0x2010, 0x5)
		self.cpu.X = 0x10
		assert self.cpu.absoluteX.read(0x1000) == 0x5	

	def test_address_absolute_y_read(self):
		self.cpu.memory.write(0x1000, 0x2000)
		self.cpu.memory.write(0x2010, 0x5)
		self.cpu.Y = 0x10
		assert self.cpu.absoluteY.read(0x1000) == 0x5			

	def test_address_indirect_read(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write16(0x2000, 0x3000)
		self.cpu.memory.write(0x3000, 0x5)
		assert self.cpu.indirect.read(0x1000) == 0x5

	def test_address_indirect_x_read(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write16(0x2010, 0x3000)
		self.cpu.memory.write(0x3000, 0x5)
		self.cpu.X = 0x10
		assert self.cpu.indirectX.read(0x1000) == 0x5
	
	def test_address_indirect_y_read(self):
		self.cpu.memory.write16(0x1000, 0x2000)
		self.cpu.memory.write16(0x2000, 0x3000)
		self.cpu.memory.write(0x3010, 0x5)
		self.cpu.Y = 0x10
		assert self.cpu.indirectY.read(0x1000) == 0x5

	def test_address_implied_read(self):
		assert self.cpu.implied.read(0x1000) == None

	def test_address_accumulator_read(self):
		self.cpu.A = 5
		assert self.cpu.accumulator.read(0x1000) == 5

	def test_address_immediate_read(self):
		self.cpu.memory.write(0x1000, 0x10)
		assert self.cpu.immediate.read(0x1000) == 0x10	

	def test_address_relative_read(self):
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

	def test_force_interrupt(self):
		pass

	def test_bit_test(self):
		pass

	def test_clc(self):
		initCycles = self.cpu.cycles
		self.cpu.C = 1
		self.cpu.PC = 0x1000
		self.cpu.execute(*self.cpu.instructions[0x18])
		assert self.cpu.C == 0
		assert self.cpu.cycles == initCycles + 2
		assert self.cpu.PC == 0x1001

	def test_cld(self):
		initCycles = self.cpu.cycles
		self.cpu.D = 1
		self.cpu.PC = 0x1000
		self.cpu.execute(*self.cpu.instructions[0xd8])
		assert self.cpu.D == 0
		assert self.cpu.cycles == initCycles + 2
		assert self.cpu.PC == 0x1001

	def test_cli(self):
		initCycles = self.cpu.cycles
		self.cpu.I = 1
		self.cpu.PC = 0x1000
		self.cpu.execute(*self.cpu.instructions[0x58])
		assert self.cpu.I == 0
		assert self.cpu.cycles == initCycles + 2
		assert self.cpu.PC == 0x1001

	def test_clv(self):
		initCycles = self.cpu.cycles
		self.cpu.V = 1
		self.cpu.PC = 0x1000
		self.cpu.execute(*self.cpu.instructions[0xb8])
		assert self.cpu.V == 0
		assert self.cpu.cycles == initCycles + 2
		assert self.cpu.PC == 0x1001

	def test_cmp(self):
		#test zero result
		initCycles = self.cpu.cycles
		self.cpu.PC = 0x1000
		self.cpu.A = 0x10
		self.cpu.memory.write(0x1001, 0x10)		
		self.cpu.execute(*self.cpu.instructions[0xc9])
		assert self.cpu.Z
		assert self.cpu.C
		assert not self.cpu.N
		#test negative result
		self.cpu.PC = 0x1000
		self.cpu.A = 0x10
		self.cpu.memory.write(0x1001, 0x11)
		self.cpu.execute(*self.cpu.instructions[0xc9])
		assert not self.cpu.Z
		assert not self.cpu.C
		assert self.cpu.N

	def test_cpx(self):
		#test zero result
		initCycles = self.cpu.cycles
		self.cpu.PC = 0x1000
		self.cpu.X = 0x10
		self.cpu.memory.write(0x1001, 0x10)		
		self.cpu.execute(*self.cpu.instructions[0xe0])
		assert self.cpu.Z
		assert self.cpu.C
		assert not self.cpu.N
		#test negative result
		self.cpu.PC = 0x1000
		self.cpu.X = 0x10
		self.cpu.memory.write(0x1001, 0x11)
		self.cpu.execute(*self.cpu.instructions[0xe0])
		assert not self.cpu.Z
		assert not self.cpu.C
		assert self.cpu.N

	def test_cpy(self):
		#test zero result
		initCycles = self.cpu.cycles
		self.cpu.PC = 0x1000
		self.cpu.Y = 0x10
		self.cpu.memory.write(0x1001, 0x10)		
		self.cpu.execute(*self.cpu.instructions[0xc0])
		assert self.cpu.Z
		assert self.cpu.C
		assert not self.cpu.N
		#test negative result
		self.cpu.PC = 0x1000
		self.cpu.Y = 0x10
		self.cpu.memory.write(0x1001, 0x11)
		self.cpu.execute(*self.cpu.instructions[0xc0])
		assert not self.cpu.Z
		assert not self.cpu.C
		assert self.cpu.N

	def test_dec(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write16(0x1001, 0x2000)
		self.cpu.memory.write(0x2000, 0x5)
		self.cpu.execute(*self.cpu.instructions[0xce])
		assert self.cpu.memory.read(0x2000) == 0x4
		assert not self.cpu.Z
		assert not self.cpu.N

	def test_dex(self):
		self.cpu.X = 0x5
		self.cpu.execute(*self.cpu.instructions[0xca])
		assert self.cpu.X == 0x4
		assert not self.cpu.Z
		assert not self.cpu.N
	
	def test_dey(self):
		self.cpu.Y = 0x5
		self.cpu.execute(*self.cpu.instructions[0x88])
		assert self.cpu.Y == 0x4
		assert not self.cpu.Z
		assert not self.cpu.N

	def test_eor(self):
		self.cpu.A = 0b01010101
		self.cpu.memory.write(0x2000, 0b10101010)
		self.cpu.memory.write16(0x1001, 0x2000)
		self.cpu.PC = 0x1000
		self.cpu.execute(*self.cpu.instructions[0x4d])
		assert self.cpu.A == 0b11111111	

	def test_inc(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write16(0x1001, 0x2000)
		self.cpu.memory.write(0x2000, 0x5)
		self.cpu.execute(*self.cpu.instructions[0xee])
		assert self.cpu.memory.read(0x2000) == 0x6
		assert not self.cpu.Z
		assert not self.cpu.N
	
	def test_inx(self):
		self.cpu.X = 0x5
		self.cpu.execute(*self.cpu.instructions[0xe8])
		assert self.cpu.X == 0x6
		assert not self.cpu.Z
		assert not self.cpu.N
	
	def test_iny(self):
		self.cpu.Y = 0x5
		self.cpu.execute(*self.cpu.instructions[0xc8])
		assert self.cpu.Y == 0x6
		assert not self.cpu.Z
		assert not self.cpu.N

	def test_jmp(self):
		print('TODO: test_jmp')

	def test_jsr(self):
		print('TODO: test_jsr')

	def test_lda(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.execute(*self.cpu.instructions[0xa9])
		assert self.cpu.A == 0x10
		assert not self.cpu.N
		assert not self.cpu.Z

	def test_ldx(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.execute(*self.cpu.instructions[0xa2])
		assert self.cpu.X == 0x10
		assert not self.cpu.N
		assert not self.cpu.Z

	def test_ldy(self):
		self.cpu.PC = 0x1000
		self.cpu.memory.write(0x1001, 0x10)
		self.cpu.execute(*self.cpu.instructions[0xa0])
		assert self.cpu.Y == 0x10
		assert not self.cpu.N
		assert not self.cpu.Z

	def test_lsr(self):
		self.cpu.A = 0b00001111
		self.cpu.execute(*self.cpu.instructions[0x4a])
		assert self.cpu.A == 0b00000111
		assert not self.cpu.Z
		assert not self.cpu.N
		assert self.cpu.C

if __name__ == '__main__':
	unittest.main()
