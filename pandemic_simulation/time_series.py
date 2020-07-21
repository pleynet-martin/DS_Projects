# Name: Martin Pleynet

import doctest
from datetime import datetime
import numpy
import matplotlib.pyplot as plt
NAME = 'Martin Pleynet'

def date_diff(date1, date2):
    """ (str, str) -> int

    Returns how many days apart the two dates are, as an integer

    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2019-12-12', '2019-12-06')
    -6
    """
    # convert date1 and date2 to correct datetime format
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    # find the difference in between date1 and date2
    difference = date2 - date1
    # access days
    return difference.days


def get_age(date1, date2):
    """ (str, str) -> int

    Returns how many complete years apart the two dates are, as an integer

    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17

    """
    # convert date1 and date2 to correct datetime format
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    # find the difference in between date1 and date2
    difference = date2 - date1
    # access days then divide to find years
    # cast as an int to find number of years
    return int(difference.days / 365.2425)
    
def stage_three(input_filename, output_filename):
    """ (str, str) -> dict

    Returns a dictionary where the keys are each day of the pandemic

    >>> stage_three('stage_two_copy.tsv', 'stage_three.tsv')
    {0: {'I': 1, 'R': 0, 'D': 0}, 1: {'I': 2, 'R': 0, 'D': 1}, 2: {'I': 5, 'R': 0, 'D': 1}}

    >>> stage_three('long_two.tsv', 'long_three.tsv')
    {0: {'I': 1, 'R': 0, 'D': 0}, 1: {'I': 2, 'R': 0, 'D': 1}, 2: {'I': 6, 'R': 0, 'D': 1}, 3: {'I': 19, 'R': 0, 'D': 1}, 4: {'I': 53, 'R': 0, 'D': 3}, 5: {'I': 137, 'R': 0, 'D': 14}, 6: {'I': 367, 'R': 2, 'D': 28}, 7: {'I': 947, 'R': 2, 'D': 108}, 8: {'I': 1219, 'R': 1, 'D': 88}}
    
    """
    # create an empty dict
    days_dict = {}
    
    f = open(input_filename, 'r')
    n = open(output_filename, 'w', encoding = 'utf-8')

    f.seek(0)
    # read lines in input file
    content = f.readlines()
    # split first row to isolate specific columns
    first_row = content[0].split('\t')
    # isolate index date
    INDEX_DATE = first_row[2]

    # iterate through all the lines in the file
    for i in range(len(content)):
        new_row = content[i].split('\t')
        
        # change entry date to date_diff 
        new_row[2] = date_diff(INDEX_DATE, new_row[2])
        
        # change date of birth to age of patient
        new_row[3] = get_age(new_row[3], INDEX_DATE)
        
        # replace patient status wih appropraite letter
        if new_row[6][0].upper() == 'M':
            new_row[6] = 'D'
        else:
            new_row[6] = new_row[6][0].upper()

        # creating dictionary with keys as pandemic day number
        if new_row[2] in days_dict:
            days_dict[new_row[2]][new_row[6]] += 1
        else:
            days_dict[new_row[2]] = {'I': 0, 'R': 0, 'D': 0}
            days_dict[new_row[2]][new_row[6]] += 1

        # write to file column by column for each line
        for j in range(len(new_row)):
            n.write(str(new_row[j]))
            if j != 8:
                n.write('\t')
    
    f.close()
    n.close()

    # return dictionary with each day of the pandemic as a key
    return days_dict


def plot_time_series(d):
    """ (dict) -> list

    Returns a list of lists, where each sublist represents each
    day of the pandemic

    >>> #d = stage_three('stage_two_copy.tsv', 'stage_three_copy.tsv')
    >>> #plot_time_series(d)
    >>> d = stage_three('long_two.tsv', 'long_three.tsv')
    >>> plot_time_series(d)
    [[1, 0, 0], [2, 0, 1], [6, 0, 1], [19, 0, 1], [53, 0, 3], [137, 0, 14], [367, 2, 28], [947, 2, 108], [1219, 1, 88]]
    
    """
    # initialize empty list
    pandemic_list = []
    # create each value dictionary in d to a list 
    for key in d:
        pandemic_list.append(list(d[key].values()))

    # plot the list and label graph
    plt.plot(pandemic_list)
    plt.legend(['Infected', 'Recovered', 'Dead'])
    plt.title("Time series of early pandemic, by " + NAME)
    plt.xlabel("Days into Pandemic")
    plt.ylabel("Number of People")
    #plt.show()
    plt.savefig("time_series.png")

    # returns a list of lists in the order Infected, Recovered, Dead
    return pandemic_list

if __name__ == '__main__':
    doctest.testmod()
