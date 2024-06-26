import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os,sys
from pandas.plotting import scatter_matrix
from sklearn import preprocessing
from glob import glob 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import matplotlib as mpl
import math


df = pd.read_csv("C:/Users/21294596/OneDrive - Curtin/Coding/Phree_t1/modified_file.csv")
print(df.info())
from sklearn.model_selection import train_test_split

train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
train_set.hist(alpha=1.,figsize = (16,10), layout=(4,5), bins=30);
test_set.hist(alpha=1.,figsize = (16,10), layout=(4,5), bins=30);
train_set.to_csv('trainset_log.csv', index=False)  
test_set.to_csv('testset_log.csv', index=False)  