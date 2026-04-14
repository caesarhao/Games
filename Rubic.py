# to learn Rubik Cube

class Rubic:
    def __init__(self, n = 3):
        self.N = n
    def numCubies(self) -> int:
        return self.N ** 3 - (self.N - 1) ** 3
    def numCornerCubies(self) -> int:
        return 8
    def numCenterCubies(self) -> int:
        if self.N % 2 == 0:
            return 0
        else:
            return 6
    def numEdgeCubies(self) -> int:
        return self.numCubies() - self.numCornerCubies() - self.numCenterCubies()

if __name__ == "__main__":
    rub = Rubic(3)
    print(rub)
    
