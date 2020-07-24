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
        self.FL = 0b00000000         # Set the flag state to 0


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
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        # elif op == "DIV":
        #     if self.register[reg_b] == 0:
        #         print("Error: Division by Zero")
        #         run_again = False
        #     else:
        #         self.register[reg_a] /= self.register[reg_b]
        elif op == "CMP":
            # `FL` bits: `00000LGE`
            num1 = self.register[reg_a]
            num2 = self.register[reg_b]

            if num1 < num2:
                # Set less than flag
                self.FL = self.FL | 0b00000100
            else:
                # Remove less than flag
                self.FL = self.FL & 0b00000011

            if num1 > num2:
                # Set greater than flag
                self.FL = self.FL | 0b00000010
            else:
                # Remove greater than flag
                self.FL = self.FL & 0b00000101

            if num1 == num2:
                # Set equal to flag
                self.FL = self.FL | 0b00000001
            else:
                # Remove equal to flag
                self.FL = self.FL & 0b00000110
        elif op == "AND":
            pass
        elif op == "OR":
            pass
        elif op == "XOR":
            pass
        elif op == "SHL":
            pass
        elif op == "SHR":
            pass
        elif op == "MOD":
            pass

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
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100
        ST = 0b10000100

        # While loop to keep running the program
        run_again = True
        while run_again:
            #print("PC:", self.PC)
            print_steps = False
            #self.trace()

            IR = self.RAM[self.PC]         # Load the instruction from RAM at PC index
            
            operand_a = self.RAM[self.PC+1]     # Load the next two locations of RAM in case
            operand_b = self.RAM[self.PC+2]     # the instruction at RAM[PC] needs them

            if IR == HLT:
                if print_steps == True:
                    print("Halting; PC:", self.PC)
                # Break the loop
                run_again = False
            
            elif IR == LDI:
                if print_steps == True:
                    print("Loading; PC:", self.PC)
                # At the next address in the memory, input the value
                # that follows
                self.register[operand_a] = operand_b
                self.PC += 3
            
            elif IR == PRN:
                if print_steps == True:
                    print("Printing; PC:", self.PC)
                # Print the value at the following address
                print(self.register[operand_a])
                self.PC += 2
            
            elif IR == MUL:
                if print_steps == True:
                    print("Multiplying; PC:", self.PC)
                # Gets the two numbers at the registers for the next two locations
                # and puts their product in the register of the first location
                # num1 = self.register[operand_a]
                # num2 = self.register[operand_b]
                # self.register[operand_a] = num1 * num2

                # Using the ALU
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3
            
            elif IR == PUSH:
                if print_steps == True:
                    print("Pushing; PC:", self.PC)
                # Push value onto the stack
                # Decrement the stack pointer
                self.register[7] -= 1
                # Copy value in operand a to the stack location in RAM
                self.RAM[self.register[7]] = self.register[operand_a]
                self.PC += 2
            
            elif IR == POP:
                if print_steps == True:
                    print("Popping; PC:", self.PC)
                # Pop value off of the stack
                # Get the value from the stack pointer and put in register location
                self.register[operand_a] = self.RAM[self.register[7]]
                # Increment the stack pointer
                self.register[7] += 1
                self.PC += 2
            
            elif IR == CALL:
                if print_steps == True:
                    print("Calling; PC:", self.PC)
                # Decrement the stack pointer
                self.register[7] -= 1
                # Save where the program counter should start AFTER using CALL
                self.RAM[self.register[7]] = self.PC + 2
                # Move program counter to where the CALL value is pointing
                self.PC = self.register[self.RAM[self.PC + 1]]

            elif IR == RET:
                if print_steps == True:
                    print("Returning; PC:", self.PC)
                # Get the program counter value stored from the most recent CALL
                self.PC = self.RAM[self.register[7]]
                # Increment the stack pointer
                self.register[7] += 1
            
            elif IR == ADD:
                if print_steps == True:
                    print("Adding; PC:", self.PC)
                # Gets the two numbers at the registers for the next two locations
                # and puts their sum in the register of the first location 
                # num1 = self.register[operand_a]
                # num2 = self.register[operand_b]
                # self.register[operand_a] = num1 + num2

                # Using the ALU
                self.alu("ADD", operand_a, operand_b)
                self.PC += 3
            
            elif IR == CMP:
                if print_steps == True:
                    print("Comparing; PC:", self.PC)
                # # `FL` bits: `00000LGE`
                # num1 = self.register[operand_a]
                # num2 = self.register[operand_b]

                # if num1 < num2:
                #     # Set less than flag
                #     self.FL = self.FL | 0b00000100
                # else:
                #     # Remove less than flag
                #     self.FL = self.FL & 0b00000011

                # if num1 > num2:
                #     # Set greater than flag
                #     self.FL = self.FL | 0b00000010
                # else:
                #     # Remove greater than flag
                #     self.FL = self.FL & 0b00000101

                # if num1 == num2:
                #     # Set equal to flag
                #     self.FL = self.FL | 0b00000001
                # else:
                #     # Remove equal to flag
                #     self.FL = self.FL & 0b00000110

                # Using ALU
                self.alu("CMP", operand_a, operand_b)

                self.PC += 3
            
            elif IR == JEQ:
                if print_steps == True:
                    print("Checking if equal; PC:", self.PC)
                if self.FL & 0b00000001 == 0b00000001:
                    self.PC = self.register[operand_a]
                else:
                    self.PC += 2
                
            elif IR == JNE:
                if print_steps == True:
                    print("Checking if not equal; PC:", self.PC)
                if self.FL & 0b00000001 != 0b00000001:
                    self.PC = self.register[operand_a]
                else:
                    self.PC += 2

            elif IR == JMP:
                if print_steps == True:
                    print("Jumping; PC:", self.PC)
                self.PC = self.register[operand_a]
            
            elif IR == ST:
                self.RAM[self.register[operand_a]] = self.RAM[self.register[operand_b]]
                self.PC += 3

            else:
                # Catch-all statement in case a command has not been registered
                print("IR:", self.RAM[self.PC])
                print("Command not recognized")
                run_again = False

        


    def ram_read(self, MAR):
        """Read the contents of RAM at location MAR."""
        return self.RAM[MAR]


    def ram_write(self, MAR, MDR):
        """Write MDR to the location MAR in RAM."""
        self.RAM[MAR] = MDR