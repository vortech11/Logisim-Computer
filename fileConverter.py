

def generateFile(fileName: str, fileData: list) -> None:
    output: str = "v2.0 raw\n"
    
    cols = 8
    
    strData = [str(value) for value in fileData]
    
    formatList = [strData[i:i + cols] for i in range(0, len(strData), cols)]
    
    outputListList = [" ".join(item) for item in formatList]
    
    outputList = "\n".join(outputListList)
    
    output += outputList
    
    with open(fileName, "w") as file:
        file.write(output)