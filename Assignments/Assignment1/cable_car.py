import os.path
import sys

from collections import defaultdict

#### Program functions ####
def import_values(input_file_name):
    #Reading in values from txt file
    input_values = []
    value = []
    with open(input_file_name) as _:
        for line in _:
            line = line.strip()
            if line:
                input_values.insert(0,line)
    input_values.reverse()

    #Make sure read and convert to int values on different lines
    if len(input_values) > 0:
        try:
            #input_values =[int(i) for i in input_values]
            for i in range(0, len(input_values)):
                value = value + [int(i) for i in input_values[i].split()]
            input_values = value
        except ValueError:
            print('Sorry, input file does not store valid data.')
            sys.exit()
    return input_values

def check_values(input_values):
    negative_numbers = sum(1 for number in input_values if number <= 0)
    #Check make sure greater than 2 values in list
    if len(input_values) < 3:
        print("Sorry, input file does not store valid data.")
        sys.exit()
    #Check make sure no negative values in list
    elif negative_numbers > 0:
        print("Sorry, input file does not store valid data.")
        sys.exit()
    #Check make sure consecutive numbers increasing
    else:
        for i in range(0, len(input_values) - 1):
            if input_values[i+1] > input_values[i]:
                continue
            else:
                print("Sorry, input file does not store valid data.")
                sys.exit()
    return

def perfect_ride(input_values):
    increment = input_values[1] - input_values[0]
    perfect_ride_count = 1
    for i in range(0, len(input_values) - 1):
        if input_values[i+1] - input_values[i] == increment:
            perfect_ride_count += 1
    if perfect_ride_count == len(input_values):
        perfect_ride_statement = print("The ride is perfect!")
    else:
        perfect_ride_statement = print("The ride could be better...")
    return perfect_ride_statement

def longest_good_ride(input_values):
    count = 0
    longest_list = []

    for i in range(0,len(input_values)-1):
        slope = input_values[i+1] - input_values[i]
        count = 0
        for j in range(i,len(input_values)-1):
            if input_values[j] + slope == input_values[j+1]:
                count += 1
            else:
                longest_list.append(count)
                count = 0
                break
            longest_list.append(count)
    return max(longest_list)

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
    max_pillar_value = max(pillars_d_value, key = pillars_d.get)
    max_pillars_value_list = pillars_d_value[max_pillar_value]

    #Checking values for maximum key to ensure perfect ride
    count = 2
    count_list = []
    slope_value = max_pillar_value
    for i in range(1, len(max_pillars_value_list)):
        if max_pillars_value_list[i] == max_pillars_value_list[i-1] + slope_value:
            count += 1
        else:
            count_list.append(count)
            continue
        count_list.append(count)

    min_remove_pillars = len(input_values) - max(count_list)
    return min_remove_pillars

#Main program body
try:
    input_file_name = input("Please enter the name of the file you want to get data from: ")
    input_values = import_values(input_file_name)
    check_values(input_values)
    perfect_ride = perfect_ride(input_values)
    longest_good_ride = longest_good_ride(input_values)
    print("The longest good ride has a length of:", longest_good_ride)
    min_remove_pillars = remove_pillars(input_values)
    remove_pillars(input_values)
    print(f'The minimal number of pillars to remove to build a perfect ride from the rest is: {min_remove_pillars}')

except FileNotFoundError:
    print("Sorry, there is no such file.")
    sys.exit()
