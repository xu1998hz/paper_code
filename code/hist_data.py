import csv
import time
import numpy as np
import matplotlib.patches as patches
from matplotlib import pyplot as plt

# Simple mouse click function to store coordinates
def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    # print 'x = %d, y = %d'%(
    #     ix, iy)

    # assign global variable to access outside of function
    global click_coords
    click_coords.append((ix, iy))

    global ax
    rect = patches.Rectangle((ix, iy),300,300,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.show()
    return

with open('feature_vec_whole_20.csv') as csvfile:
    start_time = time.time()
    readCSV = csv.reader(csvfile, delimiter=",")
    coords = []
    next(readCSV) # skip the first line
    dist_ls = []
    density = []
    for row in readCSV:
        dist_ls.append(int(float(row[2])))
        density.append(int(row[3]))
    dist_ls = np.array(dist_ls)
    density = np.array(density)
    second_time = time.time()
    print("time estimates to load the csv file: %s seconds" % (second_time-start_time))
    white_coords_x = []
    white_coords_y = []
    grey_coords_x = []
    grey_coords_y = []
    max_dist = max(dist_ls)
    min_dist = min(dist_ls)
    print("max dist: ", max_dist)
    print("min dist: ", min_dist)
    #plt.hist(density, bins=40)
    plt.hist(dist_ls, bins=40)
    plt.show()
    with open('feature_vec_whole_20.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        next(readCSV) # skip the first line
        for row in readCSV:
            print(row)
            if int(row[3]) >= 150 and int(float(row[2])) <= 45:
                white_coords_x.append(int(float(row[0])))
                white_coords_y.append(int(float(row[1])))
                #plt.scatter(int(float(row[0])), int(float(row[1])), c='coral')
            else:
                grey_coords_x.append(int(float(row[0])))
                grey_coords_y.append(int(float(row[1])))
        print(white_coords_y)

        plt.scatter(white_coords_x, white_coords_y, c='white',s=0.001, marker='.')
        plt.scatter(grey_coords_x, grey_coords_y, c='black',s=0.001, marker='.')

        annotation_x = []
        annotation_y = []
        with open('NA3777-02_AB.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            next(readCSV) # skip the first line
            for row in readCSV:
                annotation_x.append(int(row[0])/2)
                annotation_y.append(int(row[1])/2)

        fig = plt.figure(1)
        ax = fig.add_subplot(111)

        click_coords=[]
        # Call click func
        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        print("white x max: ", max(white_coords_x))
        print("white y max: ", max(white_coords_y))
        print("grey x max: ", max(grey_coords_x))
        print("grey y max: ", max(white_coords_y))
        print("annotation x max: ", max(annotation_x))
        print("annotation y max: ", max(annotation_y))
        #plt.scatter(annotation_x, annotation_y, c='black', s=1, marker='.')
        plt.show()
        print("coordinates of selected points: ", click_coords)

        with open("bbox_coords.csv","w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(click_coords)
