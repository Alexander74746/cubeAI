from config import Map, MapSize
from classes import Nps

NpsList = []

if __name__ == "__main__":
    for PositionY in range(MapSize[1]):
        for PositionX in range(MapSize[0]):
            if Map[PositionY][PositionX] == 1:
                NpsList.append(Nps([PositionX + 1, PositionY + 1]))
