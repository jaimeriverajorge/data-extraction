# shuffle the dataframe to get shuffled data
import pandas as pd
import random
import numpy as np

df = pd.read_csv(
    '../training_data/major_and_minor_veins_training_min_points_not_shuffled.csv')


shuf_df = df.sample(frac=1)

shuf_df.to_csv(
    'major_and_minor_veins_training_min_points_shuffled.csv', index=False)
