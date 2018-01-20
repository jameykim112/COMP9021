## COMP9021 - Assignment 2
## By Jamey Kim
## z3251762

from argparse import ArgumentParser
import os
from collections import Counter
from collections import deque
import sys
import math
import operator

#Convert text file into nested list with integers
def loadPolygon(filename):
    global polygon
    global polygon_list
    polygon_list = []
    polygon = []
    polygon_test = []
    polygon_test1 = []
    polygon_test2 = []
    polygon_test3 = []
    readfile = open(filename,'r')
    readlines = readfile.readlines()
    if len(readlines[0]) == 1:
        #print('Polys_3 and Polys_4 example')
        #Remove '\n' symbols from end of line through .split()
        for i in range(0, len(readlines)):
            a = readlines[i].split()
            polygon_test.append(a)
        #If length of nested list is greater than 0, then append to new list
        for i in range(len(polygon_test)):
            if len(polygon_test[i]) > 0:
                polygon_test1.append(polygon_test[i])
        #Conversion of each list element to separate strings then create new list. (Polys_4)
        for i in polygon_test1:
            for j in i:
                e = list(str(j))
                polygon_test3.extend(e)
            polygon_list.append(polygon_test3)
            polygon_test3 = []
        for i in range(len(polygon)):
            if len(polygon[i]) > 0:
                polygon_list.append(polygon[i])
    elif len(readlines[0]) > 1:
        #print('Polys_1 and Polys_2 example')
        polygon_list = [list(i.strip()) for i in readlines]

    #Conversion of polygon fromt nested list of strings to
    #nested list of integers
    polygon = []
    for i in range(len(polygon_list)):
        a = polygon_list[i]
        b = [int(k) for k in a]
        polygon.append(b)

    #Append arbitary boundaries at top, bottom, left and right of nested lists
    for i in polygon:
        i.insert(0,0)
        i.insert(len(polygon[0]),0)

    n = len(polygon[0])
    top_bot_boundary = n * [0]
    #print(top_bot_boundary)
    polygon.append(top_bot_boundary)
    polygon.insert(0,top_bot_boundary)

def printPolygon():
    for i in polygon:
        print(" ".join(map(str,i)))

def checkgrid(polygon_test):
    global A
    global letter
    global path
    global direction
    global perimeter
    global returned
    global start_point
    A = 65
    letter = chr(A)
    path = [] #Store the polygon co-ordinates
    direction = [] #Store direction polygon travels
    returned = []

    #If polygon initial input values are not 1 and 0 then incorrect
    for i in range(len(polygon)):
        for j in range(len(polygon[0])):
            if polygon[i][j] > 1:
                print("Incorrect input.")
                #output = '_output.txt'
                #f_o = open(filename[:-4]+output, 'w')
                #f_o.write("Incorrect input.\n")
                #f_o.close()
                sys.exit()
            else:
                continue

    for i in range(len(polygon)-1):
        if len(polygon[i]) != len(polygon[i+1]):
            print("Incorrect input.")
            #output = '_output.txt'
            #f_o = open(filename[:-4]+output, 'w')
            #f_o.write("Incorrect input.\n")
            #f_o.close()
            sys.exit()
        else:
            continue

    for i in range(len(polygon)):
        for j in range(len(polygon[0])):
            if polygon[i][j] == 1:
                start_point = i,j
                path.append(start_point)
                polygon[i][j] = 2
                search(i, j, letter, A)

                #If all polygons are not enclosed then False, else True
                if len(returned) == 0:
                    return False
                elif len(path) < 3:
                    return False
                convert_polygon(letter)
                A += 1
                letter = chr(A)
                path = []
                returned = []
            #Length of polygon not between 50x50 or 2x2 then incorrect input. Using values 52x52 and 4x4 as arbitary border of 0 created
            elif len(polygon[0]) > 52 or len(polygon) > 52 or len(polygon[0]) < 4 or len(polygon) < 4:
                print("Incorrect input.")
                #output = '_output.txt'
                #f_o = open(filename[:-4]+output, 'w')
                #f_o.write("Incorrect input.\n")
                #f_o.close()
                #print("Cannot get polygons as expected.\n")
                sys.exit()
    return True #Return a value of 1 if successful and continue with program

def perimeter(path):
    horizontal_vertical = 0
    diagonal = 0
    try:
        for i in range(0,len(path)):
            if (path[i][0] == path[i-1][0]) or (path[i][1] == path[i-1][1]):
                #print("East,West")
                horizontal_vertical += 1
            else:
                diagonal += 1
        perimeter_value = round((horizontal_vertical)*0.4,1)
        diagonal = round(diagonal,0)
        return perimeter_value, diagonal
    except IndexError:
        return perimeter_value, diagonal

def area(path):
    #Calculation of polygon area based on Shoelace Formula
    area = 0
    area_list = []
    path.append(path[0])
    try:
        for i in range(0,len(path)):
            area += (path[i][1]*path[i+1][0])-(path[i][0]*path[i+1][1])
        area_value = 0.5*area*0.16
        return area_value
    except IndexError:
        area_value = 0.5*area*0.16
        return area_value

def convexity(path):
    convexity = []
    positive_count = 0
    negative_count = 0
    try:
        for i in range(0,len(path)-2):
            dx1 = path[i+1][1] - path[i][1]
            dy1 = path[i+1][0] - path[i][0]
            dx2 = path[i+2][1] - path[i+1][1]
            dy2 = path[i+2][0] - path[i+1][0]
            zcrossproduct = dx1*dy2 - dy1*dx2
            convexity.append(zcrossproduct)
        for i in convexity:
            if i >= 0:
                positive_count += 1
            elif i < 0:
                negative_count += 1
        if (positive_count == len(path) - 2) or (negative_count == len(path) - 2):
            convex = 'yes'
        else:
            convex = 'no'
        return convex
    except IndexError:
        return convex

#Conversion of polygons after finished searching
def convert_polygon(letter):
    for i in range(len(polygon)):
        for j in range(len(polygon[0])):
            if polygon[i][j] == 2:
                polygon[i][j] = letter
            elif polygon[i][j] == 3:
                polygon[i][j] = 1
    return

#Depth calculation going from start position and EW
def depth(path, vertices_list_all):
    try:
        a = path[0] #Starting point of polygon depth being counted
        depth_count = 0
        vertices_list_new = []
        for i in vertices_list_all:
            i = tuple(i[:])+(i[0],)
            vertices_list_new.append(i)
        for i in vertices_list_new:
            if winding_nb_inside(a, i, depth_count) == 'Inside':
                depth_count += 1
        return depth_count
    except IndexError:
        pass

def winding_nb_inside(startpoint, vertices_list, path_list):
    #path is current path which is to be checked
    #path_list contains all paths which should be checked
    #Using the Winding Number methodology to calculate whether point lies within polygon
    J = []
    K = []
    winding_number = 0
    vertices_length = len(vertices_list) - 1
    b = startpoint
    b0 = b[0]
    b1 = b[1]
    nb_iterations = 0
    j = 0
    if vertices_length > 0 and b != 0:
        while nb_iterations < vertices_length:
        #for i in range(0,vertices_length):
            J = list(vertices_list[nb_iterations])
            K = list(vertices_list[nb_iterations+1])
            nb_iterations += 1
            if b0 < min(K[0], J[0]) or b0 > max(J[0], K[0]):
                continue
            if J[0] <= b0 and K[0] > b0 and \
               ((K[1] - J[1]) * (b0 - J[0]) - (b1 - J[1]) * (K[0] - J[0])) < 0:
                winding_number -= 1
                j -= 1
            elif J[0] > b0 and K[0] <= b0 and \
                 ((K[1] - J[1]) * (b0 - J[0]) - (b1 - J[1]) * (K[0] - J[0])) > 0:
                winding_number += 1
                j += 1

        if winding_number != 0 and j != 0:
            return 'Inside'
        elif winding_number == 0 and j == 0:
            return 'Outside'
    else:
        pass

def vertices(path,direction):
    vertices_list = []
    vertices_index_list = []
    direction_list = []
    direction_list.append(direction[0])
    vertices_list.append(path[0])
    count = 0
    vertices_index = 0
    for i in range(len(direction)-1):
        if direction[i+1] == direction[i]:
            count += 1
        elif direction[i+1] != direction[i]:
            count += 1
            vertices_index = count
            vertices_index_list.append(vertices_index)
    vertices_index_list.append(vertices_index)
    #print(vertices_index_list)
    for i in range(len(vertices_index_list)-1):
        vertvalue = vertices_index_list[i]
        vertices_list.append(path[vertvalue])
        direction_list.append(direction[vertvalue])
    #print(vertices_list)
    #print(vertices_index_list)
    #print(vertices_list)
    return vertices_list

def invariant_rotations(vertices_list):
    #print(path)
    invariant_rotations_list = []
    #Base conditions which will be used to compare all sides
    distance_list = tuple(vertices_list[:])+(vertices_list[0],)+(vertices_list[1],)
    for i in range(0,len(distance_list)-2):
        x1 = distance_list[i][1]
        x2 = distance_list[i+1][1]
        y1 = distance_list[i][0]
        y2 = distance_list[i+1][0]
        b1_comp = distance(x1,x2,y1,y2) #Comparison side
        x1 = distance_list[i+1][1]
        x2 = distance_list[i+2][1]
        y1 = distance_list[i+1][0]
        y2 = distance_list[i+2][0]
        b2_comp = distance(x1,x2,y1,y2) #Second polygon side length
        x1 = distance_list[i][1]
        x2 = distance_list[i+2][1]
        y1 = distance_list[i][0]
        y2 = distance_list[i+2][0]
        b3_comp = distance(x1,x2,y1,y2) #Required to calculate angle
        angle_comp = angle(b1_comp, b2_comp, b3_comp)  #Comparison angle
        invariant_rotations_list.append([b1_comp, b2_comp,b3_comp, angle_comp])
    #print(invariant_rotations_list)
    invariant_comparison = deque(invariant_rotations_list[:])
    invariant_base = deque(invariant_rotations_list[:])
    nb_rotations = 0
    for i in range(len(invariant_rotations_list)):
        #print(i)
        if invariant_base == invariant_comparison:
            nb_rotations += 1
            invariant_comparison.rotate(1)
            #print("Rotating")
            #print(invariant_comparison)
        else:
            invariant_comparison.rotate(1)
    return nb_rotations

def distance(x1,x2,y1,y2):
    distance = math.hypot(x2-x1, y2-y1)
    #print(distance)
    return distance

def angle(d1,d2,d3):
    try:
        angle = math.acos((d1**2 + d2**2 - d3**2) / (2 * d1 * d2))
        angle = math.degrees(angle)
        return round(angle,)
    except ValueError:
        angle = 0
        return angle

def loadtexfile(depth, vertices, area):
    #print(vertices)
    output = '.tex'
    f_o = open(filename[:-4]+output, 'a')
    f_o.write("""\\documentclass[10pt]{article}
\\usepackage{tikz}
\\usepackage[margin=0cm]{geometry}
\\pagestyle{empty}

\\begin{document}

\\vspace*{\\fill}
\\begin{center}
\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]
""")
    f_o.close()

    max_area = max(area, key=area.get)
    max_area_value = area[max_area]
    min_area = min(area, key=area.get)
    min_area_value = area[min_area]

    #Sorted depth from lowest to highest
    sorted_depth = sorted(depth.items(), key = operator.itemgetter(1))
    #For all sorted values of depth
    #BORDER
    y_length = len(polygon)-2 #49
    x_length = len(polygon[0])-2 #50
    #print(i_length)
    #print(j_length)
    border = [(0,0), (x_length-1,0), (x_length-1,y_length-1), (0,y_length-1)]

    f_o = open(filename[:-4]+output, 'a')
    f_o.write("\draw[ultra thick] ")
    for i in range(len(border)):
        a = border
        f_o.write(f'{a[i]} -- ')
    f_o.write(f'cycle;\n')

    #For all remaining values depth/vertices
    for i in range(0,len(sorted_depth)):
        #For the polygon being assessed
        #If there is only one polygon then using a static colour value of 100
        if len(area) == 1:
            colour = 100
        else:
            colour = round((max_area_value-area[sorted_depth[i][0]])/(max_area_value-min_area_value)*100)

        #Grouping of depth values, always showing first hence i == 0
        if i == 0 or sorted_depth[i][1] != sorted_depth[i-1][1]:
            f_o.write(f'%Depth {sorted_depth[i][1]}\n')
        else:
            pass
        f_o.write(f'\\filldraw[fill=orange!{colour}!yellow] ')
        for j in range(0,len(vertices[sorted_depth[i][0]])):
            a = vertices[sorted_depth[i][0]]
            f_o.write(f'{a[j]} -- ')
        f_o.write(f'cycle;\n')

    f_o.write("""\\end{tikzpicture}
\\end{center}
\\vspace*{\\fill}

\\end{document}
""")

    #f_o.write(f'Polygon: {polygon_number}\n    Perimeter: {diagonal}*sqrt(.32)\n    Area: {area_value:.2f}\n    Convex: {convex_value}\n    Nb of invariant rotations: {rotations_value}\n    Depth: ' +"\n")

def start(polygon):
    global A
    global letter
    global path
    global direction
    global perimeter
    global returned
    global start_point
    A = 65
    polygon_number = 1
    letter = chr(A)
    path = [] #Store the polygon co-ordinates
    direction = [] #Store direction polygon travels
    returned = []
    path_list = [] #Path List
    vertices_list_all = []
    vertices_d = {}
    depth_d = {}
    area_d = {}

    #print(f'### Starting first Polygon with letter as {letter} ###')
    for i in range(len(polygon)):
        for j in range(len(polygon[0])):
    #for i in range(0,3):
    #    for j in range(0,3):
            if polygon[i][j] == 1:
                #print(f'Found 1, starting point at {i}, {j}')
                #Starting sequence
                start_point = i,j
                path.append(start_point)
                polygon[i][j] = 2
                search(i, j, letter, A)
                vertices_list = vertices(path,direction) #Vertices list of polygon being calculated
                vertices_list_all.append(vertices_list) #List of all polygon vertices
                #print(vertices_list)
                #print(f'Returned is: {returned}')
                #print(f'Polygon {polygon_number}')
                perimeter_value, diagonal = perimeter(path)
                #print(f'Perimeter: {perimeter_value:.1f} + {diagonal}*sqrt(.32)')
                area_value = area(path)
                #print(f'Area: {area_value:.2f}')
                convex_value = convexity(path)
                #print(f'Convex: {convex_value}')
                convert_polygon(letter)
                rotations_value = invariant_rotations(vertices_list)
                #print(f'Nb of invariant rotations: {rotations_value}')
                depth_value = depth(path,vertices_list_all)
                #print(f'Depth: {depth_value}')
                if texfile == False:
                    if perimeter_value == 0:
                        print(f'Polygon {polygon_number}:\n    Perimeter: {diagonal}*sqrt(.32)\n    Area: {area_value:.2f}\n    Convex: {convex_value}\n    Nb of invariant rotations: {rotations_value}\n    Depth: {depth_value}')
                    elif diagonal == 0:
                        print(f'Polygon {polygon_number}:\n    Perimeter: {perimeter_value:.1f}\n    Area: {area_value:.2f}\n    Convex: {convex_value}\n    Nb of invariant rotations: {rotations_value}\n    Depth: {depth_value}')
                    else:
                        print(f'Polygon {polygon_number}:\n    Perimeter: {perimeter_value:.1f} + {diagonal}*sqrt(.32)\n    Area: {area_value:.2f}\n    Convex: {convex_value}\n    Nb of invariant rotations: {rotations_value}\n    Depth: {depth_value}')
                else:
                    pass

                ####INITIATION OF VALUES FOR TEX FILE
                #Fixing of vertices to x and y co-ordinates
                vertices_list_2 = vertices_list_fix(vertices_list)
                vertices_d[polygon_number] = vertices_list_2
                depth_d[polygon_number] = depth_value
                area_d[polygon_number] = area_value

                ###RESETING VALUES IN PREPARATION TO FIND NEXT POLYGON###
                polygon_number += 1
                A += 1
                letter = chr(A)
                path = []
                direction = []
                vertices_list = []

    return depth_d,vertices_d, area_d

def vertices_list_fix(vertices_list):
    vertices_list_2 = []
    for k in vertices_list:
        i, j = k
        fixed_value = j-1, i-1
        vertices_list_2.append(fixed_value)
    return vertices_list_2

###GENERAL SEARCH FUNCTION###
def search(i,j,letter,A):
    #print(f'Searching at {i}, {j}')
    #East
    try:
        if (polygon[i][j+1] == 1) or \
           (polygon[i][j+1] == 2):
            #print(f'Located east of {i}, {j}')
            seeking_east(i,j)
            return
        #South east
        if (polygon[i+1][j+1] == 1) or \
           (polygon[i+1][j+1] == 2):
            #print(f'Located South East of {i}, {j}')
            seeking_southeast(i, j)
            return
        #South
        if (polygon[i+1][j] == 1) or \
           (polygon[i+1][j] == 2):
            #print(f'Located South of {i}, {j}')
            seeking_south(i,j)
            return
        #South West
        if (polygon[i+1][j-1] == 1 and j-1 >= 0) or \
           (polygon[i+1][j-1] == 2):
            #print(f'Located South West of {i}, {j}')
            seeking_southwest(i,j)
            return
        #West
        if (polygon[i][j-1] == 1 and j-1 >= 0) or \
           (polygon[i][j-1] == 2):
            #print(f'Located West of {i}, {j}')
            seeking_west(i,j)
            return
        #North
        if (polygon[i-1][j] == 1 and i-1 >= 0) or \
           (polygon[i-1][j] == 2 and i-1 >= 0):
            #print(f'Located North of {i}, {j}')
            seeking_north(i,j)
            return
        #North East
        if (polygon[i-1][j+1] == 1 and i-1 >= 0) or \
           (polygon[i-1][j+1] == 2):
            #print(f'Located North East of {i}, {j}')
            seeking_northeast(i,j)
            return
        #North West
        if (polygon[i-1][j-1] == 1 and i-1 >= 0 and j-1 >=0) or \
           (polygon[i-1][j-1] == 2):
            #print(f'Located North West of {i}, {j}')
            seeking_northwest(i,j)
            return
    except IndexError:
        return

def seeking_east(i,j):
    try:
        #Check NW
        if polygon[i-1][j-1] == 1 and i-1 >= 0 and j-1 >= 0:
            polygon[i-1][j-1] = 2
            location = i-1,j-1
            path.append(location)
            direction.append('NW')
            seeking_northwest(i-1,j-1)
        elif polygon[i-1][j-1] == 2 and i-1 >= 0:
            direction.append('NW')
            confirm_starting(i-1,j-1)
        #Check N
        elif polygon[i-1][j] == 1 and i-1 >= 0:
            polygon[i-1][j] = 2
            location = i-1,j
            path.append(location)
            direction.append('N')
            seeking_north(i-1,j)
        elif polygon[i-1][j] == 2 and i-1 >= 0:
            direction.append('N')
            confirm_starting(i-1,j)
        #Check NE
        elif polygon[i-1][j+1] == 1 and i-1 >= 0:
            polygon[i-1][j+1] = 2
            location = i-1,j+1
            path.append(location)
            direction.append('NE')
            seeking_northeast(i-1,j+1)
        elif polygon[i-1][j+1] == 2 and i-1 >= 0:
            direction.append('NE')
            confirm_starting(i-1,j+1)
        #Check E
        elif polygon[i][j+1] == 1:
            #print(f'Converting east of {i}, {j}')
            polygon[i][j+1] = 2
            location = i,j+1
            path.append(location)
            direction.append('E')
            seeking_east(i,j+1)
        #Checking if returned back to start position
        elif polygon[i][j+1] == 2:
            direction.append('E')
            confirm_starting(i,j+1)
        elif polygon[i][j+1] != 1:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_southeast(i,j):
    try:
        #Check N
        if polygon[i-1][j] == 1 and i-1 >= 0:
            polygon[i-1][j] = 2
            location = i-1,j
            path.append(location)
            direction.append('N')
            seeking_north(i-1,j)
        elif polygon[i-1][j] == 2 and i-1 >= 0:
            direction.append('N')
            confirm_starting(i-1,j)
        #Check NE
        elif polygon[i-1][j+1] == 1:
            polygon[i-1][j+1] = 2
            location = i-1,j+1
            path.append(location)
            direction.append('NE')
            seeking_northeast(i-1,j+1)
        elif polygon[i-1][j+1] == 2 and i-1 >= 0:
            direction.append('NE')
            confirm_starting(i-1,j+1)
        #Check E
        elif polygon[i][j+1] == 1:
            polygon[i][j+1] = 2
            location = i,j+1
            path.append(location)
            direction.append('E')
            seeking_east(i,j+1)
        elif polygon[i][j+1] == 2:
            direction.append('E')
            confirm_starting(i,j+1)
        #Check SE
        elif polygon[i+1][j+1] == 1:
            #print(f'Converting South East of {i}, {j}')
            polygon[i+1][j+1] = 2
            location = i+1,j+1
            path.append(location)
            direction.append('SE')
            seeking_southeast(i+1,j+1)
        elif polygon[i+1][j+1] == 2:
            direction.append('SE')
            confirm_starting(i+1,j+1)
            return
        elif polygon[i+1][j+1] != 1:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_south(i,j):
    try:
        #Check NE
        if polygon[i-1][j+1] == 1 and i-1 >= 0:
            polygon[i-1][j+1] = 2
            location = i-1,j+1
            path.append(location)
            direction.append('NE')
            seeking_northeast(i-1,j+1)
        elif polygon[i-1][j+1] == 2:
            direction.append('NE')
            confirm_starting(i-1,j+1)
        #Check E
        elif polygon[i][j+1] == 1:
            polygon[i][j+1] = 2
            location = i,j+1
            path.append(location)
            direction.append('E')
            seeking_east(i,j+1)
        elif polygon[i][j+1] == 2:
            direction.append('E')
            confirm_starting(i,j+1)
        #Check SE
        elif polygon[i+1][j+1] == 1:
            polygon[i+1][j+1] = 2
            location = i+1,j+1
            path.append(location)
            direction.append('SE')
            seeking_southeast(i+1,j+1)
        elif polygon[i+1][j+1] == 2:
            direction.append('SE')
            confirm_starting(i+1,j+1)
            return
        #Check S
        elif polygon[i+1][j] == 1:
            #print(f'Converting South of {i}, {j}')
            polygon[i+1][j] = 2
            location = i+1,j
            path.append(location)
            direction.append('S')
            seeking_south(i+1,j)
        elif polygon[i+1][j] == 2:
            direction.append('S')
            confirm_starting(i+1,j)
            return
        elif polygon[i+1][j] != 1:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_southwest(i,j):
    try:
        #Check E
        if polygon[i][j+1] == 1:
            polygon[i][j+1] = 2
            location = i,j+1
            path.append(location)
            direction.append('E')
            seeking_east(i,j+1)
        elif polygon[i][j+1] == 2:
            direction.append('E')
            confirm_starting(i,j+1)
            return
        #Check SE
        elif polygon[i+1][j+1] == 1:
            polygon[i+1][j+1] = 2
            location = i+1,j+1
            path.append(location)
            direction.append('SE')
            seeking_southeast(i+1,j+1)
        elif polygon[i+1][j+1] == 2:
            direction.append('SE')
            confirm_starting(i+1,j+1)
            return
        #Check S
        elif polygon[i+1][j] == 1:
            polygon[i+1][j] = 2
            location = i+1,j
            path.append(location)
            direction.append('S')
            seeking_south(i+1,j)
        elif polygon[i+1][j] == 2:
            direction.append('S')
            confirm_starting(i+1,j)
            return
        #Check SW
        elif polygon[i+1][j-1] == 1 and j-1 >= 0:
            #print(f'Converting South West of {i}, {j}')
            polygon[i+1][j-1] = 2
            location = i+1,j-1
            path.append(location)
            direction.append('SW')
            seeking_southwest(i+1,j-1)
        elif polygon[i+1][j-1] == 2:
            direction.append('SW')
            confirm_starting(i+1,j-1)
            return
        elif polygon[i+1][j-1] != 1:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_west(i,j):
    try:
        #Check SE
        if polygon[i+1][j+1] == 1:
            polygon[i+1][j+1] = 2
            location = i+1,j+1
            path.append(location)
            direction.append('SE')
            seeking_southeast(i+1,j+1)
        elif polygon[i+1][j+1] == 2:
            direction.append('SE')
            confirm_starting(i+1,j+1)
            return
        #Check S
        elif polygon[i+1][j] == 1:
            polygon[i+1][j] = 2
            location = i+1,j
            path.append(location)
            direction.append('S')
            seeking_south(i+1,j)
        elif polygon[i+1][j] == 2:
            direction.append('S')
            confirm_starting(i+1,j)
            return
        #Check SW
        elif polygon[i+1][j-1] == 1 and j-1 >= 0:
            polygon[i+1][j-1] = 2
            location = i+1,j-1
            path.append(location)
            direction.append('SW')
            seeking_southwest(i+1,j-1)
        elif polygon[i+1][j-1] == 2:
            direction.append('SW')
            confirm_starting(i+1,j-1)
            return
        #Check W
        elif polygon[i][j-1] == 1 and j-1 >= 0:
            #print(f'Converting West of {i}, {j}')
            polygon[i][j-1] = 2
            location = i,j-1
            path.append(location)
            direction.append('W')
            seeking_west(i,j-1)
        elif polygon[i][j-1] == 2:
            direction.append('W')
            confirm_starting(i,j-1)
            return
        elif polygon[i][j-1] != 1 and j-1 >= 0:
            search(i,j,letter,A)
    except IndexError:
        pass

def seeking_northwest(i,j):
    try:
        #Check S
        if polygon[i+1][j] == 1:
            polygon[i+1][j] = 2
            location = i+1,j
            path.append(location)
            direction.append('S')
            seeking_south(i+1,j)
        elif polygon[i+1][j] == 2:
            direction.append('S')
            confirm_starting(i+1,j)
        #Check SW
        elif polygon[i+1][j-1] == 1:
            polygon[i+1][j-1] = 2
            location = i+1,j-1
            path.append(location)
            direction.append('SW')
            seeking_southwest(i+1,j-1)
        elif polygon[i+1][j-1] == 2:
            direction.append('SW')
            confirm_starting(i+1,j-1)
        #Check W
        elif polygon[i][j-1] == 1 and i-1 >= 0:
            polygon[i][j-1] = 2
            location = i,j-1
            path.append(location)
            direction.append('W')
            seeking_west(i,j-1)
        elif polygon[i][j-1] == 2:
            direction.append('W')
            confirm_starting(i,j-1)
        #Check NW
        elif polygon[i-1][j-1] == 1 and i-1 >= 0 and j-1 >= 0:
            #print(f'Converting North West of {i}, {j}')
            polygon[i-1][j-1] = 2
            location = i-1,j-1
            direction.append('NW')
            path.append(location)
            seeking_northwest(i-1,j-1)
        elif polygon[i-1][j-1] == 2:
            #print("Validating if returned to start..a...")
            direction.append('NW')
            confirm_starting(i-1,j-1)
            return
        elif polygon[i-1][j-1] != 1 and j-1 >= 0 and i-1 >=0:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_north(i,j):
    try:
        #Check SW
        if polygon[i+1][j-1] == 1 and j-1 >= 0:
            polygon[i+1][j-1] = 2
            location = i+1,j-1
            path.append(location)
            direction.append('SW')
            seeking_southwest(i+1, j-1)
        elif polygon[i+1][j-1] == 2:
            direction.append('SW')
            confirm_starting(i+1,j-1)
        #Check W
        elif polygon[i][j-1] == 1:
            polygon[i][j-1] = 2
            location = i,j-1
            path.append(location)
            direction.append('W')
            seeking_west(i,j-1)
        elif polygon[i][j-1] == 2:
            direction.append('W')
            confirm_starting(i,j-1)
        #Check NW
        elif polygon[i-1][j-1] == 1 and j-1 >= 0 and i-1 >= 0:
            polygon[i-1][j-1] = 2
            location = i-1,j-1
            path.append(location)
            direction.append('NW')
            seeking_northwest(i-1,j-1)
        elif polygon[i-1][j-1] == 2:
            direction.append('NW')
            confirm_starting(i-1,j-1)
        #Check N
        elif polygon[i-1][j] == 1 and i-1 >= 0:
            #print(f'Converting North of {i}, {j}')
            polygon[i-1][j] = 2
            location = i-1,j
            path.append(location)
            direction.append('N')
            seeking_north(i-1,j)
        elif polygon[i-1][j] == 2:
            #print("Validating if returned to start..a...")
            direction.append('N')
            confirm_starting(i-1,j)
            return
        elif polygon[i-1][j] != 1 and i-1 >=0:
            search(i,j,letter,A)
    except IndexError:
        return

def seeking_northeast(i,j):
    try:
        #Check W
        if polygon[i][j-1] == 1 and j-1 >= 0:
            polygon[i][j-1] = 2
            location = i,j-1
            path.append(location)
            direction.append('W')
            seeking_west(i,j-1)
        elif polygon[i][j-1] == 2:
            direction.append('W')
            confirm_starting(i,j-1)
        #Check NW
        elif polygon[i-1][j-1] == 1 and i-1 >=0 and j-1 >=0:
            polygon[i-1][j-1] = 2
            location = i-1,j-1
            path.append(location)
            direction.append('NW')
            seeking_northwest(i-1,j-1)
        elif polygon[i-1][j-1] == 2:
            direction.append('NW')
            confirm_starting(i-1,j-1)
        #Check N
        elif polygon[i-1][j] == 1 and i-1 >= 0:
            polygon[i-1][j] = 2
            location = i-1,j
            path.append(location)
            direction.append('N')
            seeking_north(i-1,j)
        elif polygon[i-1][j] == 2:
            direction.append('N')
            confirm_starting(i-1,j)
        #Check NE
        elif polygon[i-1][j+1] == 1:
            #print(f'Converting North East of {i}, {j}')
            polygon[i-1][j+1] = 2
            location = i-1,j+1
            path.append(location)
            direction.append('NE')
            seeking_northeast(i-1,j+1)
        elif polygon[i-1][j+1] == 2:
            #print("Validating if returned to start..a...")
            direction.append('NE')
            confirm_starting(i-1,j+1)
            return
        elif polygon[i-1][j+1] != 1 and i-1 >=0:
            search(i,j,letter,A)
    except IndexError:
        return

def confirm_starting(i,j):
    return_point = i,j
    #print(path)
    #print(f'Start point: {start_point}')
    #print(f'Return point: {return_point}')
    if start_point == return_point:
        #print(f'### Success polygon {letter} returned to start ###')
        returned.append(start_point)
        returned.append(return_point)
        return
    else:
        direction.pop()
        backtrack(i,j)

def backtrack(i,j):
    #print(f'Backtracking from {i}, {j}')
    path_i, path_j = path[-1]
    #Return back to junction where theres more than one path
    for i in range(0, len(path)):
        if polygon[path_i-1][path_j+1] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i-1,path_j+1
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('NE')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i][path_j+1] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i,path_j+1
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('E')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i+1][path_j] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i+1,path_j
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('S')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i+1][path_j-1] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i+1,path_j
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('SW')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i][path_j-1] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i+1,path_j
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('W')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i-1][path_j-1] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i+1,path_j
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('NW')
                returned.append(start_point)
                returned.append(return_point)
                return
        elif polygon[path_i-1][path_j] == 2:
            #print(f'Found at {path_i}, {path_j}')
            return_point = path_i+1,path_j
            if start_point == return_point:
                #print(f'### Success polygon {letter} returned to start ###')
                direction.append('N')
                returned.append(start_point)
                returned.append(return_point)
                return
        else:
            pass
        if polygon[path_i][path_j+1] == 1 or polygon[path_i+1][path_j+1] == 1 or \
           polygon[path_i+1][path_j] == 1 or (polygon[path_i+1][path_j-1] == 1 and path_j-1 >= 0) or \
           (polygon[path_i][path_j-1] == 1 and path_j >= 0) or (polygon[path_i-1][path_j-1] == 1 and path_i-1 >=0 and path_j >= 0) or \
           (polygon[path_i-1][path_j] == 1 and path_i >= 0) or (polygon[path_i-1][path_j+1] == 1 and path_i-1 >= 0):
           #print(f'Alternative path found at {path_i}, {path_j}')
           search(path_i, path_j, letter,A)
           return
        else:
            #print(f'No alternative paths found at {path_i}, {path_j}...checking next location')
            polygon[path_i][path_j] = 3
            path.pop()
            direction.pop()
            path_i, path_j = path[-1]

try:
    #Loading in files from commandline
    global texfile
    parser = ArgumentParser()
    parser.add_argument('--file', dest = 'filename', required = True)
    parser.add_argument('-print', dest = 'texfile', required = False, action = 'store_true')
    args = parser.parse_args()
    filename = args.filename
    texfile = args.texfile

    #Load polygon, if indexerror due to file being blank then exit
    try:
        loadPolygon(filename)
    except IndexError:
        print("Cannot get polygons as expected.")
        #output = '_output.txt'
        #f_o = open(filename[:-4]+output, 'w')
        #f_o.write("Cannot get polygons as expected.")
        #f_o.close()
        #print("Cannot get polygons as expected.")
        sys.exit()

    #Load polygon successful and file is not blank
    polygon_check = polygon[:]
    check_value = checkgrid(polygon_check)
    if check_value == True:
        parser = ArgumentParser()
        parser.add_argument('--file', dest = 'filename', required = True)
        parser.add_argument('-print', dest = 'texfile', required = False, action = 'store_true')
        args = parser.parse_args()
        filename = args.filename
        texfile = args.texfile
        loadPolygon(filename)
        #Main function to start program
        depth_d, vertices_d, area_d = start(polygon)

        #Checking whether print -print included in command line to print tex file
        if texfile == True:
            #print("WE NEED TEX FILE")
            loadtexfile(depth_d, vertices_d, area_d)
        elif texfile == False:
            #print("WE DONT NEED TEX FILE")
            pass

    elif check_value == False:
        print("Cannot get polygons as expected.")
        #output = '_output.txt'
        #f_o = open(filename[:-4]+output, 'w')
        #f_o.write("Cannot get polygons as expected.\n")
        #f_o.close()
        #print("Cannot get polygons as expected.\n")
        sys.exit()
    #printPolygon()
except FileNotFoundError:
    print(f'Incorrect input.')
except OSError:
    print(f'Incorrect input.')
