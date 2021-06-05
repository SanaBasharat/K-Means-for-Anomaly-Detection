import os
import pandas as pd
import numpy as np
import scipy as sc
import seaborn as sns
import matplotlib.pyplot as plt
import pandas_profiling as profile   # To check data distributions and correlations
import warnings     # for supressing a warning when importing large files
warnings.filterwarnings("ignore")
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow as tf
from pylab import rcParams
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
from mpl_toolkits.mplot3d import Axes3D
# import matplotlib as mpl
from preprocessing import DATAPREPROCESSING
import csv
from sklearn.decomposition import PCA


# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using non-interactive Agg backend')
#     mpl.use('Agg')
# import matplotlib.pyplot as plt


#%matplotlib inline
sns.set(style='whitegrid', palette='muted', font_scale=1.5)
rcParams['figure.figsize'] = 14, 8
RANDOM_SEED = 42

LABELS = ["Normal", "Fraud"]

# Train=pd.read_csv("Train-1542865627584.csv")
# Train_Beneficiarydata=pd.read_csv("Train_Beneficiarydata-1542865627584.csv")
# Train_Inpatientdata=pd.read_csv("Train_Inpatientdata-1542865627584.csv")
# Train_Outpatientdata=pd.read_csv("Train_Outpatientdata-1542865627584.csv")


Train="Train-1542865627584.csv"
Train_Beneficiarydata="Train_Beneficiarydata-1542865627584.csv"
Train_Inpatientdata="Train_Inpatientdata-1542865627584.csv"
Train_Outpatientdata="Train_Outpatientdata-1542865627584.csv"

# Load Test Dataset

Test=pd.read_csv("Test-1542969243754.csv")
Test_Beneficiarydata=pd.read_csv("Test_Beneficiarydata-1542969243754.csv")
Test_Inpatientdata=pd.read_csv("Test_Inpatientdata-1542969243754.csv")
Test_Outpatientdata=pd.read_csv("Test_Outpatientdata-1542969243754.csv")

data = DATAPREPROCESSING(Train_Beneficiarydata, Train_Inpatientdata, Train_Outpatientdata, Train)
processed_data = data.Processing()
print(processed_data)

processed_data.to_csv("test.csv")

processed_data = processed_data.reset_index()

kmeans = KMeans(n_clusters=3).fit(processed_data)
centroids = kmeans.cluster_centers_
print(centroids)
print(kmeans.labels_)
#
# Train_Beneficiary_Features['BeneID'] = Train_Beneficiary_Features['BeneID'].astype(int)
# # print(Train_Beneficiary_Features.dtypes)
#

pca = PCA(3)
pca.fit(processed_data)

pca_data = pd.DataFrame(pca.transform(processed_data))

# print(pca_data.head())

from matplotlib import colors as mcolors
import math

clusters = 3
colors = list(zip(*sorted((
                              tuple(mcolors.rgb_to_hsv(
                                  mcolors.to_rgba(color)[:3])), name)
                          for name, color in dict(
    mcolors.BASE_COLORS, **mcolors.CSS4_COLORS
).items())))[1]

# number of steps to taken generate n(clusters) colors
skips = math.floor(len(colors[5: -5]) / clusters)
cluster_colors = colors[5: -5: skips]

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pca_data[0], pca_data[1], pca_data[2],
           c=list(map(lambda label: cluster_colors[label],
                      kmeans.labels_)))

str_labels = list(map(lambda label: '% s' % label, kmeans.labels_))
print(str_labels)

list(map(lambda data1, data2, data3, str_label:
         ax.text(data1, data2, data3, s=str_label, size=16.5,
                 zorder=20, color='k'), pca_data[0], pca_data[1],
         pca_data[2], str_labels))

plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(processed_data['Provider'], processed_data['Age'],
#            processed_data['OPAnnualReimbursementAmt'],
#            c=list(map(lambda label: cluster_colors[label], kmeans.labels_)))
#
# str_labels = list(map(lambda label: '% s' % label, kmeans.labels_))
#
# list(map(lambda data1, data2, data3, str_label:
#          ax.text(data1, data2, data3, s=str_labels, size=16.5,
#                  zorder=20, color='k'), processed_data.iloc[1], processed_data.iloc[10],
#          processed_data.iloc[8], str_labels))
#
# fig.show()













# from pandas import DataFrame
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# import tkinter as tk
# import matplotlib
#
# matplotlib.use('Agg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# df = Train_Beneficiary_Features
#
# kmeans = KMeans(n_clusters=3).fit(df)
# centroids = kmeans.cluster_centers_
#
# root = tk.Tk()
#
# canvas1 = tk.Canvas(root, width=100, height=100)
# canvas1.pack()
#
# label1 = tk.Label(root, text=centroids, justify='center')
# canvas1.create_window(70, 50, window=label1)
#
# figure1 = plt.Figure(figsize=(10, 10), dpi=100)
# ax1 = figure1.add_subplot(111)
# ax1.scatter(df['BeneID'], df['State'], df['County'], c=kmeans.labels_.astype(float), alpha=0.5)
# ax1.scatter(centroids[:, 0], centroids[:, 1], c='red')
# scatter1 = FigureCanvasTkAgg(figure1, root)
# scatter1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
#
# root.mainloop()