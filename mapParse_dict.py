import os
import json

def averageList(inList):
    sum = 0
    for i in inList:
        sum += int(i)
    return sum / float(len(inList))

roomGrid = {}

for filename in os.listdir(os.getcwd()):
    if filename == '.directory':
        continue

    with open(filename,encoding="utf-8") as f:
        data = eval(f.read())
        roomGrid[filename]= data

macList = {}

for tile in roomGrid:
    for mac in roomGrid[tile]:
        if mac not in macList:
            macList[mac] = {}
        macList[mac][tile] = roomGrid[tile][mac]
                    
        macList[mac][tile]['averageDB'] = averageList(macList[mac][tile]['db'])
        macList[mac][tile]['averageSig'] = averageList(macList[mac][tile]['signal_level'])
        if macList[mac][tile]['averageSig'] < 25:
            macList[mac][tile]['averageSig'] = 0


#splitArray = []        
#for key in macList:
    #newGrid = [[0 for x in range(19)] for y in range(34)] 

    #for tile in macList[key]:
        #row,col = tile.split('-')
        #print(row)
        #if(row.find('H') != -1):
            #H, row = row.split('H')
        #print(row)
        #row = int(row)
        #col = int(col)
        #newGrid[row][col] = macList[key][tile]['db'][0]
    #splitArray.append(newGrid)

#for col in splitArray[2]:
    #print(col)

path = '/home/sean/srp/outputMacList'
with open(path, 'w', encoding="utf-8") as f:
    f.write(json.dumps(macList))

