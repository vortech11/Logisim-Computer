
def readFile(fileName: str) -> list[str]:
    output = []
    with open(fileName, "r") as file:
        for line in file:
            output.append(line.strip())
    return output

if __name__ == "__main__":
    print(readFile("myfile.as"))