import pandas as pd
import rasterio.plot
import rasterio
import numpy as np
from scipy import stats
import time
import datetime

import matplotlib
import matplotlib.pyplot as plt


def harvest_predictor(raster, planted_date_as_str):
    planted_date = datetime.datetime.strptime(planted_date_as_str, "%Y-%m-%d").date()
    # Model
    df = pd.read_csv("data/ndvi-curve.csv")

    day = df['day']
    ndvi = df['ndvi']
    model = np.poly1d(np.polyfit(day, ndvi, 4))
    days_since_planted = (datetime.date.today() - planted_date).days
    target = np.polyval(model, days_since_planted)

    # Reading the NDVI from Leaf's
    leaf_raster = rasterio.open(raster)
    ndvi = leaf_raster.read(1).astype('float64')
    ndvi_list = [[x for x in y if not np.isnan(x)] for y in ndvi]

    ndvi = mean(ndvi_list)

    # Finding the date of the Leaf NDVI

    for pred in list(range(1, 247)):
        actual = np.polyval(mymodel, pred)
        if actual >= ndvi * 0.8 or actual <= ndvi * 1.2:
            break


# Check the date found

    if target - pred > 0:
        harvest_date = f"You are {(247) - (target - pred)} days to start the harvest operation"
    else:
        harvest_date = f"You are {(247) - (pred - target)} days to start the harvest operation"

    return harvest_date
