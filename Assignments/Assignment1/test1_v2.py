import os.path
import sys

from collections import defaultdict

input_values = [5, 10, 14, 15, 20, 25, 26, 27, 28, 30 ,31]
input_values = [5, 8, 11, 14]
input_values = [10, 13, 20, 30, 40, 42, 44, 46, 48, 50, 60, 70, 80, 82, 85, 87, 90, 100, 101, 110, 113, 117, 121]

def remove_pillars(input_values):
    pillars_d = {}
    pillars_d_value = {}
    for i in range(1,len(input_values)):
        for j in range(i,0,-1):
            try:
                slope = input_values[i] - input_values[i-j]
                if slope in pillars_d:
                    pillars_d[slope] += 1
                    pillars_d_value[slope].append(input_values[i])
                else:
                    pillars_d[slope] = 1
                    pillars_d_value[slope] = [input_values[i]]
            except IndexError:
                continue

    #Extrapolate maximum key and value
    max_pillar = max(pillars_d, key = pillars_d.get)
    #print(max_pillar)
    #print(pillars_d[max_pillar])

    #print(pillars_d)
    print(pillars_d_value)
    max_pillar_value = max(pillars_d_value, key = pillars_d.get)
    print("The max pillar is: ", max_pillar_value)
    max_pillars_value_list = pillars_d_value[max_pillar_value]
    print("The values in max pillar are: ", max_pillars_value_list)

    count = 2
    count_list = []
    slope_value = max_pillar_value
    for i in range(1, len(max_pillars_value_list)):
        print("The slope value is: ", slope_value)
        print("The slope value is", max_pillars_value_list[i] )
        print("The second slope value is:", max_pillars_value_list[i-1] + slope_value)
        if max_pillars_value_list[i] == max_pillars_value_list[i-1] + slope_value:
            count += 1
        else:
            count_list.append(count)
            count = 0
        count_list.append(count)
        print("The count is: ", count)

    min_remove_pillars = len(input_values) - max(count_list)
    return min_remove_pillars

min_remove_pillars = remove_pillars(input_values)
print(f'The minimal number of pillars to remove to build a perfect ride from the rest is: {min_remove_pillars}')
