import os.path
import sys
from collections import deque

#Program functions
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
    #print(input_values)
    #If all values on one line

    #Make sure read and convert to int values on different lines
    if len(input_values) > 0:
        try:
            #input_values =[int(i) for i in input_values]
            for i in range(0, len(input_values)):
                value = value + [int(i) for i in input_values[i].split()]
            input_values = value
        except ValueError:
            print('Sorry, input file does not store valid data')
            sys.exit()
    return input_values

def check_values(input_values):
    negative_numbers = sum(1 for number in input_values if number <= 0)
    #Check make sure greater than 2 values in list
    if len(input_values) < 3:
        print("Sorry, input file does not store valid data")
        sys.exit()
    #Check make sure no negative values in list
    elif negative_numbers > 0:
        print("Sorry, input file does not store valid data")
        sys.exit()
    #Check make sure consecutive numbers increasing
    else:
        for i in range(0, len(input_values) - 1):
            if input_values[i+1] > input_values[i]:
                continue
            else:
                print("Sorry, input file does not store valid data")
                sys.exit()
    #print("Checked input values all good")
    return

def perfect_ride(input_values):
    increment = input_values[1] - input_values[0]
    #print("Increment required for perfect ride is:", increment)
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

def pillar_removal(input_values):
    if longest_good_ride == len(input_values) - 1:
        min_pillar_removal = 0

    return min_pillar_removal

#Main program body
try:
    input_file_name = input("Please enter the name of the file you want to get data from: ")
    input_values = import_values(input_file_name)
    check_values(input_values)
    perfect_ride = perfect_ride(input_values)
    longest_good_ride = longest_good_ride(input_values)
    print("The longest good ride has a length of: ", longest_good_ride)
    min_pillar_removal = pillar_removal(input_values)
    print("The minimal number of pillars to remove to build a perfect ride from the rest is: ", min_pillar_removal)

except FileNotFoundError:
    print("Sorry, there is no such file.")
    sys.exit()
