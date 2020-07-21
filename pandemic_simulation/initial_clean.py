# Name: Martin Pleynet

import doctest

def which_delimiter(s):
    """ (str) -> str

    Takes a string and returns the most commonly used
    in the input string

    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('0,1, 3, 4')
    ','
    >>> which_delimiter('cat\\tdog\\trat')
    '\\t'
    >>> which_delimiter('a')
    Traceback (most recent call last):
    AssertionError: Should have at least one delimiter.
    """
    # constants for each delimiter
    SPACE = ' '
    COMMA = ','
    TAB = '\t'

    # dictionary to hold number of each delimiter
    delimiter = {SPACE: 0, COMMA: 0, TAB:0}
    
    # iterates through input string and counts number of each delimiter
    # with the use of teh delimiter dictionary
    for i in range(len(s)):
        if s[i] == SPACE:
            delimiter[SPACE] += 1
        elif s[i] == COMMA:
            delimiter[COMMA] += 1
        elif s[i] == TAB:
            delimiter[TAB] += 1

    # check the total number of delimiters in the string
    # regardless of the type
    total = 0
    for key in delimiter:
        total += delimiter[key]

    # if there are no delimiters, raise an AssertionError
    if total == 0:
        raise AssertionError("Should have at least one delimiter.")

    # returns key associated with max value in dictionary
    max_count = -1
    # iterates through values in dictionary and finds the delimiter
    # with the max value (one used the most)
    for key in delimiter:
        if delimiter[key] > max_count:
            max_count = delimiter[key]
            max_delim = key
    return max_delim
        
        
def stage_one(input_filename, output_filename):
    """ (str, str) -> int

    Returns how many lines were writtemn to output_filename

    >>> stage_one('260902169-short.txt', 'stage_one.tsv')
    10
    >>> stage_one('260902169.txt', 'long_one.tsv')
    3000
    """
    f = open(input_filename, 'r', encoding = 'utf-8')
    n = open(output_filename, 'w', encoding = 'utf-8')

    f.seek(0)
    # obtain all the lines in input file
    content = f.readlines()
    # iterate through each line of content
    for i in range(len(content)):
        # determine most common delimiter in a line
        change = which_delimiter(content[i])
        # change most common delimiter to a tab
        new_line = content[i].replace(change, '\t')
        # make all of the letters uppercase
        new_line = new_line.upper()
        # replace slashes with hyphens
        new_line = new_line.replace('/', '-')
        # replace periods with hyphens
        new_line = new_line.replace('.', '-')
        # write newly converted line to output file
        n.write(new_line)
    
    f.close()
    n.close()

    # return number of lines written to output file
    return (i + 1)
    
def stage_two(input_file, output_file):
    """ (str, str) -> int

    Returns how many lines were written to output_filename

    >>> stage_two('stage_one_copy.tsv', 'stage_two.tsv')
    10
    >>> stage_two('long_one.tsv', 'long_two.tsv')
    3000
    """
    f = open(input_file, 'r', encoding = 'utf-8')
    n = open(output_file, 'w', encoding = 'utf-8')

    f.seek(0)
    # obtain all the lines in input file
    content = f.readlines()
    count = 0
    # split into columns
    for i in range(len(content)):
        # split each line by tab
        split_columns = content[i].split("\t")
        # check if number of columns is 9
        if len(split_columns) == 9:
            # ensure there is a comma in temp instead of hyphen
            split_columns[7] = split_columns[7].replace('-', ',')
            # iterate through list and write item by item
            for j in range(len(split_columns)):
                n.write(split_columns[j])
                if j != 8:
                    n.write('\t')
                    
       # check cases for more than 9 columns in a line
        else:
            # check postal code column and change it
            # in case of split postal code or split NOT AVAILABLE
            if len(split_columns[5]) == 3:
                if split_columns[6][0].isdigit() or split_columns[6][0] == 'A':
                    split_columns[5] += split_columns[6]
                    split_columns.remove(split_columns[6])
                
            # check temperature column and change
            # in case of NOT AVAILABLE
            if len(split_columns[7]) == 3:
                if split_columns[8][0] == 'A':
                    split_columns[7] += ' ' + split_columns[8]
                    split_columns.remove(split_columns[8])

            # in case of temperature getting split
            # move all of the columns after back one column
            if len(split_columns) > 9:
                if split_columns[8][0].isalpha():
                    split_columns[7] += split_columns[8]
                else:
                    split_columns[7] += ',' + split_columns[8]
                split_columns[8] = split_columns[9]
                split_columns.remove(split_columns[9])

            # ensure there is a comma in temp instead of hyphen
            split_columns[7] = split_columns[7].replace('-', ',')
            
            # write column by column
            for j in range(len(split_columns)):
                n.write(split_columns[j])
                if j != 8:
                    n.write('\t')
        count += 1
        
    f.close()
    n.close()
    # return number of lines written to output file
    return count
    
if __name__ == '__main__':
    doctest.testmod()
    
