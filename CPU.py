import time
from constants import *

class CPU():
    def __init__(self, ROM, RAM, debug=False, delay=-1):
        self.regs = [0, 0] # A and B registers
        self.PC = 0
        self.Z = 0

        self.ROM = ROM
        self.RAM = RAM

        self.debug = debug
        self.delay = delay

    def getOpCode(self, instr):
        """ Gets 3 OP_CODE bits from a instruction"""
        return (instr&OP_CODE) >> 5

    def getSValue(self, instr):
        """ Choose between register or inmediate mode and return register value 
            or inmediate value respectively"""
        if (instr&SOURCE_MODE) == REG_MODE:
            return self.regs[(instr&SOURCE_REG) >> 3]
        else:
            return (instr&SOURCE_INM) >> 1

    def getDReg(self, instr):
        """ Return destination register (A or B)"""
        return instr&DEST_REG

    def getDValue(self, instr):
        """ Return destination value (only regs value allowed) """
        return self.regs[self.getDReg(instr)]

    def updateZ(self, op_result):
        """ Z=1 if op_result == 0"""
        self.Z = 1 if op_result == 0 else 0

    def printDebugInfo(self, instr):
        print(f"{OP_NAMES[self.getOpCode(instr)]}, A {self.regs[A]}, B {self.regs[B]}, PC {self.PC}, Z {self.Z}")

    
    def run(self):
        print("Running CPU...")

        while self.PC < self.ROM.size:
            """ Fetch instruction"""
            instr = self.ROM.data[self.PC] # Method to access memory?

            """ Increment PC (jumps instruction can overload it) """
            self.PC += 1

            """ Decode and execute"""
            op = self.getOpCode(instr)

            if op == OP_LOAD:
                self.regs[self.getDReg(instr)] = self.RAM.data[self.getSValue(instr)]
            elif op == OP_STORE:
                self.RAM.data[self.getSValue(instr)] = self.getDValue(instr)
            elif op == OP_ADD:
                self.regs[self.getDReg(instr)] = op_result = self.regs[A] + self.getSValue(instr)
                self.updateZ(op_result)
            elif op == OP_SUB:
                self.regs[self.getDReg(instr)] = op_result = self.regs[A] - self.getSValue(instr)
                self.updateZ(op_result)
            elif op == OP_JMP:
                self.PC = self.getSValue(instr)
            elif op == OP_BRZ:
                if self.Z:
                    self.PC = self.getSValue(instr)
            elif op == OP_AND:
                self.regs[self.getDReg(instr)] = op_result = self.regs[A] & self.getSValue(instr)
                self.updateZ(op_result)


            if self.debug:
                self.printDebugInfo(instr)
            if self.delay != -1:
                time.sleep(self.delay)
        
        print("Finish execution.")


