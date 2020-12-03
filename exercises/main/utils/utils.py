import pandas as pd
import numpy as np
import hashlib

# Custom functions
def embedding(data, p):
    data_shifted = data.copy()
    for lag in range(-p+1, 2):
        data_shifted['y_t' + '{0:+}'.format(lag)] = data_shifted['y'].shift(-lag, freq='D')
    data_shifted = data_shifted.dropna(how='any')
    y = data_shifted['y_t+1'].to_numpy()
    X = data_shifted[['y_t' + '{0:+}'.format(lag) for lag in range(-p+1, 1)]].to_numpy()
    return (X,y, data_shifted)

def smape(y_true, y_pred):
    denominator = (y_true + np.abs(y_pred)) / 200.0
    diff = np.abs(y_true - y_pred) / denominator
    diff[denominator == 0] = 0.0
    return np.mean(diff)

def keyvalue(df):
    df["horizon"] = range(1, df.shape[0]+1)
    res = pd.melt(df, id_vars = ["horizon"])
    res = res.rename(columns={"variable": "series"})
    res["Id"] = res.apply(lambda row: "s" + str(row["series"].split("-")[1]) + "h"+ str(row["horizon"]), axis=1)
    res = res.drop(['series', 'horizon'], axis=1)
    res = res[["Id", "value"]]
    res = res.rename(columns={"value": "forecasts"})
    return res