"""
Created on Thu Nov 25 17:16:04 2021

by Giulio Iannello
"""

import json
from abc import ABC, abstractmethod
import pandas as pd


def dict2df(tab):
    keys = list(tab.keys())
    events = [eventID for eventID in tab[keys[0]].keys()]
    df = pd.DataFrame(index=keys, columns=events)
    for k in keys:
        for e in events:
            df.at[k, e] = tab[k][e]
    return df


def fatal_error(message):
    """
    manage a fatal error: print a message and exit program
    :param message: message to be printed
    :return: None
    """
    print(message)
    exit()


class JSONReader():

    def __init__(self):
        pass

    def read_file(self, file_name):
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


class FeatureWriter(ABC):
    """
    abstract class
    """

    @abstractmethod
    def write_file(self, data, file_name, **kwargs):
        """
        abstract method
        """
        pass

    @staticmethod
    def create_instance(suffix):
        if suffix == 'json':
            return JSONWriter()
        elif suffix == 'xlsx':
            return ExcelWriter()
        else:
            raise ValueError('unknown file type')


class JSONWriter(FeatureWriter):

    def __init__(self):
        pass

    def write_file(self, data, file_name, indnt=3):
        """
        write data to a json file
        manage exceptions
        :param data: python object to be written to file
        :param file_name: file to be written
        :param indnt:
        :return: None
        """
        try:
            fout = open(file_name, 'w')
            json.dump(data, fout, indent=indnt)
            fout.close()
        except OSError as message:
            fatal_error(message)


class ExcelWriter(FeatureWriter):

    def __init__(self):
        pass

    def write_file(self, data, file_name):
        df = dict2df(data)
        df.to_excel(file_name)

