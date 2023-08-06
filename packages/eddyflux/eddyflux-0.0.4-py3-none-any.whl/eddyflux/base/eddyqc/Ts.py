import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .qcutils import *

def get_minute_std(dfd):
    minutes = dfd.index.map(
        lambda x: x.strftime('%Y-%m-%d %H:%M')
    ).drop_duplicates()

    stds = []
    min_out = []
    for m in minutes:
        df_minute = dfd.loc[m, :]
        if len(df_minute) <= 1: continue

        Ts = df_minute['Ts'].copy()
        Tgmp = df_minute['Tgmp'].copy()
        Ts = Ts - Tgmp

        coefs = np.polyfit(np.arange(len(Ts)), Ts.interpolate().bfill().values, 3)
        ffit = np.polyval(coefs, np.arange(len(Ts)))
        ffit = pd.Series(ffit, index = Ts.index)
        Ts = Ts - ffit

        stds.append(Ts.std())
        min_out.append(m)

    stds = pd.Series(stds, index = min_out, name = 'std')
    stds.index = pd.to_datetime(stds.index, format = '%Y-%m-%d %H:%M')
    
    std_index = iqr_qc(stds, *stats4qc(stds))
    return std_index, stds

def qc_Ts(std_index, ts):
    ano = pd.Series(std_index.copy(), name = 'datetime').to_frame()

    start = ano['datetime'].diff(1).map(
        lambda x: np.abs(x.total_seconds())
    )
    end = ano['datetime'].diff(-1).map(
        lambda x: np.abs(x.total_seconds())
    )

    tol = 5 * 60 # seconds
    end = end[end > tol].index.tolist()
    start = start[start > tol].index.tolist()
    start = [0] + start
    end = end + [len(ano) - 1]

    for s, e in zip(start, end):
        dif = (ano['datetime'][e] - ano['datetime'][s]).total_seconds() / 60
        if dif < 2: continue # minute
        s_dt = ano['datetime'][s]
        e_dt = ano['datetime'][e]
        # ts[s_dt: e_dt] = np.nan
        s_dt = s_dt - timedelta(minutes = 10)
        e_dt = e_dt + timedelta(minutes = 10)
        # ts[iqr_qc(ts[s_dt: e_dt], *stats4qc(ts[ts.index.difference(ts[s_dt:e_dt].index)]))] = np.nan
        ts[s_dt: e_dt] = np.nan
    return ts