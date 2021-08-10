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

    ordered_points = order_points(currentOak, scale)
    print(ordered_points)
    connect_points(ordered_points, currentOak)
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
    petiole_b_scaled = scale_dict(oak.petiole_blade, scale)
    petiole_blade = petiole_b_scaled[1]
    blade_tip = blade_tip_scaled[1]
    x_tip = blade_tip[0]
    current = blade_tip
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
    # boolean indicating if all points have been passed
    all_passed = False
    # find the closest sinus to the right of blade tip
    closest_sinus = find_closest(current, sinus_scaled, "r", "tip", None, None)
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
        found = True
        if current in sinus_scaled.values():
            print("at sinus:", current)
            print(point_list)
            closest_lobe = find_closest(
                current, lobes_scaled, "r", "sinus", passed_dict, None)
            #print("Closest lobe:", closest_lobe)
            # to make sure it is the right point,
            # check to see if there is a "closer"
            # point, that is above the found point
            # and to the right of the blade tip
            for i in passed_dict:
                x = i[0]
                y = i[1]
                if i in lobes_scaled.values():
                    if passed_dict[i] == False:
                        if x > x_tip and y < closest_lobe[1]:
                            closest_lobe = i
            passed_dict[closest_lobe] = True
            current = closest_lobe
            point_list.append(current)
        elif current in lobes_scaled.values():
            print("at lobe", current)
            print(point_list)
            # check if petiole blade closer than next lobe tip
            # that has not been passed
            for i in passed_dict:
                if i in lobes_scaled.values():
                    x = i[0]

                    if passed_dict[i] == False and x > (x_tip - 50):
                        found = False

            # if the next closest lobe is closer than petiole blade,
            # keep moving to next sinus
            if (not(found)):
                close_sinus = find_closest(
                    current, sinus_scaled, "r", "lobe", passed_dict, blade_tip)
                passed_dict[close_sinus] = True
                current = close_sinus
                point_list.append(current)
            else:
                # petiole blade has now been found
                # break out of loop
                petiole_found = True
                current = petiole_blade
                point_list.append(current)
                closest_lobe = find_closest(
                    current, lobes_scaled, "l", "sinus", passed_dict, None)
                passed_dict[closest_lobe] = True
                current = closest_lobe
                point_list.append(current)
    # now the petiole has been found, keep ordering
    # points on left side of petiole until all points
    # have been passed
    while(not(all_passed)):
        if current in lobes_scaled.values():
            closest_sinus = find_closest(
                current, sinus_scaled, "l", "lobe", passed_dict, blade_tip)
            passed_dict[closest_sinus] = True
            current = closest_sinus
            point_list.append(current)
        elif current in sinus_scaled.values():
            closest_lobe = find_closest(
                current, lobes_scaled, "l", "sinus", passed_dict, None)
            passed_dict[closest_lobe] = True
            current = closest_lobe
            point_list.append(current)

        # check if all points have been passed
        all_passed = all(passed_dict.values())

    return point_list


def find_closest(start_point, dicti, direction, myType, passed, tip):
    min = 50000
    point = ()
    # check every point in the dictionary
    for i in dicti:
        # calculate distance between starting point
        # and the current point in the dictionary
        dist = math.dist(start_point, dicti[i])
        if tip != None:
            x_tip = tip[0]
        x_start = start_point[0]
        x_end = dicti[i][0]
        y_end = dicti[i][1]
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
            # direction is r if we are still on the right
            # side of the petiole blade
            if direction == 'r':
                if dist < min and passed[dicti[i]] == False and x_end > (x_tip - 50):
                    min = dist
                    point = dicti[i]
            else:
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


def connect_points(myList, oak):
    # connect the outer leaf skeleton perimeter
    for i in range(len(myList)):
        if i != (len(myList) - 1):
            x = [myList[i][0], myList[i+1][0]]
            y = [myList[i][1], myList[i+1][1]]
            plt.plot(x, y, c='r')
        else:
            x = [myList[i][0], myList[0][0]]
            y = [myList[i][1], myList[0][1]]
            plt.plot(x, y, c="r")
    # connect the petiole tip to the petiole
    scale = plot_points.get_scale(oak)
    blade_tip_scaled = scale_dict(oak.blade_tip, scale)
    petiole_b_scaled = scale_dict(oak.petiole_blade, scale)
    petiole_tip_scaled = scale_dict(oak.petiole_tip, scale)
    #x = [petiole_tip_scaled[1][0], petiole_b_scaled[1][0], blade_tip_scaled[1][0]]
    #y = [petiole_tip_scaled[1][1], petiole_b_scaled[1][1], blade_tip_scaled[1][1]]
    x = [petiole_tip_scaled[1][0], petiole_b_scaled[1][0]]
    y = [petiole_tip_scaled[1][1], petiole_b_scaled[1][1]]
    plt.plot(x, y, c='r')

# TODO: trace along the midrib, connecting the petiole blade to blade tip,
# using major 2nd veins as references
# 1. sort veins in descending y-coordinate order
# 2. place the petiole blade first in list, append sorted veins
# 3. place the blade tip last on list
# 4. connect from list (reuse part of connect points code)


def trace(oak):
    line = []
    return line
# Then, use the line as the reference point to tell whether
# the point is on the left or right side


def left_or_right(point):
    str = 'r'
    return str


if __name__ == "__main__":
    main()
