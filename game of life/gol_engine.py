from PIL import Image

import numpy as np

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

class GOLEngine():
    def __init__(self, size: tuple[int,int]) -> None:
        self.__size : tuple[int, int] = size
        self.data = np.zeros(size)
        self.fill_data()

        self.n_cells_alive = 0
        self.n_cells_dead = 0

    def fill_data(self, percent: float = 0.5) -> None:
        self.data[:] = np.random.choice((1, 0), self.__size, p=(percent, 1-percent))
        self.data[[0,-1],:] = 0
        self.data[1:-1,[0,-1]] = 0

    def print(self) -> None:
        print(self.data)

    def tick(self) -> None:
        r, c = np.meshgrid(np.arange(self.__size[1]-1), np.arange(self.__size[0]-1))
        r = r[1:self.__size[0],1:self.__size[1]]
        c = c[1:self.__size[0],1:self.__size[1]]
        n_neighbour = self.data[c-1,r] + self.data[c-1,r-1] + self.data[c,r-1] + self.data[c+1,r] + self.data[c+1,r+1] + self.data[c,r+1] + self.data[c+1,r-1] + self.data[c-1,r+1]
        n_neighbour_border = np.zeros(self.__size)
        n_neighbour_border[1:self.__size[0]-1,1:self.__size[1]-1] = n_neighbour

        self.data = self.data.astype(np.int8)
        self.data &= n_neighbour_border == 2
        self.data |= n_neighbour_border == 3
        pass

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
    engine.print()
    engine.tick()
    engine.tick()
    


if __name__ == "__main__":
    main()


