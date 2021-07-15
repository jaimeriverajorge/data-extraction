# This is a script to take the landmark coordinates
# from an Oak object and make a csv file with
# x, y coordinates organized just as they are in
# the tutorial

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from plot_points import get_scale
from numpy.lib.function_base import append
import pandas as pd
import oaks

# TODO: import individual classes (with class methods)
# from oaks instead

# making the dictionary that holds the oak objects
num_images = 33
oak_dict = {}
for i in range(num_images):
    currentOak = oaks.makeOaks(i)
    id = currentOak.id
    oak_dict[i] = currentOak

"""
 dataframe layout:
 
          | 0  | 1 |  2 | ... | 34
 name.jpg |
 oak_dict[i].file_name
"""

# Now, have to extract lobe_tip coordinates and place
# x and y in separate columns, then put into dataframe
data_list = []


def extract_points(oak):
    lobes = oak.lobe_tip_margin
    blade_tips = oak.blade_tip
    name = oak.file_name
    point_list = []
    point_list.append(name)
    # optional, divide by scale to get full sized points
    scale = get_scale(oak)

    # optional: add blade tips to training data
    for i in blade_tips:
        point_list.append(int(blade_tips[i][0] / scale))
        point_list.append(int(blade_tips[i][1] / scale))

    for key in lobes:
        point_list.append(int(lobes[key][0] / scale))
        point_list.append(int(lobes[key][1] / scale))

    data_list.append(point_list)


for i in oak_dict:
    extract_points(oak_dict[i])

# print(data_list)
# make the columns for the dataframe, right now
# maximum number of lobe tips is 17, so need 34 indices
col_list = ['']
for i in range(36):
    col_list.append(i)

# make list of columns that need to be dropped, in order
# for each image to have the same number of keypoints
cols_to_drop = []
for j in range(17, 37):
    cols_to_drop.append(j)


df = pd.DataFrame(data_list, columns=col_list)
# print(cols_to_drop)
df.drop(df.columns[cols_to_drop], axis=1, inplace=True)
print(df)
df.to_csv('lobe_tip_training_full_sized_img.csv', index=False)
