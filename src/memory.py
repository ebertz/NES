class Memory:
	def __init__(self, size):
		self.memory = [0 for i in range(size)]

	def write(self, address, value):
		self.memory[address] = value

	def read(self, address):
		return self.memory[address]

	def read16(self, address):
		if address == 0xFF:
			return self.memory[address] + (self.memory[0] << 8)
		return self.memory[address] + (self.memory[address + 1] << 8)

	def write16(self, address, value):
		if address == 0xFF: 
			self.memory[address] + value & 0xFF
			self.memory[0x00] = (value >> 8) & 0xFF
		self.memory[address] = value & 0xFF
		self.memory[address + 1] = (value >> 8) & 0xFF

	def loadROM(self, rom):
		self.memory[0xC000:(0xC000 + 0x4000 * rom.prg_rom_size)] = rom.prg_rom
		