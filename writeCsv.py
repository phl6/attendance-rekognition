import csv  
import time
from os.path import exists

attenadanceDate = time.strftime("%Y-%m-%d")
attenadanceTime = time.strftime("%Y%m%d-%H%M%S")

header = ["time", "name"]
data = [attenadanceTime, "Dave Deng"]
    
def printCSV():
    if not exists("attendanceRecords/" + attenadanceDate + ".csv"):
        with open("attendanceRecords/" + attenadanceDate + ".csv", "w", encoding="UTF8", newline='') as f:
            writer = csv.writer(f)
            # write the header
            header = ["time", "name"]
            writer.writerow(header)
            writer.writerow(data)
    else: 
        with open("attendanceRecords/" + attenadanceDate + ".csv", "a", encoding="UTF8", newline='') as f:
            writer = csv.writer(f)
            # write the data
            writer.writerow(data) 

for i in range(3):
    mode = "w" if not exists("attendanceRecords/attenadanceDate.csv") else "a"
    if mode == "w":
        print("write mode is on now")
    else:
        print("read mode")
    printCSV()