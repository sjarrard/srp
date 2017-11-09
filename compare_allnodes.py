import os
import json
#import math

def getAverage(newList):
    sum = 0
    l = len(newList)
    if l == 0:
        return 0
    for i in newList:
        sum += int(i)
        if i == 0:
            l-=1
    return sum/l


def compareToMaster(masterList, newNode, allTiles):
    compareDict = {}
    for mac in masterList:
        compareDict[mac] = {}
        for tile in allTiles:
            compareDict[mac][tile] = {}
            #compareDict[mac][tile]['totalVariance'] = 0
            if mac in newNode.keys():
                
                compareDict[mac][tile]['scan'] = getAverage(newNode[mac]['signal_level'])
                if compareDict[mac][tile]['scan'] < 25:
                    compareDict[mac][tile]['scan'] = 0            
            else: 
                compareDict[mac][tile]['scan']= 0
                
            if tile in masterList[mac].keys():
                compareDict[mac][tile]['saved'] = masterList[mac][tile]['averageSig']
            else:
                compareDict[mac][tile]['saved'] = 0
            
            compareDict[mac][tile]['variance'] = abs(compareDict[mac][tile]['scan']-compareDict[mac][tile]['saved'])
            #compareDict[mac][tile]['totalVariance'] +=compareDict[mac][tile]['variance']
            #compareDict[mac][tile]['difference'] = abs(compareDict[mac]['scan']-compareDict[mac]['difference'])
    return compareDict

def calculateLikelyTiles(compareDict):
    sumDict = {}
    for key in compareDict:
        for tile in compareDict[key]:
            if tile not in sumDict.keys():
                sumDict[tile] = compareDict[key][tile]['variance']
            else:
                sumDict[tile] += compareDict[key][tile]['variance']
    return sumDict

def getBestFive(newDict):
    bestFive = []
    for i in range(7):
        min = 9999999.0
        minTile = ''
        for tile in newDict:
            if newDict[tile] < min:
                min = newDict[tile]
                minTile = tile
        bestFive.append(minTile)
        #print(minTile)
        del newDict[minTile]
    return bestFive
        

path = '/home/sean/srp/outputMacList'
with open(path, encoding="utf-8") as f:
    jsonData = f.read()
    savedData = json.loads(jsonData)
    
tileList = []
for key in savedData:
    for tile in savedData[key].keys():
        if tile not in tileList:
            tileList.append(tile)
#print(tileList)
roomGrid = {}
for filename in os.listdir(os.getcwd()):
    if filename == '.directory':
        continue

    with open(filename,encoding="utf-8") as f:
        data = eval(f.read())
        roomGrid[filename]= data

for tile in roomGrid:
    compared = compareToMaster(savedData, roomGrid[tile], tileList)
    summed = calculateLikelyTiles(compared)
    five = getBestFive(summed)
    print(tile, five)
    break
#for key in compared:
    #print(compared[key]['1-1']['variance'])


#print(five)

#for key in compared:
    #if '1-1' in compared[key].keys():
        #print(compared[key]['1-1']['variance'])
