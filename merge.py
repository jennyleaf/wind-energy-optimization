import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
import os

# merge all site CSVs
# files = glob("wind_data/*.csv")
files = glob("unofficial_sites/*.csv")
print("Found", len(files), "files")

dfs = []
for f in tqdm(files):
    site_name = os.path.basename(f)[len("site_"):-4].strip()

    # read data skipping first row
    df = pd.read_csv(f, skiprows=1)
    df.columns = df.columns.str.strip().str.lower()

    # create datetime
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
    df["site"] = site_name

    dfs.append(df[["site", "datetime", "wind speed at 100m (m/s)"]])

df_all = pd.concat(dfs, ignore_index=True)

print(df_all.shape)
print(df_all.head())

print(df_all.head())

dupes = df_all.duplicated(subset=["datetime", "site"])
print("Duplicate rows:", dupes.sum())

df_all = df_all.drop_duplicates(subset=["datetime", "site"])

W = df_all.pivot(index="datetime", columns="site", values="wind speed at 100m (m/s)")

print("Matrix shape:", W.shape)

# convert wind speed to power
V = W.to_numpy()
P = np.zeros_like(V)
mask1 = (V >= 3) & (V < 12)
mask2 = (V >= 12) & (V <= 25)
P[mask1] = ((V[mask1] - 3)**3) / (12 - 3)**3
P[mask2] = 1

# export
P = pd.DataFrame(P, index=W.index, columns=W.columns)
# P.to_csv("wind_power_matrix_sitename.csv")
P.to_csv("wind_power_matrix_sitename_new.csv")