# Script to plot the points from parsing_script onto an image

import matplotlib.pyplot as plt
import parsing_script
import matplotlib.image as mpimg
import pandas as pd
import ast


# hard coded number of images for now
num_images = 2

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
    currentOak = parsing_script.makeOaks(i)
    id = currentOak.id
    oak_dict[id] = currentOak

plt.figure(figsize=(10, 10))


def plot_points(oak, feature, color):
    my_dict = getattr(oak, feature)
    for i in range(len(my_dict)):
        curr_tup = my_dict[i+1]
        plt.plot(curr_tup[0], curr_tup[1], color)


def plot_line(oak, feature, color):
    my_tup = getattr(oak, feature)
    # this assumes that the tuple is in the order
    # (x1, y1, x2, y2)
    x = [my_tup[0], my_tup[2]]
    y = [my_tup[1], my_tup[3]]
    plt.plot(x, y, c=color)


def plot_all(oakOb):

    # we have to call the plotting function for each landmark,
    # it is a separate function for points vs lines
    plot_points(oakOb, 'blade_tip', 'r.')
    plot_points(oakOb, 'sinus_major', 'm.')
    plot_points(oakOb, 'lobe_tip_margin', 'y.')
    plot_points(oakOb, 'petiole_tip', 'g.')
    plot_points(oakOb, 'petiole_blade', 'y.')
    plot_points(oakOb, 'major_secondary', 'b.')
    plot_points(oakOb, 'minor_secondary', 'k.')
    plot_line(oakOb, 'max_width', 'b')
    plot_line(oakOb, 'min_width', 'r')
    plot_line(oakOb, 'next_width', 'y')


# for loop to plot all of the images and their corresponding landmarks
img_counter = 1
for sub_id in oak_dict:
    # get the current oak object, located at the corresponding key
    currOak = oak_dict[sub_id]
    # get the matching image name
    image_name = currOak.file_name
    myImage = mpimg.imread(f"oak_images_small/{image_name}")

    plt.subplot(1, 2, img_counter)
    plt.imshow(myImage)
    plot_all(currOak)
    img_counter += 1

plt.show()
