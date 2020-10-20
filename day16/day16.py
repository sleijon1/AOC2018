class Computer:

    def __init__(self, regs=[0, 0, 0, 0]):
        self.operations = {}
        self.regs = regs

    def set_regs(self, values=[0,0,0,0]):
        """ default - reset regs """
        self.regs = values

    def __str__(self):
        return str("16BIT, REGS: " + str(self.regs))

    def __repr__(self):
        return str(self)

    def addr(self, op):
        self.regs[op[2]] = self.regs[op[1]] + self.regs[op[0]]
    def addi(self, op):
        self.regs[op[2]] = op[1] + self.regs[op[0]]
    def mulr(self, op):
        self.regs[op[2]] = self.regs[op[1]] * self.regs[op[0]]
    def muli(self, op):
        self.regs[op[2]] = op[1] * self.regs[op[0]]
    def banr(self, op):
        bits_one = bin(self.regs[op[1]])[2:]
        bits_two = bin(self.regs[op[0]])[2:]
        bits_one = ('0'*(4-len(bits_one)))+bits_one
        bits_two = ('0'*(4-len(bits_two)))+bits_two
        result = ""
        for bit1, bit2 in zip(bits_one, bits_two):
            if int(bit1) and int(bit2):
                result += "1"
            else:
                result += "0"
        result = "0b" + result
        result = int(result, 2)
        self.regs[op[2]] = result
    def bani(self, op):
        bits_one = bin(op[1])[2:] # value B
        bits_two = bin(self.regs[op[0]])[2:] # register A
        bits_one = ('0'*(4-len(bits_one)))+bits_one
        bits_two = ('0'*(4-len(bits_two)))+bits_two
        result = ""
        for bit1, bit2 in zip(bits_one, bits_two):
            if int(bit1) and int(bit2):
                result += "1"
            else:
                result += "0"
        result = "0b" + result
        result = int(result, 2)
        self.regs[op[2]] = result
    def borr(self, op):
        bits_one = bin(self.regs[op[1]])[2:]
        bits_two = bin(self.regs[op[0]])[2:]
        bits_one = ('0'*(4-len(bits_one)))+bits_one
        bits_two = ('0'*(4-len(bits_two)))+bits_two
        result = ""
        for bit1, bit2 in zip(bits_one, bits_two):
            if int(bit1) or int(bit2):
                result += "1"
            else:
                result += "0"
        result = "0b" + result
        result = int(result, 2)
        self.regs[op[2]] = result
    def bori(self, op):
        bits_one = bin(op[1])[2:] # value B
        bits_two = bin(self.regs[op[0]])[2:] # register A
        bits_one = ('0'*(4-len(bits_one)))+bits_one
        bits_two = ('0'*(4-len(bits_two)))+bits_two
        result = ""
        for bit1, bit2 in zip(bits_one, bits_two):
            if int(bit1) or int(bit2):
                result += "1"
            else:
                result += "0"
        result = "0b" + result
        result = int(result, 2)
        self.regs[op[2]] = result


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

def test_operations():
    test_comp = Computer()
    test_comp.set_regs([3,2,1,1])
    test_comp.mulr([2,1,2])
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
    print(test_comp)

if __name__ == "__main__":
    inp = read_file()
    test_operations()
    #print(inp)

