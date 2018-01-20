import re


class DiffCommands:
    #DiffCommands can raise DiffCOmmandsError with a message if error
    #Print function for DiffCommands
    #Reference: http://stackoverflow.com/questions/1535327/how-to-print-a-class-or-objects-of-class-using-print

    #Initialisation of input values with self so can access functions within the DiffCommands class
    import re
    
    
    def __init__(self, input_file):
        self.input_file = input_file
        #Empty list diff to store diff commands
        self.diff = []
        #List containing converted #,#[a,c,d]#,# format
        self.diff_converted = []
        #Initial value to do checking
        self.diff_converted.append([0,0,0,0])
        f_o = open(self.input_file, 'r').readlines()
        self.count = 0
        for line in f_o:
            regex_match = re.match('^(\d+)((,)(\d+))?(c)(\d+)((,)(\d+))?$|^(\d+)(a)(\d+)((,)(\d+))?$|^(\d+)((,)(\d+))?(d)(\d+)$|^(\d+)((,)(\d+))?(d)(\d+)$',line)
            # Regression expression:
            # ^ = Start of string $ = End of string or just before new line + = Match 1 or more repetitions
            # ? = Optional ab? will match a or ab
            #Check make sure string is in the correct format ie. d,d?cd,d? | dad,d? | d,d?dd |
            if bool(regex_match) == False:
                raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
            #Check whether d then if right most > 0 (wrong_5.txt)
            #Subgroups numbered from left to right. Count based on opening parenthesis characters from left to right
            #Reference: https://docs.python.org/3/howto/regex.html - Search re.compile
            elif bool(regex_match) == True:
                self.diff.append(line)
                self.count += 1
        
        #Conversion based on position rather than line number
            ##CHANGE - #c#
            if (regex_match.group(9) == None) and (regex_match.group(5) == 'c'):
                position = [int(regex_match.group(1)) - 1, int(regex_match.group(1)), int(regex_match.group(6)) - 1, int(regex_match.group(6)), 1]
                self.diff_converted.append(position)
            ##CHANGE - #,#c#,#
            elif regex_match.group(9) != None and (regex_match.group(5) == 'c'):
                position = [int(regex_match.group(1)) - 1, int(regex_match.group(4)), int(regex_match.group(6)) - 1, int(regex_match.group(9)), 1]
                self.diff_converted.append(position)
                
            #Range if diff is delete (d)
            ##DELETE - #,#d#
            elif (regex_match.group(19) == None) and (regex_match.group(20) == 'd'):
                position = [int(regex_match.group(16)) - 1, int(regex_match.group(16)), int(regex_match.group(21)), int(regex_match.group(21)), 1]
                self.diff_converted.append(position)
            ##DELETE - #d#
            elif regex_match.group(19) != None and (regex_match.group(20) == 'd'):
                position = [int(regex_match.group(16)) - 1, int(regex_match.group(19)), int(regex_match.group(21)), int(regex_match.group(21)), 1]
                self.diff_converted.append(position)
                    
            ##APPEND - ##a#,#
            elif regex_match.group(13) != None and (regex_match.group(11) == 'a'):
                position = [int(regex_match.group(10)), int(regex_match.group(10)), int(regex_match.group(12)) - 1, int(regex_match.group(15)), 1]
                self.diff_converted.append(position)
            ##APPEND - #a#
            elif regex_match.group(13) == None and (regex_match.group(11) == 'a'):
                position = [int(regex_match.group(10)), int(regex_match.group(10)), int(regex_match.group(12)) - 1, int(regex_match.group(12)), 1]
                self.diff_converted.append(position)
                                   
        #Conversion completed based on position rather than line number
        #Check whether difference between consecutive numbers on left and right side same and != 0 (wrong_6.txt, wrong_7.txt)
        for i in range(0,len(self.diff_converted)-1):
            if (self.diff_converted[i+1][0] - self.diff_converted[i][1]) != (self.diff_converted[i+1][2] - self.diff_converted[i][3]):
                raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
            if (self.diff_converted[i+1][0] - self.diff_converted[i][1]) == 0 and i != 0:
                raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
            if (self.diff_converted[i+1][2] - self.diff_converted[i][3]) == 0 and i != 0:
                raise DiffCommandsError("Cannot possibly be the commands for the diff of two file")
            
    def original(self):
        f_o_original = open(self.input_file, 'r').readlines()
        return f_o_original
    
    def conversion(self):
        #Empty list diff to store diff commands
        self.diff = []
        #Count number of matching lines in diff file
        self.diff_converted = []
        f_o = open(self.input_file, 'r').readlines()
        self.count = 0
        for line in f_o:
            regex_match = re.match('^(\d+)((,)(\d+))?(c)(\d+)((,)(\d+))?$|^(\d+)(a)(\d+)((,)(\d+))?$|^(\d+)((,)(\d+))?(d)(\d+)$',line)
            # Regression expression:
            # ^ = Start of string $ = End of string or just before new line + = Match 1 or more repetitions
            # ? = Optional ab? will match a or ab
            #Check make sure string is in the correct format ie. d,d?cd,d? | dad,d? | d,d?dd |
            if bool(regex_match) == False:
                raise DiffCommandsError("Cannot possibly be the commands for the diff of two files")
            #Check whether d then if right most > 0 (wrong_5.txt)
            #Subgroups numbered from left to right. Count based on opening parenthesis characters from left to right
            #Reference: https://docs.python.org/3/howto/regex.html - Search re.compile
            #elif bool(regex_match) == True:
            if bool(regex_match) == True:
                self.diff.append(line)
                self.count += 1
    
        #Conversion based on position rather than line number
            ##CHANGE - #c#
            if (regex_match.group(9) == None) and (regex_match.group(5) == 'c'):
                position = [int(regex_match.group(1)) - 1, int(regex_match.group(1)), int(regex_match.group(6)) - 1, int(regex_match.group(6)),1]
                self.diff_converted.append(position)
            #,#c#,#
            elif regex_match.group(9) != None and (regex_match.group(5) == 'c'):
                position = [int(regex_match.group(1)) - 1, int(regex_match.group(4)), int(regex_match.group(6)) - 1, int(regex_match.group(9)),1]
                self.diff_converted.append(position)
                
            ##DELETE - #,#d# 
            elif (regex_match.group(19) == None) and (regex_match.group(20) == 'd'):
                position = [int(regex_match.group(16)) - 1, int(regex_match.group(16)), int(regex_match.group(21)), int(regex_match.group(21)),1]
                self.diff_converted.append(position)
            #d#
            elif regex_match.group(19) != None and (regex_match.group(20) == 'd'):
                position = [int(regex_match.group(16)) - 1, int(regex_match.group(19)), int(regex_match.group(21)), int(regex_match.group(21)),1]
                self.diff_converted.append(position)
                    
            ##APPEND - ##a#,#
            elif regex_match.group(13) != None and (regex_match.group(11) == 'a'):
                position = [int(regex_match.group(10)), int(regex_match.group(10)), int(regex_match.group(12)) - 1, int(regex_match.group(15)),1]
                self.diff_converted.append(position)
            #a#
            elif regex_match.group(13) == None and (regex_match.group(11) == 'a'):
                position = [int(regex_match.group(10)), int(regex_match.group(10)), int(regex_match.group(12)) - 1, int(regex_match.group(12)),1]
                self.diff_converted.append(position)
    
        return self.diff_converted
        
    #Convert object to a string to allow printing
    def __str__(self):
        if self.count == len(self.diff):
            f_o = open(self.input_file, 'r')
            print_file = f_o.read()
            return print_file[:-1]
        else:
            raise DiffCommandsError("Cannot possibly be the commands for the diff of two files") 
     
  
        #Undertake error checking on wrong files
        #Check each line to make sure all lower case. If upper case then error
        #Check make sure there is no extra line at end of file


#Declare custom exceptions in Python
class DiffCommandsError(Exception):
    def __init__(self, message):
        self.message = message
    
class OriginalNewFiles:
    #Initialise input values
    def __init__(self, file_one = None, file_two = None):
        if file_one == None or file_two == None:
            print("Error please input two file names")
        else:
            self.file_one = file_one
            self.file_two = file_two
            #Read in contents from file_1 and file_2 and create list
            #Strip the /n from the end of each list
            with open(self.file_one) as open_file_one:
                self.content_file_one = open_file_one.readlines()
                self.content_file_one = [x.strip() for x in self.content_file_one]
            with open(self.file_two) as open_file_two:
                self.content_file_two = open_file_two.readlines()
                self.content_file_two = [x.strip() for x in self.content_file_two]
                
    def is_a_possible_diff(self,diff_output):
        #Calculate the LCS of the two input files.
        #Reference: https://stackoverflow.com/questions/24547641/python-length-of-longest-common-subsequence-of-lists
        self.diff_output = diff_output
        diff_converted = diff_output.conversion()
        #Insert an initial value of [0,0,0,0] into front of list
        diff_converted.insert(0,[0]*4)
        #Insert last values to bottom of list
        diff_converted.append([len(self.content_file_one), len(self.content_file_one), len(self.content_file_two), len(self.content_file_two)])

        #Calculation of LCS based on diff_x.txt
        #LCS of Left and Right Side
        self.lcs_left = 0
        self.lcs_right = 0
        for i in range(len(diff_converted) - 1):
            difference_left = diff_converted[i+1][0] - diff_converted[i][1]
            difference_right = diff_converted[i+1][2] - diff_converted[i][3]
            #print(difference)
            self.lcs_left += difference_left
            self.lcs_right += difference_right
        #self.lcs_left = self.lcs_left + 1
        #self.lcs_right = self.lcs_right + 1
        #print(self.lcs_left, self.lcs_right)

        #CALCULATING NUMBER OF MATCHED LINES (LCS Function and Intersection methodologies)
        LCS_array = [[0] * (len(self.content_file_two) + 1) for _ in range(len(self.content_file_one) + 1)]
        for i, ca in enumerate(self.content_file_one, 1):
            for j, cb in enumerate(self.content_file_two, 1):
                LCS_array[i][j] = (
                    LCS_array[i - 1][j - 1] + 1 if ca == cb else
                    max(LCS_array[i][j - 1], LCS_array[i - 1][j]))
        self.LCS = LCS_array[-1][-1]
        #print(self.LCS)

        #Calculate the number of matched lines between two input files.
        #set = Unordered collection with no duplicate elements
        #intersection = Finds matching values or intersects between two file types
        same = set(self.content_file_one).intersection(self.content_file_two)

        #Checking whether lines actually match
        file_check_1 = []
        file_check_2 = []
        count = 0
        try: 
            for i in range(0,len(diff_converted)-1):
                for j in range(diff_converted[i][1], diff_converted[i+1][0]):
                    file_check_1.append(self.content_file_one[j])
                for k in range(diff_converted[i][3], diff_converted[i+1][2]):
                    file_check_2.append(self.content_file_two[k])

            
                for i in range(len(file_check_1)):
                    if file_check_1[i] == file_check_2[i]:
                        count += 1
                #LCS must be same as matched lines
                if (self.lcs_left == self.lcs_right) and self.LCS == self.lcs_right:
                    if count == len(file_check_1):
                        return True
                else:
                    return False
        except IndexError:
            return False


    def output_diff(self, diff_output):
        self.diff_output = diff_output
        diff_converted = diff_output.conversion()
        diff_original = diff_output.original()
        diff_original = [x.strip() for x in diff_original]
        #self.content_file_one
        #self.content_file_two
        #print(diff_converted)
        #print(diff_original)
        for i in range(len(diff_converted)):
            #Diff print statement for Change - c 
            if (diff_converted[i][1] != diff_converted[i][0]) and (diff_converted[i][3] != diff_converted[i][2]):
                print(diff_original[i])
                if diff_converted[i][0] != diff_converted[i][1]:
                    for j in range(diff_converted[i][0], diff_converted[i][1]):
                        print(f'< {self.content_file_one[j]}')
                if diff_converted[i][2] != diff_converted[i][3]:
                    print('---')
                    for k in range(diff_converted[i][2], diff_converted[i][3]):
                        print(f'> {self.content_file_two[k]}')
            #Diff print statement for Delete - D                
            elif diff_converted[i][1] != diff_converted[i][0] and diff_converted[i][2] == diff_converted[i][3]:
                print(diff_original[i])
                for n in range(diff_converted[i][0], diff_converted[i][1]):
                    print(f'< {self.content_file_one[n]}')
            
            elif diff_converted[i][1] == diff_converted[i][0]:
                print(diff_original[i])
                for m in range(diff_converted[i][2], diff_converted[i][3]):
                    print(f'> {self.content_file_two[m]}')

    def output_unmodified_from_original(self, diff_output):
        self.diff_output = diff_output
        diff_converted = diff_output.conversion()
        diff_original = diff_output.original()
        diff_original = [x.strip() for x in diff_original]

        #Insert an initial value of [0,0,0,0] into front of list
        diff_converted.insert(0,[0]*4)
        #Insert last values to bottom of list
        diff_converted.append([len(self.content_file_one), len(self.content_file_one), len(self.content_file_two), len(self.content_file_two)])

        #print(diff_converted)
        #print(self.content_file_one)
        
        try:
            for i in range(len(diff_converted)):
                if diff_converted[i][0] != diff_converted[i][1]:
                    print('...')
                for j in range(diff_converted[i][1], diff_converted[i+1][0]):
                    print(f'{self.content_file_one[j]}')
        except IndexError:
            pass
            
    def output_unmodified_from_new(self, diff_output):
        self.diff_output = diff_output
        diff_converted = diff_output.conversion()
        diff_original = diff_output.original()
        diff_original = [x.strip() for x in diff_original]

        #Insert an initial value of [0,0,0,0] into front of list
        diff_converted.insert(0,[0]*4)
        #Insert last values to bottom of list
        diff_converted.append([len(self.content_file_one), len(self.content_file_one), len(self.content_file_two), len(self.content_file_two)])
        #print(diff_converted)
        #print(self.content_file_two)
        
        try:
            for i in range(len(diff_converted)):
                if diff_converted[i][2] != diff_converted[i][3]:
                    print('...')
                #if diff_converted[i][3] != diff_converted[i][2]:
                for k in range(diff_converted[i][3], diff_converted[i+1][2]):
                    print(f'{self.content_file_two[k]}')
                
        except IndexError:
            pass

    def get_all_diff_commands(self):
        self.content_file_one
        self.content_file_two
        self.diff_list = []
        self.diff_list.append(self.content_file_one)
        return self.diff_list
