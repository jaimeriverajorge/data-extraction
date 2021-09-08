# This is a file to take the landmark coordinates
# from the Oak objects and make a csv file with the
# coordinates to be used in the model
# 'locating objects without bounding boxes'

# Each time the script is run, the only things that need
# to be changed are all in the main function:
# 1. the number of images (num_images)
# 2. the list of landmarks you want to retrieve (lm_list)
# 3. the name of the csv file you are creating (csv_name)

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
        oak_dict[i] = currentOak
    # Optional: initialize an oak object to test outputs
    #testOak = oaks.makeOaks(0)
    # print(len(testOak.lobe_tip_margin))

    # name of the csv file to create, do not include .csv
    csv_name = 'lowbb_training_data_all_veins_152img'

    # data list will be the outer dataframe with
    # a row for each image
    data_list = []
    # the list of landmarks that we want to retrieve
    lm_list = ['major_secondary', 'minor_secondary']
    # number of landmarks we are including in the data
    num_lm = len(lm_list)

    if num_lm == 1:
        # column list if just have one class
        col_list = ['filename', 'count', 'locations']
    else:
        # column list if using multiple classes
        col_list = ['filename', 'count', 'classes', 'locations']

    # for each image, add the count of landmark(s) as well as the
    # point coordinates
    for i in oak_dict:
        # create empty list that will hold the info for each image
        # includes file name, count of points,
        # classes (if more than 1 landmark), and point coordinates
        image_points = []

        count = 0
        # instatiate variable with current Oak object
        myOak = oak_dict[i]
        # retrieve image name of current Oak
        name = myOak.file_name
        # add image name to the points list
        image_points.append(name)
        # retrieve count of the landmark(s) we want
        for i in lm_list:
            length = len(getattr(myOak, i))
            count += length
        # add the count to the points list for the image
        image_points.append(count)
        if num_lm == 1:
            # add all points to points list of specified landmark
            image_points = extract_points(
                oak_dict[i], lm_list[0], image_points, None, None, to_scale=True)
        else:
            # if adding more than one landmark,
            # return the point list and class list from extract_points
            # then append to the image points before adding to data_list

            # make empty list to hold the point locations for the image
            point_list = []
            # make empty list to hold the class values for the image
            class_list = []

            # add to the point list and class list for each landmark
            for i in lm_list:
                point_list, class_list = extract_points(
                    myOak, i, image_points, class_list, point_list, to_scale=True)

            image_points.append(class_list)
            image_points.append(point_list)
        # add the points list to the overall data list, which will
        # contain the points for all of the Oak images
        data_list.append(image_points)
        # print(data_list)

    # creates a data frame from the list of lists (data list)
    df = pd.DataFrame(data_list, columns=col_list)
    # print(df)
    df.to_csv(f'{csv_name}.csv', index=False)

    # shuffles the data list to have a random order of the images
    # calls random.Random(2021) to specify the seed
    random.Random(2021).shuffle(data_list)
    # creates a new dataframe with the shuffled list
    shuf_df = pd.DataFrame(data_list, columns=col_list)
    shuf_df.to_csv(
        f'{csv_name}shuffled.csv', index=False)


def extract_points(oak, landmark, image_list, classes, points, to_scale):
    return_list = image_list  # [name, count, ]
    if points == None:
        point_list = []
    else:
        point_list = points
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

    if(classes == None):
        return_list.append(point_list)
        return return_list
    else:
        return point_list, class_list


if __name__ == "__main__":
    main()
