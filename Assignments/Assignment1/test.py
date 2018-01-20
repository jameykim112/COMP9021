input_values = ['5 8', '11 14']
value = []
for i in range(0, len(input_values)):
    #print(input_values[i])

    value = value + [int(i) for i in input_values[i].split()]

    print(value)
input_values = value
    #input_values_1 = input_values_1.extend(value)

#If all values on one line
    if len(input_values) <= 1:
        input_values = input_values[0]
        try:
            input_values =[int(i) for i in input_values.split()]
        except ValueError:
            print('Incorrect input, giving up. Not all int')
            sys.exit()
