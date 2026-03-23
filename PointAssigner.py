import json
from tqdm import tqdm
import random
import math

random.seed()

mapLength = 15
mapWidth = 7
ascension1 = True
ascension6 = True
lessUnknowns = False

def GaussianInt(mean: int, stdDev: int, min: int, max: int):
    while True:
        d = 1 - random.random()
        num = 1 - random.random()
        num2 = math.sqrt(-2 * math.log(d)) * math.sin(math.pi * 2 * num)
        a = mean + stdDev * num2
        num3 = round(a)
        if num3 >= min and num3 <= max:
            return num3

def getNumOfRests():
    res = GaussianInt(7, 1, 6, 7)
    if ascension6:
        res -= 1
    return res

def getNumOfShops():
    return 3

def getNumOfElites():
    if ascension1:
        return 8
    else:
        return 5

def getNumOfUnknowns():
    res = GaussianInt(12, 1, 10, 14)
    if lessUnknowns:
        res -= 1
    return res

def validPointType(map, assigned: dict, point, type, pIndex) -> bool:
    if point["row"] >= mapLength - 3:
        if type in [2]:
            return False
    if point["row"] < 5:
        if type in [2, 5]:
            return False
    if type in [2, 3, 4, 5]:
        for parent in point["parent"]:
            if assigned.get((map[parent]["row"], map[parent]["column"]), -1) == type:
                return False
        for child in point["children"]:
            if assigned.get((map[child]["row"], map[child]["column"]), -1) == type:
                return False
    if type in [0, 1, 2, 3, 5]:
        for parent in point["parent"]:
            for child in map[parent]["children"]:
                if child == pIndex:
                    continue
                if assigned.get((map[child]["row"], map[child]["column"]), -1) == type:
                    return False
    return True

def assign(map):
    grid = {}
    assigned = {}
    for point in map:
        grid[(point["row"], point["column"])] = point
    for i in range(mapWidth):
        if (mapLength - 1, i) in grid.keys():
            assigned[(mapLength - 1, i)] = 2
        if (mapLength - 7, i) in grid.keys():
            assigned[(mapLength - 7, i)] = 4
        if (1, i) in grid.keys():
            assigned[(1, i)] = 0
    
    pointTypes = []
    for _ in range(getNumOfRests()):
        pointTypes.append(2)
    for _ in range(getNumOfShops()):
        pointTypes.append(3)
    for _ in range(getNumOfElites()):
        pointTypes.append(5)
    for _ in range(getNumOfUnknowns()):
        pointTypes.append(1)
    random.shuffle(pointTypes)

    
    tempList = list(range(len(map)))
    random.shuffle(tempList)
    while len(pointTypes) > 0:
        pIndex = tempList[0]
        point = map[pIndex]
        while assigned.__contains__((point["row"], point["column"])):
            tempList.pop(0)
            if len(tempList) == 0:
                return False, _
            pIndex = tempList[0]
            point = map[pIndex]
        index = 0
        while index < len(pointTypes) and not validPointType(map, assigned, point, pointTypes[index], pIndex):
            index += 1
        if index < len(pointTypes):
            assigned[(point["row"], point["column"])] = pointTypes[index]
            pointTypes.pop(index)
            tempList = list(range(len(map)))
            random.shuffle(tempList)
        else:
            tempList.pop(0)
        if len(tempList) == 0:
            return False, _
    return True, assigned

with open("Maps.json", "r") as file:
    data = json.load(file)

debugIndex = 0
with tqdm(total=len(data)) as pbar:
    pbar.set_description("Assigning points")
    assignedData = []
    for map in data:
        succeed = False
        while not succeed:
            succeed, assigned = assign(map)
        
        for point in map:
            point["type"] = assigned.get((point["row"], point["column"]), 0)
        assignedData.append(map)
        pbar.update(1)
        debugIndex += 1
        pbar.refresh()


with open("AssignedMaps.json", "w") as file:
    json.dump(assignedData, file, indent=4)