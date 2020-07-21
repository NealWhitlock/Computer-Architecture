"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256         # Memory list to hold up to 256 commands
        self.register = [0] * 8      # Register to store up to 8 values
        self.PC = 0                  # Program counter
        self.register[7] = 0xF4      # Stack pointer set to F4 in the RAM

    #     # Storing command codes for easier reference
    #     HLT = 0b00000001        # Halt execution
    #     LDI = 0b10000010        # Load immediate
    #     PRN = 0b01000111        # Print
    #     MUL = 0b10100010        # Multiply

    #     # Create branch table
    #     self.branchtable = {}
    #     self.branchtable[HLT] = self.halt_op
    
    # def halt_op(self):



    def load(self, program=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.RAM[address] = instruction
        #     print(instruction)
        #     print(self.RAM[address])
        #     address += 1

        with open(program, 'r') as f:
            incoming = f.read().splitlines()

        # print(incoming)

        for instruction in incoming:
            if instruction != "" and instruction[0] != "#":
                # print(instruction)
                self.RAM[address] = int(instruction[:8], 2)
                # print(self.RAM[address])
                address += 1

        # for i, line in enumerate(incoming):
        #     print(i, line)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()


    def run(self):
        """Run the CPU."""
        # Storing command codes for easier reference
        HLT = 0b00000001        # Halt execution
        LDI = 0b10000010        # Load immediate
        PRN = 0b01000111        # Print
        MUL = 0b10100010        # Multiply
        PUSH = 0b01000101       # Push an item onto the stack
        POP = 0b01000110        # Pop an item off of the stack

        # While loop to keep running the program
        run_again = True
        while run_again:

            #self.trace()

            IR = self.RAM[self.PC]         # Load the instruction from RAM at PC index
            
            operand_a = self.RAM[self.PC+1]     # Load the next two locations of RAM in case
            operand_b = self.RAM[self.PC+2]     # the instruction at RAM[PC] needs them

            if IR == HLT:
                # Break the loop
                run_again = False
            
            elif IR == LDI:
                # At the next address in the memory, input the value
                # that follows
                self.register[operand_a] = operand_b
                self.PC += 3
            
            elif IR == PRN:
                # Print the value at the following address
                print(self.register[operand_a])
                self.PC += 2
            
            elif IR == MUL:
                # Gets the two numbers at the registers for the next two locations
                # and puts their product in the register of the first location
                num1 = self.register[operand_a]
                num2 = self.register[operand_b]
                self.register[operand_a] = num1 * num2
                self.PC += 3
            
            elif IR == PUSH:
                # Push value onto the stack
                # Decrement the stack pointer
                self.register[7] -= 1
                # Copy value in operand a to the stack location in RAM
                self.RAM[self.register[7]] = self.register[operand_a]
                self.PC += 2
            
            elif IR == POP:
                # Pop value off of the stack
                # Get the value from the stack pointer and put in register location
                self.register[operand_a] = self.RAM[self.register[7]]
                # Increment the stack pointer
                self.register[7] += 1
                self.PC += 2

        


    def ram_read(self, MAR):
        """Read the contents of RAM at location MAR."""
        return self.RAM[MAR]


    def ram_write(self, MAR, MDR):
        """Write MDR to the location MAR in RAM."""
        self.RAM[MAR] = MDR