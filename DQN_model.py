# # Import:
# # -------
import random
import torch.nn as nn
import torch.nn.functional as F


class Qnet(nn.Module):
    def __init__(self, no_actions, no_states):
        super(Qnet, self).__init__()
        # EXP1: 1 Hidden layer 16 Neurons
        self.fc1 = nn.Linear(no_states, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, no_actions)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def sample_action(self, observation, epsilon):
        a = self.forward(observation)
        # ! Exploration
        if random.random() < epsilon:
            return random.randint(0, self.fc3.out_features - 1)
        # ! Exploitation
        else:
            return a.argmax().item()
