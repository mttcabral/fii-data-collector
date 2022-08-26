from utils import dir_handler


def get_fii_id_list():
    """
    # Function task: from 'data/table_ifix.html', collected
    # by 'scrape_id_and_participation' function, return
    # a list containing the 'FII' IDs
    """

    with open((dir_handler.get_data_path()+'FII_id_list.txt'), 'r') as file:
        fii_id_list = file.read()
        file.close()

    return fii_id_list
