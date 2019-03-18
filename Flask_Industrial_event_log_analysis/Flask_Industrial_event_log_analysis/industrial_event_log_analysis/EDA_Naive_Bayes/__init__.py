import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# intially decide to use different algo
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
# to plot
import seaborn as sns
import matplotlib.pyplot as plt
# to analyse predictions
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline

# to balance the dataset
from sklearn.utils import resample
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
import os
import getpass
import re
import math
import sys
