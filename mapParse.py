import os

#path = '~/srp/fingerprints'


roomGrid = [[0]*19] *27

for filename in os.listdir(os.getcwd()):
    if filename == '.directory':
        continue
    row,col = filename.split('-')
    row = int(row)
    col = int(col)

    with open(filename,encoding="utf-8") as f:
        data = eval(f.read())
        roomGrid[row][col] = data

#print(roomGrid[13][13].keys())
#print(roomGrid
gridDict = {}

for row in roomGrid:
    for col in row:
        for key in col.keys():
            if key not in gridDict:
                
    
 
