import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# RATINGS

g = pd.read_csv("Giovanni.csv", index_col=0)
m = pd.read_csv("mat.csv", index_col=0)
r = pd.read_csv("Rebecca.csv", index_col=0)

m.columns = g.columns

ratings = pd.merge(g, m, on="Image_ID")
ratings = pd.merge(ratings, r, on="Image_ID")

ratings.iloc[:,[1,2,3]] = ratings.iloc[:,[1,2,3]].apply(lambda x: (x - x.mean()) / x.std())
ratings.iloc[:,[1,2,3]].hist()

plt.savefig("rating_distr.png")
ratings.to_csv("ratings.csv")

# IMAGES

for image in os.listdir("data"):
    im = Image.open("data/" + image).convert('L')
    width, height = im.size   # Get dimensions

    new_width = 300
    new_height = 300

    left = (width - new_width)/2
    top = (height - new_height)/2 + 90
    right = (width + new_width)/2
    bottom = (height + new_height)/2 + 90

    im = im.crop((left, top, right, bottom))
    im = im.resize((64,64))
    im.save("preprocessed/" + image)
