# import torch
# import torch.nn as nn
#
#
# class PolynomialLSTM(nn.Module):
#
#     def __init__(
#         self,
#         input_size=1,
#         hidden_size=64,
#         num_layers=2,
#         output_size=3,
#         dropout=0.2,
#     ):
#
#         super().__init__()
#
#         self.lstm = nn.LSTM(
#             input_size=input_size,
#             hidden_size=hidden_size,
#             num_layers=num_layers,
#             batch_first=True,
#             dropout=dropout,
#         )
#
#         self.fc = nn.Sequential(
#
#             nn.Linear(hidden_size, 32),
#
#             nn.ReLU(),
#
#             nn.Linear(32, output_size),
#
#         )
#
#     def forward(self, x):
#
#         output, (hidden, cell) = self.lstm(x)
#
#         last_hidden = hidden[-1]
#
#         prediction = self.fc(last_hidden)
#
#         return prediction
import torch
import torch.nn as nn


class PolynomialLSTM(nn.Module):

    def __init__(
        self,
        input_size=1,
        hidden_size=128,
        num_layers=2,
        output_size=3,
        dropout=0.2,
    ):

        super().__init__()


        # LSTM encoder
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout,
        )


        # Normalize LSTM output
        self.norm = nn.LayerNorm(
            hidden_size
        )


        # Prediction head
        self.fc = nn.Sequential(

            nn.Linear(
                hidden_size,
                128
            ),

            nn.ReLU(),

            nn.Dropout(
                dropout
            ),


            nn.Linear(
                128,
                64
            ),

            nn.ReLU(),


            nn.Linear(
                64,
                output_size
            )

        )



    def forward(self, x):

        # x shape:
        # (batch, sequence_length, input_size)

        output, (hidden, cell) = self.lstm(x)


        # Take output from last timestep
        last_output = output[:, -1, :]


        # Normalize
        last_output = self.norm(
            last_output
        )


        # Predict next values
        prediction = self.fc(
            last_output
        )


        return prediction