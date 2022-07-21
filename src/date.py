from datetime import datetime

"""
# This file was made to handle all date-related problems
"""

# In B3's site (https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias/Index?agencia=18), a period
# of time is required to make a search.
# The 'get_previous_month_date()' and 'get_period()' functions are responsible
# for getting a period of 30 days in the last month


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


def get_period():
    period = []

    previous_month = get_previous_month_date().split('/')[0]
    year = get_previous_month_date().split('/')[1]

    # Checking if 'year' is a leap year
    if ((int(year) - 2000)) % 4 == 0:
        leap_year = True
    else:
        leap_year = False

    # Formatting date
    if int(previous_month) < 10:
        previous_month = '0' + previous_month

    if previous_month == '02' and leap_year == False:
        from_date = '01' + '/' + previous_month + '/' + year
        to_date = '28' + '/' + previous_month + '/' + year

    elif previous_month == '02' and leap_year == True:
        from_date = '01' + '/' + previous_month + '/' + year
        to_date = '29' + '/' + previous_month + '/' + year

    elif previous_month == '01' or previous_month == '03' or previous_month == '05' or previous_month == '07' or previous_month == '08' or previous_month == '10' or previous_month == '12':
        from_date = '02' + '/' + previous_month + '/' + year
        to_date = '31' + '/' + previous_month + '/' + year

    else:
        from_date = '01' + '/' + previous_month + '/' + year
        to_date = '30' + '/' + previous_month + '/' + year

    period.append(from_date)
    period.append(to_date)

    return period
