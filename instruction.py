
from enum import Enum, auto

from re import search

#class Operand(Enum):
#    Reg = auto()
#    Address = auto()
#    Value = auto()


class Opcode(Enum):
    NOP = 0
    HLT = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    LDI = auto()
    INC = auto()
    DEC = auto()
    JMP = auto()
    BRH = auto()

class Registers(Enum):
    R0 = 0
    R1 = auto()
    R2 = auto()
    R3 = auto()
    R4 = auto()
    R5 = auto()
    R6 = auto()
    R7 = auto()
    R8 = auto()
    R9 = auto()
    R10 = auto()
    R11 = auto()
    R12 = auto()
    R13 = auto()
    R14 = auto()
    R15 = auto()

class Condition(Enum):
    zero = 0
    notZero = auto()
    carry = auto()
    notCarry = auto()

MathopOrder = [
    Opcode.ADD,
    Opcode.SUB,
    Opcode.MUL,
    Opcode.DIV,
]

def formatInt(value) -> str:
    return f"{int(value)}"

def formatToBase(value: str, base: int) -> str:
    return f"{int(value, base)}"

def formatBinToHex(value: str):
    return f"{formatHex(int(formatToBase(value, 2)))}"

def formatHex(value: int):
    return f"{value:x}"

def formatBin(value, bits: int) -> str:
    return f"{value:0{bits}b}"

def getOpcodeRomMap():
    codeMap = []
    for opcode in Opcode:
        mathOp = False
        mathIndex = 0
        loadImediate = False
        jump = False
        condition = False
        if opcode in MathopOrder:
            mathOp = True
            mathIndex = MathopOrder.index(opcode)
        match opcode:
            case Opcode.LDI:
                loadImediate = True
            case Opcode.INC:
                loadImediate = True
                mathOp = True
                mathIndex = MathopOrder.index(Opcode.ADD)
            case Opcode.DEC:
                loadImediate = True
                mathOp = True
                mathIndex = MathopOrder.index(Opcode.SUB)
            case Opcode.JMP:
                jump = True
            case Opcode.BRH:
                jump = True
                condition = True
        
        outputOrder = [formatBin(condition, 1), formatBin(jump, 1), formatBin(loadImediate, 1), formatBin(mathIndex, 4), formatBin(mathOp, 1)]
        code = "".join(outputOrder)
        code = formatBinToHex(code)
        codeMap.append(code)
    return codeMap
        

class Instruction:
    def __init__(self, opcode: Opcode, parameters: list[int]) -> None:
        self.opcode: Opcode = opcode
        self.parameters = parameters
        
    def format(self) -> list[str]:
        if self.opcode == Opcode.NOP:
            return [formatInt(0)] * 4
        
        formatOpcode = formatHex(self.opcode.value)
        
        sector2 = formatBin(0, 8)
        sector3 = formatBin(0, 8)
        sector4 = formatBin(0, 8)
        
        if self.opcode in MathopOrder:
            sector3 = f"0000{formatBin(self.parameters[2], 4)}"
            
        match self.opcode:
            case Opcode.ADD | Opcode.SUB | Opcode.MUL | Opcode.DIV:
                sector2 = f"{formatBin(self.parameters[0], 4)}{formatBin(self.parameters[1], 4)}"
            case Opcode.LDI:
                sector2 = f"{formatBin(self.parameters[0], 4)}0000"
                sector3 = f"{formatBin(self.parameters[1], 8)}"
            case Opcode.INC:
                sector2 = f"{formatBin(self.parameters[0], 4)}0000"
                sector3 = f"{formatBin(self.parameters[1], 8)}"
            case Opcode.JMP:
                bits = formatBin(self.parameters[0], 14)
                sector2 = f"{bits[8:14]}00"
                sector3 = f"{bits[:8]}"
            case Opcode.BRH:
                condition = formatBin(self.parameters[0], 2)
                bits = formatBin(self.parameters[1], 14)
                sector2 = f"{bits[8:14]}{condition}"
                sector3 = f"{bits[:8]}"
        
        return [formatOpcode, formatBinToHex(sector2), formatBinToHex(sector3), formatBinToHex(sector4)]
    
    def __str__(self):
        return f"{self.opcode} {self.parameters}"
    
    def __repr__(self):
        return f"Instruction( opcode={self.opcode}, parameters={self.parameters} )"


def translateFile(data: list[str]) -> list[Instruction]:
    output = []
    for line in data:
        words = line.split(" ")
        if not words[0] in Opcode.__members__:
            continue
        parameters = []
        for word in words[1::]:
            if word in Registers.__members__:
                parameters.append(Registers[word].value)
            elif word in Condition.__members__:
                parameters.append(Condition[word].value)
            elif word.isdecimal():
                parameters.append(int(word))
        instruction = Instruction(Opcode[words[0]], parameters)
        output.append(instruction)
    return output

if __name__ == "__main__":
    print(getOpcodeRomMap())