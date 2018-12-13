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
        self.cycles = 0

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
        self.SP = 0x01FF
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
        self.jumpAbsolute = addressing.JumpAbsolute(self)
        self.NONE = addressing.NONE(self)
        #instructions stored in form [{operation}, {addressing mode}, {size}, {clock cycles}]
        self.instructions = {
            0x00: [self.brk, self.NONE, 7],
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

            0x20: [self.jsr, self.jumpAbsolute, 6],
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
            0x4c: [self.jmp, self.jumpAbsolute, 3],
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

            0x60: [self.rts, self.NONE, 6],
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

    #stack is located at 0x0100-0x01FF, top-down, wraps to start of stack if overflow
    def pushStack(self, value):
        self.memory.write(self.SP, value)
        self.SP -= 1

    def popStack(self):
        self.SP += 1
        return self.memory.read(self.SP)

    # NV_BDIZC
    def getProcessorStatus(self):
        return (((self.N << 7) | (self.V << 6) | (self.B << 4) | (self.D << 3)
               | (self.I << 2) | (self.Z << 1) | self.C) & 0xFF)

    def setProcessorStatus(self, value):
        self.N = (value >> 7) & 1
        self.V = (value >> 6) & 1
        self.B = (value >> 4) & 1
        self.D = (value >> 3) & 1
        self.I = (value >> 2) & 1
        self.Z = (value >> 1) & 1
        self.C = value & 1

    def setZN(self, value):
        self.Z = 1 if value & 0xFF == 0 else 0
        self.N = 1 if ((value & 0xFF) >> 7 ) & 1 else 0

    def setSP(self, value):
        self.SP = 0x100 + (value & 0xFF)

    # execute an instruction        
    def execute(self, instruction, addressingMode, cycles):
        instruction(addressingMode)
        self.PC += addressingMode.size
        self.cycles += cycles

    # OPERATIONS 
    # http://www.obelisk.me.uk/6502/reference.html
    # http://www.6502.org/tutorials/6502opcodes.html
    
    # add with carry [A,Z,C,N = A+M+C]
    def adc(self, mode):
        result = mode.get() + self.A + self.C
        self.A = result & 0xFF
        self.V = self.A != result
        self.C = result > 0xFF
        self.setZN(result)

    # logical and [A,Z,N = A&M]
    def _and(self, mode):
        result = mode.get() & self.A
        self.setZN(result)
        self.A = result

    # arithmetic left shift [A,Z,C,N = M*2],[M,Z,C,N = M*2]
    def asl(self, mode):
        result = mode.get() << 1;
        self.C = result > 0xFF
        self.setZN(result)
        mode.set(result)

    # branch if carry clear
    def bcc(self, mode):
        if self.C:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # branch if carry set
    def bcs(self, mode):
        if not self.C:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # branch if equal
    def beq(self, mode):
        if not self.Z:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # bit test [A&M, N=M7, V=M6]
    def bit(self, mode):
        value = mode.get()
        result = value & self.A
        self.Z = int(result == 0)
        self.N = value >> 7 & 1
        self.V = value >> 6 & 1

    # branch if minus
    def bmi(self, mode):
        if not self.N:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # branch not equal
    def bne(self, mode):
        if self.Z:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # branch if positive
    def bpl(self, mode):
        if self.N:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # force interrupt
    def brk(self, mode):
        #push status flags and PC
        self.pushStack((self.PC >> 8) & 0xFF)
        self.pushStack(self.PC & 0xFF)
        self.pushStack(self.getProcessorStatus())
        irq = self.memory.read16(0xfffe)
        self.PC = irq
        self.B = 1;

    # branch if overflow clear
    def bvc(self, mode):
        if self.V:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # branch if overflow set
    def bvs(self, mode):
        if not self.V:
            return
        relAddr = mode.get()
        self.cycles += mode.crossPageCycles if (self.PC >> 8) != (relAddr >> 8) else 1
        self.PC = relAddr

    # clear carry flag
    def clc(self, mode):
        self.C = 0

    # clear decimal mode
    def cld(self, mode):
        self.D = 0

    # clear interrupt disable
    def cli(self, mode):
        self.I = 0

    # clear overflow flag
    def clv(self, mode):
        self.V = 0

    # compare [Z,C,N = A-M]
    def cmp(self, mode):
        operand = mode.get()
        self.C = self.A >= operand
        diff = (self.A - operand) & 0xFF
        self.setZN(diff)

    # compare X register [Z,C,N = X-M]
    def cpx(self, mode):
        operand = mode.get()
        self.C = self.X >= operand
        diff = (self.X - operand) & 0xFF
        self.setZN(diff)

    # compare Y register [Z,C,N = Y-M]
    def cpy(self, mode):
        operand = mode.get()
        self.C = self.Y >= operand
        diff = (self.Y - operand) & 0xFF
        self.setZN(diff)

    # decrement memory [M,Z,N = M-1]
    def dec(self, mode):
        result = (mode.get() -1) & 0xFF
        self.setZN(result)
        mode.set(result)

    # decrement X register [X,Z,N = X-1]
    def dex(self, mode):
        self.X -= 1
        self.setZN(self.X)

    # decrement Y register [Y,Z,N = Y-1]
    def dey(self, mode):
        self.Y -= 1
        self.setZN(self.Y)

    # exclusive or [A,Z,N = A^M]
    def eor(self, mode):
        self.A = self.A ^ mode.get()
        self.setZN(self.A)

    # increment memory [M,Z,N = M+1]
    def inc(self, mode):
        result = (mode.get() + 1) & 0xFF
        self.setZN(result)
        mode.set(result)

    # increment x register [X,Z,N = X+1]
    def inx(self, mode):
        self.X = (self.X + 1) & 0xFF
        self.setZN(self.X)

    # increment y register [Y,Z,N = Y+1]
    def iny(self, mode):
        self.Y = (self.Y + 1) & 0xFF
        self.setZN(self.Y)

    # jump
    def jmp(self, mode):
        self.PC = mode.get()

    # jump subroutine
    def jsr(self, mode):
        pc = self.PC + 3
        self.pushStack((pc >> 8) & 0xFF)
        self.pushStack(pc & 0xFF)
        self.PC = mode.get()

    # load accumulator [A,Z,N = M]
    def lda(self, mode):
        self.A = mode.get()
        self.setZN(self.A)

    # load X register [X,Z,N = M]
    def ldx(self, mode):
        self.X = mode.get()
        self.setZN(self.X)

    # load Y register
    def ldy(self, mode):
        self.Y = mode.get()
        self.setZN(self.Y)

    # logical right shift
    def lsr(self, mode):
        operand = mode.get()
        result = (operand >> 1) & 0b0111111
        self.C = operand & 1
        self.setZN(result)
        mode.set(result)

    # no operation
    def nop(self, mode):
        pass

    # logical inclusive or [A,Z,N = A|M]
    def ora(self, mode):
        result = self.A | mode.get()
        self.setZN(result)
        self.A = result & 0xFF

    # push accumulator
    def pha(self, mode):
        self.pushStack(self.A)

    # push processor status
    def php(self, mode):
        self.pushStack(self.getProcessorStatus())

    # pull accumulator
    def pla(self, mode):
        self.A = self.popStack()
        self.setZN(self.A)

    # pull processor status
    def plp(self, mode):
        self.setProcessorStatus(self.popStack())

    # rotate left
    def rol(self, mode):
        operand = mode.get()
        result = ((operand << 1) | self.C) & 0xFF
        self.C = (operand >> 7) & 1
        mode.set(result)

    # rotate right
    def ror(self, mode):
        operand = mode.get()
        result = ((operand >> 1) | (self.C << 7)) & 0xFF
        self.C = (operand >> 7) & 1
        mode.set(result)

    # return from interrupt - pull flags then PC from stack
    def rti(self, mode):
        self.setProcessorStatus(self.popStack())
        self.PC = self.popStack() + (self.popStack() << 8)

    # return from subroutine - pulls PC (minus one) from stack
    def rts(self, mode):
        self.PC = self.popStack() + (self.popStack() << 8)

    # subtract with carry [A,Z,C,N = A-M-(1-C)]
    def sbc(self, mode):
        value = mode.get()
        result = self.A - mode.get() - (1-self.C)
        self.C = result > 0xFF
        self.V = int(((self.A ^ value) & 0x80 != 0) and ((self.A ^ result) & 0x80 != 0))
        self.A = result & 0xFF
        self.setZN(result)

    # set carry flag
    def sec(self, mode):
        self.C = 1

    # set decimal flag
    def sed(self, mode):
        self.D = 1

    # set interrupt disable flag
    def sei(self, mode):
        self.I = 1
    # store accumulator
    def sta(self, mode):
        mode.set(self.A)

    # store X register
    def stx(self, mode):
        mode.set(self.X)

    # store Y register
    def  sty(self, mode):
        mode.set(self.Y)

    # transfer A to X
    def tax(self, mode):
        self.X = self.A
        self.setZN(self.X)

    # transfer A to Y
    def tay(self, mode):
        self.Y = self.A
        self.setZN(self.Y)

    # transfer SP to X
    def tsx(self, mode):
        self.X = self.SP
        self.setZN(self.X)

    # transfer X to A
    def txa(self, mode):
        self.A = self.X
        self.setZN(self.A)

    # transfer X to SP
    def txs(self, mode):
        self.setSP(self.X)

    # transfer Y to A
    def tya(self, mode):
        self.A = self.Y
        self.setZN(self.A)
