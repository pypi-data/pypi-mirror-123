# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 16:42:00 2021
V1 on Thu Jan 07 09:07:00 2021

@author: sz394@exeter.ac.uk
"""

import warnings
import numpy as np

def crosscorr(Uz, scalar, lag = 0):
    """Lag-N cross correlation. 
    Parameters
    ----------
    Uz, scaler : pandas.Series objects of equal length, Uz is vertial wind, scaler is CO2, H2O etc.
    lag : int, default 0

    Returns
    ----------
    corr : float
    
    Note:
    -----
    Pearson correlation (method 1):
        keyword can be 'pearson', 'kendall', 'spearman'
        https://stackoverflow.com/questions/33171413/cross-correlation-time-lag-correlation-with-pandas
    Covariance correlation (methhod 2):
        corr = cov(x, y) / (std(x) * std(y))
        https://study.com/academy/lesson/covariance-correlation-equations-examples.html#:~:text=The%20correlation%20coefficient%20is%20represented,standard%20deviations%20of%20each%20variable.&text=A%20correlation%20coefficient%20uses%20the,takes%20it%20one%20step%20further.
    
    Math:
    -----
    Scalar(e.g. CO2) is the lagged variable due to the tube wall effect etc.
    for example(df):
        Uz  |CO2
        ---------
        8:00|7:00
        9:00|8:00
    so the scalar = scalar.shift(-lag) --> Note the "-" sign (lag is positive)
        Uz  |CO2
        ---------
        8:00|8:00
        9:00|NaN    
    cov = SUM(
        (x - mean(x)) * (y - mean(y))
    ) / (N-1)
    """
    scalar = scalar.shift(-lag)
    corr = Uz.cov(scalar) / (Uz.std() * scalar.std())
    # # or (not recommended by its similar result yet lower speed):
    # corr = Uz.corr(scalar, method = "spearman")
    return corr

def remove_lag(df, Uz, scalar, window = [-50, 200], hz = 10, thre_q = 0.75, fco2 = 1):
    """
    Parameters
    ----------
    df : Pandas DataFrame
        EC data containing vertical velocity(UZ) and scalar(e.g. CO2)
    velocity: str
        name of vertical wind in df
    scalar: str
        name of CO2, H2O etc in df
    window: list, default is [-50, 200], because normally scalar signal is lagged behind wind
        range for shifting, the unit is EC freq, 100 ms for 10Hz systems.
    hz: int, default is 10
        EC system frequency
    thre_q: percentile to determine the sign of covariance correlation
    
    Returns
    ---------
    pandas.Series: lag removed series
    float: delay seconds
    """
    # window = range(window[0], window[1])
    coefs = [
      crosscorr(df[Uz], df[scalar], lag = l) for l in range(*window)
    ]
    
    coefs = np.array(coefs)
    window = np.arange(*window)

    # ----------------------------------------------
    # decide choose max or min coef
    timestamp = (df.index[0] + (df.index[-1] - df.index[0]) / 2).replace(microsecond=0)
    hour = timestamp.hour
    choice = -1 # -1 for min, 1 for max 
    if (hour > 8) and (hour < 16): # day, cov < 0
        choice = -1 # n_shift = window[np.argmin(coefs)]
    elif (hour < 5) or (hour > 21): # night, cov > 0
        choice = 1 # n_shift = window[np.argmax(coefs)]
    else:
        thre_sun = np.quantile(coefs, thre_q)
        if thre_sun > 0:
            choice = 1 # n_shift = window[np.argmax(coefs)]
        else:
            choice = -1 # n_shift = window[np.argmin(coefs)]
    if choice * fco2 == -1:
        n_shift = window[np.argmin(coefs)]
    else:
        n_shift = window[np.argmax(coefs)]
    # ----------------------------------------------
    # what if n_shift too far
    
    df[scalar] = df[scalar].shift(-n_shift)
    lag_sec = n_shift / hz
    return df, lag_sec