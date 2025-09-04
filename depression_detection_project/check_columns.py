import pandas as pd

df = pd.read_csv("dataset/depression_dataset_reddit_cleaned.csv")
print("Columns in dataset:", df.columns.tolist())
print(df.head())
