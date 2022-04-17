from codecs import getencoder
import email
from turtle import color

import numpy as np
import pandas as pd
import os

from pathlib import Path

df = pd.read_csv('outfit.csv')

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# print(df)
del df["year"]
del df["Unnamed: 10"]
del df["Unnamed: 11"]
y = 0

path = 'E:\Dragons-Den\ML_model\static\OutfitD'
print(path)
# Path(name).stem
for root, directories, files in os.walk(path, topdown=True):
    for name in files:
        print(Path(os.path.join(name)).stem + "")
