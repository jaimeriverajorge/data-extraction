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
    # data list will be the outer dataframe with
    # a row for each image
    data_list = []
    # number of landmarks we are including in the data
    num_lm = 1
    # initialize an oak object to test outputs
    #testOak = oaks.makeOaks(0)
    # print(len(testOak.lobe_tip_margin))
    if num_lm == 1:
        # column list if just have one class
        col_list = ['filename', 'count', 'locations']
    else:
        # column list if using multiple classes
        col_list = ['filename', 'count', 'classes', 'locations']

    for i in oak_dict:
        # create empty list that will hold the info for each image
        # includes file name, count of points, and point coordinates
        image_points = []

        # the landmark that we want to retrieve
        lm = 'minor_secondary'
        class_list = []
        # instatiate variable with current Oak object
        myOak = oak_dict[i]
        # retrieve image name of current Oak
        name = myOak.file_name
        # add image name to the points list
        image_points.append(name)

        if num_lm == 1:
            # retrieve count of the landmark we want
            count = len(getattr(myOak, lm))
            # add count to the points list
            image_points.append(count)
            # add all points to points list of specified landmark
            image_points = extract_points(
                oak_dict[i], lm, image_points, None, to_scale=True)
        else:
            # TODO: if adding more than one landmark,
            # return the point list and class list from extract_points
            # then append to the image points before add
            class_list = 2
        # add the points list to the overall data list, which will
        # contain the points for all of the Oak images
        data_list.append(image_points)
        # print(data_list)

    # creates a data frame from the list of lists (data list)
    df = pd.DataFrame(data_list, columns=col_list)
    # print(df)
    df.to_csv(f'lowbb_training_data_{lm}_152img.csv', index=False)

    # shuffles the data list to have a random order of the images
    # calls random.Random(2021) to specify the seed
    random.Random(2021).shuffle(data_list)
    # creates a new dataframe with the shuffled list
    shuf_df = pd.DataFrame(data_list, columns=col_list)
    shuf_df.to_csv(
        f'lowbb_training_data_{lm}_152img_shuffled.csv', index=False)


def extract_points(oak, landmark, points, classes, to_scale):
    return_point_list = points  # [name, count, ]
    point_list = []
    # get the landmark attribute that we are looking for
    lm = getattr(oak, landmark)
    # turn dict items into list
    lm_list = list(lm.items())
    # shuffle list items
    random.Random(2021).shuffle(lm_list)
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
            myTup.append(landmark_dict[j][1])
            myTup.append(landmark_dict[j][0])
            point_list.append(tuple(myTup))
    # return_point_list.append(class_list)
    return_point_list.append(point_list)
    if(class_list == None):
        return return_point_list
    else:
        return point_list, class_list


if __name__ == "__main__":
    main()
