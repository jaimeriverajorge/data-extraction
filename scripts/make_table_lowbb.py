# This is a file to take the landmark coordinates
# from the Oak objects and make a csv file with the
# coordinates to be used in the model
# 'locating objects without bounding boxes'

import pandas as pd
import oaks
import random
import plot_points as pp

# make the dictionary that will hold the oak objects
num_images = 33
oak_dict = {}
for i in range(num_images):
    currentOak = oaks.makeOaks(i)
    id = currentOak.id
    oak_dict[i] = currentOak

testOak = oaks.makeOaks(0)
print(len(testOak.lobe_tip_margin))

"""
Layout of csv file:
filename,count,locations
img1.png,3,"[(28, 52), (58,53), (135,50)]"

coordinates must be in y,x format
"""

data_list = []


def extract_point(oak, landmark, points, to_scale):
    return_list = points  # [name, count]
    point_list = []
    # get the landmark attribute that we are looking for
    lm = getattr(oak, landmark)
    # turn dict items into list
    lm_list = list(lm.items())
    # shuffle list items
    random.shuffle(lm_list)
    # convert back to dict
    landmark_dict = dict(lm_list)
    if to_scale:
        scale = pp.get_scale(oak)
        for i in landmark_dict:
            myTup = []
            myTup.append(int(landmark_dict[i][1] / scale))
            myTup.append(int(landmark_dict[i][0] / scale))
            point_list.append(tuple(myTup))
    else:
        for j in landmark_dict:
            myTup = []
            myTup.append(landmark_dict[j][0])
            myTup.append(landmark_dict[j][1])
            point_list.append(tuple(myTup))
    return_list.append(point_list)
    return return_list


# """
for i in oak_dict:
    # create empty list
    points_list = []
    # instatiate variable with current Oak object
    myOak = oak_dict[i]
    # retrieve image name of current Oak
    name = myOak.file_name
    # add image name to the points list
    points_list.append(name)
    # retrieve count of lobe_tip_margin
    count = len(myOak.lobe_tip_margin)
    # add count to the points list
    points_list.append(count)
    # add all points to points list of specified landmark
    points_list = extract_point(
        oak_dict[i], "lobe_tip_margin", points_list, to_scale=True)

    # add the points list to the overall data list, which will
    # contain the points for all of the Oak images

    data_list.append(points_list)
# """
col_list = ['filename', 'count', 'locations']
df = pd.DataFrame(data_list, columns=col_list)
df.to_csv('new_training_data.csv', index=False)

random.shuffle(data_list)
shuf_df = pd.DataFrame(data_list, columns=col_list)
shuf_df.to_csv('new_training_data_shuffled.csv', index=False)
