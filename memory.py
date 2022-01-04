class memory_ROM():
    def __init__(self):
        self.size = 256
        self.data = [0] * self.size

    def printInBinary(self):
        cont = 0
        for index, row in enumerate(self.data):
            if index % 4 == 0:
                print(f"\n{index}:", end="\t")
            print(bin(row), end=" ")
        print()


    def loadBinaryFile(self, file_path):
        print("Loading file into ROM...")
        
        cont = 0
        with open(file_path) as f:
            data = f.read(8)
            while data and cont < self.size:
                self.data[cont] = int(data, 2)
                data = f.read(8)
                cont += 1

            if data:
                self.data = [0] * self.size
                print("No hay suficiente espacio, memoria reseteada.")

class memory_RAM():
    def __init__(self):
        self.size = 256
        self.data = [0] * self.size

    def printInBinary(self):
        cont = 0
        for index, row in enumerate(self.data):
            if index % 4 == 0:
                print(f"\n{index}:", end="\t")
            print(bin(row), end=" ")
        print()

    def printInDecimal(self):
        cont = 0
        for index, row in enumerate(self.data):
            if index % 4 == 0:
                print(f"\n{index}:", end="\t")
            print(row, end=" ")
        print()