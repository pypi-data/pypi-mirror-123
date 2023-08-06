"""
Automated Solution Checker
"""

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def solution_checker(function_code, question_number):
    if question_number == 1:
        test_string = "Hey!! I am Sam with ID number: 007 from Umbrella Corporation office at USA. Call me at 6543291234"
        output = function_code(test_string)
        if output == 'Region: USA, Phone: +1-6543291234':
            result = True
            print(OKGREEN + 'Passed!!' + ENDC)
        else:
            result = False
            print(OKGREEN + 'Oops Failed :(' + ENDC)

    elif question_number == 2:
        test_string = "Kevin Scaria"
        output = function_code(test_string)
        if output == 'Scaria, Kevin':
            result = True
            print(OKGREEN + 'Passed!!' + ENDC)
        else:
            result = False
            print(OKGREEN + 'Oops Failed :(' + ENDC)

    return result
