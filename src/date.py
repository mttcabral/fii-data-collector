from datetime import datetime

"""
# This file was made to handle all date-related problem
"""


def get_previous_month_date():
    # Getting current month and year
    current_date = datetime.today().strftime('%m/%Y')
    current_month = current_date.split('/')[0]
    current_year = current_date.split('/')[1]

    # Getting previous month
    if (current_month != 1):
        previous_month_date = str(
            (int(current_month) - 1)) + '/' + current_year
    else:
        previous_month_date = '12' + '/' + str((int(current_year) - 1))

    return previous_month_date
