# CPU architecture references :
# http://www.obelisk.me.uk/6502/reference.html
# http://www.6502.org/tutorials/6502opcodes.html
import memory
import addressing

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

        self.implied = addressing.Implied(self)
        self.accumulator = addressing.Accumulator(self)
        self.immediate = addressing.Immediate(self)
        self.zeroPage = addressing.ZeroPage(self)
        self.zeroPageX = addressing.ZeroPageX(self)
        self.zeroPageY = addressing.ZeroPageY(self)
        self.relative = addressing.Relative(self)
        self.absolute = addressing.Absolute(self)
        self.absoluteX = addressing.AbsoluteX(self)
        self.absoluteY = addressing.AbsoluteY(self)
        self.indirect = addressing.Indirect(self)
        self.indirectX = addressing.IndirectX(self)
        self.indirectY = addressing.IndirectY(self)
        #instructions stored in form [{operation}, {addressing mode}, {size}, {clock cycles}]
        self.instructions = {
            0x00: [self.brk, self.implied, 7],
            0x01: [self.ora, self.indirectX, 6],
            0x05: [self.ora, self.zeroPage, 3],
            0x06: [self.asl, self.zeroPage, 3],
            0x08: [self.php, self.implied, 3],
            0x09: [self.ora, self.immediate, 2],
            0x0a: [self.asl, self.accumulator, 2],
            0x0d: [self.ora, self.absolute, 4],
            0x0e: [self.asl, self.absolute, 6],
            0x10: [self.bpl, self.relative, 2],
            0x11: [self.ora, self.indirectY, 5],
            0x15: [self.ora, self.zeroPageX, 4],
            0x16: [self.asl, self.zeroPageX, 6],
            0x18: [self.clc, self.implied, 2],
            0x19: [self.ora, self.absoluteY, 4],
            0x1d: [self.ora, self.absoluteX, 4],
            0x1e: [self.asl, self.absoluteX, 7],

            0x20: [self.jsr, self.absolute, 6],
            0x21: [self._and, self.indirectX, 6],
            0x24: [self.bit, self.zeroPage, 3],
            0x25: [self._and, self.zeroPage, 3],
            0x26: [self.rol, self.zeroPage, 5],
            0x28: [self.plp, self.implied, 4],
            0x29: [self._and, self.immediate, 2],
            0x2a: [self.rol, self.accumulator, 2],
            0x2c: [self.bit, self.absolute, 4],
            0x2d: [self._and, self.absolute, 4],
            0x2e: [self.rol, self.absolute, 6],
            0x30: [self.bmi, self.relative, 2],
            0x31: [self._and, self.indirectY, 5],
            0x35: [self._and, self.zeroPageX, 6],
            0x36: [self.rol, self.zeroPageX, 6],
            0x38: [self.sec, self.implied, 2],
            0x39: [self._and, self.absoluteY, 4],
            0x3d: [self._and, self.absoluteX, 4],
            0x3e: [self.rol, self.absoluteX, 7],

            0x40: [self.rti, self.implied, 6],
            0x41: [self.eor, self.indirectX, 6],
            0x45: [self.eor, self.zeroPage, 2],
            0x46: [self.lsr, self.zeroPage, 5],
            0x48: [self.pha, self.implied, 3],
            0x49: [self.eor, self.immediate, 2],
            0x4a: [self.lsr, self.accumulator, 2],
            0x4c: [self.jmp, self.absolute, 3], #check pc_inc
            0x4d: [self.eor, self.absolute, 4],
            0x4e: [self.lsr, self.absolute, 6],
            0x50: [self.bvc, self.relative, 2],
            0x51: [self.eor, self.indirectY, 5],
            0x55: [self.eor, self.zeroPageX, 4],
            0x56: [self.lsr, self.zeroPageX, 6],
            0x58: [self.cli, self.implied, 2],
            0x59: [self.eor, self.absoluteY, 4],
            0x5d: [self.eor, self.absoluteX, 4],
            0x5e: [self.lsr, self.absoluteX, 7],

            0x60: [self.rts, self.implied, 6],
            0x61: [self.adc, self.indirectX, 6],
            0x65: [self.adc, self.zeroPage, 3],
            0x66: [self.ror, self.zeroPage, 5],
            0x68: [self.pla, self.implied, 4],
            0x69: [self.adc, self.immediate, 2],
            0x6a: [self.ror, self.accumulator, 2],
            0x6c: [self.jmp, self.indirect, 5],
            0x6d: [self.adc, self.absolute, 4],
            0x6e: [self.ror, self.absolute, 6],
            0x70: [self.bvs, self.relative, 2],
            0x71: [self.adc, self.indirectY, 5],
            0x75: [self.adc, self.zeroPageX, 4],
            0x76: [self.ror, self.zeroPageX, 6],
            0x78: [self.sei, self.implied, 2],
            0x79: [self.adc, self.absoluteY, 4],
            0x7d: [self.adc, self.absoluteX, 4],
            0x7e: [self.ror, self.absoluteX, 7],

            0x81: [self.sta, self.indirectX, 6],
            0x84: [self.sty, self.zeroPage, 3],
            0x85: [self.sta, self.zeroPage, 3],
            0x86: [self. stx, self.zeroPage, 3],
            0x88: [self.dey, self.implied, 2],
            0x8a: [self.txa, self.implied, 2],
            0x8c: [self.sty, self.absolute, 4],
            0x8d: [self.sta, self.absolute, 4],
            0x8e: [self.stx, self.absolute, 4],
            0x90: [self.bcc, self.relative, 2],
            0x91: [self.sta, self.indirectY, 6],
            0x94: [self.sty, self.zeroPageX, 4],
            0x95: [self.sta, self.zeroPageX, 4],
            0x96: [self.stx, self.zeroPageY, 4],
            0x98: [self.tya, self.implied, 2],
            0x99: [self.sta, self.absoluteY, 5],
            0x9a: [self.txs, self.implied, 2],
            0x9d: [self.sta, self.absoluteX, 5],

            0xa0: [self.ldy, self.immediate, 2],
            0xa1: [self.lda, self.indirectX, 6],
            0xa2: [self.ldx, self.immediate, 2],
            0xa4: [self.ldy, self.zeroPage, 3],
            0xa5: [self.lda, self.zeroPage, 3],
            0xa6: [self.ldx, self.zeroPage, 3],
            0xa8: [self.tay, self.implied, 2],
            0xa9: [self.lda, self.immediate, 2],
            0xaa: [self.tax, self.implied, 2],
            0xac: [self.ldy, self.absolute, 4],
            0xad: [self.lda, self.absolute, 4],
            0xae: [self.ldx, self.absolute, 4],
            0xb0: [self.bcs, self.relative, 2],
            0xb1: [self.lda, self.indirectY, 5],
            0xb4: [self.ldy, self.zeroPageX, 4],
            0xb5: [self.lda, self.zeroPageX, 4],
            0xb6: [self.ldx, self.zeroPageY, 4],
            0xb8: [self.clv, self.implied, 2],
            0xb9: [self.lda, self.absoluteY, 4],
            0xba: [self.tsx, self.implied, 2],
            0xbc: [self.ldy, self.absoluteX, 4],
            0xbd: [self.lda, self.absoluteX, 4],
            0xbe: [self.ldx, self.absoluteY, 4],

            0xc0: [self.cpy, self.immediate, 2],
            0xc1: [self.cmp, self.indirectX, 6],
            0xc4: [self.cpy, self.zeroPage, 3],
            0xc5: [self.cmp, self.zeroPage, 3],
            0xc6: [self.dec, self.zeroPage, 5],
            0xc8: [self.iny, self.implied, 2],
            0xc9: [self.cmp, self.immediate, 2],
            0xca: [self.dex, self.implied, 2],
            0xcc: [self.cpy, self.absolute, 4],
            0xcd: [self.cmp, self.absolute, 4],
            0xce: [self.dec, self.absolute, 6],
            0xd0: [self.bne, self.relative, 2],
            0xd1: [self.cmp, self.indirectY, 5],
            0xd5: [self.cmp, self.zeroPageX, 4],
            0xd6: [self.dec, self.zeroPageX, 6],
            0xd8: [self.cld, self.implied, 2],
            0xd9: [self.cmp, self.absoluteY, 4],
            0xdd: [self.cmp, self.absoluteX, 4],
            0xde: [self.dec, self.absoluteX, 7],

            0xe0: [self.cpx, self.immediate, 2],
            0xe1: [self.sbc, self.indirectX, 6],
            0xe4: [self.cpx, self.zeroPage, 3],
            0xe5: [self.sbc, self.zeroPage, 3],
            0xe6: [self.inc, self.zeroPage, 5],
            0xe8: [self.inx, self.implied, 2],
            0xe9: [self.sbc, self.immediate, 2],
            0xea: [self.nop, self.implied, 2],
            0xec: [self.cpx, self.absolute, 4],
            0xed: [self.sbc, self.absolute, 4],
            0xee: [self.inc, self.absolute, 6],
            0xf0: [self.beq, self.relative, 2],
            0xf1: [self.sbc, self.indirectY, 5],
            0xf5: [self.sbc, self.zeroPageX, 4],
            0xf6: [self.inc, self.zeroPageX, 6],
            0xf8: [self.sed, self.implied, 2],
            0xf9: [self.sbc, self.absoluteY, 4],
            0xfd: [self.sbc, self.absoluteX, 4],
            0xfe: [self.inc, self.absoluteX, 7],
        }

    def setCarry(self, value):
        self.C = 1 if value > 0xFF else 0

    def setZero(self,value):
        self.Z = 1 if value & 0xFF == 0 else 0

    def setNegative(self, value):
        self.N = 1 if ((value & 0xFF) >> 7 ) & 1 else 0

    def setInterruptDisable(self, condition):
        self.I = 1 if condition else 0

    def setDecimalMode(self, condition):
        self.D = 1 if condition else 0

    def setBreakCommand(self, condition):
        self.B = 1 if condition else 0

    def setOverflow(self, condition):
        self.V = 1 if condition else 0

    def execute(self, instruction, addressingMode, cycles):

        instruction(addressingMode)
        print('burned ' + str(cycles) + ' cycles\n')
        self.PC += addressingMode.size

    # OPERATIONS 
    # http://www.obelisk.me.uk/6502/reference.html
    # http://www.6502.org/tutorials/6502opcodes.html
    

    # add with carry [A,Z,C,N = A+M+C]
    def adc(self, mode):
        result = mode.get() + self.A + self.C
        self.A = result & 0xFF
        self.setOverflow(self.A != result)
        self.setCarry(result)
        self.setNegative(result)
        self.setZero(result)

    # logical and [A,Z,N = A&M]
    def _and(self, mode):
        result = mode.get() & self.A
        self.setZero(result)
        self.setNegative(result)
        self.A = result

    # arithmetic left shift [A,Z,C,N = M*2, M,Z,C,N = M*2]
    def asl(self, mode):
        result = mode.get() << 1;
        self.setCarry(result)
        self.setZero(result)
        self.setNegative(result)

    # branch if carry clear
    def bcc(self, mode):
        if self.C:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # branch if carry set
    def bcs(self):
        if not self.C:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # branch if equal
    def beq(self):
        if not self.Z:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # bit test
    def bit(self):
        pass

    # branch if minus
    def bmi(self):
        if not self.N:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # branch not equal
    def bne(self):
        if self.Z:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # branch if positive
    def bpl(self):
        if self.N:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # force interrupt
    def brk(self):
        self.A = 5

    # branch if overflow clear
    def bvc(self):
        if self.V:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

    # branch if overflow set
    def bvs(self):
         if not self.V:
            return
        relAddr = mode.get()
        extraCycles = mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr + extraCycles

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

