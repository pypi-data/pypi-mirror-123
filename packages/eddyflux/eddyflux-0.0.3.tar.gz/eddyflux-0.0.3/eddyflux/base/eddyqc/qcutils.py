import numpy as np
import pandas as pd
from .CO2 import center_rolling


def stats4qc(ts):
    # statistics
    q1 = ts.quantile(0.25)
    q3 = ts.quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5*iqr
    high = q3 + 1.5*iqr
    return [low, high]

def iqr_qc(ts, low, high):
    return ts[(ts < low) | (ts > high)].index

def glbdec(ts):
    ts = ts.copy()
    tsr = ((ts / center_rolling(ts, 601)).abs() - 1) * 100
    tsr = tsr.abs().resample("600S").mean()
    tsr = tsr.resample("100ms").interpolate()
    tsr = tsr[ts.index]

    ts[iqr_qc(tsr, *stats4qc(tsr))] = np.nan
    tsr = ((ts / center_rolling(ts, 101)).abs() - 1) * 100
    ts[tsr.abs() > 2] = np.nan
    return ts

def despike(ts, threshold = 2):
    ts = ts.copy()
    tsr = ((ts / center_rolling(ts, 101)).abs() - 1) * 100
    ts[tsr.abs() > threshold] = np.nan
    return ts

def detrend(ts, order = 3):
    ts = ts.copy()
    coefs = np.polyfit(np.arange(len(ts)), ts.interpolate().bfill().values, order)
    ffit = np.polyval(coefs, np.arange(len(ts)))
    ffit = pd.Series(ffit, index = ts.index)
    return ts - ffit

def deplatform(ts, order = 2):
    ts = ts.copy()
    tsd = detrend(ts, order = order)
    # print(tsd)
    # tsr = ((tsd / center_rolling(tsd, 101, method = 'mean')).abs() - 1) * 100
    # tsc = ts.copy()
    ts[iqr_qc(tsd, *stats4qc(tsd))] = np.nan
    return ts