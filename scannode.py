import re
import subprocess
import json
import sys

cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^Quality=(?P<signal_level>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<db>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_level>\d+)/(?P<signal_total>\d+).*$"),
]
numCycles = 5

# Runs the comnmand to scan the list of networks.
# Must run as super user.
# Does not specify a particular device, so will scan all network devices.
def scan(interface='wlan0'):
    cmd = ["iwlist", interface, "scan"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    points = proc.stdout.read().decode('utf-8')
    return points


# Parses the response from the command "iwlist scan"
def parse(content):
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            cells.append(cellNumber.groupdict())
            continue
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                cells[-1].update(result.groupdict())
                continue
    return cells


# Create a new dictionary based on mac addresses.
# Each unique address references a signal level and decibel level (db)
# Signal Level and db each reference a list to hold levels from successive runs.
def createDict(cells):
    addressDict = {}
    for line in cells:
        if line['mac'] not in addressDict.keys():
            addressDict[line['mac']] = {'signal_level': [line['signal_level']], 'db':[line['db']]}
    return addressDict


# Mesh the new dictionary with the composite dictionary
def mergeDict(fullCycleDict, newDict):
    for i in newDict:
        if i not in fullCycleDict.keys():
            fullCycleDict[i] = newDict[i]
        else:
            fullCycleDict[i]['signal_level'].append(newDict[i]['signal_level'][0])
            fullCycleDict[i]['db'].append(newDict[i]['db'][0])
    return fullCycleDict


# Run iwlist 5 times to get a baseline average for a new node
# Signal Levels collected into a list in mergeDict
def runCycle():
    fullCycleDict = {}
    for i in range(numCycles):
        newScan = scan()
        newCells = parse(newScan)
        newDict = createDict(newCells)
        if fullCycleDict =={}:
            fullCycleDict = newDict
        else:
            fullCycleDict = mergeDict(fullCycleDict, newDict)
    return fullCycleDict


newNode = runCycle()
filename = sys.argv[1]

with open(filename, 'w') as f:
    json.dump(newNode, f)

#for line in newCells:
#    print(line['mac'])
#    print(line['db'])
