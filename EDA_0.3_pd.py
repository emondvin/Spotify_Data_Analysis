import pandas as pd
import matplotlib
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
    """Obtain averages for spotify audio features less than one"""
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
# -----------------------------------------------------
# to do:
# ---- Create radial plot of average audio features for my playlists
# Tempo analysis over the years
# Tempo and non- 0-1 features analysis for me vs spot and mine
# Word cloud
# Difference in mean of my vs spot values
# Variety of audio features using standard dev (avg) and show stdev for feats
# Features correlation?
# Pearson plot

labels= list(spmean.keys())
spstats= list(spmean)
spstats
mystats = mymean.tolist()
mystats

angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
angles
# close the plot
spstats =np.concatenate((spstats,[spstats[0]]))
mystats =np.concatenate((mystats,[mystats[0]]))
angles=np.concatenate((angles,[angles[0]]))

#Size of the figure

fig=plt.figure(figsize = (18,18))

ax = fig.add_subplot(221, polar=True)
ax.plot(angles, spstats, 'o-', linewidth=2, label = "Spotify", color= 'gray')
ax.fill(angles, spstats, alpha=0.25, facecolor='gray')
ax.set_thetagrids(angles * 180/np.pi, labels , fontsize = 13)


ax.set_rlabel_position(250)
plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
plt.ylim(0,1)

ax.plot(angles, mystats, 'o-', linewidth=2, label = "My music", color = 'm')
ax.fill(angles, mystats, alpha=0.25, facecolor='m' )
ax.set_title('Mean Values of the audio features')
ax.grid(True)

plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

# ------------------------------------------------------------

def big_features(dataframe):
    """Obtain averages for spotify audio features with values greater than one"""
    mean = dataframe.mean()
    bigfeat = mean.drop(mean[abs(mean.values)<1].index)
    return bigfeat

sp_df.head()
sp_big = big_features(sp_df)
my_big = big_features(my_df)
sp_big
my_big

def bar_plot(feat, Title = 'None', ylabel = 'None'):
    feat_list = [sp_big['{}'.format(feat)], my_big['{}'.format(feat)]]
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(0, feat_list[0], width, label='Spotify')
    rects2 = ax.bar(0 + 1*width, feat_list[1], width, label='My Music')
    ax.set_ylabel(f'{ylabel}')
    ax.set_xticklabels('')
    ax.set_title(f'{Title}')
    ax.legend()
    plt.tick_params(axis = 'x', bottom = False, top = False)
    plt.show()

# bar_plot('tempo', 'Mean Tempo', 'Tempo')
# bar_plot('popularity', 'Mean Popularity Comparison', 'popularity')

sp_big

for items in sp_big.keys():
    # for titles in ['Key', ]
    bar_plot(items,'Mean {} comparison'.format(items), items)



# for i in
# bar_plot()

# tempos = [sp_big['tempo'], my_big['tempo']]
# width = 0.35
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(0, tempos[0], width, label='Spotify')
# rects2 = ax.bar(0 + 1*width, tempos[1], width, label='My Music')
# ax.set_ylabel('Tempo')
# ax.set_xticklabels('')
# ax.set_title('Mean Tempo Comparison')
# ax.legend()
# plt.tick_params(axis = 'x', bottom = False, top = False)
# plt.show()



# plt.bar(0, sp_big['tempo'], 0.25, label = 'Spotify', color = 'lightblue')
# plt.bar(x+1.1*0.25, tempos[1], 0.25, label = 'My music', color = 'lightgreen')
#
# plt.subplot(221)
# width = 0.35
# plt.bar(ind, tempo_jhon.mean() , width, label='Jonathan', color = 'lightslategray')
# plt.bar(ind + 1.1*width, tempo_emy.mean(), width, label='Emily', color = 'mediumvioletred')
#
# plt.ylabel('Mean [BPM]', fontsize = 14)
# plt.title('Tempo Means')
#
# plt.xticks(ind + width / 2, (list(tempo_emy)[:]), fontsize = 12)
# plt.legend(loc='best')
# style.use("ggplot")
