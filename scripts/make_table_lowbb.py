# This is a file to take the landmark coordinates
# from the Oak objects and make a csv file with the
# coordinates to be used in the model
# 'locating objects without bounding boxes'

import pandas as pd
import oaks
import random
import plot_points as pp

"""
Layout of csv file:
filename,count,locations
img1.png,3,"[(28, 52), (58,53), (135,50)]"

coordinates must be in y,x format
"""


def main():
    # make the dictionary that will hold the oak objects
    num_images = 152
    oak_dict = {}
    for i in range(num_images):
        currentOak = oaks.makeOaks(i)
        id = currentOak.id
        oak_dict[i] = currentOak
    data_list = []
    testOak = oaks.makeOaks(0)
    # print(len(testOak.lobe_tip_margin))

    for i in oak_dict:
        # create empty list
        points_list = []
        class_list = []
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
        points_list, class_list = extract_point(
            oak_dict[i], "lobe_tip_margin", points_list, class_list, to_scale=True)

        # add the points list to the overall data list, which will
        # contain the points for all of the Oak images
        data_list.append(points_list)
        # print(data_list)

    # column list if just have one class
    #col_list = ['filename', 'count', 'locations']
    # column list if using multiple classes
    col_list = ['filename', 'count', 'classes', 'locations']

    # creates a data frame from the list of lists (data list)
    df = pd.DataFrame(data_list, columns=col_list)
    # print(df)
    df.to_csv('lowbb_training_data_test.csv', index=False)

    """
    # shuffles the data list to have a random order of the images
    random.shuffle(data_list)
    # creates a new dataframe with the shuffled list
    shuf_df = pd.DataFrame(data_list, columns=col_list)
    shuf_df.to_csv(
        'lowbb_training_data_lobes_152img_shuffled.csv', index=False)
    """


def extract_point(oak, landmark, points, classes, to_scale):
    return_point_list = points  # [name, count]
    point_list = []
    # get the landmark attribute that we are looking for
    lm = getattr(oak, landmark)
    # turn dict items into list
    lm_list = list(lm.items())
    # shuffle list items
    random.shuffle(lm_list)
    # convert back to dict
    landmark_dict = dict(lm_list)
    if classes != None:
        class_list = classes
        class_num = 0
        if landmark == 'blade_tip':
            class_num = 0
        elif landmark == 'sinus_major':
            class_num = 1
        elif landmark == 'lobe_tip_margin':
            class_num = 2
        elif landmark == 'petiole_tip':
            class_num = 3
        elif landmark == 'petiole_blade':
            class_num = 4
        elif landmark == 'major_secondary':
            class_num = 5
        elif landmark == 'minor_secondary':
            class_num = 6
        for i in landmark_dict:
            class_list.append(class_num)
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
    return_point_list.append(class_list)
    return_point_list.append(point_list)

    return return_point_list, class_list


if __name__ == "__main__":
    main()
