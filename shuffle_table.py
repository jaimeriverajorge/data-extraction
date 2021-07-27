# shuffle the dataframe to get shuffled data
import pandas as pd
import random
import numpy as np

df = pd.read_csv('lobe_tip_training_full_sized_img.csv')


shuf_df = df.sample(frac=1)

shuf_df.to_csv('shuffled_data.csv', index=False)
