import random
import os
from copy import deepcopy
from PIL import Image

def load_image(path: str) -> list[list[bool]]:
    image = Image.open(path, 'r')
    raw_data = list(image.getdata())
    data: list[list[bool]] = [] # valeur de data[x][y] -> état de la case (x, y)

    for x in range(0, image.width):
        data.append([])
        for y in range(0, image.height):
            if raw_data[(y * image.width) + x][3] > 50:
                data[x].append(True)
            else:
                data[x].append(False)

    return data


class GOLEngine:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.n_cells_alive = 0
        self.n_cells_dead = 0
        
        self.fill_grid(50)

        self.__temp_cells: list[list[bool]] = deepcopy(self.__data)

    def tick(self, change_state: bool = True) -> None:
        
        self.n_cells_alive = 0

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                will_live = self.will_live(x,y)
                if change_state:
                    self.__temp_cells[x][y] = will_live
                if will_live:
                    self.n_cells_alive += 1
        
        self.n_cells_dead = (self.width * self.height) - self.n_cells_alive
                
        self.__data, self.__temp_cells  = self.__temp_cells, self.__data

    def fill_grid(self, percent_filled: int) -> None:
        self.__data: list[list[bool]] = [] # valeur de data[x][y] -> état de la case (x, y)

        for x in range(0, self.__width):
            self.__data.append([])
            for y in range(0, self.__height):
                if (y != 0 and x != 0 and 
                    y != self.__height -1 and x != self.__width -1):

                    state = (random.randint(1, 100) <= percent_filled) 
                    self.__data[x].append(state)

                else:
                    self.__data[x].append(False)

        self.__temp_cells: list[list[bool]] = deepcopy(self.__data)

    def will_live(self, x: int, y: int)-> bool:
        state = self.__data[x][y]
        n_neighbour = self.count_neighbour(x,y)
        result = False

        if state == True:
            if n_neighbour in [3,2]:
                result = True
        else:
            if n_neighbour in [3]:
                result = True

        return result

    def count_neighbour(self,x,y) -> int:
        n_neighbour = 0

        for collumn in self.__data[x-1:x+2]:
            for case in collumn[y-1:y+2]:
                n_neighbour += case

        n_neighbour -= self.__data[x][y]

        return n_neighbour
    
    def set_map(self, map: str) -> None:
        path = os.path.join(os.path.dirname(__file__), "maps/" + map)
        map_data = load_image(path)
        self.resize(len(map_data),len(map_data[0]))
        self.__data = map_data
        self.__temp_cells = deepcopy(map_data)
    
    def resize(self, width: int, height: int):
        self.__data: list[list[bool]] = [] # valeur de data[x][y] -> état de la case (x, y)

        self.__height = height
        self.__width = width

        for x in range(0, self.__width):
            self.__data.append([])
            for y in range(0, self.__height):
                if (y != 0 and x != 0 and 
                    y != self.__height -1 and x != self.__width -1):

                    state = (random.randint(1, 100) <= 50) 
                    self.__data[x].append(state)
                else:
                    self.__data[x].append(False)
        
        self.__temp_cells = deepcopy(self.__data)
    
    def get_cell_at(self, x: int, y: int) -> bool:
        return self.__data[x][y]


    @property
    def data(self):
        return self.__data    

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width
    

if __name__ == "__main__":
    print(load_image("maps/metatronCube.png"))