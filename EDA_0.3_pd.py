import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import numpy as np
import glob
from wordcloud import *


#Pull the files
sp_files = glob.glob("SpApp/sp*[2018,2019,n].csv")
sp_files
my_files = glob.glob("User/*[2018,19].csv")
my_files



def df_from_files(files):
    """Create a dataframe from any list of csv files"""
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index = True)
    return df

def mean_features(dataframe):
    """Obtain averages for spotify audio features"""
    mean = dataframe.mean()
    meanfeat = mean.drop(mean[abs(mean.values)>1].index)
    return meanfeat

sp_df = df_from_files(sp_files)
my_df = df_from_files(my_files)

mymean = mean_features(my_df)
spmean = mean_features(sp_df)


plot_df = pd.DataFrame({'My Music': mymean, 'Spotify': spmean}, index = spmean.index)
ax = plot_df.plot.bar(title = 'Average audio features for top of year playlists: 2018 & 2019')
avg_plt_fig = ax.get_figure().savefig('Average.png', bbox_inches = 'tight')


sp2018df = pd.read_csv('SpApp/sp_top_2018.csv')
sp2019df = pd.read_csv('SpApp/sp_top_2019.csv')
my2018df = pd.read_csv('User/top_2018.csv')
my2019df = pd.read_csv('User/top_2019.csv')

mymean18 = mean_features(my2018df)
mymean19 = mean_features(my2019df)
spmean18 = mean_features(sp2018df)
spmean19 = mean_features(sp2019df)

plotdf = pd.DataFrame({'My Music 2018' : mymean18, 'My Music 2019': mymean19,
'Spotify 2018': spmean18, 'Spotify 2019': spmean19}, index = mymean18.index)

plotdf
axe = plotdf.plot.bar(title = 'Average audio features for top of year playlists: 2018 & 2019')
dis_plot_fig = axe.get_figure().savefig('Discrete_plot.png', bbox_inches = 'tight')


# -----------------------------------------------------
