# Script to plot the points from the Oaks landmarks onto an image

import matplotlib.pyplot as plt
import oaks
import matplotlib.image as mpimg
import pandas as pd
import cv2


# hard coded number of images for now
num_images = 1

"""
This was a function to find the file name corresponding to the subject_id,
it is no longer needed as the Zooniverse data now contains the file name

# read the csv file with the matching subject ID and file names
df = pd.read_csv("nfn-private-project-subjects.csv")

def find_name(subject_ID):
    # function to find the file name corresponding to the subject_id
    name = ""
    for i in range(len(df)):
        currID = df.iloc[i][0]
        if currID == subject_ID:
            # ast.literal_eval takes in the string from the
            # metadata column and turns it into a dict
            # {"Filename": "IM-EA-2345.jpg"}
            name_dict = ast.literal_eval(df.iloc[i][4])
            name = name_dict["Filename"]
    return name
"""


# creating dictionary object that will hold all of the images,
# with their respective landmarks
oak_dict = {}
for i in range(num_images):
    currentOak = oaks.makeOaks(i)
    #id = currentOak.id
    oak_dict[i] = currentOak

plt.figure(figsize=(10, 10))


def get_scale(oak):
    scale = 1.0
    name = oak.file_name
    small = cv2.imread(f'oak_images_small/{name}')
    large = cv2.imread(f'../oak_images/{name}')
    scaleY = small.shape[0] / large.shape[0]
    scaleX = small.shape[1] / large.shape[1]
    scale = (scaleX + scaleY) / 2.0
    return scale


def plot_points(oak, feature, color, scale):
    # if plotting on small size image, scale
    # will be passed in as 0, else it will be
    # the scaling factor used from large
    # image to small image
    my_dict = getattr(oak, feature)
    for i in range(len(my_dict)):
        curr_tup = my_dict[i+1]
        if scale != 0:
            plt.plot((curr_tup[0] / scale), (curr_tup[1] / scale), color)
        else:
            plt.plot(curr_tup[0], curr_tup[1], color)


def plot_line(oak, feature, color, scale):
    my_tup = getattr(oak, feature)
    # this assumes that the tuple is in the order
    # (x1, y1, x2, y2)
    if scale != 0:
        x = [(my_tup[0] / scale), (my_tup[2] / scale)]
        y = [(my_tup[1] / scale), (my_tup[3] / scale)]
    else:
        x = [my_tup[0], my_tup[2]]
        y = [my_tup[1], my_tup[3]]

    plt.plot(x, y, c=color)


def plot_all(oakOb, scale):

    # we have to call the plotting function for each landmark,
    # it is a separate function for points vs lines
    plot_points(oakOb, 'blade_tip', 'r.', scale)
    plot_points(oakOb, 'sinus_major', 'm.', scale)
    plot_points(oakOb, 'lobe_tip_margin', 'y.', scale)
    plot_points(oakOb, 'petiole_tip', 'g.', scale)
    plot_points(oakOb, 'petiole_blade', 'y.', scale)
    plot_points(oakOb, 'major_secondary', 'b.', scale)
    plot_points(oakOb, 'minor_secondary', 'k.', scale)
    plot_line(oakOb, 'max_width', 'b', scale)
    plot_line(oakOb, 'min_width', 'r', scale)
    plot_line(oakOb, 'next_width', 'y', scale)


# for loop to plot all of the images and their corresponding landmarks
img_counter = 1
for i in range(num_images):
    # get the current oak object, located at the corresponding key
    currOak = oak_dict[i]
    # get the matching image name
    image_name = currOak.file_name
    myImage = mpimg.imread(f"../oak_images/{image_name}")

    plt.subplot(1, 1, img_counter)
    scale = get_scale(currOak)
    plt.imshow(myImage)
    plt.gca().set_title(f'{image_name}')
    plot_all(currOak, scale)
    #plot_points(currOak, 'lobe_tip_margin', 'y.', scale)
    #plot_points(currOak, 'blade_tip', 'r.', scale)
    img_counter += 1

# plt.show()
