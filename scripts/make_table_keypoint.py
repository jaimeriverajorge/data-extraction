# This is a script to take the landmark coordinates
# from an Oak object and make a csv file with
# x, y coordinates organized just as they are in
# the tutorial

from plot_points import get_scale
from numpy.lib.function_base import append
import pandas as pd
import oaks
import random


def main():

    # making the dictionary that holds the oak objects
    num_images = 230
    oak_dict = {}
    for i in range(num_images):
        currentOak = oaks.makeOaks(i)
        oak_dict[i] = currentOak

    # Now, have to extract coordinates and place
    # x and y in separate columns, then put into dataframe
    data_list = []
    """
    # test the shuffling of the veins
    currOak = oaks.makeOaks(0)
    veins = currOak.minor_secondary

    v_list = list(veins.items())
    #print("List not shuffled:", v_list)
    random.shuffle(v_list)
    #print("Shuffled list:", v_list)
    v_shuf = dict(v_list)
    # print(v_shuf)
    """

    landmark_list = ['blade_tip', 'petiole_blade', 'petiole_tip']
    for i in oak_dict:
        # create empty list
        points_list = []
        # instatiate variable with current Oak object
        myOak = oak_dict[i]
        # retrieve image name of current Oak
        name = myOak.file_name
        # add image name to the points list
        points_list.append(name)
        # add all points to points list of specified landmark
        for j in landmark_list:
            points_list = extract_point(
                myOak, j, points_list, to_scale=True)

        # contain the points for all of the Oak images

        data_list.append(points_list)

    # make the columns for the dataframe, length
    # depends on how many, and which, landmarks are
    # being used
    col_list = ['']
    for i in range(6):
        col_list.append(i)

    # make list of columns that need to be dropped
    # for each image to have the same number of keypoints
    # only necessary if doing lobe tips, sinuses, or veins
    cols_to_drop = []
    for j in range(9, 39):
        cols_to_drop.append(j)

    df = pd.DataFrame(data_list, columns=col_list)
    # print(df)
    df.to_csv(
        'three_points_training_not_shuffled.csv', index=False)

    random.shuffle(data_list)
    all_df = pd.DataFrame(data_list, columns=col_list)
    # rint(all_df)
    all_df.to_csv(
        'three_points_training_shuffled.csv', index=False)

    min_df = pd.DataFrame(data_list, columns=col_list)
    #min_df.drop(min_df.columns[cols_to_drop], axis=1, inplace=True)
    # min_df.to_csv(
    #    'sinus_training_min_points_shuffled.csv', index=False)


def extract_point(oak, landmark, points, to_scale):
    point_list = points
    # get the landmark attribute that we are looking for
    lm = getattr(oak, landmark)
    # turn dict items into list
    lm_list = list(lm.items())
    # shuffle list items
    random.shuffle(lm_list)
    # convert back to dict
    landmark_dict = dict(lm_list)
    if to_scale:
        scale = get_scale(oak)
        for i in landmark_dict:
            point_list.append(int(landmark_dict[i][0] / scale))
            point_list.append(int(landmark_dict[i][1] / scale))
    else:
        for j in landmark_dict:
            point_list.append(landmark_dict[j][0])
            point_list.append(landmark_dict[j][1])
    return point_list


if __name__ == "__main__":
    main()
