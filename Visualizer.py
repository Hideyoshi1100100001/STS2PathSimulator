import cv2
import numpy as np
import math
import json

mapLength = 15

icons = [
    cv2.imread("./icons/Monster.png", cv2.IMREAD_UNCHANGED), #0 Monster
    cv2.imread("./icons/Unknown.png", cv2.IMREAD_UNCHANGED), #1 Unknown
    cv2.imread("./icons/Rest.png", cv2.IMREAD_UNCHANGED), #2 Rest
    cv2.imread("./icons/Shop.png", cv2.IMREAD_UNCHANGED), #3 Shop
    cv2.imread("./icons/Treasure.png", cv2.IMREAD_UNCHANGED), #4 Treasure
    cv2.imread("./icons/Elite.png", cv2.IMREAD_UNCHANGED), #5 Elite
]

def upsideDown(row: int, column: int):
    return mapLength - 1 - row, column

def setIcon(image, row: int, column: int, type: int):
    row, column = upsideDown(row, column)
    icon = icons[type]
    image[row * 100 + 50 - math.floor(icon.shape[0] / 2): row * 100 + 50 + math.ceil(icon.shape[0] / 2),
          column * 100 + 50 - math.floor(icon.shape[1] / 2): column * 100 + 50 + math.ceil(icon.shape[1] / 2)] = icon[:, :]

def connect(image, point0, point1):
    row0, column0 = upsideDown(point0[0], point0[1])
    row1, column1 = upsideDown(point1[0], point1[1])
    cv2.line(image, (column0 * 100 + 50, row0 * 100 + 50), (column1 * 100 + 50, row1 * 100 + 50), (90, 66, 55, 255), 5)

def VisualizeMap():
    image = np.zeros((1500, 700, 4), dtype=np.uint8)
    with open("Maps.json", "r") as file:
        data = json.load(file)
    map = data[1827]
    visited = [False for _ in range(len(map))]
    queue, queue1 = [map[0]], []
    while len(queue) > 0:
        while len(queue) > 0:
            point = queue.pop(0)
            for child in point["children"]:
                connect(image, (point["row"], point["column"]), (map[child]["row"], map[child]["column"]))
                if not visited[child]:
                    queue1.append(map[child])
                    visited[child] = True
            setIcon(image, point["row"], point["column"], 0)
        queue, queue1 = queue1, queue
    cv2.imshow("Map", image)
    cv2.imwrite("Map.png", image)
    cv2.waitKey(0)

def VisualizeAssignedMap():
    image = np.zeros((1500, 700, 4), dtype=np.uint8)
    with open("AssignedMaps.json", "r") as file:
        data = json.load(file)
    map = data[0]
    visited = [False for _ in range(len(map))]
    queue, queue1 = [map[0]], []
    while len(queue) > 0:
        while len(queue) > 0:
            point = queue.pop(0)
            for child in point["children"]:
                connect(image, (point["row"], point["column"]), (map[child]["row"], map[child]["column"]))
                if not visited[child]:
                    queue1.append(map[child])
                    visited[child] = True
            setIcon(image, point["row"], point["column"], point["type"])
        queue, queue1 = queue1, queue
    cv2.imshow("AssignedMap", image)
    cv2.imwrite("AssignedMap.png", image)
    cv2.waitKey(0)

VisualizeMap()
#VisualizeAssignedMap()