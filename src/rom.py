# https://wiki.nesdev.com/w/index.php/INES
filepath = 'tests/testROMs/nestest.nes'

class ROM:
	def __init__(self):
		file = open(filepath, 'rb')
		header = bytearray(file.read(16))

		if header[0:3].decode('utf-8') != 'NES':
			print('Invalid ROM')
		self.prg_rom_size = header[4]
		self.chr_rom_size = header[5]
		self.prg_rom = file.read(0x4000 * self.prg_rom_size)
		self.chr_rom = file.read(0x2000 * self.chr_rom_size)

		self.data = header [16:]
		#TODO: handle flags from data[6:10]
		file.close()

#print("{:02x}".format(self.data[i]))
