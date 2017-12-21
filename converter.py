import csv
import sys
import os
from collections import Counter

def main(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    csv_name = os.path.splitext(filename)[0] + ".csv"
    fieldnames = ["Designator", "Footprint",
                  "Mid X", "Mid Y", 
                  "Ref X", "Ref Y",
                  "Pad X", "Pad Y",
                  "Layer", "Rotation",
                  "Comment"]
    with open(csv_name, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        smd_parts = []
        for line in lines:
            line = line.replace("\n", "")    
            eagle_part = (list(filter(None, line.split(" "))))
            smd_part = {}
            smd_part["Designator"] = eagle_part[0]
            smd_part["Footprint"] = eagle_part[5]
            for place in ["Mid", "Ref", "Pad"]:
                smd_part[place + " X"] = eagle_part[1]+"mm"
                smd_part[place + " Y"] = eagle_part[2]+"mm"            
            smd_part["Layer"] = "T"
            smd_part["Rotation"] = eagle_part[3]
            smd_part["Comment"] = eagle_part[4]
            smd_parts.append(smd_part)
        comment_counts = Counter([smd_part["Comment"] for smd_part in smd_parts]).most_common()
        comment_counts = {element[0]: element[1] for element in comment_counts}
        smd_parts.sort(key=lambda x: x["Comment"])        
        smd_parts.sort(key=lambda x: comment_counts[x["Comment"]], reverse=True)


        for smd_part in smd_parts:
            writer.writerow(smd_part)
        
        
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 2:
        print("Usage: python converter.py [eagle_mount_file]")
        exit(1)
    main(sys.argv[1])