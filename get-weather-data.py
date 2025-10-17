import requests
import pandas as pd
import os
from tqdm import tqdm
import time
from urllib.parse import quote

API_BASE = "https://developer.nrel.gov/api/wind-toolkit/v2/wind/wtk-led-climate-v1-0-0-download.csv"
API_KEY = "xxx" 
YEAR = 2020
ATTRIBUTES = "windspeed_100m,winddirection_100m"
OUT_DIR = "unofficial_sites"

os.makedirs(OUT_DIR, exist_ok=True)

# sites = pd.read_csv("candidate_sites_new.csv")
sites = pd.read_csv("candidate_sites_new.csv")

for _, row in tqdm(sites.iterrows(), total=len(sites)):
    name = row["NAME"]
    lon, lat = row["LONGITUDE"], row["LATITUDE"]
    out_file = os.path.join(OUT_DIR, f"site_{name}.csv")

    # Skip if already downloaded
    if os.path.exists(out_file):
        continue

    # Build query parameters
    params = {
        "api_key": API_KEY,
        "wkt": f"POINT({lon} {lat})",  
        "attributes": ATTRIBUTES,
        "names": YEAR,
        "interval": 60,
        "utc": "true",
        "leap_day": "false",
        "email": "jy3056@columbia.edu"
    }

    try:
            response = requests.get(API_BASE, params=params, timeout=60)
            response.raise_for_status()
            # Save the CSV text
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            time.sleep(0.5)  # polite delay
    except Exception as e:
        print(f"⚠️ Failed for site {name} ({lon},{lat}): {e}")
