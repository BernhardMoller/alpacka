from typing import List
from alpacka.functions import statistic_methods as s
from alpacka.functions import presentation_functions as pf
from configparser import ConfigParser


class tfidf_pipeline:

    def __init__(self):
        # config = ConfigParser()
        # path = config_path
        # config.read(path)
        # self.Dot = int(config['TFIDF']['Dot'])
        self.Dot = 10
        # self.Supported_inputs = config['TFIDF']['Supported_inputs']
        self.Verbose = True
        self.num_words = None
        # c_var = config['TFIDF']['num_words']
        # if c_var == 'None':
        #     self.num_words = None
        # else:
        #     self.num_words = int(c_var)

        # if config['TFIDF']['Input_data_type'] not in self.Supported_inputs:
        #     raise TypeError(
        #         f"Selected input data type ({config['TFIDF']['Input_data_type']}) not currently supported as an "
        #         f"input. \n Please format the input in on of the supported formats. \n Supported formats: "
        #         f"{self.Supported_inputs}")
        # self.Input_data_type = config['TFIDF']['Input_data_type']
    def print_all_methods(self):
        object_methods = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        print(object_methods)

    #### Check input data type ####
    def check_data_type(self, data):
        """self function that checks if the input data type is known to be compatible with the remaining functions"""
        if type(data).__name__ != 'list':
            raise TypeError(
                f"Input type ({type(data)}) not currently supported as an input. "
                f"\n Please format the input in on of the supported formats. "
                f"\n Supported formats: list")

    #### calc_TFIDF ####
    def calc_tfidf(self, data: list, labels: list):
        """
        Calculates the TF-IDF score for the positive and negative class.
        Returns the score and dictionary used for the calculations as lists where the indexes of the elements acts as
        'keys'
        @param data: list
        @param labels: list
        @return: Score, Dict: List[List[float]] , dict
        """
        self.check_data_type(data)

        self.score, self.dict = s.calc_TFIDF_from_raw_data(data, labels, nr_words=self.get_num_words())
        if self.Verbose:
            print(f" TF-IDF score added under 'self.score' "
                  f" use self.get_--- to access the result")

    ####
    def get_score(self):
        """Returns the Tf-idf score stored in the object"""
        return self.score

    ####
    def get_dict(self):
        """Returns the dict stored in the object"""
        return self.dict

    #### Split score ####
    def split_score(self):
        """splits the TF-idf score into two categories based on the Tf-idf value for each element. Returns the
        element indexes corresponding to the following three categories. INPUT: Inliers:      elements with tf-idf
        score between mean +- 1 sigma, outliers: elements with tf-idf score greater than mean +1 sigma, The outliers
        are returned as a list of lists where index 0 is the 1-2 sigma outliers, index 1 is the 2-3 sigma outlers,
        and index 2 is 3-> outliers The outliers for the negative class is stored in [0] The outliers for the
        positive class is stored in [1] """
        self.inliers, self.outliers = pf.sigma_splitter_TF_IDF(self.get_score)
        if self.Verbose:
            print(
                f" Inliers added under 'self.Inliers' \n Positive outliers added under 'self.Pos_outliers' \n use "
                f"self.get_--- to access the result")

    ####
    def get_inliers(self):
        """Returns the Tf-idf inliers indexes stored in the object
        The inliers for the negative class is stored in [0]
        The inliers for the positive class is stored in [1]
        OUTPUT:
            type : list of lists containing integer"""
        return self.inliers

    ####
    def get_outliers(self):
        """Returns the Tf-idf outlier indexes stored  in the object
        The outliers for the negative class is stored in [0]
        The outliers for the positive class is stored in [1]
        OUTPUT:
            type : list of lists containing integer"""
        return self.outliers

    ####

    #### unique_outliers_per_class ####
    def unique_outliers_per_class(self):
        """Seperates outliers that only occures in either the positive or negative class
        sor of only works for dataset with two classes
        OUTPUT:
            outliers_unique_neg: List[List[Any]]
            outliers_unique_pos: List[List[Any]]"""
        outliers = self.get_outliers()

        neg = outliers[0]
        pos = outliers[1]

        outliers_unique_from_positive_class = []
        outliers_unique_from_negative_class = []
        for i in range(len(pos)):
            in_pos_not_neg = set(pos[i]).difference(set(neg[i]))
            in_neg_not_pos = set(neg[i]).difference(set(pos[i]))

            outliers_unique_from_positive_class.append(list(in_pos_not_neg))
            outliers_unique_from_negative_class.append(list(in_neg_not_pos))

        self.outliers_unique_neg = outliers_unique_from_negative_class
        self.outliers_unique_pos = outliers_unique_from_positive_class
        if self.Verbose:
            print(
                f" Outliers unique for the two classes added under self.outliers_unique_neg & self.outliers_unique_pos"
                f"\n use self.get_--- to access the result")

    ####
    def get_outliers_unique_neg(self):
        """Returns the ouliers for each sigma line that only appears in the negative class"""
        return self.outliers_unique_neg

    ####
    def get_outliers_unique_pos(self):
        """Returns the ouliers for each sigma line that only appears in the positive class"""
        return self.outliers_unique_pos

    #### indexes 2 words ####
    def ind_2_txt(self, lst_of_lst):
        """Converts a list of integers to the corresponding list of words (str) stored in the objects dictionary
         INPUT:
         lst: list of integers"""
        words_all = []
        for lst in lst_of_lst:
            words = pf.ind_2_txt(lst, self.get_dict())
            words_all.append(words)
        return words_all

    #### Plot ####
    def scatter(self, classes: List[str] = None):
        """
        Plots the tf-idf score stored in the object, inliers and outliers are plotted in seperate colours for clarity
        Currently only supports two classes
        @param classes: List[str]
        """
        if classes is None:
            classes = ['negative', 'positive']
        Dot = self.get_dot()
        for score, inliers, outliers, class_name in zip(self.get_score(), self.get_inliers(), self.get_outliers(),
                                                        classes):
            pf.TFIDF_plot(score, inliers, outliers, Dot, class_name)

    #### plot outliers ####
    def plot_outliers(self, score: list, outliers: List[List[List[int]]], from_class: List[str]):
        """
        Plots the score over the TFIED outliers
        @param score: list, np array with the TFIDF score for the same class as the outliers originates
        @param outliers: List[List[int]], list of list with the integer indexes of the outliers
        @param from_class: str, string with the title of the plot
        """
        pf.TFIDF_plot_outliers(score, outliers, self.get_dot(), from_class)

    #### PLOT MERGED HISTOGRAMS####
    def plot_merged_histogram(self, data: List[List[float]], bins: int = None, x_label: str = None, y_label: str = None,
                              title: str = None, legend: List[str] = None):
        """
        Plots a merged histogram of the input data
        @param data: List[List[float]]
        @param bins: int
        @param x_label: str
        @param y_label: str
        @param title: str
        @param legend: List[str]
        """
        pf.plot_merged_histogram(data, bins, x_label, y_label, title, legend)
        if self.Verbose:
            print(f"Printing merged histograms")

    #### PLOT HISTOGRAMS####
    def plot_histogram(self, data: List[float], bins: int = None, x_label: str = None, y_label: str = None,
                       title: str = None,
                       legend: List[str] = None):
        """
        Plots a histogram of the input data
        @param data: List[float]
        @param bins: int
        @param x_label: str
        @param y_label: str
        @param title: str
        @param legend: List[str]
        """
        pf.plot_histogram(data, bins, x_label, y_label, title, legend)
        if self.Verbose:
            print(f"Printing merged histograms")

    #### remove stop words ####
    def remove_stop_words(self, lst_of_lst: List[List[str]], stop_words: List[str]) -> List[List[str]]:
        """
        Removes stopwords from the inputtexts @param lst_of_lst: List[List[str]], list of list of text words in the
        format that is recieved from the methods ind_2_txt @param stop_words: List[str], List of strings containing
        the stop words @return: words_all: List[List[str]], input list with stopwords removed
        """
        words_all = []
        for lst in lst_of_lst:
            words = [w for w in lst if w not in stop_words]
            words_all.append(words)
        return words_all

    #####  CONFIG  ###
    def set_verbose(self, bol: bool= False):
        """
        Set the self variable verbose,
        @param bol: bool, standard value False
        """
        self.Verbose = bol

    def get_num_words(self):
        return self.num_words

    def set_num_words(self, new_val: int):
        """
        Set the self variable num_words,
        @param new_val: int
        """
        self.num_words = new_val

    #### DOT ####
    def set_dot(self, new_val: int):
        """
        Set the self variable dot, used during plotting
        @param new_val: int
        """
        self.Dot = new_val

    ####
    def get_dot(self):
        return self.Dot

    # #### Input_data_type ####
    # def get_input_data_type(self):
    #     return self.Input_data_type
    #
    # ####
    # def set_input_data_type(self, string: str):
    #     if string not in self.Supported_inputs:
    #         raise TypeError(
    #             f"Selected input data type ({string}) not currently supported as an input. "
    #             f"\n Please format the input in on of the supported formats. "
    #             f"\n Supported formats: {self.Supported_inputs}")
    #     self.Input_data_type = string
