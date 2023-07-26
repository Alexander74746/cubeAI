class Cell:
    def __init__(self, position: list[int, int]) -> None:
        self.PositionX = position[0]
        self.PositionY = position[1]


class Nps(Cell):
    def __init__(self, position: list[int, int]) -> None:
        super().__init__(position)
        self.Live = 10

    def moving(self, directions: dict[1:bool, 2:bool, 3:bool, 4:bool, 5:bool, 6:bool, 7:bool, 8:bool]) -> None:
        if directions[0]:
            self.PositionX -= 1
            self.PositionY -= 1
        elif directions[1]:
            self.PositionY -= 1
        elif directions[2]:
            self.PositionX += 1
            self.PositionY -= 1
        elif directions[3]:
            self.PositionX += 1
        elif directions[4]:
            self.PositionX += 1
            self.PositionY -= 1
        elif directions[5]:
            self.PositionY += 1
        elif directions[6]:
            self.PositionX -= 1
            self.PositionY += 1
        elif directions[7]:
            self.PositionX -= 1

    @staticmethod
    def searching_for_food(world_map: list):
        radius = 1
        while True:
            for PositionY in range(radius):
                for PositionX in range(radius):
                    try:
                        if world_map[PositionY][PositionX] == 2:
                            return [PositionX + 1, PositionY + 1]
                    except IndexError:
                        return None
            else:
                radius += 1

