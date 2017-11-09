import os
import json
#import math

def compareToMaster(masterList, newNode, allTiles):
    compareDict = {}
    for mac in masterList:
        compareDict[mac] = {}
        for tile in allTiles:
            compareDict[mac][tile] = {}
            #compareDict[mac][tile]['totalVariance'] = 0
            if mac in newNode.keys():
                compareDict[mac][tile]['scan'] = abs(int(newNode[mac]['signal_level'][0]))
               # if compareDict[mac][tile]['scan'] < 30:
                   # compareDict[mac][tile]['scan'] = 0                   
            else: 
                compareDict[mac][tile]['scan']= 0
                
            if tile in masterList[mac].keys():
                compareDict[mac][tile]['saved'] = abs(masterList[mac][tile]['averageSig'])
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
    for i in range(5):
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
with open('14-12',encoding="utf-8") as f:
    data = eval(f.read())
    node = data
    
compared = compareToMaster(savedData, node, tileList)
for key in compared:
    print(compared[key]['13-12'])

summed = calculateLikelyTiles(compared)
five = getBestFive(summed)
print(five)

#for key in compared:
    #if '1-1' in compared[key].keys():
        #print(compared[key]['1-1']['variance'])
