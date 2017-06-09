import re
import subprocess
import json
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
# Each unique address references a signal level.
# For redudancy/future proofing, signal level is list of signal and db
def createDict(cells):
    addressDict = {}
    for line in cells:
        if line['mac'] not in addressDict.keys():
            addressDict[line['mac']] = [line['signal_level'], line['db']]
    return addressDict


# Run iwlist 5 times to get a baseline average for a new node
def runCycle():
    fullCycleList = []
    for i in range(numCycles):
        newScan = scan()
        newCells = parse(newScan)
        fullCycleList.append(createDict(newCells))
    return fullCycleList

#newScan = scan()
#ewNode = parse(newScan)




newNode = runCycle()
#print(type(newNode))

with open('test.json', 'w') as f:
    json.dump(newNode, f)

#for line in newCells:
#    print(line['mac'])
#    print(line['db'])
