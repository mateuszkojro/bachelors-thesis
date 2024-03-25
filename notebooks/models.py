# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, ConfusionMatrixDisplay, confusion_matrix, accuracy_score


import pandas as pd
import numpy as np

from dataset import split_validation_training,  FFT_COLS, split_x_y, prepare_labels

#% %
def to_scikit_input(x: np.ndarray):
    shape = x.shape
    return x.reshape(-1, np.prod(shape[1:]))

def score_model(model, x: np.ndarray, y: np.ndarray):
    pred = model.predict(x)
    f1 = f1_score(y, pred)
    acc = accuracy_score(y, pred)
    return {"f1": f1, "acc": acc}

# %%

df = pd.read_csv('../results/dataset.csv')
training, validation = split_validation_training(df)

scaler = StandardScaler()
scaler.fit(training[FFT_COLS(training)])
# %%

window_sizes = [2**i for i in range(8, 10)]

forrest_depths = [2**i for i in range(3, 10)] 
models = [RandomForestClassifier(max_depth=depth) for depth in forrest_depths]

trained_models = []

for window_size in window_sizes:
    x_train, y_train = split_x_y(training, FFT_COLS(training), ["label_num"], window_size, True, scaler)
    x_val, y_val = split_x_y(validation, FFT_COLS(training), ["label_num"], window_size, True, scaler)

    y_train = prepare_labels(y_train, 'rounded_median')
    y_val = prepare_labels(y_val, 'rounded_median')

    for model in models:
        print(f"{window_size=}, {model=}")
        model.fit(to_scikit_input(x_train), y_train)
        score = score_model(model, to_scikit_input(x_val), y_val)
        print(score)
        trained_models.append(model)
# %%
