# Python file to parse the csv file with the x,y coordinates
# of the landmarks from Zooniverse and create a simplified
# csv file with just the coordinates

# need pandas to create dataframe from csv file
# need re for regular expression to find strings
# in tuple
import pandas as pd
import re


# creating a class for the images, each image will be an
# instance of the class
class oakImage:

    def __init__(self, id, blade_tip, sinus_major, lobe_tip_margin, petiole_tip,
                 petiole_blade, major_secondary, minor_secondary, max_width,
                 min_width, next_width, file_name):
        self.id = id  # int
        self.blade_tip = blade_tip  # tuple
        self.sinus_major = sinus_major  # dictionary
        self.lobe_tip_margin = lobe_tip_margin  # dictionary
        self.petiole_tip = petiole_tip  # tuple
        self.petiole_blade = petiole_blade  # tuple
        self.major_secondary = major_secondary  # dictionary
        self.minor_secondary = minor_secondary  # dictionary
        self.max_width = max_width  # 4-tuple
        self.min_width = min_width  # 4-tuple
        self.next_width = next_width  # 4-tuple
        self.file_name = file_name


# convert csv file to pandas dataframe for easier access
df = pd.read_csv("landmark-data.csv")


# Dictionary of landmarks names, matching exactly what they are in csv file
l_counter_csv = {"blade_tip": 0, "sinus_major": 0,
                 "lobe_tip_margin": 0,
                 "petiole_tip": 0, "petiole_blade": 0,
                 "minor_secondary": 0,
                 "major_secondary": 0,
                 "max_width": 0, "min_width": 0, "next_width": 0}

# step 1:
# for loop to increment values of landmark counter to correspond with
# the amount of columns present in csv file for each landmark AND
# to figure out the starting index
start_index = 0
index_counter = 0
for i in l_counter_csv:
    for name in df.columns:
        # grab starting index if corresponding to "tip of blade"
        # in dictionary and in csv file
        if name[0:9] == "blade_tip" and i == name[0:len(i)]:
            l_counter_csv["blade_tip"] += 1
            # assign start index to index counter (3 in the original file)
            start_index = index_counter
        elif i == name[0:len(i)]:
            l_counter_csv[i] += 1
        index_counter += 1

# print("starting index for first run is:", start_index)
# print(l_counter_csv)
# Step 2:
# extract values from CSV file / dataframe by accessing each index,
# starting at the index (i, 0), where i is the number of the image
# we are on, and 0 is the first column to get the subject ID.
# Then, start at the start_index to get the first landmark coordinate
# will be the blade_tip, then continue to sinus, have for loop which
# will have the range of the corresponding counter value in the
# counter dictionary

# this code will depend on the order that the columns are in within
# the outputted csv file


def int_tuple(my_tup):
    # function to turn strings inside the tuples to integers
    tup = ()
    for v in my_tup:
        # get rid of '1' and '2' from the lines
        if v != '1' and v != '2':
            v_int = (int(v),)
            tup += v_int
    return tup


def make_dict(column, image_number, curr_index):
    # function to make a dictionary of the landmark that is passed in
    ret_dict = {}
    for j in range(l_counter_csv[column]):
        # need to test if index is empty first
        if pd.isna(df.loc[image_number][curr_index]):
            # still need to update the current index to
            # keep moving along in dataframe
            curr_index += 1
        else:
            curr_val = str(df.loc[image_number][curr_index])
            # grab the coordinate using reg ex, which outputs
            # a list of each integer within curr_vall
            # cast into a tuple
            my_tup = tuple(re.findall('\d+', curr_val))
            my_tup = int_tuple(my_tup)
            ret_dict[j+1] = my_tup
            curr_index += 1
    return ret_dict, curr_index


def make_tuple(image_number, current):
    ret_tuple = ()
    if pd.isna(df.loc[image_number][current]):
        current += 1
    else:
        curr_val = str(df.loc[image_number][current])
        ret_tuple = tuple(re.findall('\d+', curr_val))
        current += 1
    return ret_tuple, current


def makeOaks(i):
    # function to make an oak object from the image
    # parameter i is the image number that we are on,
    # which is the index of the dataframe that we want
    sinus_dict = {}
    lobe_tip_dict = {}
    petiole_tip = ()
    petiole_blade = ()
    major_dict = {}
    minor_dict = {}
    max_width = ()
    min_width = ()
    next_width = ()

    # keep track of current index
    curr_index = start_index
    # grab the subject id, will be in the first
    # index in row i
    subject_id = df.loc[i][0]

    # move on to the start index to grab the
    # first coordinate, will be the blade_tip
    # call methods to create all tuples and
    # dictionaries needed for the landmarks
    blade_tip, curr_index = make_dict("blade_tip", i, curr_index)
    sinus_dict, curr_index = make_dict("sinus_major", i, curr_index)
    lobe_tip_dict, curr_index = make_dict(
        "lobe_tip_margin", i, curr_index)
    petiole_tip, curr_index = make_dict("petiole_tip", i, curr_index)
    petiole_blade, curr_index = make_dict("petiole_blade", i, curr_index)
    minor_dict, curr_index = make_dict(
        "minor_secondary", i, curr_index)
    major_dict, curr_index = make_dict(
        "major_secondary", i, curr_index)
    max_width, curr_index = make_tuple(i, curr_index)
    max_width = int_tuple(max_width)
    min_width, curr_index = make_tuple(i, curr_index)
    min_width = int_tuple(min_width)
    next_width, curr_index = make_tuple(i, curr_index)
    next_width = int_tuple(next_width)

    file_name = df.iloc[i][curr_index]

    myOak = oakImage(subject_id, blade_tip, sinus_dict, lobe_tip_dict, petiole_tip,
                     petiole_blade, major_dict, minor_dict, max_width, min_width, next_width, file_name)
    return myOak
