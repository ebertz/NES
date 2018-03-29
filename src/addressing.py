# 6502 addressing modes
# http://www.obelisk.me.uk/6502/addressing.html#ZPX
# http://nesdev.com/NESDoc.pdf

class AddressingMode:
	def __init__(self, size, cpu, crossPageCycles):
		self.cpu = cpu
		self.size = size
		self.crossPageCycles = crossPageCycles

	def read(self, address):
		return None

	def write(self, address, value):
		pass

	def get(self):
		return self.read(self.cpu.PC + 1)

	def set(self, value):
		return self.write(self.cpu.PC + 1, value)

class Implied(AddressingMode):
	def __init__(self, cpu):
		super().__init__(1, cpu, 0)

class Immediate(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 0)

	def read(self, address):
		return address

class Accumulator(AddressingMode):
	def __init__(self, cpu):
		super().__init__(1, cpu, 0)

	def read(self, address):
		return self.cpu.A

	def write(self, address, value):
		self.cpu.A = value & 0xFF

class ZeroPage(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 0)

	def read(self, address):
		return self.cpu.memory.read(address & 0xFF)

	def write(self, address, value):
		self.cpu.memory.write(address & 0xFF, value)

class ZeroPageX(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 0)

	def read(self, address):
		return self.cpu.memory.read((address + self.cpu.X) & 0xFF)

	def write(self, address, value):
		self.cpu.memory.write((address + self.cpu.X) & 0xFF, value)

class ZeroPageY(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 0)

	def read(self, address):
		return self.cpu.memory.read((address + self.cpu.Y) & 0xFF)

	def write(self, address, value):
		self.cpu.memory.write((address + self.cpu.Y) & 0xFF, value)

class Absolute(AddressingMode):
	def __init__(self, cpu):
		super().__init__(3, cpu, 0)

	def read(self, address):
		return self.cpu.memory.read(address)

	def write(self, address, value):
		self.cpu.memory.write(address, value)

class AbsoluteX(AddressingMode):
	def __init__(self, cpu):
		super().__init__(3, cpu, 1)

	def read(self, address):
		return self.cpu.memory.read(address + self.cpu.X)

	def write(self, address, value):
		self.cpu.memory.write(address + self.cpu.X, value)

class AbsoluteY(AddressingMode):
	def __init__(self, cpu):
		super().__init__(3, cpu, 1)

	def read(self, address):
		return self.cpu.memory.read(address + self.cpu.Y)

	def write(self, address, value):
		self.cpu.memory.write(address + self.cpu.Y, value)

class Indirect(AddressingMode):
	def __init__(self, cpu):
		super().__init__(3, cpu, 0)

	def read(self, address):
		indirect_address = self.cpu.memory.read16(address)
		return self.cpu.memory.read(indirect_address)


# X is added before indirection
class IndirectX(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 0)

	def read(self, address):
		indirect_address = self.cpu.memory.read16(address + self.cpu.X)
		return self.cpu.memory.read(indirect_address)

	def write(self, address, value):
		indirect_address = self.cpu.memory.read16(address + self.cpu.X)
		self.cpu.memory.write(indirect_address, value)

# Y is added after indirection
class IndirectY(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 1)

	def read(self, address):
		indirect_address = self.cpu.memory.read16(address )
		return self.cpu.memory.read(indirect_address + self.cpu.Y)

	def write(self, address, value):
		indirect_address = self.cpu.memory.read16(address )
		self.cpu.memory.write(indirect_address + self.cpu.Y, value)

class Relative(AddressingMode):
	def __init__(self, cpu):
		super().__init__(2, cpu, 2) #TODO: check branch behavior

	def read(self, address):
		return (self.cpu.PC + self.cpu.memory.read(address)) & 0xFFFF