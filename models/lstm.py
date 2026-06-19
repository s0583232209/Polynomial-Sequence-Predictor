import torch
import torch.nn as nn


class PolynomialLSTM(nn.Module):

    def __init__(
        self,
        input_size=1,
        hidden_size=64,
        num_layers=2,
        output_size=3,
        dropout=0.2,
    ):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout,
        )

        self.fc = nn.Sequential(

            nn.Linear(hidden_size, 32),

            nn.ReLU(),

            nn.Linear(32, output_size),

        )

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        last_hidden = hidden[-1]

        prediction = self.fc(last_hidden)

        return prediction