import torch
import torch.nn as nn


class PolynomialLSTM(nn.Module):
    """LSTM-based model that predicts the next 3 values of a polynomial sequence
    given 8 input values, without being told the underlying formula."""

    def __init__(
        self,
        input_size=1,
        hidden_size=64,
        num_layers=2,
        output_size=3,
        dropout=0.2,
    ):
        # input_size=1  : each timestep is a single scalar value
        # hidden_size=64: number of features in the LSTM hidden state
        # num_layers=2  : two stacked LSTM layers
        # output_size=3 : predict the next 3 values
        # dropout=0.2   : applied between LSTM layers to reduce overfitting
        super().__init__()

        # 2-layer LSTM that reads the input sequence one value at a time.
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout,
        )

        # Fully connected head: maps the final hidden state to 3 predictions.
        self.fc = nn.Sequential(

            nn.Linear(hidden_size, 32),

            nn.ReLU(),

            nn.Linear(32, output_size),

        )

    def forward(self, x):
        # Run the full input sequence through the LSTM.
        output, (hidden, cell) = self.lstm(x)

        # Use only the last layer's hidden state as a summary of the sequence.
        last_hidden = hidden[-1]

        # Pass through the FC head to produce the 3 predicted values.
        prediction = self.fc(last_hidden)

        return prediction
