from utils import dir_handler
import json

"""
# This file holds all calculation logic for
# calculating the dividend yield of IFIX
"""


def calc_dy():
    # After scraping all information needed, this method
    # will be called to calculate the dividend yield of IFIX

    with open((dir_handler.get_data_path()+'FII_id_list.json'), 'rb') as file:
        # Since the list was saved as JSON, when reading, the
        # data returned is a list of lists, so it's necessary to
        # convert to a normal list
        file_content1 = json.load(file)

        fii_id_list = []
        for x in range(len(file_content1)):
            fii_id_list.append(file_content1[x][0])

        file.close()

    with open((dir_handler.get_data_path()+'FII_id_and_closing_quotation.json'), 'rb') as file:
        closing_quotation = json.load(file)

        file.close()

    with open((dir_handler.get_data_path()+'FII_id_and_participation.json'), 'rb') as file:
        participation = json.load(file)

        file.close()

    with open((dir_handler.get_data_path()+'FII_id_and_proceed.json'), 'rb') as file:
        proceed = json.load(file)

        file.close()

    # ptIFIX
    ptIFIX = 0
    counter = 0
    for fii_id_proceed, fii_id_participation in zip(proceed, participation):
        if fii_id_proceed == fii_id_list[counter] and fii_id_participation == fii_id_list[counter]:
            ptIFIX = ptIFIX + (proceed[fii_id_proceed] *
                               participation[fii_id_participation])
            counter += 1

    # ctIFIX
    ctIFIX = 0
    counter = 0

    for fii_id_closing_quotation, fii_id_participation in zip(closing_quotation, participation):
        if fii_id_closing_quotation == fii_id_list[counter] and fii_id_participation == fii_id_list[counter]:
            ctIFIX = ctIFIX + (closing_quotation[fii_id_closing_quotation] *
                               participation[fii_id_participation])
            counter += 1

    # rIFIX
    rIFIX = ptIFIX/ctIFIX

    print("\nDividend Yield of IFIX: " + str(rIFIX*100))
