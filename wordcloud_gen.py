import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import numpy as np
import glob
from wordcloud import *
from collections import *

#Pull the data files
sp_files = glob.glob("sp*.csv")
sp_files
my_files = glob.glob("[!sp]*.csv")
my_files


def df_from_files(files):
    """Combine a list of csv files into a DataFrame"""
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index = True)
    return df

sp_df = df_from_files(sp_files)
my_df = df_from_files(my_files)

def words(df):
    """Get the genre column from the dataframe and convert to list of genres"""
    df = df.genres
    df_genres = []
    word_list = []
    for i in range(0,len(df)):
        df_genres.extend(df[i].strip('[]').replace("'",'').split(','))
    for j in range(0,len(df_genres)):
        word_list.append(df_genres[j].strip())
            # Clean up the entries
    word_list = list(filter(None, word_list))
        # Filter any empty elements
    return word_list
    # return df_genres

my_words = words(my_df)
my_words

sp_words = words(sp_df)
sp_words


def count_frequency(list):
    """ Create an ordered dictionary from genre list that counts frequency of keys """
    freq = {}
    for item in list:
        if item in freq:
            freq[item] +=1
        else:
            freq[item] = 1
    freq = OrderedDict(sorted(freq.items(), key = lambda x: x[1], reverse = True))
    return freq

spfreq = count_frequency(sp_words)
myfreq = count_frequency(my_words)

# Create a word cloud from the ordered dictionary
mycloud = WordCloud(max_words = 10, background_color = 'whitesmoke', mode = 'RGB').generate_from_frequencies(myfreq)
plt.imshow(mycloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()

spcloud = WordCloud(max_words = 10, background_color = 'whitesmoke', mode = 'RGB').generate_from_frequencies(spfreq)
plt.imshow(spcloud, interpolation = 'bilinear')
plt.axis('off')
plt.show()
