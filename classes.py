import sys
from random import randint
from time import time
from config import MapSize, FoodList, NewMap


class Cell:
    def __init__(self, position: list[int, int]) -> None:
        self.PositionX = position[0]
        self.PositionY = position[1]


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
        self.FoodNumber = None
        self.Live = 10
        self.Number = number
        self.MoveTimer = 0

    def moving(self, directions: dict[str:bool]) -> None:
        if '1' not in directions:
            directions['1'] = False
        if '2' not in directions:
            directions['2'] = False
        if '3' not in directions:
            directions['3'] = False
        if '4' not in directions:
            directions['4'] = False
        if '5' not in directions:
            directions['5'] = False
        if '6' not in directions:
            directions['6'] = False
        if '7' not in directions:
            directions['7'] = False
        if '8' not in directions:
            directions['8'] = False

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
        self.Live -= 1

        if NewMap[self.PositionY - 1][self.PositionX - 1] == 2:
            self.Live += 10
            for food in FoodList:
                if food.Number == self.FoodNumber:
                    food.re_generating()
        if self.Live <= 0:
            sys.exit(0)
        NewMap[last_position[1] - 1][last_position[0] - 1] = 0
        NewMap[self.PositionY - 1][self.PositionX - 1] = 1

    @staticmethod
    def searching_for_food() -> list[int, int]:
        radius = 1
        while True:
            for PositionY in range(radius):
                for PositionX in range(radius):
                    if NewMap[PositionY][PositionX] == 2:
                        return [PositionX + 1, PositionY + 1]
            radius += 1

    def going(self) -> None:
        if time() - self.MoveTimer >= 1:
            self.MoveTimer = time()
            self.FoodPosition = self.searching_for_food()
            for food in FoodList:
                if food.PositionX == self.FoodPosition[0] and food.PositionY == self.FoodPosition[1]:
                    self.FoodNumber = food.Number

            direction = {}
            for StepX in range(abs(self.PositionX - self.FoodPosition[0])):
                if self.FoodPosition[0] < self.PositionX:
                    direction["8"] = True
                elif self.FoodPosition[0] > self.PositionX:
                    direction["4"] = True
                else:
                    continue
            for StepY in range(abs(self.PositionY - self.FoodPosition[1])):
                if self.FoodPosition[1] < self.PositionY:
                    direction["2"] = True
                elif self.FoodPosition[1] > self.PositionY:
                    direction["6"] = True
                else:
                    continue
            self.moving(direction)
            print(f"----------\n"
                  f"go №{self.Number}, lives:{self.Live}\n"
                  f"----------\n"
                  f"{str(NewMap[0])}\n"
                  f"{str(NewMap[1])}\n"
                  f"{str(NewMap[2])}\n"
                  f"{str(NewMap[3])}\n"
                  f"{str(NewMap[4])}\n"
                  f"----------")
