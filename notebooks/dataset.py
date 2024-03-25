# %%
import pandas as pd
from sklearn.preprocessing import StandardScaler
import sklearn
import numpy as np

# %%
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

VALIDATION_SET = [
    "0c524511-6248-433c-8519-3c9e1f120e0d",
    "02622b86-0934-410c-95df-72fec7b731a5",
    "2c435c24-4c67-429e-9b47-c76841ad450b"
]

OUTLIERS = [
    "0ecb8717-ad3e-49ad-bf29-6c56dd93e1c0"
]

def FFT_COLS(df: pd.DataFrame):
    return [col for col in df.columns.unique() if col.startswith('POW')]

# %%
def split_validation_training(df: pd.DataFrame):
    df = df.query('label != "calibration"')
    validation = df.query(f'id in {VALIDATION_SET}')
    training = df.query(f"id not in {OUTLIERS}").query(f'id not in {VALIDATION_SET}')
    print(f"{training.shape=}, {validation.shape=}")
    return training, validation


# %%
def split_x_y(df: pd.DataFrame, x_cols: list[str], y_cols: list[str], window_size: int, rolling: bool, scaler: sklearn.base.TransformerMixin):
    df = df[x_cols + y_cols].dropna()
    if scaler is not None:
        df[x_cols] = scaler.transform(df[x_cols])
    
    windowed = []
    for i, window in enumerate(df.rolling(window_size)):
        if window.shape[0] != window_size:
            continue
        windowed.append(window)

    windowed = np.array(windowed)
    X = windowed[:, :, :-len(y_cols)]
    Y = windowed[:, :, len(x_cols):]

    print(f"{X.shape=}, {Y.shape=}")
    return X, Y

# %%
def prepare_labels(y: np.ndarray, method):
    assert method == 'rounded_median'
    labels = np.round(np.median(y, axis=-2))
    print(f"{labels.shape=}")
    return labels

# %%


def prepare_data():
    df = pd.read_csv('../results/dataset.csv')
    training, validation = split_validation_training(df)
    
    scaler = StandardScaler()
    scaler.fit(training[FFT_COLS()])
    
    x_train, y_train = split_x_y(training, FFT_COLS, ["label_num"], 10, True, scaler)
    x_val, y_val = split_x_y(validation, FFT_COLS, ["label_num"], 10, True, scaler)


    y_train = prepare_labels(y_train, 'median')
    y_val = prepare_labels(y_val, 'median')