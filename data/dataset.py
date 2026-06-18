import pandas as pd
import torch
from torch.utils.data import Dataset
from pathlib import Path
import ast


DATA_DIR = Path(__file__).resolve().parent
GENERATED_DIR = DATA_DIR / "generated"


def parse_seq(s):
    return torch.tensor(ast.literal_eval(f"[{s}]"), dtype=torch.float32)


class PolynomialDataset(Dataset):
    def __init__(self, split="train", use_coefficients=False):
        path = GENERATED_DIR / f"{split}.csv"
        self.df = pd.read_csv(path)

        self.use_coefficients = use_coefficients

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        x = parse_seq(row["input_sequence"])
        y = parse_seq(row["target_sequence"])

        degree = torch.tensor(row["degree"], dtype=torch.long)

        coeffs = None
        if self.use_coefficients:
            coeffs = parse_seq(row["coefficients"])

        if self.use_coefficients:
            return x, y, degree, coeffs

        return x, y, degree