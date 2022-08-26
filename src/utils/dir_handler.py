from __future__ import absolute_import
import os


def create_data_dir():
    # The 'data' folder is included in '.gitignore', hence
    # if it doesn't exist, it's necessary to create it.
    if (not (os.path.isdir('data'))):
        os.mkdir('data')
        print("----------Create 'data' directory!----------")


def get_data_path():
    # Get the correct 'data' folder path in any os
    absolute_path = os.path.dirname(__file__)
    data_path = os.path.join(absolute_path, '..\\..\\data\\')

    return data_path
