#!/usr/bin/env python3


class Gate:
    def __init__(self, gate_type, input1, input2, output, input_values):
        self.gate_type = gate_type  # Type of gate: AND, OR, XOR
        self.input1 = input1  # Name of the first input
        self.input2 = input2  # Name of the second input
        self.output = output  # Name of the output
        self.input_values = input_values  # Dictionary of inputs and their constant values (0 or 1)

    def evaluate(self):
        # Fetch the values for the inputs
        try:
            val1 = self.input_values[self.input1]
            val2 = self.input_values[self.input2]
        except:
            return False

        # Perform the logic operation based on the gate type
        if self.gate_type == "AND":
            result = val1 & val2
        elif self.gate_type == "OR":
            result = val1 | val2
        elif self.gate_type == "XOR":
            result = val1 ^ val2
        else:
            raise ValueError(f"Unsupported gate type: {self.gate_type}")

        # Update the input values dictionary with the output
        self.input_values[self.output] = result
        return True

    @classmethod
    def from_string(cls, gate_string, input_values):
        # Parse the input string to extract the components
        parts = gate_string.split()
        if len(parts) != 5 or parts[3] != "->":
            raise ValueError("Invalid gate string format. Expected format: '<input1> <GATE> <input2> -> <output>'")

        input1 = parts[0]
        gate_type = parts[1]
        input2 = parts[2]
        output = parts[4]

        return cls(gate_type, input1, input2, output, input_values)

    def __str__(self):
        """Return a string representation of the gate."""
        return f"Gate({self.gate_type}): {self.input1}, {self.input2} -> {self.output}"

# Evaluate all gates in a list until all are successfully evaluated or an irrecoverable error occurs
def evaluate_all_gates(gates):
    while gates:
        progress = False
        for gate in gates[:]:  # Iterate over a copy of the list
            if gate.evaluate():
                print(f"Successfully evaluated {gate.output}")
                gates.remove(gate)  # Remove successfully evaluated gate
                progress = True
        if not progress:  # No gates were evaluated in this iteration
            print("Unable to evaluate remaining gates due to missing dependencies or errors.")
            return False
    return True

def get_z_values_as_bit_string_and_decimal(input_values):
    # Get all keys starting with 'z', sort them, and fetch their values
    z_keys = sorted((k for k in input_values if k.startswith('z')), reverse=True)
    bit_string = ''.join(str(input_values[k]) for k in z_keys)
    decimal_value = int(bit_string, 2)
    return bit_string, decimal_value

if __name__ == '__main__':
    values = dict()
    gates = []
    with open('input') as fd:
        for line in fd:
            line = line.strip()

            if ':' in line:
                value, constant = line.split(':')
                value = value.strip()
                values[value] = int(constant)
            elif line:
                gates.append(Gate.from_string(line, values))

        print(values)
        
        for g in gates:
            print(g)

    # Evaluate all gates
    if evaluate_all_gates(gates):
        print("All gates evaluated successfully.")
        print(get_z_values_as_bit_string_and_decimal(values))
    else:
        print("Some gates could not be evaluated.")
