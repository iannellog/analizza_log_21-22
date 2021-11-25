"""
Created on Thu Nov 25 17:16:04 2021

by Giulio Iannello
"""

import json


def fatal_error(message):
    """
    manage a fatal error: print a message and exit program
    :param message: message to be printed
    :return: None
    """
    print(message)
    exit()


def read_json_file(file_name):
    """
    read a json file and returns data
    manage exceptions
    :param file_name: file to be read
    :return: data structure corresponding to file content
    """
    try:
        fin = open(file_name)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except OSError as message:
        fatal_error(message)
    except json.JSONDecodeError as message:
        fatal_error(f'*** json error *** {message}')


def write_json_file(data, file_name, indnt=3):
    """
    write data to a json file
    manage exceptions
    :param data: python object to be written to file
    :param file_name: file to be written
    :param indent:
    :return: None
    """
    try:
        fout = open(file_name, 'w')
        json.dump(data, fout, indent=indnt)
        fout.close()
    except OSError as message:
        fatal_error(message)


