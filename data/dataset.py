"""
PyTorch Dataset for polynomial sequence prediction.

This module:
    1. Loads generated polynomial sequence data from CSV files.
    2. Converts string representations of sequences into tensors.
    3. Normalizes each sequence independently.
    4. Returns input sequences and target values in a format
       suitable for training an LSTM model.
"""

import ast
from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import Dataset


# ==========================================================
# Paths
# ==========================================================

DATA_DIR = Path(__file__).resolve().parent
GENERATED_DIR = DATA_DIR / "generated"


# ==========================================================
# Helper Functions
# ==========================================================

def parse_seq(s: str) -> torch.Tensor:
    """
    Convert a sequence stored as a CSV string into a PyTorch tensor.

    Example:
        Input:
            "1,2,3,4"

        Output:
            tensor([1., 2., 3., 4.])

    Args:
        s:
            String representation of a numerical sequence.

    Returns:
        A float32 PyTorch tensor containing the sequence.
    """

    return torch.tensor(
        ast.literal_eval(f"[{s}]"),
        dtype=torch.float32,
    )


# ==========================================================
# Polynomial Dataset
# ==========================================================

class PolynomialDataset(Dataset):
    """
    Dataset for polynomial sequence prediction.

    Each sample contains:
        - Input sequence:
            8 known values of a polynomial sequence.
        - Target sequence:
            The next 3 values that the model should predict.

    The data is normalized per sample using the mean and
    standard deviation of the input sequence. This allows the
    model to focus on the pattern of the sequence rather than
    its absolute scale.
    """

    def __init__(self, split="train", mean=None, std=None):
        """
        Initialize the dataset.

        Args:
            split:
                Dataset split to load ("train", "validation", or "test").

            mean:
                Optional normalization mean.

            std:
                Optional normalization standard deviation.
        """

        path = GENERATED_DIR / f"{split}.csv"

        self.df = pd.read_csv(path)

        # Kept for possible future global normalization.
        self.mean = mean
        self.std = std


    def __len__(self):
        """
        Return the number of samples in the dataset.
        """

        return len(self.df)


    def __getitem__(self, idx: int):
        """
        Retrieve one training example.

        Args:
            idx:
                Index of the requested sample.

        Returns:
            tuple:
                (
                    normalized_input_sequence,
                    normalized_target_sequence
                )

            Input shape:
                (sequence_length, 1)

            Target shape:
                (number_of_predictions,)
        """

        row = self.df.iloc[idx]


        # Convert input sequence to tensor and add feature dimension.
        # LSTM expects input shape:
        # (batch_size, sequence_length, features)
        x = parse_seq(
            row["input_sequence"]
        ).unsqueeze(-1)


        # Convert target sequence to tensor.
        y = parse_seq(
            row["target_sequence"]
        )


        # Normalize using statistics from the input sequence.
        # This preserves the shape/pattern while removing scale differences.
        mean = x.mean()
        std = x.std()


        # Prevent division by zero for constant sequences.
        if std < 1e-8:
            std = 1.0


        x = (x - mean) / std
        y = (y - mean) / std


        return x, y