# This file will make a rough estimation of the outer perimeter of the leaf skeleton,
# by connecting the blade tip, lobe tips, sinuses, and petiole points
import plot_points
import oaks
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math


def main():
    #plt.figure(figsize=(10, 10))
    currentOak = oaks.makeOaks(0)
    scale = plot_points.get_scale(currentOak)
    image_name = currentOak.file_name
    myImg = mpimg.imread(f"../../oak_images/{image_name}")
    plt.imshow(myImg)
    plt.title(f"{image_name}")
    plot_points.plot_points(currentOak, "blade_tip", "r.", scale)
    plot_points.plot_points(currentOak, "lobe_tip_margin", "y.", scale)
    plot_points.plot_points(currentOak, "petiole_tip", "r.", scale)
    plot_points.plot_points(currentOak, "petiole_blade", "b.", scale)
    plot_points.plot_points(currentOak, "sinus_major", "m.", scale)

    print(order_points(currentOak, scale))
    plt.show()


def order_points(oak, scale):
    # this function will return a list containing
    # the blade tip, lobe tips, sinuses, and
    # petiole blade in clockwise order

    # ordered point list to return
    point_list = []
    # dictionary showing if point has been passed
    passed_dict = {}
    # boolean indicating if petiole_meets_blade
    # has been found
    petiole_found = False

    blade_tip_scaled = scale_dict(oak.blade_tip, scale)
    current = blade_tip_scaled[1]
    point_list.append(current)

    # scale the sinuses and lobes to the full sized image
    sinus_scaled = scale_dict(oak.sinus_major, scale)
    lobes_scaled = scale_dict(oak.lobe_tip_margin, scale)
    # add the sinuses and lobes to the passed dictionary
    # with a starting value of False
    for j in lobes_scaled:
        passed_dict[lobes_scaled[j]] = False
    for i in sinus_scaled:
        passed_dict[sinus_scaled[i]] = False
    # find the closest sinus to the right of blade tip
    closest_sinus = find_closest(current, sinus_scaled, "r", "tip", None)
    # check that there is not a closer lobe tip
    for i in lobes_scaled:
        x_lobe = lobes_scaled[i][0]
        x1 = current[0]
        xS = closest_sinus[0]
        if x_lobe > x1 and x_lobe < xS:
            current = lobes_scaled[i]
            passed_dict[current] = True
    # update current, mark point as passed
    current = closest_sinus
    passed_dict[current] = True
    # add current to point list
    point_list.append(current)

    # while the petiole has not been found
    while(not(petiole_found)):
        if current in sinus_scaled:
            closest_lobe = find_closest(
                current, lobes_scaled, "r", "sinus", passed_dict)
            passed_dict[closest_lobe] = True
            current = closest_lobe
            point_list.append(current)
        elif current in lobes_scaled:
            close_sinus = find_closest(
                current, sinus_scaled, "none", "lobe", passed_dict)
    return point_list


def find_closest(start_point, dicti, direction, myType, passed):
    min = 50000
    point = ()
    # check every point in the dictionary
    for i in dicti:
        # calculate distance between starting point
        # and the current point in the dictionary
        dist = math.dist(start_point, dicti[i])
        x_start = start_point[0]
        x_end = dicti[i][0]
        # In first case, we are moving to the right and are starting at
        # the blade tip or a sinus, have not yet found petiole blade
        if myType == 'tip':
            # check if current distance is less
            # than the minimum, and that the
            # new point is farther to the right
            # than the start point
            if dist < min and x_start < x_end:
                # update min
                min = dist
                point = dicti[i]
        elif myType == "sinus":
            if direction == 'r':
                if dist < min and x_start < x_end:
                    # update min, if new point has not been passed
                    if(passed[dicti[i]] == False):
                        min = dist
                        point = dicti[i]
            elif direction == 'l':
                if dist < min and x_start > x_end:
                    if(passed[dicti[i]] == False):
                        min = dist
                        point = dicti[i]
        elif myType == 'lobe':
            # third case, currently moving from a lobe,
            # direction does not matter, just
            # want the closest sinus
            if dist < min and passed[dicti[i]] == False:
                min = dist
                point = dicti[i]
    return point


def scale_dict(dict, scale):
    scaled_dict = {}
    for i in dict:

        x = int(dict[i][0] / scale)
        y = int(dict[i][1] / scale)
        scaled_point = (x, y)
        scaled_dict[i] = scaled_point
    return scaled_dict


if __name__ == "__main__":
    main()
