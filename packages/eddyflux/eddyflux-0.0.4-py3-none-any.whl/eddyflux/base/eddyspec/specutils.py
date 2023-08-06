import numpy as np
import pandas as pd
from datetime import datetime

# ==================================================================================
# Read spectra/cospectra data:
def SplitFFT(fnS, format = '%d/%m/%y %H:%M:%S'):
    df = pd.read_csv(fnS)
    df.columns = df.columns.str.strip()
    datetimes = df['Date'].drop_duplicates().values

    if 'Date' in datetimes:
        datetimes = datetimes[np.where(datetimes != 'Date')]
    datetimes = pd.to_datetime(datetimes, format = format)

    df['Signal'] = df['Signal'].str.strip()
    signals = df['Signal'].drop_duplicates().values
    signals = signals[np.where(signals != 'Signal')]

    freq = [c for c in df.columns if all([i.isnumeric() for i in c.split('.',1)])]

    S = {}
    for sig in signals:
        covar = df.loc[df['Signal'] == sig, 'Co/Var']
        covar.index = datetimes
        S[sig + '_covar'] = covar.astype(float)
        spec = df.loc[df['Signal'] == sig, freq]
        spec.index = datetimes
        S[sig] = spec

    frequency = np.array(freq).astype(float)
    frequency = frequency.reshape(1, -1)

    frequency = np.tile(frequency, (len(datetimes), 1))

    S['Frequency'] = frequency
    
    return S

# ==================================================================================
# Read time-series
def remove_duplicated_index(df, keep = 'last'):
    df = df.copy()
    df = df[~df.index.duplicated(keep=keep)]
    df = df.sort_index()
    return df

def get_date_format(x):
    date_formats = ["%d/%m/%y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%y %I:%M:%S %p"]
    for date_format in date_formats:
        try:
            d = datetime.strptime(x, date_format)
            # print(date_format)
            break
        except ValueError as e:
            pass
    return d

def SplitCSV(p):    
    csv = pd.read_csv(p, index_col = 0)
    # flux.index = pd.to_datetime(flux.index, format = "%d/%m/%y %H:%M:%S")
    # csv.index = str2dt(csv)
    csv = csv[csv.index != 'Date/Time']
    csv.index = csv.index.map(
        lambda x: get_date_format(x)
    )
    csv = remove_duplicated_index(csv)
    csv = csv.replace(" ", np.nan)
    csv.columns = csv.columns.str.strip()
    csv = csv.astype(float)
    return csv

# ==================================================================================
# Convert number, list, pd.Dataframe, and pd.Series to np.ndarray
def numlist2arr(input):
    if isinstance(input, list):
        return np.array(input)
    elif np.isscalar(input):
        return np.array([input])
    elif isinstance(input, pd.DataFrame) | isinstance(input, pd.Series):
        return input.values
    elif isinstance(input, np.ndarray):
        return input
    else:
        raise(Exception('Wrong type'))


# ==================================================================================
# fetch variable from read-in spectra and timeseries dict 
def fetch(data_dict, name, key_map = {}, transpose = False):
    # key_map: name conversion map from user-defined in EdiRe to fixed spectra analysis functions.
    if name in key_map.keys():
        name = key_map[name]
    data = data_dict[name]
    if isinstance(data, pd.Series) | isinstance(data, pd.DataFrame):
        data = data.values
    elif isinstance(data, list):
        data = np.array(data)
        
    if data.ndim == 1:
        data = data[:, np.newaxis]
    if transpose:
        # data = data.reshape(1, -1)
        data = data.T
    return data