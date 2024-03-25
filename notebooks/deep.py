# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, ConfusionMatrixDisplay, confusion_matrix, accuracy_score
import torch.nn as nn
import torch
import torch.optim as optim
import time
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from deep_models import DeepNet, from_torch, decode_onehot, x_to_torch, y_to_torch
from dataset import split_validation_training,  FFT_COLS, split_x_y, prepare_labels

def score_model(model: nn.Module, x: np.ndarray, y: np.ndarray):
    pred = model(x)
    pred = decode_onehot(from_torch(pred))
    y = decode_onehot(from_torch(y))
    f1 = f1_score(y, pred)
    acc = accuracy_score(y, pred)
    plt.clf()
    sns.heatmap(confusion_matrix(y, pred), annot=True)
    plt.savefig(f"img/{time.time()}.png")
    return {"f1": f1, "acc": acc}

def train_model(model: nn.Module, x_train: np.ndarray, y_train: np.ndarray, x_val: np.ndarray, y_val: np.ndarray, epochs: int, loss_fn: nn.Module, optimizer: optim.Optimizer, logging_interval=None):
    if logging_interval is None:
        # If interval is not specified, log every epoch
        logging_interval = x.shape[0]
    
    for epoch in range(epochs):
        running_loss = 0.
        start = time.time()
        for i, (x, y) in enumerate(zip(x_train, y_train)):
            outputs = model(x)
            loss = loss_fn(outputs, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            running_loss += loss.item()
            if i % logging_interval == logging_interval - 1:
                print(f'[{i}] loss: {running_loss / logging_interval:.3f}')
                running_loss = 0.
        
        with torch.no_grad():
            print(f"== [{epoch}/{epochs}] [{int(time.time()-start)}s] {score_model(model, x_val, y_val)}")

        # with open(f"model_{epoch}.pth", "w") as f:
        torch.save(model, f"model_{epoch}.pth")


# %%

df = pd.read_csv('../results/dataset.csv')
training, validation = split_validation_training(df)

scaler = StandardScaler()
scaler.fit(training[FFT_COLS(training)])
# %%
# window_sizes = [2**i for i in range(3, 8)]
window_sizes = [128]
trained_models = []
num_classes = 2
epochs = 500

for window_size in window_sizes:
    try:
        print(f"==== {window_size=}")
        x_train, y_train = split_x_y(training, FFT_COLS(training), ["label_num"], window_size, True, scaler)
        x_val, y_val = split_x_y(validation, FFT_COLS(training), ["label_num"], window_size, True, scaler)

        y_train = prepare_labels(y_train, 'rounded_median')
        y_val = prepare_labels(y_val, 'rounded_median')

        num_channels = x_val.shape[-1]
        net = DeepNet(window_size, num_channels)

        device = torch.device("mps")

        # batch_size = x_train.shape[0] // np.product(x_train.shape[1:])
        batch_size = 14
        x_train = x_to_torch(x_train, batch_size=batch_size, time_steps=window_size, channels=num_channels, device=device)
        y_train = y_to_torch(y_train, batch_size=batch_size, num_classes=num_classes, device=device)

        # batch_size = x_val.shape[0] // np.product(x_train.shape[1:])
        batch_size = 1
        x_val = x_to_torch(x_val, batch_size=batch_size, time_steps=window_size, channels=num_channels, device=device)
        y_val = y_to_torch(y_val, batch_size=batch_size, num_classes=num_classes, device=device)

        train_model(model=net.to(device), 
                    x_train=x_train, 
                    y_train=y_train, 
                    x_val=x_val, 
                    y_val=y_val, 
                    epochs=epochs, 
                    loss_fn=nn.BCELoss(), 
                    optimizer=optim.Adam(net.parameters(), lr=0.001), 
                    logging_interval=1000)


    except Exception as e:
        print(e)
