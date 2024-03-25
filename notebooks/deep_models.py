import numpy as np
import torch.nn as nn
import torch
import torch.nn.functional as F


class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 3, 5)
        self.conv2 = nn.Conv2d(3, 5, 5)
        self.fc1 = nn.Linear(282, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2,1))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2,1))
        # x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DeepNet(nn.Module):
    def __init__(self, time_steps: int, channels: int, num_classes: int = 2):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(channels * time_steps, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, num_classes),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def x_to_torch(x: np.ndarray, batch_size: int, time_steps: int, channels: int, device=torch.device('cpu')):
    x = torch.tensor(x, dtype=torch.float, device=device).reshape(-1, batch_size, time_steps, channels)
    print(f"{x.shape=}")
    return x

def y_to_torch(y: np.ndarray, batch_size: int, num_classes: int, device=torch.device('cpu')):
    y = torch.tensor(y-1, dtype=torch.long, device=device)
    y = F.one_hot(y).reshape(-1, batch_size, num_classes).float()
    print(f"{y.shape=}")
    return y

def x_to_keras(y: np.ndarray):
    pass

def from_torch(tensor: torch.Tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()

def decode_onehot(y: np.ndarray):
    y = np.argmax(y, axis=-1)
    print(f"{y.shape=}")
    return y