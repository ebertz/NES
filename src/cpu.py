class CPU:

    def __init__(self):
        self.console = None
        self.memory = None
        self.clock = None
        self.instructions = {
            0x00: [self.brk, self.addressNone, 7],
            0x01: [self.ora, self.addressIndirectX, 6],
        }

        self.statusFlags = {
            'C': 0,  # carry
            'Z': 0,  # zero
            'I': 0,  # interrupt disable
            'D': 0,  # decimal mode
            'B': 0,  # break
            'v': 0,  # overflow
            'N': 0  # negative
        }

        self.registers = {
            'A': 0,  # accumulator
            'X': 0,  # index reg X
            'Y': 0,  # index reg X
            'P': 0,  # processor status
            'SP': 0,  # stack pointer
            'PC': 0  # program counter
        }
    def execute(self, instruction, addressingMode, cycles):
        # fetch operands based on addressing mode
        # execute instruction
        # burn clock cycles
        pass

    def step(self):
        # fetch instruction from address in PC
        # look up opcode in instruciton table
        # execute() instruction
        # increment PC
        pass

    ###
    # ADDRESSING MODES
    ###

    def addressImmediate(self):
        pass

    def addressZeroPage(self):
        pass

    def addressZeroPageX(self):
        pass

    def addressAbsolute(self):
        pass

    def addressAbsoluteX(self):
        pass

    def addressAbsoluteY(self):
        pass

    def addressIndirectX(self):
        pass

    def addressIndirectY(self):
        pass

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
        pass

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
