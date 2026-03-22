import json
import random
from tqdm import tqdm

random.seed()

## Parameters

## The length of the map. 15 for Act 1, 14 for Act 2, 13 for Act3. If multiplayer, -1.
mapLength: int = 15
## The width of the map. Fixed 7.
mapWidth: int = 7
## How many maps to generate
maps: int = 10000

class Point:
    def __init__(self, row: int, column: int, parent):
        self.row = row
        self.column = column
        self.children = []
        self.parent = [parent]

## Core.Map.StandardActMap.GenerateMap
def GenerateMap():
    grid = [[None for _ in range(mapWidth)] for _ in range(mapLength)]
    root = Point(0, mapWidth // 2, None)
    grid[0][mapWidth // 2] = root
    for i in range(mapWidth):
        getOrCreatePointColumn: int = random.randint(0, 6)
        if i == 1:
            while (grid[1][getOrCreatePointColumn] != None):
                getOrCreatePointColumn = random.randint(0, 6)
        if grid[1][getOrCreatePointColumn] is None:
            grid[1][getOrCreatePointColumn] = Point(1, getOrCreatePointColumn, root)
            root.children.append(grid[1][getOrCreatePointColumn])
        PathGenerate(grid, 1, getOrCreatePointColumn)
    return grid, root

## Core.Map.StandardActMap.PathGenerate
def PathGenerate(grid, pRow, pColumn):
    if pRow < mapLength - 1:
        coordList = [max(0, pColumn - 1), pColumn, min(mapWidth - 1, pColumn + 1)]
        random.shuffle(coordList)
        for column in coordList:
            crossoverCheck: bool = True
            if column != pColumn and grid[pRow][column] is not None:
                for child in grid[pRow][column].children:
                    if child.column == pColumn:
                        crossoverCheck = False
                        break
            if not crossoverCheck:
                continue
            if grid[pRow + 1][column] is None:
                grid[pRow + 1][column] = Point(pRow + 1, column, grid[pRow][pColumn])
            else:
                if grid[pRow][pColumn] not in grid[pRow + 1][column].parent:
                    grid[pRow + 1][column].parent.append(grid[pRow][pColumn])
            if grid[pRow + 1][column] not in grid[pRow][pColumn].children:
                grid[pRow][pColumn].children.append(grid[pRow + 1][column])
            PathGenerate(grid, pRow + 1, column)
            return

if 0:
    with open("Maps.json", "r") as file:
        data = json.load(file)
else:
    data = []

with tqdm(total=maps) as pbar:
    pbar.set_description("Generating maps")
    for _ in range(maps):
        grid, root = GenerateMap()
        mapArray = [{
            "row": root.row,
            "column": root.column,
            "parent": [],
            "children": []
        }]
        visited = [[-1 for _ in range(mapWidth)] for _ in range(mapLength)]
        visited[root.row][root.column] = 0
        queue = [(root, 0)]
        queue1 = []
        while len(queue) > 0:
            while len(queue) > 0:
                point, pointId = queue.pop(0)
                for child in point.children:
                    if visited[child.row][child.column] < 0:
                        visited[child.row][child.column] = len(mapArray)
                        queue1.append((child, len(mapArray)))
                        mapArray.append({
                            "row": child.row,
                            "column": child.column,
                            "parent": [pointId],
                            "children": []
                        })
                    else:
                        mapArray[visited[child.row][child.column]]["parent"].append(pointId)
                    mapArray[pointId]["children"].append(visited[child.row][child.column])
            queue, queue1 = queue1, queue
        data.append(mapArray)
        pbar.update(1)

with open("Maps.json", "w") as file:
    json.dump(data, file, indent=4)