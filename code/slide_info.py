import csv
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance_matrix
from PIL import Image

# load data into the program, store all the coordinates
with open('NA3777-02_AB-Grey.csv') as csvfile:
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
    datapoints = np.zeros((height, width), dtype='uint8')
    ini_data = time.time()
    print("time estimates to initialize data plane: %s seconds" % (ini_data-load_time))
    for x, y in coords:
        datapoints[int(x)][int(y)] = 1
    data_build = time.time()
    print("time estimates to finish building the data plane: %s seconds" % (data_build-ini_data))
    print(datapoints)

    feature_vec= []
    #create distance matrix to improve efficiency
    temp = np.zeros((101,101))
    x, y = np.where(temp==0)
    dist_matrix = distance_matrix(np.dstack((x,y))[0], [[101, 101]])
    dist_matrix = dist_matrix.flatten()
    for x, y in coords:
        if (int(x)>=50) and (int(x)<height-50) and (int(y)>=50) and (int(y) < width-50):
            start_epoach = time.time()
            # Create a box shape 301*301, center is (150,150)
            box_coords = datapoints[int(x)-50:int(x)+51, int(y)-50:int(y)+51]
            print("current coordinates: ", (x,y))
            # count all the points in the local region
            points_count = np.sum(box_coords)
            # calculate distance to the center for all the points in the local region
            box_dist = box_coords.flatten()*dist_matrix
            # calculate the standard deviation for all the distances
            #dist_sorted = sorted(box_dist)
            std = np.std(np.trim_zeros(box_dist))
            # compute average distance of all the points in the local region
            avg_dist = sum(box_dist)/points_count
            print("average distance: ", avg_dist)

            print("std: ", std)
            feature_vec.append([x, y, avg_dist, points_count, std, abs(x-mid_height), abs(y-mid_width)]) # transform each coordinate to be a feature vector
            print("time estimates to compute current epoach of feature vectors: %s seconds" % (time.time() - start_epoach))
            print()

    with open("feature_NA3777-02_AB-Grey.csv","w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(feature_vec)
    print("total time in running this window based operation to compute feature vector: %s seconds" % (time.time() - start_time))
