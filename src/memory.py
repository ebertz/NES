class Memory:
	def __init__(self):
		self.memory = [0 for i in range(0xFFFF)]

	def write(self, address, value):
		self.memory[address] = value

	def read(self, address):
		return self.memory[address]

	def read16(self, address):
		return self.memory[address] + (self.memory[address + 1] << 8)

	def write16(self, address, value):
		self.memory[address] = value & 0xFF
		self.memory[address + 1] = (value >> 8) & 0xFF