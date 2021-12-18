# A simple 8bit CPU by alvarogd16

# Two registers A and B

# 8 bit instruction
# 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0
# 
# [7..5] -> OpCode
# [4..1] -> Source ([4] -> Address mode, [3] -> Reg, [3..1] inmediate value)
# [0]    -> Destination reg
# 
# Address mode 
# 0 -> from register (1 bit)
# 1 -> inmediate value (3 bit :( )


# ************* Op Codes *********************

# Op  |  Mnemonic | Description          |  Micro instructions
# 000    NOP        No operation
# 001    LOAD       Load from memory        D <- (S) (Source reg value indicate memory direction)
# 010    STORE      Store from memory       (S) <- D (Source reg value indicate memory direction) I have to interchange the S and D sorry :(
# 011    ADD        Add registers or Inm    D <- A + S
# 100    SUB        Sub registers or inm    D <- A - S
# 101    JMP        Jump inconditional      PC <- S   
# 110    BRZ        Branch if zero          if Z==1: PC <- S else: PC+=1  
# 111    AND        And registers or Inm    D <- A and S


# ********* This part is from jmi2k *****************
OP0 = lambda op: op<<5
OP1 = lambda op: lambda a: op<<5 | (a&0b1111)<<1
OP2 = lambda op: lambda a, b: op<<5 | (a&0b1111)<<1 | b&0b1

NOP = OP0(0b000)
LOAD = OP2(0b001)
STORE = OP2(0b010)
ADD = OP2(0b011)
SUB = OP2(0b100)
JMP = OP1(0b101)
BRZ = OP1(0b110)
AND = OP2(0b111)

A = 0
B = 1
# ****************************************************

import time


# ************ Memories **********************

# 256 * 8bit data memory
memory = [0] * 256

memory[0] = 10
memory[1] = 0
memory[2] = 0
memory[3] = 1
memory[4] = 0
memory[5] = 16

# 256 * 8bit instruction ROM
ROM = [0] * 256

# # Sum two numbers in memory[0] and [1], and store in [2]
# ROM[0] = 0b00110000 # A <- memory[0]
# ROM[1] = 0b00110011 # B <- memory[1]
# ROM[2] = 0b01101001 # B <- A + B
# ROM[3] = 0b01010101 # memory[2] <- B

# Fibonacci serie n_times -> memory[0]  (max 13 because fib(13) = 233 < 255 -> 8bits)
# cont -> memory[1] 
# f0 -> memory[2]
# f1 -> memory[3]
# f2 -> memory[4]
# fin -> memory[5] (etiqueta fin de programa)
ROM[0] = LOAD(0, A)
ROM[1] = LOAD(1, B)
ROM[2] = SUB(B, B)
ROM[3] = LOAD(5, A)
ROM[4] = BRZ(A)
ROM[5] = LOAD(2, A)
ROM[6] = LOAD(3, B)
ROM[7] = ADD(B, A)
ROM[8] = STORE(4, A)
ROM[9] = LOAD(3, B)
ROM[10] = STORE(2, B)
ROM[11] = STORE(3, A)
ROM[12] = LOAD(1, A)
ROM[13] = ADD(1, A)
ROM[14] = STORE(1, A)
ROM[15] = JMP(0)

# ROM[0] = 0b00110000 # A <- memory[0]
# ROM[1] = 0b00110011 # B <- memory[1]
# ROM[2] = 0b10001001 # B <- A - B        Si (n_times == cont) salta a fin 
# ROM[3] = 0b00111010 # A <- memory[5]    Direccion del salto       
# ROM[4] = 0b11000000 # if Z==1 PC=fin
# ROM[5] = 0b00110100 # A <- memory[2]
# ROM[6] = 0b00110111 # B <- memory[3]
# ROM[7] = 0b01101000 # A <- A + B
# ROM[8] = 0b01011000 # memory[4] <- A    Carga f0+f1 en f2   
# ROM[9] = 0b00110111 # B <- memory[3]    Carga f1 en f0
# ROM[10] = 0b01010101 # memory[2] <- B
# ROM[11] = 0b01010110 # memory[3] <- A   Carga f2 en f1
# ROM[12] = 0b00110010 # A <- memory[1]    
# ROM[13] = 0b01110010 # A++              Incrementamos cont
# ROM[14] = 0b01010010 # memory[1] <- A   Carga cont++ en memoria
# ROM[15] = 0b10110000 # jmp 0            Salta a la comprobación



# ****************** CPU Emulator **************************

# A in regs[0], B in regs[1]
CPU_state = {
    "regs": [0, 0],
    "PC": 0,
    "Z": 0
}

# Return Op bites [7..5] from a instruction 
def getOpCode(instruction):
    return (instruction & 0b11100000)>>5

# Return S value deppending of address mode 
def getSValue(instruction, CPU_state):
    # Register mode, register in [3], A is 0 and B is 1
    if (instruction & 0b00010000) == 0:
        return CPU_state['regs'][(instruction & 0b00001000)>>3]
    # Inmediate mode, value [3..1]
    else:
        return (instruction & 0b00001110)>>1


# Return 0 if A reg in destination 
# Return 1 if B reg in destination
def getDReg(instruction):
    return instruction & 0b00000001

# Return D value
def getDValue(instruction, CPU_state):
    return CPU_state['regs'][instruction & 0b00000001]

# Update Z flag depending of operationRes
def updateZ(CPU_state, operationRes):
    if operationRes == 0:
        CPU_state['Z'] = 1
    else:
        CPU_state['Z'] = 0

# For debug info
opCodeNames = ["NOP", "LOAD", "STORE", "ADD", "SUB", "JMP", "BRZ", "AND"]
def printDebugInfo(inst, CPU_state):
    print(f"{opCodeNames[getOpCode(inst)]}, A {CPU_state['regs'][0]}, B {CPU_state['regs'][1]}, PC {CPU_state['PC']}, Z {CPU_state['Z']}")



def runCPU(memory, CPU_state):
    while(CPU_state['PC'] < len(ROM)):
        # Fetch instruction 
        instruction = ROM[CPU_state['PC']]

        # Increment PC
        CPU_state['PC'] += 1

        # Decode and execute
        op = getOpCode(instruction)

        # LOAD
        if op == 0b001:
            CPU_state['regs'][getDReg(instruction)] = memory[getSValue(instruction, CPU_state)]
        # STORE
        elif op == 0b010:
            memory[getSValue(instruction, CPU_state)] = getDValue(instruction, CPU_state)
        # ADD
        elif op == 0b011:
            operationRes = CPU_state['regs'][0] + getSValue(instruction, CPU_state)
            CPU_state['regs'][getDReg(instruction)] = operationRes
            updateZ(CPU_state, operationRes)
        # SUB 
        elif op == 0b100:
            operationRes = CPU_state['regs'][0] - getSValue(instruction, CPU_state)
            CPU_state['regs'][getDReg(instruction)] = operationRes
            updateZ(CPU_state, operationRes)
        # JMP
        elif op == 0b101:
            CPU_state['PC'] = getSValue(instruction, CPU_state)
        # BRZ
        elif op == 0b110:
            if CPU_state['Z'] == 1:
                CPU_state['PC'] = getSValue(instruction, CPU_state)
        # AND
        elif op == 0b111:
            operationRes = CPU_state['regs'][0] & getSValue(instruction, CPU_state)
            CPU_state['regs'][getDReg(instruction)] = operationRes
            updateZ(CPU_state, operationRes)
        
        printDebugInfo(instruction, CPU_state)
        # time.sleep(0.1)

runCPU(memory, CPU_state)
print(memory)