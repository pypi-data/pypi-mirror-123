"""
Automated Solution Checker
"""

import pandas as pd

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def solution_checker(function_code, question_number):

    if question_number == 2:
        test_string = "Kevin Scaria"
        output = function_code(test_string)
        if output == 'Scaria, Kevin':
            result = True
            print(OKGREEN + 'Passed!!' + ENDC)
        else:
            result = False
            print(FAIL + 'Oops Failed :(' + ENDC)

    elif question_number == 1:
        test_string = "Hey!! I am Sam with ID number: 007 from Umbrella Corporation office at USA. Call me at 6543291234"
        output = function_code(test_string)
        if output == 'Region: USA, Phone: +1-6543291234':
            result = True
            print(OKGREEN + 'Passed!!' + ENDC)
        else:
            result = False
            print(FAIL + 'Oops Failed :(' + ENDC)

    elif question_number == 3:
        test_df = pd.DataFrame({'F_ID': [1, 2, 3, 4, 5],
                                'Bio': ["Hey, I'm James Bond. I have 5+ years experience in Analytics and I can help you find hidden\
                        from your company's data. You can contact me at +21-321-654-7891 and bond.james@analytics4hire.com.\
                        Hire me at $95/hr.",
                                        "Hey, I'm Max Payne. I have 3+ years experience in Game Development and I can deveop \
                        amazing gamified platforms for your ed tech company.You can contact me at +91-1216547891 \
                        and max.payne@gameit.io.\
                        My per hour fee is $110/hr.",
                                        "Hey, I'm Neo. I have 2+ years experience in Analytics and I create reporting dashboards\
                        that are automated. You can contact me at +1-3216547891 and neo.anderson@matrix.com\
                        Hire me at $155/hr.",
                                        "Hey, I'm Wreck Ralph. I have 5+ years experience in Construction and I can help you build \
                        your dream homes. You can contact me at +31-3216137891 and wreckitralph@construct.com\
                        Hire me at $67/hr.",
                                        "Hey, I'm Jordan Belfort. I have 8+ years experience in Investment and I can help you invest and \
                        get amazing returns. You can contact me at +21-3212547891 and jordanbelfort@wolfofwallstreet.com\
                        Hire me at $90/hr."]})

        output_df, output_dict = function_code(test_df)

        test_df['Name'] = test_df['Bio'].apply(
            lambda x: x.split("I'm ")[1].split('.')[0])
        test_df['Industry'] = test_df['Bio'].apply(
            lambda x: x.split("experience in ")[1].split('and')[0])
        test_df['E-mail'] = test_df['Bio'].apply(lambda x: '@'.join(
            [x.split('@')[0].split(' ')[-1], x.split('@')[1].split(' ')[0]]))
        test_df['Cost of service'] = test_df['Bio'].apply(
            lambda x: x.split("/hr")[0].split('$')[1]).astype(float)
        test_dict = test_df.groupby('Industry').mean()

        if output_df.equals(test_df) and output_dict == test_dict:
            result = True
            print(OKGREEN + 'Passed!!' + ENDC)
        else:
            result = False
            print(FAIL + 'Oops Failed :(' + ENDC)

    return result


def evaluate(answer_list):
    print(f'Total: {sum(answer_list)*100/len(answer_list)}%')
    print(
        f'Summary: {sum(answer_list)} of {len(answer_list)} questions passed')
