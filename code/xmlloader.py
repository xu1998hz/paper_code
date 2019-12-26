from xml.dom import minidom
import csv

mydoc = minidom.parse('NA4077-02_AB.xml')

items = mydoc.getElementsByTagName('Vertex')

datapoints = []
for row in items:
    x = int(row.attributes['X'].value)
    y = int(row.attributes['Y'].value)
    datapoints.append([x,y])

with open("NA4077_02AB_cell.csv","w") as f:
    writer = csv.writer(f)
    writer.writerows(datapoints)
