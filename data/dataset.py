# import pandas as pd
# import torch
# from torch.utils.data import Dataset
# from pathlib import Path
# import ast
#
#
#
# DATA_DIR = Path(__file__).resolve().parent
# GENERATED_DIR = DATA_DIR / "generated"
# MEAN = 0
# STD = 1000
#
# def parse_seq(s)  -> torch.Tensor:
#     return torch.tensor(ast.literal_eval(f"[{s}]"), dtype=torch.float32)
#
#
# class PolynomialDataset(Dataset):
#     def __init__(self, split="train", use_coefficients=False):
#         path = GENERATED_DIR / f"{split}.csv"
#         self.df = pd.read_csv(path)
#
#         self.use_coefficients = use_coefficients
#
#     def __len__(self) ->int:
#         return len(self.df)
#
#
#     def __getitem__(self, idx: int):
#         row = self.df.iloc[idx]
#
#         x = (parse_seq(row["input_sequence"]) - MEAN) / STD
#         y = (parse_seq(row["target_sequence"]) - MEAN) / STD
#
#
#
#
#
#         return x, y
#
# def normalize(x):
#     return x / 1000.0
import pandas as pd
import torch
from torch.utils.data import Dataset
from pathlib import Path
import ast

# ----------------------------
# Paths
# ----------------------------
DATA_DIR = Path(__file__).resolve().parent
GENERATED_DIR = DATA_DIR / "generated"

# ----------------------------
# Helpers
# ----------------------------
def parse_seq(s: str) -> torch.Tensor:
    """
    Convert CSV string like:
    "1,2,3,4"
    into tensor([1,2,3,4])
    """
    return torch.tensor(ast.literal_eval(f"[{s}]"), dtype=torch.float32)

# ----------------------------
# Dataset
# ----------------------------
class PolynomialDataset(Dataset):

    def __init__(self, split="train", mean=None, std=None):
        path = GENERATED_DIR / f"{split}.csv"
        self.df = pd.read_csv(path)

        # optional normalization (recommended)
        self.mean = mean
        self.std = std

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx: int):
        row = self.df.iloc[idx]

        # input sequence -> (seq_len, 1) for LSTM
        x = parse_seq(row["input_sequence"]).unsqueeze(-1)

        # target sequence -> (output_len,)
        y = parse_seq(row["target_sequence"])

        # ----------------------------
        # normalization (SAFE)
        # ----------------------------
        # compute statistics from the input sequence
        mean = x.mean()
        std = x.std()

        # avoid division by zero
        if std < 1e-8:
            std = 1.0

        # normalize input and target
        x = (x - mean) / std
        y = (y - mean) / std
        return x, y