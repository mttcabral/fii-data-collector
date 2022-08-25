def get_fii_id_list():
    """
    # Function task: from 'data/table_ifix.html', collected
    # by 'scrape_id_and_participation' function, return
    # a list containing the 'FII' IDs
    """

    # Relative path = 'data/table_ifix.html'
    with open('data/FII_id_list.txt', 'r') as file:
        fii_id_list = file.read()
        file.close()

    return fii_id_list
