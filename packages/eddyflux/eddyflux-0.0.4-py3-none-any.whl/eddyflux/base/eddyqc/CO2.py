import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def center_rolling(ts, rolling_window, method = 'mean'):
    # rolling_window = 5
    ts = ts.copy()
    assert rolling_window%2 == 1, "Not an odd rolling windown"
    shift_step = -int((rolling_window - 1) / 2)
    # ts = ts.rolling(rolling_window, min_periods = 1).median().shift(shift_step).ffill()
    if method == 'median':
        ts = ts.rolling(rolling_window).median().shift(shift_step)
    elif method == 'min':
        ts = ts.rolling(rolling_window).min().shift(shift_step)
    else:
        ts = ts.rolling(rolling_window).mean().shift(shift_step)
    return ts


def retuning(ts, window_size):
    # returning issue detection function v2
    ts = ts.copy()
    # timeseries ratio
    tsr = ((ts / center_rolling(ts, window_size)).abs() - 1) * 100 # 101: window = 10 seconds
    tsr = tsr.abs().resample("60S").min()
    tsr = tsr.resample("100ms").interpolate()
    
    anomaly = ts[tsr > 0.2]
    if not anomaly.empty:
        ano = anomaly.to_frame().reset_index()
        
        start = ano['datetime'].diff(1).map(
            lambda x: np.abs(x.total_seconds())
        )
        end = ano['datetime'].diff(-1).map(
            lambda x: np.abs(x.total_seconds())
        )
        
        tol = 30 # seconds
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
            s_dt = s_dt - timedelta(minutes = 5)
            e_dt = e_dt + timedelta(minutes = 5)
            # ts[iqr_qc(ts[s_dt: e_dt], *stats4qc(ts[ts.index.difference(ts[s_dt:e_dt].index)]))] = np.nan
            ts[s_dt: e_dt] = np.nan
    
    """
    ts[tsr > 0.1] = np.nan
    
    if not ts[tsr > 0.1].empty:
    
        s = ts.index.get_loc(ts[tsr > 0.1].index[0])
        e = ts.index.get_loc(ts[tsr > 0.1].index[-1])

        ts[iqr_qc(ts, *stats4qc(ts[ts.index.difference(ts[s:e].index)]))] = np.nan
    """
    return ts

def quality_control_co2(ts):    
    # ==================================================================================
    # retuning
    tsd = ts.copy()
    tsd_retuning = retuning(tsd, 601) # seconds
    # # local (hourly) detection:
    # [low, high] = stats4qc(tsd_retuning)
    # print(low, high)
    # tsd_retuning[iqr_qc(tsd_retuning, low, high)] = np.nan
    # print(tsd_retuning)
    # # global (daily) detection:
    # ==================================================================================
    # despiking
    # tsd_retuning = despike(tsd_retuning, threshold = 2)
    # tsd_retuning[despike(detrend(tsd_retuning)).isna()] = np.nan
    # # -----------------------------------------------------------------------------
    # # plotting
    # fig, axes = plt.subplots(3, 1, figsize = (10, 6))
    # axes = axes.flatten()
    # axes[0].scatter(tsd.index, tsd)
    # axes[1].scatter(tsd_retuning.index, tsd_retuning)
    # axes[0].sharex(axes[1])
    # axes[0].sharey(axes[1])
    # ax = axes[2]
    # ax.hist(tsd_retuning, bins = 300)
    # ax.axvline(low, c = 'red')
    # ax.axvline(high, c = 'red')
    # # -----------------------------------------------------------------------------
    # break
    # ==================================================================================
    # iqr control
    #     ts[iqr_qc(ts, *stats4qc(ts))] = np.nan
    return ts, tsd_retuning