import os.path
import sys

from collections import defaultdict

input_values = [5, 10, 14, 15, 20, 25, 26, 27, 28, 30 ,31]
#input_values = [5, 8, 11, 14]

def remove_pillars(input_values):
    pillars_d = {}
    for i in range(1,len(input_values)):
        for j in range(i,0,-1):
            try:
                slope = input_values[i] - input_values[i-j]
                if slope in pillars_d:
                    pillars_d[slope] += 1
                else:
                    pillars_d[slope] = 1
            except IndexError:
                continue

    #Extrapolate maximum key and value
    max_pillar = max(pillars_d, key = pillars_d.get)
    print(max_pillar)
    print(pillars_d[max_pillar])
    min_remove_pillars = len(input_values) - pillars_d[max_pillar] - 1
    print(pillars_d)
    return min_remove_pillars

min_remove_pillars = remove_pillars(input_values)
remove_pillars(input_values)
print(f'The minimal number of pillars to remove to build a perfect ride from the rest is: {min_remove_pillars}')
