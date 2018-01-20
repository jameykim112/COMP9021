

def perfect_ride(input_values):
    increment = input_values[1] - input_values[0]
    print("Increment required for perfect ride is:", increment)
    perfect_ride_count = 1
    for i in range(0, len(input_values) - 1):
        if input_values[i+1] - input_values[i] == increment:
            perfect_ride_count += 1
    if perfect_ride_count == len(input_values):
        print("The ride is perfect!")
        print("The longest good ride has a length of: ", perfect_ride_count - 1)
    else:
        print("The ride could be better...")
        #print("The input value length is: ", len(input_values))
        #print("The perfect_ride_count is: ", perfect_ride_count)

def longest_good_ride(input_values):
    count = 0
    longest_list = []

    for i in range(0,len(input_values)-1):
        slope = input_values[i+1] - input_values[i]
        count = 0
        print("The slope is: ", slope)
        print("I is: ", i)
        for j in range(i,len(input_values)-1):
            print("j is: ",j)
            if input_values[j] + slope == input_values[j+1]:
                count += 1
                print("Count is:", count)
            else:
                longest_list.append(count)
                print("List is: ", longest_list)
                count = 0
                break
            longest_list.append(count)
            print("List is: ", longest_list)
    return max(longest_list)



#input_values = [5, 8, 11, 14]
input_values = [5, 8, 11, 14]
#perfect_ride(input_values)
longest_good_ride = longest_good_ride(input_values)
print("The longest good ride has length of: ", longest_good_ride)
#consecutive_ride(input_values)
