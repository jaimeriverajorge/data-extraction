# data-extraction
The following scripts are written to extract data from landmarks of Oak leaves made on the Zooniverse platform.

This is written to be used in LeafMachine 2.0, an updated version of LeafMachine created by Will Weaver, written in Python instead. Work was supported by Dr. Andrew Hipp's lab at the Morton Arboretum Center for Tree Science.

Within the "scripts" folder, there are 8 Python files:

1. oaks.py
    - This file parses the csv file with the x,y coordinates of the landmarks from Zooniverse and creates Oak objects with each image, each Oak has instance variables that correspond to a type of landmark, or the ID / filename of the image
2. plot_points.py
    -  Script to plot the points from the Oaks landmarks onto an image
3. make_folder.py
    - Script to make the folder of training data,containing only the oak images that have already been landmarked
4. fill_with_1s.py
    - a python script to fill any empty spot in a csv file with 1s
5. make_table_keypoint.py
    - This is a script to take the landmark coordinates from an Oak object and make a csv file with x, y coordinates organized just as they are in the "facial keypoint detection" tutorial
6. make_table_lowbb.py
    - This is a file to take the landmark coordinates from the Oak objects and make a csv file with the coordinates to be used in the model 'locating objects without bounding boxes'
7. show_image.py
    - Script to show an image from a specific folder
8. skeleton.py
    - This file will make a rough estimation of the outer perimeter of the leaf skeleton, by connecting the blade tip, lobe tips, sinuses, and petiole points

The following supplementary files are included:

1. landmark-data.csv: this is the parsed output from Zooniverse, with the raw locations of the landmark points made on Zooniverse