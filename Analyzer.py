import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from functools import cmp_to_key

forges = 2

def writeLog(line, log):
    print(line)
    log.write(line+"\n")
    log.flush()

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

def realistic(path, path1):
    info = infoFromPath(path)
    info1 = infoFromPath(path1)
    
    ## At least 1 shop
    if info[3] != info1[3]:
        if min(info[3], info1[3]) < 1:
            return info[3] - info1[3]
    
    ## No elite before the first rest place
    cnt, cnt1 = 0, 0
    mCnt, mCnt1 = 0, 0
    for type in path:
        if type == 2:
            break
        if type == 5:
            cnt += 1
        if type == 0:
            mCnt += 1
    for type1 in path1:
        if type == 2:
            break
        if type1 == 5:
            cnt1 += 1
        if type == 0:
            mCnt1 += 1
    if cnt != cnt1:
        return cnt1 - cnt
    
    ## Most rest place

    if info[2] != info1[2]:
        return info[2] - info1[2]
    
    ## Least monster before the first rest place

    if mCnt != mCnt1:
        return mCnt1 - mCnt
    
    ## Most shop

    if info[3] != info1[3]:
        return info[3] - info1[3]

    ## Least monster

    if info[0] != info1[0]:
        return info1[0] - info[0]

def realisticNoShop(path, path1):
    info = infoFromPath(path)
    info1 = infoFromPath(path1)
    
    ## No elite before the first rest place
    cnt, cnt1 = 0, 0
    mCnt, mCnt1 = 0, 0
    for type in path:
        if type == 2:
            break
        if type == 5:
            cnt += 1
        if type == 0:
            mCnt += 1
    for type1 in path1:
        if type == 2:
            break
        if type1 == 5:
            cnt1 += 1
        if type == 0:
            mCnt1 += 1
    if cnt != cnt1:
        return cnt1 - cnt
    
    ## Most rest place

    if info[2] != info1[2]:
        return info[2] - info1[2]
    
    ## Least monster before the first rest place

    if mCnt != mCnt1:
        return mCnt1 - mCnt
    
    ## Most shop

    if info[3] != info1[3]:
        return info[3] - info1[3]

    ## Least monster

    if info[0] != info1[0]:
        return info1[0] - info[0]

def getMostRestAtLeastOneShop(allPaths):
    pass

with open("AssignedMaps.json", "r") as file:
    data = json.load(file)

log = open("log.txt","w")
log.flush()

pathData = {
    "Rests": [],
    "Shops": [],
    "Monsters": [],
    "Elites": [],
    "Unknowns": [],
    "NormalMonstersBeforeFirstRest": [],
    "ElitesBeforeFirstRest": [],
    "HpLossPerMonster": []
}

with tqdm(total=len(data)) as pbar:
    pbar.set_description("Analyzing maps")
    for map in data:
        allPaths = getAllPossiblePaths(map)
        path = max(allPaths, key=cmp_to_key(realistic))
        typeNum = infoFromPath(path)
        pathData["Monsters"].append(typeNum[0])
        pathData["Unknowns"].append(typeNum[1])
        pathData["Rests"].append(typeNum[2])
        pathData["Shops"].append(typeNum[3])
        pathData["Elites"].append(typeNum[4])

        NMBFR = 0
        EBFR = 0
        for type in path:
            if type == 2:
                break
            if type == 0:
                NMBFR += 1
            if type == 5:
                EBFR += 1
        NMBFR = max(0, NMBFR - 3)
        pathData["NormalMonstersBeforeFirstRest"].append(NMBFR)
        pathData["ElitesBeforeFirstRest"].append(EBFR)

        pathData["HpLossPerMonster"].append(min(20, (26 + 21 * max(0, typeNum[2] - forges)) / (max(0.001, typeNum[0] - 3) + typeNum[4] * 2)))

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
    mean = 0
    if i == 0:
        line = "Monsters\t"
    elif i == 1:
        line = "Unknowns\t"
    elif i == 2:
        line = "Rests\t"
    elif i == 3:
        line = "Shops\t"
    elif i == 4:
        line = "Elites\t"
    for j in range(nums.shape[1]):
        line += "{:.3f}\t".format(nums[i, j])
        mean += j * nums[i, j]
    writeLog(line, log)
    line = "mean\t{:.3f}".format(mean)
    writeLog(line, log)

x = np.linspace(0, maxNum, maxNum + 1)
plt.plot(x, nums[0], color=(0.5, 0, 0), marker='o', label="Monsters")
plt.plot(x, nums[1], color=(0, 0, 0), marker='o', label="Unknowns")
plt.plot(x, nums[2], color=(0.5, 0, 0.5), marker='o', label="Rests")
plt.plot(x, nums[3], color=(0.5, 0.5, 0), marker='o', label="Shops")
plt.plot(x, nums[4], color=(1, 0, 0), marker='o', label="Elites")
plt.title("Realistic Path Type Distributions")
plt.xlabel("Number")
plt.ylabel("Probability")
plt.legend()
plt.savefig("fig.png")
plt.clf()

maxNum = max(max(pathData["NormalMonstersBeforeFirstRest"]), max(pathData["ElitesBeforeFirstRest"]))
y = np.zeros((2, maxNum + 1))
for num in pathData["NormalMonstersBeforeFirstRest"]:
    y[0, num] += 1
for num in pathData["ElitesBeforeFirstRest"]:
    y[1, num] += 1

writeLog("Before First Rest", log)
for i in range(y.shape[0]):
    y[i] /= np.sum(y[i])
    mean = 0
    if i == 0:
        line = "Monsters\t"
    elif i == 1:
        line = "Elites\t"
    for j in range(y.shape[1]):
        line += "{:.3f}\t".format(y[i, j])
        mean += j * y[i, j]
    writeLog(line, log)
    line = "mean\t{:.3f}".format(mean)
    writeLog(line, log)

x = np.array(list(range(maxNum + 1)))
plt.plot(x, y[0], color=(0.5, 0, 0), marker='o', label="Monsters")
plt.plot(x, y[1], color=(1, 0, 0), marker='o', label="Elites")
plt.title("Monster Distribution Before First Rest")
plt.xlabel("Number")
plt.ylabel("Probability")
plt.legend()
plt.savefig("fig1.png")
plt.clf()

binSize = 0.5

monsters = np.maximum(0, np.array(pathData["Monsters"]) - 3 + 2 * np.array(pathData["Elites"]))
rests = np.maximum(0.001, np.array(pathData["Rests"]) - forges)
ratio = np.minimum(10, monsters / rests)
maxNum = int(np.ceil(max(ratio) / binSize))
y = np.zeros(maxNum + 1)
for num in ratio:
    y[int(np.floor(num / binSize))] += 1
y /= np.sum(y)
mean = 0
writeLog("Monster / Rest", log)
for i in range(y.shape[0]):
    writeLog("{:.1f}\t{:.3f}".format(i * binSize, y[i]), log)
    mean += i * binSize * y[i]
writeLog("mean\t{:.3f}".format(mean), log)

x = np.array([i * binSize for i in range(y.shape[0])])
plt.plot(x, y, color=(0.5, 0, 0), marker='o')
plt.title("Monster / Rest")
plt.xlabel("Number")
plt.ylabel("Probability")
plt.savefig("fig2.png")
plt.clf()

maxNum = 20
y = np.zeros(maxNum + 1)
for num in pathData["HpLossPerMonster"]:
    y[int(np.floor(num))] += 1
y /= np.sum(y)
mean = 0
writeLog("Hp Loss per Monster", log)
for i in range(y.shape[0]):
    writeLog("{}\t{:.3f}".format(i, y[i]), log)
    mean += i * y[i]
writeLog("mean\t{:.3f}".format(mean), log)

x = np.array(list(range(maxNum + 1)))
plt.plot(x[:-1], y[:-1], color=(1, 0, 0), marker='o')
plt.title("Hp Loss Per Monster")
plt.xlabel("Number")
plt.ylabel("Probability")
plt.savefig("fig3.png")
plt.show()