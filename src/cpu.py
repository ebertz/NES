# CPU architecture references :
# http://www.obelisk.me.uk/6502/reference.html
# http://www.6502.org/tutorials/6502opcodes.html
import memory

class CPU:

    def __init__(self):
        self.console = None
        self.memory = memory.Memory()
        self.clock = None

        #status flags
        self.C = 0
        self.Z = 0
        self.I = 0
        self.D = 0
        self.B = 0
        self.V = 0
        self.N = 0

        #registers
        self.A = 0
        self.X = 0
        self.Y = 0
        self.P = 0
        self.SP = 0
        self.PC = 0

        #instructions stored in form [{operation}, {addressing mode}, {size}, {clock cycles}]
        self.instructions = {
            0x00: [self.brk, self.address_none, 1, 7],
            0x01: [self.ora, self.address_indirect_x, 2, 6],
            0x05: [self.ora, self.address_zero_page, 2, 3],
            0x06: [self.asl, self.address_zero_page, 2, 3],
            0x08: [self.php, self.address_none, 1, 3],
            0x09: [self.ora, self.address_immediate, 2, 2],
            0x0a: [self.asl, self.address_accumulator, 1, 2],
            0x0d: [self.ora, self.address_absolute, 3, 4],
            0x0e: [self.asl, self.address_absolute, 3, 6],
            0x10: [self.bpl, self.address_relative, 2, 2],
            0x11: [self.ora, self.address_indirect_y, 2, 5],
            0x15: [self.ora, self.address_zero_page_x, 2, 4],
            0x16: [self.asl, self.address_zero_page_x, 2, 6],
            0x18: [self.clc, self.address_none, 1, 2],
            0x19: [self.ora, self.address_absolute_y, 3, 4],
            0x1d: [self.ora, self.address_absolute_x, 3, 4],
            0x1e: [self.asl, self.address_absolute_x, 3, 7],

            0x20: [self.jsr, self.address_jump_absolute, 3, 6],
            0x21: [self._and, self.address_indirect_x, 2, 6],
            0x24: [self.bit, self.address_zero_page, 2, 3],
            0x25: [self._and, self.address_zero_page, 2, 3],
            0x26: [self.rol, self.address_zero_page, 2, 5],
            0x28: [self.plp, self.address_none, 1, 4],
            0x29: [self._and, self.address_immediate, 2, 2],
            0x2a: [self.rol, self.address_accumulator, 1, 2],
            0x2c: [self.bit, self.address_absolute, 3, 4],
            0x2d: [self._and, self.address_absolute, 3, 4],
            0x2e: [self.rol, self.address_absolute, 3, 6],
            0x30: [self.bmi, self.address_relative, 2, 2],
            0x31: [self._and, self.address_indirect_y, 2, 5],
            0x35: [self._and, self.address_zero_page_x, 2, 6],
            0x36: [self.rol, self.address_zero_page_x, 2, 6],
            0x38: [self.sec, self.address_none, 1, 2],
            0x39: [self._and, self.address_absolute_y, 3, 4],
            0x3d: [self._and, self.address_absolute_x, 3, 4],
            0x3e: [self.rol, self.address_absolute_x, 3, 7],

            0x40: [self.rti, self.address_none, 1, 6],
            0x41: [self.eor, self.address_indirect_x, 2, 6],
            0x45: [self.eor, self.address_zero_page, 2, 2],
            0x46: [self.lsr, self.address_zero_page, 2, 5],
            0x48: [self.pha, self.address_none, 1, 3],
            0x49: [self.eor, self.address_immediate, 2, 2],
            0x4a: [self.lsr, self.address_accumulator, 1, 2],
            0x4c: [self.jmp, self.address_jump_absolute, 3, 3], #check pc_inc
            0x4d: [self.eor, self.address_absolute, 3, 4],
            0x4e: [self.lsr, self.address_absolute, 3, 6],
            0x50: [self.bvc, self.address_relative, 2, 2],
            0x51: [self.eor, self.address_indirect_y, 2, 5],
            0x55: [self.eor, self.address_zero_page_x, 2, 4],
            0x56: [self.lsr, self.address_zero_page_x, 2, 6],
            0x58: [self.cli, self.address_none, 1, 2],
            0x59: [self.eor, self.address_absolute_y, 3, 4],
            0x5d: [self.eor, self.address_absolute_x, 3, 4],
            0x5e: [self.lsr, self.address_absolute_x, 3, 7],

            0x60: [self.rts, self.address_none, 1, 6],
            0x61: [self.adc, self.address_indirect_x, 2, 6],
            0x65: [self.adc, self.address_zero_page, 2, 3],
            0x66: [self.ror, self.address_zero_page, 2, 5],
            0x68: [self.pla, self.address_none, 1, 4],
            0x69: [self.adc, self.address_immediate, 2, 2],
            0x6a: [self.ror, self.address_accumulator, 1, 2],
            0x6c: [self.jmp, self.address_indirect, 3, 5],
            0x6d: [self.adc, self.address_absolute, 3, 4],
            0x6e: [self.ror, self.address_absolute, 3, 6],
            0x70: [self.bvs, self.address_relative, 2, 2],
            0x71: [self.adc, self.address_indirect_y, 2, 5],
            0x75: [self.adc, self.address_zero_page_x, 2, 4],
            0x76: [self.ror, self.address_zero_page_x, 2, 6],
            0x78: [self.sei, self.address_none, 1, 2],
            0x79: [self.adc, self.address_absolute_y, 3, 4],
            0x7d: [self.adc, self.address_absolute_x, 3, 4],
            0x7e: [self.ror, self.address_absolute_x, 3, 7],

            0x81: [self.sta, self.address_indirect_x, 2, 6],
            0x84: [self.sty, self.address_zero_page, 2, 3],
            0x85: [self.sta, self.address_zero_page, 2, 3],
            0x86: [self. stx, self.address_zero_page, 2, 3],
            0x88: [self.dey, self.address_none, 1, 2],
            0x8a: [self.txa, self.address_none, 1, 2],
            0x8c: [self.sty, self.address_absolute, 3, 4],
            0x8d: [self.sta, self.address_absolute, 3, 4],
            0x8e: [self.stx, self.address_absolute, 3, 4],
            0x90: [self.bcc, self.address_relative, 2, 2],
            0x91: [self.sta, self.address_indirect_y, 2, 6],
            0x94: [self.sty, self.address_zero_page_x, 2, 4],
            0x95: [self.sta, self.address_zero_page_x, 2, 4],
            0x96: [self.stx, self.address_zero_page_y, 2, 4],
            0x98: [self.tya, self.address_none, 1, 2],
            0x99: [self.sta, self.address_absolute_y, 3, 5],
            0x9a: [self.txs, self.address_none, 1, 2],
            0x9d: [self.sta, self.address_absolute_x, 3, 5],

            0xa0: [self.ldy, self.address_immediate, 2, 2],
            0xa1: [self.lda, self.address_indirect_x, 2, 6],
            0xa2: [self.ldx, self.address_immediate, 2, 2],
            0xa4: [self.ldy, self.address_zero_page, 2, 3],
            0xa5: [self.lda, self.address_zero_page, 2, 3],
            0xa6: [self.ldx, self.address_zero_page, 2, 3],
            0xa8: [self.tay, self.address_none, 1, 2],
            0xa9: [self.lda, self.address_immediate, 2, 2],
            0xaa: [self.tax, self.address_none, 1, 2],
            0xac: [self.ldy, self.address_absolute, 3, 4],
            0xad: [self.lda, self.address_absolute, 3, 4],
            0xae: [self.ldx, self.address_absolute, 3, 4],
            0xb0: [self.bcs, self.address_relative, 2, 2],
            0xb1: [self.lda, self.address_indirect_y, 2, 5],
            0xb4: [self.ldy, self.address_zero_page_x, 2, 4],
            0xb5: [self.lda, self.address_zero_page_x, 2, 4],
            0xb6: [self.ldx, self.address_zero_page_y, 2, 4],
            0xb8: [self.clv, self.address_none, 1, 2],
            0xb9: [self.lda, self.address_absolute_y, 3, 4],
            0xba: [self.tsx, self.address_none, 1, 2],
            0xbc: [self.ldy, self.address_absolute_x, 3, 4],
            0xbd: [self.lda, self.address_absolute_x, 3, 4],
            0xbe: [self.ldx, self.address_absolute_y, 3, 4],

            0xc0: [self.cpy, self.address_immediate, 2, 2],
            0xc1: [self.cmp, self.address_indirect_x, 2, 6],
            0xc4: [self.cpy, self.address_zero_page, 2, 3],
            0xc5: [self.cmp, self.address_zero_page, 2, 3],
            0xc6: [self.dec, self.address_zero_page, 2, 5],
            0xc8: [self.iny, self.address_none, 1, 2],
            0xc9: [self.cmp, self.address_immediate, 2, 2],
            0xca: [self.dex, self.address_none, 1, 2],
            0xcc: [self.cpy, self.address_absolute, 3, 4],
            0xcd: [self.cmp, self.address_absolute, 3, 4],
            0xce: [self.dec, self.address_absolute, 3, 6],
            0xd0: [self.bne, self.address_relative, 2, 2],
            0xd1: [self.cmp, self.address_indirect_y, 2, 5],
            0xd5: [self.cmp, self.address_zero_page_x, 2, 4],
            0xd6: [self.dec, self.address_zero_page_x, 2, 6],
            0xd8: [self.cld, self.address_none, 1, 2],
            0xd9: [self.cmp, self.address_absolute_y, 3, 4],
            0xdd: [self.cmp, self.address_absolute_x, 3, 4],
            0xde: [self.dec, self.address_absolute_x, 3, 7],

            0xe0: [self.cpx, self.address_immediate, 2, 2],
            0xe1: [self.sbc, self.address_indirect_x, 2, 6],
            0xe4: [self.cpx, self.address_zero_page, 2, 3],
            0xe5: [self.sbc, self.address_zero_page, 2, 3],
            0xe6: [self.inc, self.address_zero_page, 2, 5],
            0xe8: [self.inx, self.address_none, 1, 2],
            0xe9: [self.sbc, self.address_immediate, 2, 2],
            0xea: [self.nop, self.address_none, 1, 2],
            0xec: [self.cpx, self.address_absolute, 3, 4],
            0xed: [self.sbc, self.address_absolute, 3, 4],
            0xee: [self.inc, self.address_absolute, 3, 6],
            0xf0: [self.beq, self.address_relative, 2, 2],
            0xf1: [self.sbc, self.address_indirect_y, 2, 5],
            0xf5: [self.sbc, self.address_zero_page_x, 2, 4],
            0xf6: [self.inc, self.address_zero_page_x, 2, 6],
            0xf8: [self.sed, self.address_none, 1, 2],
            0xf9: [self.sbc, self.address_absolute_y, 3, 4],
            0xfd: [self.sbc, self.address_absolute_x, 3, 4],
            0xfe: [self.inc, self.address_absolute_x, 3, 7],
        }

    def getRegister(name):
        return self.registers[name]

    def execute(self, instruction, addressingMode, size, cycles):
        address = None
        if size == 2:
            address = self.memory.read(self.PC + 1)
        if size == 3 :
            address = self.memory.read(self.PC + 1) + (self.memory.read(self.PC + 2) << 8)

        data = addressingMode(addr)
        instruction(data)

        print('burned ' + str(cycles) + ' cycles\n')
        self.registers['PC'] += size

    def step(self):
        # fetch instruction from address in PC
        # look up opcode in instruciton table
        # execute() instruction
        # increment PC
        pass

    ###
    # ADDRESSING MODES http://nesdev.com/NESDoc.pdf Appendix E (p39)
    ###

    def address_none(self, addr):
        return None

    def address_accumulator(self, addr):
        return self.A

    def address_relative(self, addr):
        return addr

    def address_immediate(self, addr):
        return addr

    def address_zero_page(self, addr):
        return self.memory.read(addr);

    def address_zero_page_x(self, addr):
        return self.memory.read(addr + self.X)

    def address_zero_page_y(self, addr):
        return self.memory.read(addr + self.Y)

    def address_absolute(self, addr):
        return self.memory.read(addr)

    def address_absolute_x(self, addr):
        return self.memory.read(addr + self.X)

    def address_absolute_y(self, addr):
        return self.memory.read(addr + self.Y)

    def address_jump_absolute(self, addr):
        pass #TODO: this

    def address_indirect(self, addr):
        return self.memory.read(self.memory.read(addr) + (self.memory.read(addr + 1) << 8))

    def address_indirect_x(self, addr):
        a = self.memory.read(addr + self.X) + (self.memory.read(addr + self.X + 1) << 8)
        return self.memory.read(a)

    def address_indirect_y(self, addr):
        a = self.memory.read(addr + self.X) + (self.memory.read(addr + self.X + 1) << 8)
        return self.memory.read(a)

    ###
    # OPERATIONS http://www.obelisk.me.uk/6502/reference.html
    ###

    # add with carry
    def adc(self):
        pass

    # logical and
    def _and(self):
        pass

    # arithmetic left shift
    def asl(self):
        pass

    # branch if carry clear
    def bcc(self):
        pass

    # branch if carry set
    def bcs(self):
        pass

    # branch if equal
    def beq(self):
        pass

    # bit test
    def bit(self):
        pass

    # branch if minus
    def bmi(self):
        pass

    # branch not equal
    def bne(self):
        pass

    # branch if positive
    def bpl(self):
        pass

    # force interrupt
    def brk(self):
        self.registers['A'] = 5

    # branch if overflow clear
    def bvc(self):
        pass

    # branch if overflow set
    def bvs(self):
        pass

    # clear carry flag
    def clc(self):
        pass

    # clear decimal mode
    def cld(self):
        pass

    # clear interrupt disable
    def cli(self):
        pass

    # clear overflow flag
    def clv(self):
        pass

    # compare
    def cmp(self):
        pass

    # compare X register
    def cpx(self):
        pass

    # compare Y register
    def cpy(self):
        pass

    # decrement memory
    def dec(self):
        pass

    # decrement X register
    def dex(self):
        pass

    # decrement Y register
    def dey(self):
        pass

    # exclusive or
    def eor(self):
        pass

    # increment memory
    def inc(self):
        pass

    # increment x register
    def inx(self):
        pass

    # increment y register
    def iny(self):
        pass

    # jump
    def jmp(self):
        pass

    # jump subroutine
    def jsr(self):
        pass

    # load accumulator
    def lda(self):
        pass

    # load X register
    def ldx(self):
        pass

    # load Y register
    def ldy(self):
        pass

    # logical right shift
    def lsr(self):
        pass

    # no operation
    def nop(self):
        pass

    # logical inclusive or
    def ora(self):
        pass

    # push accumulator
    def pha(self):
        pass

    # push processor status
    def php(self):
        pass

    # pull accumulator
    def pla(self):
        pass

    # pull processor status
    def plp(self):
        pass

    # rotate left
    def rol(self):
        pass

    # rotate right
    def ror(self):
        pass

    # return from interrupt
    def rti(self):
        pass

    # return from subroutine
    def rts(self):
        pass

    # subtract with carry
    def sbc(self):
        pass

    # set carry flag
    def sec(self):
        pass

    # set decimal flag
    def sed(self):
        pass

    # set interrupt disable flag
    def sei(self):
        pass
    # store accumulator
    def sta(self):
        pass

    # store X register
    def stx(self):
        pass

    # store Y register
    def  sty(self):
        pass

    # transfer A to X
    def tax(self):
        pass

    # transfer A to Y
    def tay(self):
        pass

    # transfer SP to X
    def tsx(self):
        pass

    # transfer X to A
    def txa(self):
        pass

    # transfer X to SP
    def txs(self):
        pass

    # transfer Y to A
    def tya(self):
        pass

