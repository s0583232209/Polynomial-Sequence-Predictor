# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**PolySeqNet** — a PyTorch LSTM that learns to predict the next 3 values of an integer polynomial sequence given 8 input values, without being told the formula or degree.

**Task:** `[5, 8, 13, 20, 29, 40, 53, 68]` → `[85, 104, 125]`

## Commands

All commands run from the project root unless noted otherwise.

```bash
# 1. Generate raw dataset (run from data/generators/)
python data/generators/polynomial_generator.py

# 2. Split into train/validation/test CSVs
python data/tools/database_split.py

# 3. Explore dataset statistics
python data/tools/database_explore.py

# 4. Verify dataset loading
python data/test_dataset.py

# 5. Verify model architecture (shape smoke test)
python test_modle.py

# 6. Train the model
python train.py
```

Generated CSVs live in `data/generated/` and are gitignored. They must exist before training. `best_model.pth` is also gitignored (*.pth).

## Architecture

```
data/generators/polynomial_generator.py  →  data/generated/polynomial_sequences.csv
data/tools/database_split.py             →  train.csv / validation.csv / test.csv
data/dataset.py  (PolynomialDataset)     →  loads CSVs, normalizes, returns tensors
utils/dataloaders.py (create_dataloaders) →  wraps dataset in DataLoaders
models/lstm.py   (PolynomialLSTM)        →  2-layer LSTM + FC head
train.py                                 →  training loop, saves best_model.pth
```

### Data flow

- `PolynomialDataset.__getitem__` returns `x: (8, 1)` and `y: (3,)` as float tensors.
- Normalization is **per-sample**: mean/std computed from the 8-value input, then applied to both `x` and `y`. This means targets are in the same normalized scale as inputs.
- `PolynomialLSTM` expects input shape `(batch, 8, 1)` — the trailing `1` is the feature dimension (each timestep is a scalar).
- The LSTM uses the **last hidden state** (not the full output sequence) and passes it through `Linear(64→32) → ReLU → Linear(32→3)`.

### Dataset

50,000 synthetic samples, 10,000 per polynomial degree (1–5). Coefficients are integers in [-10, 10]; starting index is random in [-20, 30]. No duplicate sequences allowed. Split: 80% train / 10% validation / 10% test, stratified by degree.

## Design Decisions

- `pathlib` everywhere — no string paths.
- `use_coefficients` parameter exists in `PolynomialDataset` but is not yet wired up; the model only receives the sequence values.
- `scikit-learn` is used only for `train_test_split` in `database_split.py`.
- `config.py` at the project root defines shared path constants for the `data/tools/` scripts.
