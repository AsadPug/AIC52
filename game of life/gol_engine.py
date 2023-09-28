import os
from copy import deepcopy

from PIL import Image

import numpy as np

def load_image(path: str) -> np.ndarray:
    image = Image.open(path, 'r')
    raw_data = list(image.getdata())
    data: np.ndarray = np.zeros(image.size).flatten()
    for x in range(0, image.width * image.height):
        if raw_data[x][3] > 50:
            data[x] = 1
            
    return data.reshape(image.size)

class GOLEngine():
    def __init__(self, size: tuple[int, int]) -> None:
        self.__size : tuple[int, int] = size
        self.data = np.zeros(size)
        self.fill_data()

        self.n_cells_alive = 0
        self.n_cells_dead = 0

    def resize_data(self, size: tuple[int, int]) -> None:
        self.data = np.zeros(size)
        self.__size = size

    def fill_data(self, percent: float = 0.5) -> None:
        self.data[1:-1,1:-1] = np.random.choice(
            (1, 0), (self.__size[0]-2,self.__size[1] - 2), p=(percent, 1-percent)
        )

    def tick(self) -> None:
        r, c = np.meshgrid(np.arange(1, self.__size[1]-1), np.arange(1, self.__size[0]-1))
        n_neighbour = (
            self.data[c-1,r] + self.data[c-1,r-1] + self.data[c,r-1] +
            self.data[c+1,r] + self.data[c+1,r+1] + self.data[c,r+1] +
            self.data[c+1,r-1] + self.data[c-1,r+1]
        )
        n_neighbour_border = np.zeros(self.__size)
        n_neighbour_border[1:self.__size[0]-1,1:self.__size[1]-1] = n_neighbour

        self.data = self.data.astype(np.uint8)
        self.data &= n_neighbour_border == 2
        self.data |= n_neighbour_border == 3

        self.n_cells_alive = np.count_nonzero(self.data)
        self.n_cells_dead = self.__size[0] * self.__size[1] -self.n_cells_alive

    def set_map(self, map: str) -> None:
        path = os.path.join(os.path.dirname(__file__), "maps/" + map)
        map_data = load_image(path)
        self.resize_data(map_data.shape)
        self.data = map_data

    def get_cell_at(self, x: int, y: int) -> bool:
        return self.data[x, y]
    
    

    @property
    def width(self):
        return self.__size[0]
    
    @property
    def height(self):
        return self.__size[1]


def main() -> None:
    engine = GOLEngine((5, 5))
    print(engine.data)
    engine.tick1()
    
    


if __name__ == "__main__":
    main()


