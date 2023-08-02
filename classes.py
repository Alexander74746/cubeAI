from config import MapSize, FoodList, NpsList, NewMap, SimulationSpeed, CmdSize
from os import system
from random import randint
from time import time
from colorama import Fore, Back, Style


def clear_console():
    system('cls')


def frame():
    p_map = ''
    for line in NewMap:
        for sym in line:
            match sym:
                case 0:
                    p_map += Fore.GREEN + str(sym) + Style.RESET_ALL
                case 1:
                    p_map += Fore.BLUE + Back.BLUE + str(sym) + Style.RESET_ALL
                case 2:
                    p_map += Fore.RED + Back.RED + str(sym) + Style.RESET_ALL
            p_map += " "
        p_map += "\n"

    lives = ''
    num = 0
    for nps in NpsList:
        num += 1
        if num % 5 == 0:
            lives += '\n'
        lives += (
            f"{Fore.GREEN}N: {Fore.YELLOW + str(nps.Number) + Fore.GREEN}, "
            f"L: {Fore.YELLOW + str(nps.Live) + Style.RESET_ALL}; "
        )

    message = (
        f"{p_map}"
        f"{Fore.CYAN + '-' * CmdSize[0] + Style.RESET_ALL}\n"
        f"{lives}\n"
        f"{Fore.CYAN + '-' * CmdSize[0] + Style.RESET_ALL}\n"
    )

    clear_console()
    print(message)


class Cell:
    def __init__(self, position: list[int, int]) -> None:
        self.PositionX: int = position[0]
        self.PositionY: int = position[1]


class Food(Cell):
    def __init__(self, position: list[int, int], number: int) -> None:
        super().__init__(position)
        self.Number = number

    def re_generating(self):
        while True:
            random_position_x = randint(1, MapSize[0])
            random_position_y = randint(1, MapSize[1])
            if NewMap[random_position_y - 1][random_position_x - 1] == 0:
                NewMap[random_position_y - 1][random_position_x - 1] = 2
                self.PositionX = random_position_x
                self.PositionY = random_position_y
                break


class Nps(Cell):
    def __init__(self, position: list[int, int], number: int) -> None:
        super().__init__(position)
        self.FoodPosition = None
        self.Live = 10
        self.Number = number
        self.MoveTimer = 0

    def activity(self) -> None:
        """Nps live activity function"""
        self.going()
        self.segmentation()
        self.dying()

    def segmentation(self):
        if self.Live >= 25:
            dying = True
            for iteration in range(1, 9):
                random_position_x = randint(self.PositionX - 1, self.PositionX + 1)
                random_position_y = randint(self.PositionY - 1, self.PositionY + 1)
                try:
                    if NewMap[random_position_y - 1][random_position_x - 1] == 0:
                        dying = False
                        number = 1
                        for _ in NpsList:
                            number += 1
                        NpsList.append(Nps([random_position_x, random_position_y], number))
                        break
                except IndexError:
                    pass
            if dying:
                self.dying()

    def dying(self):
        if self.Live <= 0:
            NewMap[self.PositionY - 1][self.PositionX - 1] = 2
            number = 0
            for _ in NpsList:
                number += 1
            number += 1
            for nps in NpsList:
                if nps.Number == self.Number:
                    FoodList.append(Food([self.PositionX, self.PositionY], number))
                    NpsList.remove(nps)

    def _searching_for_food(self) -> list[int, int]:
        radius = 1
        while True:
            for PositionX in range(-radius, radius):
                for PositionY in range(-radius, radius):
                    try:
                        if NewMap[self.PositionY - 2 + PositionY][self.PositionX - 2 + PositionX] == 2:
                            pos_x = self.PositionX - 1 + PositionX
                            pos_y = self.PositionY - 1 + PositionY
                            if pos_x == -1:
                                pos_x = MapSize[0]
                            elif pos_x == MapSize[0] + 1:
                                pos_x = 1
                            if pos_y == -1:
                                pos_y = MapSize[1]
                            elif pos_y == MapSize[1] + 1:
                                pos_y = 1

                            return [pos_x, pos_y]
                    except IndexError:
                        pass
            if radius > MapSize[0]:
                radius = 0
            radius += 1

    def _moving(self, directions: dict[str:bool]) -> None:
        last_position = [self.PositionX, self.PositionY]
        if directions["1"]:
            self.PositionX -= 1
            self.PositionY -= 1
        elif directions["2"]:
            self.PositionY -= 1
        elif directions["3"]:
            self.PositionX += 1
            self.PositionY -= 1
        elif directions["4"]:
            self.PositionX += 1
        elif directions["5"]:
            self.PositionX += 1
            self.PositionY -= 1
        elif directions["6"]:
            self.PositionY += 1
        elif directions["7"]:
            self.PositionX -= 1
            self.PositionY += 1
        elif directions["8"]:
            self.PositionX -= 1

        if self.PositionX == -1:
            self.PositionX = MapSize[0]
        elif self.PositionX == MapSize[0] + 1:
            self.PositionX = 1
        if self.PositionY == -1:
            self.PositionY = MapSize[1]
        elif self.PositionY == MapSize[1] + 1:
            self.PositionY = 1

        if NewMap[self.PositionY - 1][self.PositionX - 1] == 2:
            self.Live += 10
            for food in FoodList:
                if food.PositionX == self.PositionX and food.PositionY == self.PositionY:
                    food.re_generating()
        self.Live -= 1

        NewMap[last_position[1] - 1][last_position[0] - 1] = 0
        NewMap[self.PositionY - 1][self.PositionX - 1] = 1

    def going(self) -> None:
        if time() - self.MoveTimer >= SimulationSpeed:
            self.MoveTimer = time()

            self.FoodPosition = self._searching_for_food()
            direction = {}

            if self.FoodPosition[1] < self.PositionY:
                direction["2"] = True
            elif self.FoodPosition[0] > self.PositionX:
                direction["4"] = True
            if self.FoodPosition[1] > self.PositionY:
                direction["6"] = True
            elif self.FoodPosition[0] < self.PositionX:
                direction["8"] = True

            if '1' not in direction:
                direction['1'] = False
            if '2' not in direction:
                direction['2'] = False
            if '3' not in direction:
                direction['3'] = False
            if '4' not in direction:
                direction['4'] = False
            if '5' not in direction:
                direction['5'] = False
            if '6' not in direction:
                direction['6'] = False
            if '7' not in direction:
                direction['7'] = False
            if '8' not in direction:
                direction['8'] = False

            self._moving(direction)
