# This is a script to take the landmark coordinates
# from an Oak object and make a csv file with
# x, y coordinates organized just as they are in
# the tutorial

from plot_points import get_scale
from numpy.lib.function_base import append
import pandas as pd
import oaks
import random

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
test_list = []


def extract_points(oak):
    petiole = oak.petiole_tip
    blade_tips = oak.blade_tip
    petiole_blade = oak.petiole_blade
    name = oak.file_name
    point_list = []
    point_list.append(name)
    # optional, divide by scale to get full sized points
    scale = get_scale(oak)

    # optional: add blade tips to training data
    for i in blade_tips:
        point_list.append(int(blade_tips[i][0] / scale))
        point_list.append(int(blade_tips[i][1] / scale))

    for key in petiole:
        point_list.append(int(petiole[key][0] / scale))
        point_list.append(int(petiole[key][1] / scale))

    for point in petiole_blade:
        point_list.append(int(petiole_blade[point][0] / scale))
        point_list.append(int(petiole_blade[point][1] / scale))

    data_list.append(point_list)
    test_list.append(point_list)


for i in oak_dict:
    extract_points(oak_dict[i])


random.shuffle(test_list)


# print(data_list)
# make the columns for the dataframe, right now
# maximum number of lobe tips is 17, so need 34 indices
col_list = ['']
for i in range(6):
    col_list.append(i)

# make list of columns that need to be dropped, in order
# for each image to have the same number of keypoints
cols_to_drop = []
for j in range(17, 37):
    cols_to_drop.append(j)

print(data_list)
print(test_list)

df = pd.DataFrame(data_list, columns=col_list)
print(df)
#df.drop(df.columns[cols_to_drop], axis=1, inplace=True)

shuf_df = pd.DataFrame(test_list, columns=col_list)
print(shuf_df)
#shuf_df.drop(shuf_df.columns[cols_to_drop], axis=1, inplace=True)
#shuf_df.to_csv('three__training_data_full_sized_shuffled.csv', index=False)

#df.to_csv('lobe_tip_training_full_sized_img.csv', index=False)
