"""
Automated Solution Checker
"""

#Solution Checker
def solution_checker(function_code, question_number):
    if question_number == 1:
        test_string = "Hey!! I am Sam with ID number: 007 from Umbrella Corporation office at USA. Call me at 6543291234"
        output = function_code(test_string)
        if output == 'Region: USA, Phone: +1-6543291234':
            result = True
        else:
            result = False
    
    return result