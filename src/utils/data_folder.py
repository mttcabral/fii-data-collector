import os

"""
# The 'data' folder is included in '.gitignore', hence
# if it doesn't exist, it's necessary to create it.
"""


def create_data_dir():
    if(not (os.path.isdir('data'))):
        os.mkdir('data')
        print("----------Create 'data' directory!----------")
