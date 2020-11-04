import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip


class Computer:
    def __init__(self, regs=[0, 0, 0, 0, 0, 0]):
        self.operations = {
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "setr": self.setr,
            "seti": self.seti,
            "borr": self.borr,
            "bori": self.bori,
            "bani": self.bani,
            "banr": self.banr,
            "mulr": self.mulr,
            "muli": self.muli,
            "addr": self.addr,
            "addi": self.addi,

        }
        self.opcode_table = {}
        self.regs = regs
        self.instruction_ptr = None

    def set_regs(self, values=[0, 0, 0, 0, 0, 0]):
        """ default - reset regs """
        self.regs = values

    def __str__(self):
        return str("REGS: " + str(self.regs))

    def __repr__(self):
        return str(self)

    def eqir(self, op):
        self.regs[op[2]] = int(op[0] == self.regs[op[1]])
    def eqri(self, op):
        self.regs[op[2]] = int(self.regs[op[0]] == op[1])
    def eqrr(self, op):
        self.regs[op[2]] = int(self.regs[op[0]] == self.regs[op[1]])
    def gtir(self, op):
        self.regs[op[2]] = int(op[0] > self.regs[op[1]])
    def gtri(self, op):
        self.regs[op[2]] = int(self.regs[op[0]] > op[1])
    def gtrr(self, op):
        self.regs[op[2]] = int(self.regs[op[0]] > self.regs[op[1]])
    def setr(self, op):
        self.regs[op[2]] = self.regs[op[0]]
    def seti(self, op):
        self.regs[op[2]] = op[0]
    def addr(self, op):
        self.regs[op[2]] = self.regs[op[1]] + self.regs[op[0]]
    def addi(self, op):
        self.regs[op[2]] = op[1] + self.regs[op[0]]
    def mulr(self, op):
        self.regs[op[2]] = self.regs[op[1]] * self.regs[op[0]]
    def muli(self, op):
        self.regs[op[2]] = op[1] * self.regs[op[0]]
    def banr(self, op):
        self.regs[op[2]] = self.regs[op[1]] & self.regs[op[0]]
    def bani(self, op):
        self.regs[op[2]] = op[1] & self.regs[op[0]]
    def borr(self, op):
        self.regs[op[2]] = self.regs[op[1]] | self.regs[op[0]]
    def bori(self, op):
        self.regs[op[2]] = op[1] | self.regs[op[0]]



def format_input(inp):
    ptr_reg = int(inp.pop(0).split(" ")[1])
    for i, instruction in enumerate(inp):
        name, r1, r2, r3 = instruction.split(" ")
        inp[i] = [name, int(r1), int(r2), int(r3)]
    return ptr_reg, inp


def execute_program(pc, instructions):
    """ executes the instructions on the Computer pc """
    while True:
        try:
            instruction = instructions[pc.regs[pc.instruction_ptr]]
        except IndexError:
            print("Instruction pointer out of bounds: Stopping.")
            pc.regs[pc.instruction_ptr] -= 1
            break
        r1, r2, r3 = instruction[1], instruction[2], instruction[3]
        print("Doing instruction: " + str(instruction))
        print(pc.regs)
        pc.operations[instruction[0]]([r1, r2, r3])
        if pc.regs[pc.instruction_ptr] == 29:
            print(instructions[pc.regs[pc.instruction_ptr]])
            exit()
        pc.regs[pc.instruction_ptr] += 1
    print("Last state computer regs part one: " + str(pc.regs))
    return pc.regs

def part_two():
    """ reverse engineer of what the instructions
    actually do:
    adds all the values (to register 0) from 0 to 10551275
    that 10551275 are divisible by
    """
    r_0 = 0
    for i in range(1, 10551276):
        if (10551275/i).is_integer():
            r_0 = r_0 + i
    print("register 0 final value part two: " + str(r_0))
    return r_0


if __name__ == "__main__":
    INPUT = read_and_strip(file_name="input.txt")
    ptr_reg, INPUT = format_input(INPUT)
    print(ptr_reg, INPUT)
    computer = Computer([16311888, 0, 0, 0, 0, 0])
    computer.instruction_ptr = ptr_reg
    final_state_regs_p1 = execute_program(computer, INPUT)
# r[5] = r[1] +1  if r[5] * 256 > r[2] something happens
# 11714978
# 8617725
# 5322775
# 9935705
# 736874
