import random
from copy import deepcopy

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: list[list[bool]] = []# valeur de cell[x][y] -> état de la case (x, y)
        for y in range(0, self.height):
            self.cells.append([])
            for x in range(0, self.width):
                if (y != 0 and x != 0 and 
                    y != height -1 and x != width -1):
                    state = True if random.randint(1, 100) % 15 == 0 else False
                    self.cells[y].append(state)
                else:
                    self.cells[y].append(False)

    def update_grid(self) -> None:
        temp_cells: list[list[bool]] = deepcopy(self.cells)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                temp_cells[x][y] = self.will_live(x,y)
        self.cells = temp_cells

    def will_live(self, x: int, y: int)-> bool:
        state = self.cells[x][y]
        n_neighbour = self.count_neighbour(x,y)
        result = False

        if state == True:
            if 3>= n_neighbour >=2:
                result = True
        else:
            if n_neighbour == 3:
                result = True

        return result


    def count_neighbour(self,x,y) -> int:
        n_neighbour = 0
        if self.cells[x-1][y] == True:
            n_neighbour+=1
        if self.cells[x-1][y-1] == True:
            n_neighbour+=1
        if self.cells[x-1][y+1] == True:
            n_neighbour+=1
        if self.cells[x+1][y] == True:
            n_neighbour+=1
        if self.cells[x+1][y-1] == True:
            n_neighbour+=1
        if self.cells[x+1][y+1] == True:
            n_neighbour+=1
        if self.cells[x][y-1] == True:
            n_neighbour+=1
        if self.cells[x][y+1] == True:
            n_neighbour+=1
        return n_neighbour
