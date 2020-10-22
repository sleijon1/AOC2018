def test_operations():
    test_comp = Computer()
    test_comp.set_regs([3,2,1,1])
    test_comp.operations["mulr"]([2,1,2])
    assert(test_comp.regs == [3,2,2,1])
    test_comp.set_regs([3,2,1,1])
    test_comp.addi([2,1,2])
    assert(test_comp.regs == [3,2,2,1])
    test_comp.set_regs([15,15,15,1])
    test_comp.banr((1,2,3))
    assert(test_comp.regs == [15,15,15,15])
    test_comp.set_regs([14,1,15,1])
    test_comp.bani((0, 1, 3))
    assert(test_comp.regs == [14,1,15,0])
    test_comp.set_regs([14,1,15,1])
    test_comp.bori((0, 1, 3))
    assert(test_comp.regs == [14,1,15,15])
    test_comp.set_regs([1,2,15,1])
    test_comp.borr((0,1,3))
    assert(test_comp.regs == [1,2,15,3])
    test_comp.set_regs([3,2,1,1])
    test_comp.seti([2,1,2])
    assert(test_comp.regs == [3,2,2,1])
    test_comp.set_regs([3,1,1,1])
    test_comp.gtir([2,1,0])
    assert(test_comp.regs == [1,1,1,1])
    test_comp.set_regs([3,1,3,1])
    test_comp.gtri([2,2,0])
    assert(test_comp.regs == [1,1,3,1])
    test_comp.set_regs([0,1,1,1])
    test_comp.eqri([2,1,0])
    assert(test_comp.regs == [1,1,1,1])
    print("passed all tests.")

class Computer:

    def __init__(self, regs=[0, 0, 0, 0]):
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
        self.regs = regs

    def set_regs(self, values=[0,0,0,0]):
        """ default - reset regs """
        self.regs = values
    def __str__(self):
        return str("16BIT, REGS: " + str(self.regs))
    def __repr__(self):
        return str(self)

    def eqir(self, op): #
        self.regs[op[2]] = int(op[0] == self.regs[op[1]])
    def eqri(self, op): #
        self.regs[op[2]] = int(self.regs[op[0]] == op[1])
    def eqrr(self, op): #
        self.regs[op[2]] = int(self.regs[op[0]] == self.regs[op[1]])
    def gtir(self, op): #
        self.regs[op[2]] = int(op[0] > self.regs[op[1]])
    def gtri(self, op): #
        self.regs[op[2]] = int(self.regs[op[0]] > op[1])
    def gtrr(self, op): #
        self.regs[op[2]] = int(self.regs[op[0]] > self.regs[op[1]])
    def setr(self, op): #
        self.regs[op[2]] = self.regs[op[0]]
    def seti(self, op): #
        self.regs[op[2]] = op[0]
    def addr(self, op): #
        self.regs[op[2]] = self.regs[op[1]] + self.regs[op[0]]
    def addi(self, op): #
        self.regs[op[2]] = op[1] + self.regs[op[0]]
    def mulr(self, op): #
        self.regs[op[2]] = self.regs[op[1]] * self.regs[op[0]]
    def muli(self, op): #
        self.regs[op[2]] = op[1] * self.regs[op[0]]
    def banr(self, op): #
        self.regs[op[2]] = self.regs[op[1]] & self.regs[op[0]]
    def bani(self, op): #
        self.regs[op[2]] = op[1] & self.regs[op[0]]
    def borr(self, op): #
        self.regs[op[2]] = self.regs[op[1]] | self.regs[op[0]]
    def bori(self, op): #
        self.regs[op[2]] = op[1] | self.regs[op[0]]


def read_file():
    f = open("input.txt", "r")
    f = f.read()
    inp, test_program = f.split("\n\n\n")
    lines = inp.splitlines()
    lines.append('')

    formatted = []
    operation = list()
    for line in lines:
        if line == '':
            formatted.append(operation)
            operation = list()
        else:
            operation.append(line)

    # additional formatting
    for operation in formatted:
        operation[0] = operation[0].split(": ")[1]
        operation[0] = [int(char) for char in operation[0] \
                        if char not in (',',' ', '[', ']')]
        operation[1] = operation[1].split(" ")
        operation[1] = [int(char) for char in operation[1]]
        operation[2] = operation[2].split(": ")[1]
        operation[2] = [int(char) for char in operation[2] \
                        if char not in (',',' ', '[', ']')]
    return formatted

def test_opcodes(inp):
    #inp = [[[3,2,1,1],[9,2,1,2],[3,2,2,1]]]
    computer = Computer()
    computer.set_regs()
    op_names = computer.operations.keys()

    three_or_more = 0
    for sample in inp:
        ops = []
        possible_op = 0
        before = sample[0]
        instruction = sample[1][1:4] # skip opcode
        after = sample[2]
        for op in op_names:
            computer.set_regs(list(before))
            #print("actual before:" + str(before))
            #print("before:" + str(computer.regs))
            #print("op: " + op)
            computer.operations[op](instruction)
            if computer.regs == after:
                #print("+1")
                ops.append(op)
                possible_op += 1
        if possible_op == 2:
            print(ops)
            print(sample[1][0])
        if possible_op >= 3:
            three_or_more += 1
    print(three_or_more)

if __name__ == "__main__":
    inp = read_file()
    test_operations()
    test_opcodes(inp)
    #print(inp)

