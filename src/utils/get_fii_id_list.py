from utils import dir_handler
import json


def get_fii_id_list():
    """
    # Function task: from 'data/table_ifix.html', collected
    # by 'scrape_id_and_participation' function, return
    # a list containing the 'FII' IDs
    """

    with open((dir_handler.get_data_path()+'FII_id_list.json'), 'rb') as file:
        # Since the list was saved as JSON, when reading, the
        # data returned is a list of lists, so it's necessary to
        # convert to a normal list
        file_content = json.load(file)

        fii_id_list = []
        for x in range(len(file_content)):
            fii_id_list.append(file_content[x][0])

        file.close()

    return fii_id_list
