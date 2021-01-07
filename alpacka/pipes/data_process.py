import inspect
import os.path
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import Tuple, List

import pandas as pd


def save_2_file(path: str, lst: list, sort: bool = True):
    """
    Saves the input list of words to a txt file at the specified path.
    If no file is available at path location the function creates a new, else overwrites the existing file
    @param path: str
    @param lst: list
    @param sort: bool
    """
    if sort:
        lst.sort()
    else:
        pass

    if os.path.isfile(path):
        with open(path, 'w') as file:
            for w in lst:
                file.write(str(w) + '\n')
    else:
        with open(path, "w+") as file:
            for w in lst:
                file.write(str(w) + '\n')


def print_outliers_to_terminal(lst: List[List[list]], sort: bool = True):
    """
    Saves the input list of words to a txt file at the specified path.
    If no file is available at path location the function creates a new, else overwrites the existing file
    @param path: str
    @param lst: list
    @param sort: bool
    """
    if sort:
        lst.sort()
    else:
        pass
    sigmas = ["1", "2", "3"]
    for outliers, sigma in zip(lst, sigmas):
        if sort:
            print(f"Printing {sigma}-sigma outliers, alphabetically sorted")
        else:
            print(f"Printing {sigma}-sigma outliers")
        print(20 * "#")
        for word in outliers:
            print(f"{word}")
        print(20 * "#")

class data_process:
    def __init__(self, config_path: str):
        config = ConfigParser()
        # cur_path = os.path.dirname(__file__)
        # path = os.path.relpath('../alpacka/config.ini', cur_path)
        path = config_path
        config.read(path)
        self.Verbose = config['Data']['Verbose']
        # self.num_words = config['Data']['num_words']
        self.data_file = config['Data']['data_file']
        self.data_folder = config['Data']['data_folder']
        self.stop_word_file_name = config['Data']['stop_word_file_name']

    def lis_all_methods(self):
        object_methods = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        print(object_methods)

    def load_file(self, field_data=str, field_label=str) -> Tuple[list, list]:
        """
        Loads data from the path specifed by self.data_folter + self.data_file.
        The expected data format is csv, retuns two lists with the data and labels.

        @param field_data: str
        @param field_label: str
        @return: data, labels : list, list

         if no path is specifed then returns an error.
        """

        def csv_2_list(path_data, field_data, field_label) -> Tuple[list, list]:
            """
            Loads data from a csv file and exports it as two lists. The CSV file is read from the path specified in the config file (self.path_data)

            @param path_data: str,  path to the data file
            @param field_data: str, string with the name of the field containing the data
            @param field_label: str, sting with the name of the field containing the labels
            @return: Data, Labels: list, list
            """
            if self.Verbose:
                print(f"Loading data from {path_data}")
                print(f"Dropping any NAN objects from the data")
            df = pd.read_csv(path_data)
            df = df.dropna()

            if self.Verbose:
                print(f"Removing any non str objects from the data")
            labels = df[field_label].tolist()
            data = df[field_data].tolist()

            data, labels = remove_non_str(data, labels)
            data, labels = remove_non_str(data, labels)

            return data, labels

        def remove_non_str(data: list, labels: list) -> Tuple[list, list]:
            """
            Removes any elements from the Data that are of type non-string, removes the corresponding index in labels
            @param data: list
            @param labels: list
            @return: data, labels: list, list
            """

            for i, elm in enumerate(data):
                if not isinstance(elm, str):
                    data.pop(i)
                    labels.pop(i)
            return data, labels

        if self.data_folder is None or self.data_file is None:
            raise ValueError(f"Please check the data path. \n Currently folder or file path is not defined.\n "
                             f"self.data_foler: {self.data_folder}"
                             f"self.data_file: {self.data_file}"
                             f"Assign a path in the config.ini file")

        path_data = Path(self.data_folder) / Path(self.data_file)
        data, labels = csv_2_list(path_data.__str__(), field_data, field_label)

        return data, labels

    def load_stop_words(self, nr_words: int = None) -> list:
        """
        Returns a list containing the nr_words most common stopwords. Path taken from the config.ini file

        @param nr_words: int,  number of stop words to be included
        @return: cont: list of str, list containing nr_words stop words
        """
        if nr_words is None:
            print(f"Nr_words not define, reverting to standard setting of nr_words = {100}.")
            nr_words = 100
        if self.Verbose:
            print(f"Loading {nr_words} stop words from {self.stop_word_file_name}")

        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parent_dir = os.path.dirname(current_dir)
        path = os.path.join(parent_dir, self.stop_word_file_name)

        f = open(path)
        cont = f.read()
        cont = cont.split()
        if nr_words > len(cont):
            raise ValueError(f"number of specifed words are more than available, max nr of words is {len(cont)}")
        return cont[:nr_words]

    def lemmatize_score(self, score, dict):
        "todo: implemnt ths function"
        pass

    def set_data_folder(self, data_folder: str):
        """
        Sets the self variable data_folder to what the user specifes
        @param data_folder: str, path to the folder containing the data
        """
        self.data_folder = data_folder

    def set_data_file(self, data_file=str):
        """Sets the self variable data_file to what the user specifies
        @param data_file = str, name of the file containing data"""
        self.data_file = data_file

    def get_num_words(self):
        """Returns the number of words to be used for the stop words """
        return self.num_words

    def set_num_words(self, new_val=int):
        """Sets the number of stop words to be used.
        @param new_val: int, new value of the number of words to be used"""
        self.num_words = new_val

    def set_verbose(self, bol: bool):
        """Sets the self variable Verbose.
        @param bol: bool, true or false value for Verbose"""
        self.Verbose = bool
