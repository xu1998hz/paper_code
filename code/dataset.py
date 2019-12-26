import csv
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# load data into the program, store all the coordinates
with open('NA4077_02AB.csv') as csvfile:
    start_time = time.time()
    readCSV = csv.reader(csvfile, delimiter=",")
    coords = []
    next(readCSV) # skip the first line
    for row in readCSV:
        if len(row) > 0:
            x = row[0].split()[3]
            y = row[0].split()[4]
            if x != 'NaN' and y != 'NaN':
                coord = [float(x), float(y)]
                coords.append(coord)
    load_time = time.time()
    #print(coords)
    print("time estimates to load the csv file: %s seconds" % (load_time-start_time))
    x_list = [i[0] for i in coords]
    y_list = [i[1] for i in coords]
    datapoints = np.zeros((int(max(x_list))+1, int(max(y_list))+1), dtype='uint8')
    ini_data = time.time()
    print("time estimates to initialize data plane: %s seconds" % (ini_data-load_time))
    for x, y in coords:
        datapoints[int(x)][int(y)] = 255

    data_build = time.time()
    print("time estimates to finish building the data plane: %s seconds" % (data_build-ini_data))

    # store all the boundary images starting from 0
    i = 0
    with open('NA4077_02AB_cell.csv') as csvfile2:
        readCSV = csv.reader(csvfile2, delimiter=",")
        next(readCSV) # skip the first line
        for row in readCSV:
            if len(row) == 2:
                x = int(float(row[0]))
                y = int(float(row[1]))
                # Create a box shape 501*801, center is (250, 400)
                if (x+128 < (int(max(x_list))+1)) and (x-128 > 0) and (y+128 < (int(max(y_list))+1)) and (y-128 > 0):
                    box_coords = datapoints[x-128:x+128, y-128:y+128]
                #print(points)
                if sum(sum(box_coords))>255*40:
                    im = Image.fromarray(box_coords)
                    img_name = "./4077_boundary" + str(i) + "_boundary.png"
                    im.save(img_name)
                    print("save image ", img_name)
                    i+=1
