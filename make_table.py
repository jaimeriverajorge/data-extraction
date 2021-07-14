# This is a script to take the landmark coordinates
# from an Oak object and make a csv file with
# x, y coordinates organized just as they are in
# the tutorial

import matplotlib.pyplot as plt
import parsing_script
import matplotlib.image as mpimg
import pandas as pd

# making the dictionary that holds the oak objects
num_images = 33
oak_dict = {}
for i in range(num_images):
    currentOak = parsing_script.makeOaks(i)
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
    name = oak.file_name
    point_list = []
    point_list.append(name)
    for key in lobes:
        point_list.append(lobes[key][0])
        point_list.append(lobes[key][1])

    data_list.append(point_list)


for i in oak_dict:
    extract_points(oak_dict[i])

print(data_list)
# make the columns for the dataframe, right now
# maximum number of lobe tips is 17, so need 34 indices
col_list = ['']
for i in range(34):
    col_list.append(i)

# TODO: make a dataframe from a list of lists, instead of from a dictionary
# get all of the points into lists with the appropriate

df = pd.DataFrame(columns=col_list)
