# This file will make a rough estimation of the outer perimeter of the leaf skeleton,
# by connecting the blade tip, lobe tips, sinuses, and petiole points
from numpy.core.fromnumeric import trace
import plot_points
import oaks
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

currentOak = oaks.makeOaks(102)
scale = plot_points.get_scale(currentOak)


def main():
    #plt.figure(figsize=(10, 10))

    image_name = currentOak.file_name
    myImg = mpimg.imread(f"../../oak_images/{image_name}")
    plt.imshow(myImg)
    plt.title(f"{image_name}")
    plot_points.plot_points(currentOak, "blade_tip", "r.", scale)
    plot_points.plot_points(currentOak, "lobe_tip_margin", "y.", scale)
    plot_points.plot_points(currentOak, "petiole_tip", "r.", scale)
    plot_points.plot_points(currentOak, "petiole_blade", "b.", scale)
    plot_points.plot_points(currentOak, "sinus_major", "m.", scale)

    line = trace_midrib()
    sinus = scale_dict(currentOak.sinus_major, scale)
    #s = sinus[9]
    lobes = scale_dict(currentOak.lobe_tip_margin, scale)
    #s = lobes[10]
    #a, b = find_between(line, s)
    # print(s)
    #print(a, b)
    #print(left_or_right(s, a, b))

    # plt.show()
    ordered_points = order_points(currentOak, scale)
    print(ordered_points)
    connect_points(ordered_points, currentOak)
    plt.show()


def order_points(oak, scale):
    # this function will return a list containing
    # the blade tip, lobe tips, sinuses, and
    # petiole blade in clockwise order
    line = trace_midrib()
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
    closest_sinus = find_closest(
        current, sinus_scaled, "r", "tip", passed_dict, lobes_scaled)
    current = closest_sinus
    # check that there is not a closer lobe tip
    """
    for i in lobes_scaled:
        lo = lobes_scaled[i]
        a, b = find_between(line, lo)
        t_dir = left_or_right(lo, a, b)

        x_lobe = lo[0]
        x1 = current[0]
        xS = closest_sinus[0]

        if t_dir == 'r' and x_lobe < xS:
            current = lobes_scaled[i]
    """
    # update current, mark point as passed

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
            #print("closest so far:", closest_lobe)
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
                        a, b = find_between(line, i)
                        direction = left_or_right(i, a, b)
                        if direction == 'r' and y < closest_lobe[1]:
                            closest_lobe = i
            print('')
            print("closest lobe:", closest_lobe)
            passed_dict[closest_lobe] = True
            print(passed_dict)
            print('')
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
                    a, b = find_between(line, i)
                    direction = left_or_right(i, a, b)
                    if passed_dict[i] == False and direction == 'r':
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
    print("Petiole has been found")
    while(not(all_passed)):
        if current in lobes_scaled.values():
            print('at lobe:', current)
            print(passed_dict)
            print(point_list)
            print('')
            closest_sinus = find_closest(
                current, sinus_scaled, "l", "lobe", passed_dict, blade_tip)
            passed_dict[closest_sinus] = True
            current = closest_sinus
            point_list.append(current)
        elif current in sinus_scaled.values():
            print('at sinus:', current)
            print(point_list)
            print(passed_dict)
            print('')
            closest_lobe = find_closest(
                current, lobes_scaled, "l", "sinus", passed_dict, None)
            # check to see if there is a "closer"
            # point, that is above the found point
            # and to the left of the blade tip
            for i in passed_dict:
                x = i[0]
                y = i[1]
                if i in lobes_scaled.values():
                    if passed_dict[i] == False:
                        a, b = find_between(line, i)
                        direction = left_or_right(i, a, b)
                        if direction == 'l' and y > closest_lobe[1]:
                            closest_lobe = i
            print("closest lobe:", closest_lobe)
            passed_dict[closest_lobe] = True
            current = closest_lobe
            point_list.append(current)

        # check if all points have been passed

        all_passed = all(passed_dict.values())

    return point_list


def find_closest(start_point, dicti, direction, myType, passed, extra_dict):
    min = 50000
    point = ()
    # get the line that is from the traced midrib
    line = trace_midrib()

    # check every point in the dictionary
    for i in dicti:
        # potential closest point
        p = dicti[i]
        x_p = p[0]
        # calculate distance between starting point
        # and the current point in the dictionary
        dist = math.dist(start_point, p)
        # find the segment of the midrib closest
        # to the potential "closest point"
        a, b = find_between(line, p)
        dir = left_or_right(p, a, b)

        # In first case, we are moving to the right and are starting at
        # the blade tip or a sinus, have not yet found petiole blade
        if myType == 'tip':
            # check if current distance is less
            # than the minimum, and that the
            # new point is farther to the right
            # than the start point
            if dist < min and direction == dir:
                # update min
                min = dist
                point = p
                # TODO: check for closer lobe tip
                for i in extra_dict:
                    lo = extra_dict[i]
                    x_l = lo[0]
                    if passed[lo] == False:
                        a, b = find_between(line, lo)
                        t_dir = left_or_right(lo, a, b)
                        dist2 = math.dist(start_point, lo)
                        if t_dir == 'r' and dist2 < min and x_l < x_p:
                            point = lo

        elif myType == "sinus":
            if dist < min and direction == dir:
                # update min, if new point has not been passed
                if(passed[p] == False):
                    min = dist
                    point = p
        elif myType == 'lobe':
            # third case, currently moving from a lobe,
            # direction is r if we are still on the right
            # side of the petiole blade
            if direction == 'r':
                if dist < min and passed[p] == False and direction == dir:
                    min = dist
                    point = p
            else:
                if dist < min and passed[p] == False:
                    min = dist
                    point = p
    return point


def scale_dict(dict, scale):
    # returns the dictionary with all of the points,
    # scaled up to match the full resolution image
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

# Trace along the midrib, connecting the petiole blade to blade tip,
# using major 2nd veins as references
# 1. sort veins in descending y-coordinate order
# 2. place the petiole blade first in list, append sorted veins
# 3. place the blade tip last on list
# 4. draw midrib


def trace_midrib():
    major_scaled = scale_dict(currentOak.major_secondary, scale)
    petiole_b_scaled = scale_dict(currentOak.petiole_blade, scale)
    blade_tip_scaled = scale_dict(currentOak.blade_tip, scale)
    line = []
    line.append(petiole_b_scaled[1])
    for i in major_scaled:
        tup = major_scaled[i]
        line.append(tup)
    line = sorted(line, key=lambda x: x[1], reverse=True)
    line.append(blade_tip_scaled[1])
    x = []
    y = []
    for i in line:
        x.append(i[0])
        y.append(i[1])
    plt.plot(x, y, c="b")

    return line
# Then, use the line as the reference point to tell whether
# the point is on the left or right side
# First, need to find out which part of the midrib
# the point falls within
# (since the midrib is made up of multiple lines)
# next, return that line as two points a, b


def find_between(line, point):
    y_p = point[1]
    x_p = point[0]
    length = len(line)
    a = 0
    b = 0
    for i in range(length):
        if i != (length - 1):
            x_1 = line[i][0]
            y_1 = line[i][1]
            x_2 = line[i+1][0]
            y_2 = line[i+1][1]
            if (y_p <= y_1) and (y_p >= y_2):
                a = [x_1, y_1]
                b = [x_2, y_2]
            # a will still equal 0 when there is no
            # "in between" line based off y-coordinates,
            # which happens if the midrib is lower than a sinus
            # in this case, use x-coordinates instead
            if (a == 0) or (b == 0):
                # TODO: use x coordinates to find two points
                if(x_p <= x_1) and (x_p >= x_2):
                    a = [x_1, y_1]
                    b = [x_2, y_2]
    return a, b


# Use a and b in the left or right function, which
# uses the cross product to determine the direction that
# the point is int

def left_or_right(point, line_a, line_b):
    # right = 1
    # left = -1
    str = 'none'
    x_p = point[0]
    y_p = point[1]
    x_a = line_a[0]
    y_a = line_a[1]
    x_b = line_b[0]
    y_b = line_b[1]

    # subtract coordinates of point A from
    # point P and point B to make A the origin
    x_p -= x_a
    y_p -= y_a
    x_b -= x_a
    y_b -= y_a

    # determine cross product
    cross_prod = (x_b * y_p) - (y_b * x_p)

    if (cross_prod > 0):
        str = 'r'
    elif(cross_prod < 0):
        str = 'l'
    return str


if __name__ == "__main__":
    main()
