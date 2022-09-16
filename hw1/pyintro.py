#############################################################################################################
#
#  Homework 1 (Python Intro)
#  Types, Loops, Conditionals, Functions
#
#  Instructions:
#    * for each of the functions below, read the docstring and implement the function as described.
#
#    * feel free to to add helper functions, but DO NOT MODIFY the descriptions of the original functions.
#
#    * absolutely NO import statements should be added, they will result in an automatic 0 (the autograder
#    will break)
#
#    * Some functions specify that certain built in functions may not be used. BE MINDFUL OF THIS.
#
#    * If for whatever reason, an implementation detail is unclear, feel free to email for clarification.
#
#    * Have Fun!
#
#############################################################################################################

from curses.ascii import isdigit
from gettext import find
from sre_compile import isstring


def power(base, exp):
    """
    Implement the math.pow function for integer powers. Note: exp can still be negative. This should be
    handled properly. What other edge cases should we be careful of? Return base^exp as a float.

    THIS IMPLEMENTATION SHOULD NOT USE: math.pow(base, exp) or base ** exp

    :param base: number to raise to a given power
    :type base: int
    :param exp: power to raise the base to. NOTE: this number can be negative!
    :type exp: int
    :return: base to the exp power
    :rtype: float
    """
    # replace the line below with your code
    ans = 1.0
    if exp < 0:
        exp = 0 - exp
        for i in range(exp):
            ans /= base
        return ans
    elif exp > 0:
        for i in range(exp):
            ans *= base
        return ans
    else:
        return ans

def list_sum(l):
    """
    given a list l, return the sum of all the elements of l. You can assume that l only contains ints & floats.

    :param l: list of floats/ints
    :type l: list
    :return: the sum of all the elements in l, AS A FLOAT
    :rtype: float
    """
    # replace the line below with your code
    list_total = 0
    for num in l:
        list_total += num
    return list_total

def str_to_int(num_string):
    """
    Turn a string into an integer. For this function, num_string can be a string representation of a number in either
    binary, octal, decimal, or hexadecimal. Depending on the base, the string will start differently:
        binary:      "0b100" = 4 "0b" is first 2 characters
        octal:       "0o11"  = 9 "0o" is first 2 characters
        decimal:     "10"    = 10 no extra characters
        hexadecimal: "0xa"   = 10
     For binary, octal, and hexadecimal, the string will always be longer than 2 (i.e. the base prefix, and then the
     number. No matter the base, you are to correctly convert the string to an int and return it.

     If the base is unrecognized (the first two are not numbers, and also are not '0b', '0o', or '0x', the function
     should return -1.

    Don't worry about negative numbers!

    **hint** remember that the int() function can take multiple parameters. What was that second parameter?

    :param num_string: string representation of the integer
    :type num_string: str
    :return: integer with the value represented in the string, or negative one if the base is unrecognized
    :rtype: int
    """
    # replace the line below with your code
    if num_string[:2] == "0b":
        return int(num_string, 2)
    elif num_string[:2] == "0o":
        return int(num_string, 8)
    elif num_string[:2] == "0x":
        return int(num_string, 16)
    elif num_string[:2].isdigit():
        return int(num_string)
    else:
        return -1

def print_christmas_tree(size):
    """
    A christmas tree with size n is defined as a string having n + 1 rows, where the i'th row contains the (i-1)'th row's
    number of stars + 2, arranged in a symmetrical manner. the 0'th row should have 1 star. the last (n'th) row should
    be equivalent to the 0'th row (the trunk of the tree). the stars are asterisks: '*'. size is always >= 2.

    Example of a size 4 tree:
       *
      ***
     *****
    *******
       *

    The return should be a single string, with each row separated by '\n'. Mind the spacing in each row--there should
    be spaces before the '*'s on each row, but not after.

    size 4 tree as string:
        "   *\n  ***\n *****\n*******\n   *"

    **hint** print out your tree to the console a few times to make sure the spacing is correct.

    :param size: a number >=2
    :type size: int
    :return: string representation of a christmas tree
    :rtype: str
    """
    # replace the line below with your code
    stars = [ ( " " * (size - s) + "*" * (2 * s - 1) + "\n" ) for s in range(1, size + 1) ]
    tree = ""
    for i in stars:
        tree += i
    tree += " " * (size - 1) + "*"
    return tree

def list_to_str(l):
    """
    Implement the __str()__ function for the list class. This function should take a list, and convert
    it to its string representation. You can assume that for each element in the list, the str() function
    will give the appropriate string to use for the entire list string. Some examples of list strings:
        [1, 2, 3, 4, 5, 6]
        [True, False, True, True, False]
        ['hi', 'my', 'name', 'is']

    * NOTICE: for string elements, the string itself is surrounded by single quotes. You are expected to
              implement this. this is the only special case you should be aware of
    * you will not be graded on the spacing of your string representation, i.e. [1,2,3] == [1, 2, 3] == [ 1, 2, 3 ]
    * you can assume that there will be no nested lists/dictionaries/tuples nested in the list
    * do NOT assume that all elements in the list are of the same type

    * YOU ARE EXPECTED TO USE str() FOR EACH ELEMENT IN THE LIST
    * DO NOT USE str() ON THE LIST ITSELF

    :param l: list to convert to string
    :type l: list
    :return: string representation of that list
    :rtype: str
    """
    # replace the line below with your code
    list_string = "["
    for element in l:
        if type(element) == str:
            list_string += "'" + str(element) + "'" + ", "
        else:
            list_string += str(element) + ", "
    list_string = list_string[:(len(list_string) - 2)]
    list_string += "]"
    return list_string


def remove_substring_instances(in_str, substr):
    """
    given the string input, find all instances of substr and remove them from the input. Then, return the number of
    instances of substr that were removed, as well as the new string with all instances of substr removed, as a tuple.
    for example:
        return num_instances, new_string

    :param in_str: string to clean up
    :type in_str: str
    :param substr: substring to find and remove
    :type substr: str
    :return: a tuple where the first element is the number of elements removed, and the second is the string after
        cleaning
    :rtype: tuple
    """
    # replace the line below with your code
    count = 0
    while substr in in_str:
        i = in_str.find(substr)
        in_str = in_str[:i] + in_str[i + len(substr):]
        count += 1
    return count, in_str

def tree(size):
    result = ""
    for i in range(size):
        result += ' '*(size - i - 1) + '*' * (2 * i + 1) + '\n'
    result += ' ' * (size - 1) + '*'
    print(result)
    
