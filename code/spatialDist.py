import csv
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix
from PIL import Image

# load data into the program, store all the coordinates
with open('cell_wo_residue.csv') as csvfile:
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
    print("time estimates to load the csv file: %s seconds" % (load_time-start_time))
    x_list = [i[0] for i in coords]
    y_list = [i[1] for i in coords]
    height = int(max(x_list))+1
    width = int(max(y_list))+1
    mid_height = height/2
    mid_width = width/2
    min_height = int(min(x_list))+1
    min_width = int(min(y_list))+1
    print("max height of the data: ", height)
    print("max width of the data: ", width)
    print("min height of the data: ", int(min(x_list))+1)
    print("min width of the data: ", int(min(y_list))+1)
    datapoints = np.zeros((height, width), dtype='uint8')
    ini_data = time.time()
    print("time estimates to initialize data plane: %s seconds" % (ini_data-load_time))
    for x, y in coords:
        datapoints[int(x)][int(y)] = 1
    data_build = time.time()
    print("time estimates to finish building the data plane: %s seconds" % (data_build-ini_data))
    print(datapoints)

    #feature_vec = []
    with open('spatialdist.csv', "w") as file:
        writer = csv.writer(file, delimiter=',')
        with open('NA3777-02_AB-White.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            next(readCSV) # skip the first line
            for row in readCSV:
                if len(row) > 0:
                    x = row[0].split()[2]
                    y = row[0].split()[3]
                    if x != 'NaN' and y != 'NaN':
                        x,y = float(x), float(y)

                        writer.writerow([min(abs(x-min_height), abs(x-height), abs(y-width), abs(y-min_width))])

    #print(feature_vec)
