
# Code for the alpacka Python package, used to extract metadata from text data sets
#### Folder "functions" contains functions for calculating the NCOF and TF-IDF score for a user specified data set. 
#### The file "Pipes" contains pipelins for the two methods that can be used to create a better workflow when using the package as well as a tool for loading the data.
#### To use the package begin by importing Pipes and then you can initiate the Data loader, NCOF, or TFIDF class. 
#### Alter the config.ini file to change the base setup and alter the paths to your data

# Walkthrough
### Install the alpacka package through pip, or download the package through github.

    > pip install alpacka

[Link to github repo](https://github.com/BernhardMoller/alpacka)

### Set up
Many of the classes and functions in the alpacka package require data paths and other infromation to be able to run. For convenience sake the code reads this info from a config file so that you as a user only have to input this info once. 

The config file is formatted as a standard `config.ini`	file and an example is located in the package directory. the directory can be accessed by calling `pip show alpacka` in you prompt and following the `Location` path to the alpacka folder. 

	   > pip show alpacka
		...
	   > Location: c:\users\path\to\venv\lib\site-packages

Copy the `config.ini` file and place it in you project directory / working path for convenience, but can be placed anywhare you like. 
		
### Now we are ready to start to work with alpacka.
  Import the data processor from data loader and intanciate it
  

	    from alpacka.pipes.data_process import data_process
	    d = data_process(config_path = "config.ini")


Settings are loaded from the `config.ini` file. 

### Import and instanciate the NCOF and TF-IDF methods.
	 

	    from alpacka.pipes.ncof_pipeline import ncof_pipeline
		ncof = ncof_pipe(config_path="config.ini")  

	    from alpacka.pipes.tfidf_pipeline import tfidf_pipeline
    	tfidf = tfidf_pipe(config_path="config.ini")


### Load the data using the data_process class 
The data path can be changed by altering the `config.ini` file . In the `config.ini` file alter `data_file ` & `data_folder ` to the file name and path to the location of your data. 

    [Data]  
	    Verbose = True  
	    num_words = None  
	    Supported_inputs = list  
	    Input_data_type = list  
	    stop_word_path = Stopord.txt  
	    data_file = data_file_name.csv  			<-----
	    data_folder = path\to\data\folder 			<-----
Or your can call the `set_data_file` and `set_data_folder` and input the name of you data file and path to your data folder from the  `Data_process`class.

    d.set_data_file('data_file_name.csv')
    d.set_data_folder('path\to\data\folder')

### Now you should be ready to load your data.  Load the data by calling the `load_file`method from your `Data_process`class. Currently  the alpacka package only supports `.csv` files as input. 
The required inputs of the `load_file`call is the names of the columns that contains the data and its labels. 

    data , labels = d.load_file( 'preprocessed_text', 'label')
    
In this example a `csv` file were loaded where the data are contained in the column named `preprocessed_text` and the labels in a column named `label`.

### Now that the data is loaded we can simply calculate our NCOF and TF-IDF score for the data set by calling the `calc_NCOF` & `calc_TFIDF`methods from their respective class. The scores will be saved wihin the classes and can be vieved and assigned to a external variable by calling `.get_Score()`.
   

    ncof.calc_ncof(data, labels)
    score_ncof = ncof.get_score()

	tfidf.calc_tfidf(data, labels)
    score_tfidf = tfidf.get_score()

### From the score the outliers can be seperated & identified by calling `.split_score()`. 
No inputs are needed, the method is fully self contained.

	    ncof.split_score()
	    tfidf.split_score()

### Now the NCOF score is ready to be plotted, and its outliers get be viewed by calling 
This will extract the indexes of the NCOF outliers. 
	

		pos_outliers = ncof.get_pos_outliers()
and

   		neg_outliers = ncof.get_neg_outliers()


### The TF-IDF methods requires one additional step before it is ready to be plotted. 
This step is to identify which outliers are only occuring in the positive or negative class and is done by calling `.unique_outliers_per_class()`. 

    tfidf.unique_outliers_per_class()
The results can be viewed by calling 

		 pos_outliers =	tfidf.get_outliers_unique_pos()
and 
		
    neg_outliers =	tfidf.get_outliers_unique_neg() 

This will extract the indexes of the TF-IDF outliers. 		

### The reults can now finally be plotted by the `.scatter() `method. 
 For simplicity the method does not require any inputs, if more contoll is needed for the plot it is recomended that a custom function is created. 
 

    ncof.scatter()
    tfidf.scatter()



