# Martin Pleynet

import doctest
import matplotlib.pyplot as plt
import numpy as np
NAME = 'Martin Pleynet'

# create a patient class with 9 attributes representing
# each column of the cleaned data
class Patient:
    def __init__(self, num, day_diagnosed, age, sex_gender, postal, state, temps, days_symptomatic):
        # initilaize constants
        NUMBERS = '0123456789.'
        MALE = 'MHB'
        FEMALE = 'FWG'

    ## initialize all 9 attributes
        self.num = int(num)
        self.day_diagnosed = int(day_diagnosed)
        self.age = int(age)

        # change sex gender to either M, F, or X
        if sex_gender[0] in MALE:
            sex_gender = 'M'
        elif sex_gender[0] in FEMALE:
            sex_gender = 'F'
        else:
            sex_gender = 'X'
        self.sex_gender = sex_gender

        # change postal code to first 3 characters
        if postal[0] == 'H':
            if postal[1].isdigit():
                if postal[2].isalpha():
                    postal = postal[0:3]
        # if not a valid postal code, default to 000
        else:
            postal = '000'
        self.postal = postal

        self.state = state

        # initialize temperature list
        self.temps = []

        # assign non valid temepratures to 0 (case of n-a)
        if not temps[0].isdigit():
            temps = 0.0
        else:
            # replace comma with period
            temps = temps.replace(',', '.')
            # remove any char that is not a number or period
            for char in temps:
                if char not in NUMBERS:
                    temps = temps.replace(char, '')
                    
        # if temperature greater than 45 convert to celsius
        if float(temps) > 45:
            temps = round((float(temps) - 32) / 1.8, 2)
            self.temps.append(temps)
        else:
            self.temps.append(temps)
            
        self.days_symptomatic = int(days_symptomatic)

    def __str__(self):
        """
        Takes patient and represents it as a string representation
        
        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> #print(str(p))
        #0\t42\tF\tH3Z\t0\tI\t12\t39.0
        """
        # initialize empty string
        temp_str = ''
        # iterate through temp list and append values to string with
        # semicolons in between each temp
        for t in range(len(self.temps)):
            temp_str += str(self.temps[t])
            if t != len(self.temps) - 1:
                temp_str += ';'

        # store all of patient attributes in attributes list
        attributes = [str(self.num), str(self.age), str(self.sex_gender), \
                      str(self.postal), str(self.day_diagnosed), \
                      str(self.state), str(self.days_symptomatic), str(temp_str)]
        return '\t'.join(attributes)
    

    def update(self, p1):
        """ (patient object) -> (patient object)

        Take patient object as an input and if attributes match
        update self to represent cahnges in input patient object
        
        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2F', '12')
        >>> p1 = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'R', '103.4', '15')
        >>> p.update(p1)
        >>> print(str(p))
        0       42      F       H3Z     0       R       12      39.0;39.67
        """
        # check id num, postal, and sex gender attributes are the same
        # in the two patient objects
        if self.num == p1.num:
            if self.sex_gender == p1.sex_gender:
                if self.postal == p1.postal:
                    # assign input patient attributes to self
                    self.days_symptomatic = p1.days_symptomatic
                    self.state = p1.state
                    self.temps.extend(p1.temps)

        # if attributes don't match for both patients raise an error
        else:
            raise AssertionError("Attributes don't match")


def stage_four(input_filename, output_filename):
    """ (str, str) -> dict

    Takes file as input and returns a dictionary with keys as each patient
    number and values the patient object associated with key number
    
    >>> p1 = stage_four('stage_three_copy.tsv', 'stage_four.tsv')
    >>> len(p1)
    7
    >>> print(str(p1[0]))
    0	23	F	H4A	0	D	3	41;0.0
    """
    f = open(input_filename, 'r', encoding = 'utf-8')
    n = open(output_filename, 'w', encoding = 'utf-8')

    # initialize empty dict
    patient_dict = {}
 
    f.seek(0)
    # read lines of imput file
    content = f.readlines()
    # iterate through lines in input file
    for i in range(len(content)):
        # split each line to access attributes
        split_row = content[i].split('\t')
        # create pateint object using each line
        current_patient = Patient(split_row[1], split_row[2], split_row[3], \
                                  split_row[4], split_row[5], split_row[6], \
                                  split_row[7], split_row[8])
        # store value of patient number
        ID = current_patient.num

        # if patient object exists in dict update
        if ID in patient_dict:
            patient_dict[ID].update(current_patient)
        # create a new object and add to dictionary with key as patient number        
        else: 
            patient_dict[ID] = current_patient
            
    # write each patient to output file
    for j in range(len(content)):
        if j in patient_dict:
            n.write(str(patient_dict[j]) + '\n')
    
    f.close()
    n.close()
    
    # return dictionary of patients with keys as patient numbers
    return patient_dict


def fatality_by_age(d):
    """
    >>> d = stage_four('long_three_copy.tsv', 'long_four.tsv')
    >>> #print(d)
    >>> fatality_by_age(d)
    [1.0, 1.0, 1.0, 1.0, 1.0, 0.9375, 1.0, 1.0, 0.9285714285714286, 1.0, 0.8823529411764706, 1.0, 1.0, 0.9375, 1.0, 1.0, 1.0, 1.0, 1.0]
    """
    # initialize emoty dictionary
    rounded_age_dict = {}

    # iterate through keys of d and find patient age
    # to the nearest multiple of 5
    for key in d:
        new_age = 5 * round(d[key].age / 5)

        # add 1 to the condition of patient for a given age if age
        # is in the dictionary
        if new_age in rounded_age_dict:
            if d[key].state != 'I':
                rounded_age_dict[new_age][d[key].state] += 1

        # initialize key value pair with age as key and dict of conditions
        # of patients at that age as value
        elif new_age not in rounded_age_dict:
            if d[key].state != 'I':
                rounded_age_dict[new_age] = {'D': 0, 'R': 0}
                rounded_age_dict[new_age][d[key].state] += 1

    # iterate through keys of dictionary
    for age in rounded_age_dict:
        total = 0
        # create a list which contains number dead and number recovered
        states = list(rounded_age_dict[age].values())
        # iterate through list adn determine total number of patients
        for i in range(2):
            total += int(states[i])
        # reassign recovered to total number of patients
        states[1] = total
        
        # determine fatality probability
        # if possible
        try:
            rounded_age_dict[age] = states[0] / states[1]
        # if not possible
        except ZeroDivisionError:
            rounded_age_dict[age] = 1

    # x coordinates will be age
    x = sorted(rounded_age_dict)
    y = []
    # y coordinates will be fatality proability associated with each age
    for item in x:
        y.append(rounded_age_dict[item])

    # plot x and y coordinate lists and label graph
    plt.plot(x,y)
    plt.title("Probability of death vs age, by " + NAME)
    plt.xlabel("Age")
    plt.ylabel("Deaths / (Deaths + Recoveries)")
    plt.ylim((0, 1.2))
    #plt.show()
    plt.savefig("fatality_by_age.png")

    # return list of death probabilities for each age
    return y


if __name__ == "__main__":
    doctest.testmod()
