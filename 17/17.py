#!/usr/bin/env python3

class ThreeBitComputer:
    def __init__(self, program):
        self.program = program  # List of 3-bit numbers (opcodes + operands)
        self.registers = {"A": 0, "B": 0, "C": 0}  # Registers
        self.instruction_pointer = 0  # Program counter
        self.output = []  # Collected outputs

    def run(self):
        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]

            # Execute the current instruction
            self.execute(opcode, operand)

            # Advance instruction pointer (unless modified by jnz)
            if opcode == 3 and self.registers['A'] != 0:  # jnz may jump
                continue
            else:
                self.instruction_pointer += 2

    def execute(self, opcode, operand):
        # Operand value resolution
        if operand is not None:
            combo_operand = self.resolve_operand(operand)

        # Handle each opcode
        if opcode == 0:  # adv
            self.registers["A"] //= 2 ** combo_operand
        elif opcode == 1:  # bxl
            self.registers["B"] ^= operand
        elif opcode == 2:  # bst
            self.registers["B"] = combo_operand % 8
        elif opcode == 3:  # jnz
            if self.registers["A"] != 0:
                self.instruction_pointer = operand
        elif opcode == 4:  # bxc
            self.registers["B"] ^= self.registers["C"]
        elif opcode == 5:  # out
            self.output.append(combo_operand % 8)
        elif opcode == 6:  # bdv
            self.registers["B"] = self.registers["A"] // (2 ** combo_operand)
        elif opcode == 7:  # cdv
            self.registers["C"] = self.registers["A"] // (2 ** combo_operand)

    def resolve_operand(self, operand):
        """Resolves the operand value based on its type."""
        if operand <= 3:  # Literal values 0–3
            return operand
        elif operand == 4:  # Value of register A
            return self.registers["A"]
        elif operand == 5:  # Value of register B
            return self.registers["B"]
        elif operand == 6:  # Value of register C
            return self.registers["C"]
        elif operand == 7:  # Reserved
            raise ValueError("Invalid operand: 7")

    def get_output(self):
        """Returns the output of the program."""
        return ','.join([str(i) for i in self.output])

if __name__ == '__main__':
    with open('input') as fd:
        registers = []
        instructions = []
        for line in fd:
            if 'Register' in line:
                registers.append(int(line.split(':')[1]))
            elif 'Program' in line:
                instructions = [int(s) for s in line.split(':')[1].strip().split(',')]

        output = []
        a = 0
        while instructions != output:
            _,b,c = registers
            tbc = ThreeBitComputer(instructions)
            tbc.registers['A'] = a
            tbc.registers['B'] = b
            tbc.registers['C'] = c

            tbc.run()
            output = tbc.output
            a += 1
        print(a - 1)
