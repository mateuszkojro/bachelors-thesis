import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
import numpy as np

EEG_COLS = [
    "EEG.AF3",
    "EEG.F7",
    "EEG.F3",
    "EEG.FC5",
    "EEG.T7",
    "EEG.P7",
    "EEG.O1",
    "EEG.O2",
    "EEG.P8",
    "EEG.T8",
    "EEG.FC6",
    "EEG.F4",
    "EEG.F8",
    "EEG.AF4",
]


def make_dataset(
    df,
    window_size=256,
    rolling_mean=None,
    start=0,
    end=None,
    cols_to_include=None,
    calibration_as_waiting=False,
    sample=None,
):
    if sample is not None:
        df = df.sample(frac=sample)
    if calibration_as_waiting:
        df = df.replace("calibration", "waiting")
        df["label_num"] = pd.Categorical(df["label"]).codes
    cols = EEG_COLS + ["label_num"]
    if cols_to_include is not None:
        cols += cols_to_include
    windows = df[cols]
    if rolling_mean is not None:
        windows = windows.rolling(rolling_mean).mean().dropna()
    if end is not None:
        windows = windows[start:end]
    else:
        windows = windows[start:]
    windows = list(windows.rolling(window=window_size))
    windows = windows[window_size:]
    windows = np.array(windows)
    return windows


def split_xy(data, window_size):
    X = data[:, :, :-1].reshape(-1, window_size * 14)
    Y = np.mean(data[:, :, -1], axis=1)
    Y = Y.astype(int)
    return X, Y

class Loader:
    def __init__(self, step) -> None:
        self.step = step

    def next(self):
        pass