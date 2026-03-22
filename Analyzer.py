import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from functools import cmp_to_key

def getAllPossiblePaths(map):
    res = []
    queue, queue1 = [(map[0], [])], []
    while len(queue) > 0:
        while len(queue) > 0:
            point, path = queue.pop(0)
            path.append(point.get("type", -1))
            if len(point["children"]) > 0:
                for child in point["children"]:
                    queue1.append((map[child], path.copy()))
            else:
                path.pop(0)
                res.append(path)
        queue, queue1 = queue1, queue
    
    return res

def infoFromPath(path):
    res = [0, 0, 0, 0, 0] ## Monster, Unknown, Rest, Shop, Elite
    for type in path:
        if type == 4:
            continue
        elif type == 5:
            res[4] += 1
        else:
            res[type] += 1
    return res

def naiveBestPath(path, path1):
    path = infoFromPath(path)
    path1 = infoFromPath(path1)
    if path[2] != path1[2]:
        return path[2] - path1[2]
    if path[3] != path1[3]:
        return path[3] - path1[3]
    if path[4] != path1[4]:
        return path1[4] - path[4]
    if path[0] != path1[0]:
        return path1[0] - path[0]
    return 0

def leastElite(path, path1):
    path = infoFromPath(path)
    path1 = infoFromPath(path1)
    if path[4] != path1[4]:
        return path1[4] - path[4]
    if path[2] != path1[2]:
        return path[2] - path1[2]
    if path[3] != path1[3]:
        return path[3] - path1[3]
    if path[0] != path1[0]:
        return path1[0] - path[0]
    return 0

def getMostRestAtLeastOneShop(allPaths):
    pass

with open("AssignedMaps.json", "r") as file:
    data = json.load(file)

pathData = {
    "Rests": [],
    "Shops": [],
    "Monsters": [],
    "Elites": [],
    "Unknowns": [],

}

with tqdm(total=len(data)) as pbar:
    pbar.set_description("Analyzing maps")
    for map in data:
        allPaths = getAllPossiblePaths(map)
        path = max(allPaths, key=cmp_to_key(leastElite))
        typeNum = infoFromPath(path)
        pathData["Monsters"].append(typeNum[0])
        pathData["Unknowns"].append(typeNum[1])
        pathData["Rests"].append(typeNum[2])
        pathData["Shops"].append(typeNum[3])
        pathData["Elites"].append(typeNum[4])
        pbar.update(1)

maxNum = max(max(pathData["Rests"]), max(pathData["Shops"]), max(pathData["Monsters"]), max(pathData["Elites"]), max(pathData["Unknowns"]))
nums = np.zeros((5, maxNum + 1))
for num in pathData["Monsters"]:
    nums[0][num] += 1
for num in pathData["Unknowns"]:
    nums[1][num] += 1
for num in pathData["Rests"]:
    nums[2][num] += 1
for num in pathData["Shops"]:
    nums[3][num] += 1
for num in pathData["Elites"]:
    nums[4][num] += 1
for i in range(nums.shape[0]):
    nums[i] /= np.sum(nums[i])

x = np.linspace(0, maxNum, maxNum + 1)
plt.plot(x, nums[0], color=(0.5, 0, 0), marker='o', label="Monsters")
plt.plot(x, nums[1], color=(0, 0, 0), marker='o', label="Unknowns")
plt.plot(x, nums[2], color=(0.5, 0, 0.5), marker='o', label="Rests")
plt.plot(x, nums[3], color=(0.5, 0.5, 0), marker='o', label="Shops")
plt.plot(x, nums[4], color=(1, 0, 0), marker='o', label="Elites")
plt.title("Least Elite Path Type Distributions")
plt.xlabel("Number")
plt.ylabel("Probability")
plt.legend()
plt.savefig("fig.png")
plt.show()