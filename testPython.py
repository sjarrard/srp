import subprocess
import shlex
import re

cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<essid>.+)\"$"),
    re.compile(r"^Protocol:(?P<protocol>.+)$"),
    re.compile(r"^Mode:(?P<mode>.+)$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+) \(Channel (?P<channel>\d+)\)$"),
    re.compile(r"^Encryption key:(?P<encryption>.+)$"),
    re.compile(r"^Quality=(?P<signal_level>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<db>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_level>\d+)/(?P<signal_total>\d+).*$"),
    ]
iwlistCommand = "sudo iwlist wlan0 scan" 
# | grep 'Address\| ESSID\| Signal level'"

iwArgs =shlex.split(iwlistCommand)
#print(iwArgs)
p = subprocess.Popen(iwArgs, stdout=subprocess.PIPE)#, shell=True )
#grepCommand = "grep 'Address\| ESSID\| Signal level'"
#pLines = p.stdout.readlines()
#print(pLines)
#grepArgs = shlex.split(grepCommand)
#q = subprocess.Popen(grepArgs, stdin=p.stdout, stdout=subprocess.PIPE)
content = p.stdout.read().decode('utf-8')
cells  = []
lines = content.split('\n')
for line in lines:#q.stdout.readlines():
#    cells.append(line.decode('utf-8'))
    print(line)
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

print(lines)
for line in cells:
#print(cells[0])
    print(line)
#for i in range(len(lines)):
#   print(i)


