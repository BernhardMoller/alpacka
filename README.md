
# Code for the alpacka Python package, used to extract metadata from text data sets
#### Folder "functions" contains functions for calculating the NCOF and TF-IDF score for a user specified data set. 
#### The file "Pipes" contains pipelins for the two methods that can be used to create a better workflow when using the package as well as a tool for loading the data.
#### To use the package begin by importing Pipes and then you can initiate the NCOF or TFIDF class. 


# Walkthrough
This walkthrough will only deal with the `NCOF`method available in the package, an example of the `TF-IDF` based method is available in the demos folder. This walkthrough is available as a notebook in the demos folder.
### Install the alpacka package through pip, or download the package through github.

    > pip install alpacka

[Link to github repo](https://github.com/BernhardMoller/alpacka)

### Set up
To be able to use the alpacka package a data set for the analysis is needed. For this walkthrough we will use the Amazon reviews data set, available at [link to data set source], (https://jmcauley.ucsd.edu/data/amazon/) 

		
### Load and preprocess the data 
Before you can pply the alpacka package you will need to load your data and perform preprocessessing/ data cleaning to you likeing. 

For this walkthrough we will load the data using `Pandas` and do some quick preprocessesing using `Keras`. 
  
 

    import pandas as pd
    data = pd.read_csv('data/Reviews.csv')
    nr_samples = 100000
    score = data['Score']
    text = data['Text']
    
	score = score[0:nr_samples]
	text = text[0:nr_samples]
	
	score = score[0:nr_samples]  
	score = [elm - 1 for elm in score]
    
From the code we can see that the data has been loaded and $100,000$ samples has been seperated into the texts and the review score. 

**IMPORTANT:** The translation of the review score is preformed due to the scores have the range of `[1 5]` and alpacka requires all labels to have the range of `[0 n]`. Thus the range is translated from `[1 5]` to `[0 4]`. 

### Preprocess the data
For this walkthrough the data will be preprocessed by passing it though the Tokenizer available in the `Keras`package. This method is not a best practice but good eough for this walkthrough. 

	from tensorflow.keras.preprocessing.text import Tokenizer
	
	t = Tokenizer(lower = True)  
    t.fit_on_texts(text)  
    integers = t.texts_to_sequences(text)  
    text = t.sequences_to_texts(integers)


All the data is now transformed to lowercase and characters such as 
'!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n' are removed. 

**IMPORTANT:** It is recomended to convert all data to lower or uppercase and remove special characters from the data since alpacka does differentiate between `spam` ,`Spam`, and `spam!`, which can cause skewed results if you interested in the distrubution of `spam` in you data.

### Importing and initiating alpacka
Now we are ready to import and initiate alpacka. 
 
    from alpacka.Pipeline import Pipeline
	
	p = Pipeline()


Now the `NCOF` and `TF-IDF` pipelines are initiated through the wrapper `Pipeline` and the induvidual analysis methods can be accessed be calling:

    p.ncof.some_functions()
   or

    p.tfidf.some_functions()

Now we are ready to start the analysis of our data. 

Note that the  `.some_functions()` function is a placeholder and do exist.

### NCOF method:
There are some setting that we can make in the NCOF method that we need to specify before we start. One of which is how many unique tokens do we want to to take into consideration in the analysis, variable `num_words`. The defult setting for this variable is `None` meaning that all unique tokens will be used in the analysis. For "large" data sets this choice is quite ambitious given that the number of tokens that appear only once or twice in the a corpus. 

Another setting that we need to specify is for what class we want the results presented for, variable `class_perspective`. As the NCOF method presents results regarding if a token is overrepresented in a class compared to the rest of the corpus, which class to investigate nees to be specified, the defult value of `class_perspective` is `1`.

    p.ncof.set_num_words(10000)
    p.ncof.set_class_perspective(0)
For this walkthrough we will limit the analysis to the $10,000$ most common words in the corpus and use the perspective of class $0$, menaning that we will investigate what tokens are over or under represented in 1-star reviews, remember that we have translated the review scores. 
#### Calculate NCOF
Now we are ready to calculate the NCOF score for the review data and its scores. This is done by calling the `.calc_ncof(data,labels)` function.  For this example the input in the `data` field is the texts, and the `labels` is the review scores. 

    p.ncof.calc_ncof(text, score)
We now have an array, `ncof_score`, that contains the NCOF results for our data. This array will have the size `[1,num_words]` and positive and negatives values, indicating if a token is more or less common in investigated class (positives values), or the remaining classes (negative values). The array can be accessed by calling: 

	ncof_score = p.ncof.get_score()

In addition to an array with the scores the `.calc_ncof()` function saves a dictionary that maps the indexes in the  `ncof_score ` array to its text representations, and can be accessed by calling:

    dictionary = p.ncof.get_dict()


#### Sorting results
To sort the array into inliers and outliers for the positive and negative values the function `.split_score()`needs to be called. The inliers can be accessed through: 

    p.ncof.split_score()
    
    ncof_pos = p.ncof.get_pos_outliers()  
    ncof_neg = p.ncof.get_neg_outliers()
Which will return the indexes of the words in the dictionary that are considered as outliers in the NCOF results. 

The results are sorted within the `ncof_pos `and `ncof_neg ` as the following:

   ncof_pos[0] = $\mu+\sigma\leq result <\mu+2\sigma$
   ncof_pos[1] = $\mu+2\sigma\leq result <\mu+3\sigma$
   ncof_pos[2] = $\mu+3\sigma\leq result$
   
   ncof_neg[0] = $\mu-\sigma\geq result >\mu-2\sigma$
   ncof_neg[1] = $\mu-2\sigma\geq result >\mu-3\sigma$
   ncof_neg[2] = $\mu-3\sigma\geq result$

#### Plotting results
These results can be plotted by calling the function `.scatter()` which will give visual information regarding what tokens are over or under represented in the investigated class. 

    p.ncof.scatter()

#### Converting results from indexes to text
Since it is quite difficult to interpret the socre for each the indexes directly, it is suggested that the indexes are transformed back to their text representations. This can be done by calling the `.ncof.ind_2_txt(data)`function, the function input should be either indexes of the positive or negative outlers. 

	words_pos = p.ncof.ind_2_txt(ncof_pos)
	words_neg = p.ncof.ind_2_txt(ncof_neg)

If the text results want to be cleaned from stop words for clarification. The function `.remove_stop_words(data,stop_words)` can be called. This functon compares the content of the input `data` to that of the input `stop-words` and removes any matches between them from the `data`. For this walkthrough we will use the stop words available from the NLTK package. 

    import nltk  
	from nltk.corpus import stopwords  
	nltk.download('stopwords')  
	stop_words = set(stopwords.words('english'))

Now stop words can be removed from our results.

    words_pos = 	p.ncof.remove_stop_words(words_pos,stop_words)
    
    words_neg = 	p.ncof.remove_stop_words(words_neg,stop_words)

#### Print results to terminal. 
We have now gone through all the steps required to produce, plot, and clean the reults from the NCOF analysis method. The last part is to either save the results to a file or to print them to the terminal. Since format to save the results to is a user preference no function for this is provided in the alpacka package, however the results can be printed to the terminal by calling the following function.

    p.ncof.print_outliers_to_terminal(words_pos, sort = True)
    
    p.ncof.print_outliers_to_terminal(words_neg, sort = True)

The input variable `sort` can be set to either `True` or `False` and decides if the results should be printed as alphabetically sorted or not. 
   
