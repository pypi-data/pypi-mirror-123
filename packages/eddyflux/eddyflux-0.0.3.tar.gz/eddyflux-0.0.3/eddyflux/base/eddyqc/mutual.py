import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .CO2 import center_rolling
from .qcutils import detrend

def two_systems(s1, s2, shift_hz = 100, step_hz = 10, thre1 = 10, thres2 = 10, window_size = 601, ifplot = False):
    # # example:
    # two_systems(df2d['CO2'], df5d['CO2'])
    s1 = s1.copy(); s2 = s2.copy()
    s1d = detrend(s1); s2d = detrend(s2)
    # ===========================================================
    # difference between two series
    mean_val = (s1.mean() + s2.mean()) / 2 
    s_dif = []
    for i in np.arange(-shift_hz, shift_hz + 1, step = step_hz):
        s_dif.append((s1d.shift(i) - s2d) / mean_val * 100)
    s_dif = pd.concat(s_dif, axis = 1).abs().min(axis = 1)
    
    index1 = s_dif[s_dif > thre1].index
    index2 = s_dif[s_dif > s_dif.quantile(0.90)].index
    
    index = index1.union(index2)
    # ===========================================================
    # difference between neighbouring 10 hz
    s1_rm = center_rolling(s1, rolling_window = window_size, method = 'mean').abs()
    s2_rm = center_rolling(s2, rolling_window = window_size, method = 'mean').abs()
    
    s1_rmr = (s1[index] / s1_rm[index] - 1).abs() * 100
    s2_rmr = (s2[index] / s2_rm[index] - 1).abs() * 100
    
    # -----------------------------------------------------------------------------
    # plot indicators
    if ifplot:
        fig, axes = plt.subplots(2, 1, figsize = (10, 6), sharex = True, sharey = True)
        axes = axes.flatten()
        ax = axes[0]
        ax.scatter(s1_rmr.index, s1_rmr)
        ax = axes[1]
        ax.scatter(s2_rmr.index, s2_rmr)
    # -----------------------------------------------------------------------------

    index1 =  s1_rmr[s1_rmr > thres2].index
    index2 =  s2_rmr[s2_rmr > thres2].index
    return index, index1, index2

def user_rolling_qc(s, window_size = 601, method = 'mean'):
    s = s.copy()
    s_rm = center_rolling(s, rolling_window = window_size, method = method).abs()
    s_rmr = (s / s_rm - 1).abs() * 100
    return s_rmr