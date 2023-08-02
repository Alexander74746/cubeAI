from config import StartMap, MapSize, FoodList, NpsList, SimulationSpeed
from classes import Nps, Food, frame
from time import time

if __name__ == "__main__":
    NpsNumber = 1
    for PositionY in range(MapSize[1]):
        for PositionX in range(MapSize[0]):
            if StartMap[PositionY][PositionX] == 1:
                NpsList.append(Nps([PositionX + 1, PositionY + 1], NpsNumber))
                NpsNumber += 1
    FoodNumber = 1
    for PositionY in range(MapSize[1]):
        for PositionX in range(MapSize[0]):
            if StartMap[PositionY][PositionX] == 2:
                FoodList.append(Food([PositionX + 1, PositionY + 1], FoodNumber))
                FoodNumber += 1

    frame()
    FrameTimer = time()
    RunFlag = True
    while RunFlag:
        if time() - FrameTimer >= SimulationSpeed:
            FrameTimer = time()
            for Nps in NpsList:
                Nps.activity()
            frame()
            if not NpsList:
                print("Restart the program, please.")
                i = input()
                RunFlag = False
