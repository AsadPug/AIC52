import random
from copy import deepcopy

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height

        self.__data: list[list[bool]] = [] # valeur de data[x][y] -> état de la case (x, y)
        for x in range(0, self.width):
            self.__data.append([])
            for y in range(0, self.height):
                if (y != 0 and x != 0 and 
                    y != height -1 and x != width -1):

                    state = (random.randint(1, 100) % 2 == 0) 
                    self.__data[x].append(state)

                else:
                    self.__data[x].append(False)

    def update_grid(self) -> None:
        self.__temp_cells: list[list[bool]] = deepcopy(self.__data)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.__temp_cells[x][y] = self.will_live(x,y)
        self.__data, self.__temp_cells  = self.__temp_cells, self.__data

    def will_live(self, x: int, y: int)-> bool:
        state = self.__data[x][y]
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

        for collumn in self.__data[x-1:x+2]:
            for case in collumn[y-1:y+2]:
                n_neighbour += case

        n_neighbour -= self.__data[x][y]

        return n_neighbour
    
    def resize(self, width: int, height: int):
        if height > self.__height:
            n_extend = height - self.__height
            for column in self.__data:
                column.extend([False] * n_extend)
        if width > self.__width:
            n_extend = width - self.__width
            self.__data.extend([[False] * height]* n_extend)
        if height < self.__height:
            n_shrink = self.__height - height
            for column in self.__data:
                column = column[:-n_shrink]
        if width < self.__width:
            n_shrink = self.__width - width
            self.__data[:-n_shrink]
    
        self.__height = height
        self.__width = width
    
    def get_cell_at(self, x: int, y: int) -> bool:
        return self.__data[x][y]


    @property
    def data(self):
        return self.__data    

    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, value):
        self.resize(self.width, value)

    @property
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, value):
        self.resize(value, self.height)


if __name__ == "__main__":
    grid = Grid(10, 10)
    grid.resize(8, 8)
    grid.height = 6
    print(grid.width,  grid.height)