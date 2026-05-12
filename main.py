
from fileConverter import *
from instruction import *
from scanner import *

inputFile = "myFile.as"
outputName = "myfile.txt"
controlRom = "controlRom.txt"

inputData = readFile(inputFile)
instructions = translateFile(inputData)

#print(instructions)

#instructions = [Instruction(Opcode.NOP, []), Instruction(Opcode.ADD, []), Instruction(Opcode.HLT, [])]
#instructions = [Instruction(Opcode.LDI, [1, 1]), Instruction(Opcode.LDI, [2, 2]), Instruction(Opcode.ADD, [1, 2, 3])]
instructionValues = [instruction.format() for instruction in instructions]
instructionValues = [item for sublist in instructionValues for item in sublist]

codeMap = getOpcodeRomMap()

generateFile(outputName, instructionValues)
generateFile(controlRom, codeMap)