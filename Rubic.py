# to learn Rubik Cube
from enum import Enum

# x-axis towards Front, y-axis towards Right, z-axis towards Up
class Face(Enum):
    UP     =  0
    LEFT   =  1
    FRONT  =  2
    RIGHT  =  3
    BACK   =  4
    DOWN   =  5

class Color(Enum):
    N = (0, 0, 0)
    W = (200, 200, 200)
    R = (255, 0, 0)
    G = (0, 255, 0)
    B = (0, 0, 255)
    O = (255, 165, 0)
    Y = (255, 255, 0)

class Cubie:
    def __init__(self, coor, colors):
        self.coord = coor.copy()
        self.colors = colors.copy()
    
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
    def getFace(face : Face):
        pass

if __name__ == "__main__":
    rub = Rubic(3)
    print(rub)
    
