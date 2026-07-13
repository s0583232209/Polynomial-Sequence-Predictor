# Polynomial Sequence Predictor

**AI-powered polynomial integer sequence prediction, built with PyTorch.**

PolySeqNet learns to predict the continuation of polynomial integer sequences directly from data — without ever being given the underlying formula. Given an 8-number input sequence, the model predicts the next 3 values.

```
Input:  5, 8, 13, 20, 29, 40, 53, 68
Output: 85, 104, 125
```

This project was developed as a Computer Science / Artificial Intelligence university project.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation Results](#evaluation-results)
- [Roadmap](#roadmap)
- [Design Decisions](#design-decisions)
- [Tech Stack](#tech-stack)

---

## Overview

PolySeqNet generates a large synthetic dataset of polynomial sequences (degrees 1–5), then trains an LSTM-based neural network to learn the underlying numeric pattern and extrapolate it. A finite-differences baseline solver is included as a mathematical benchmark to sanity-check the learned model's performance.

## Architecture

```
Input (8)
   ↓
LSTM (2 layers, hidden size = 64)
   ↓
Dropout
   ↓
Linear
   ↓
ReLU
   ↓
Linear
   ↓
Output (3)
```

A Transformer-based architecture is planned as a future comparison point against the current LSTM model.

## Project Structure

```
project/
├── data/
│   ├── generated/
│   │   ├── polynomial_sequences.csv
│   │   ├── train.csv
│   │   ├── validation.csv
│   │   └── test.csv
│   │
│   └── tools/
│       ├── database_generator.py
│       ├── database_explore.py
│       └── database_split.py
│
├── models/
├── rules/
├── gui/
├── utils/
│
├── train.py
├── predict.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Dataset

The dataset is fully synthetic and generated with `database_generator.py`.

- **Polynomial degrees:** 1, 2, 3, 4, 5
- **Samples per degree:** 10,000
- **Total samples:** 50,000
- **Input sequence length:** 8
- **Target sequence length:** 3
- **Random starting index:** `start_n ∈ [-20, 30]`
- **Coefficients:** positive, negative, and random values (leading coefficient always non-zero)
- **No duplicate sequences** (enforced via a Python `set()` and a `while True` generation loop)

### CSV columns

| Column | Description |
|---|---|
| `degree` | Polynomial degree |
| `formula` | Human-readable formula |
| `coefficients` | Polynomial coefficients |
| `start_n` | Starting index of the sequence |
| `input_length` | Length of the input sequence (8) |
| `target_length` | Length of the target sequence (3) |
| `input_sequence` | The 8-number input |
| `target_sequence` | The 3-number continuation |

**Example**

| degree | formula | input_sequence | target_sequence |
|---|---|---|---|
| 2 | n²+2n+7 | 4,7,12,19,28,39,52,67 | 84,103,124 |

### Data pipeline tools

| Tool | Purpose | Status |
|---|---|---|
| `database_generator.py` | Generates the balanced, duplicate-free dataset | ✅ Done |
| `database_explore.py` | Reports sample counts, duplicates, missing values, degree distribution | ✅ Done |
| `database_split.py` | Splits data into train/validation/test (80/10/10) | ✅ Done |

Generated CSV files are **not** tracked in Git (see `.gitignore`).

## Installation

```bash
git clone https://github.com/<your-username>/Polynomial-Sequence-Predictor.git
cd Polynomial-Sequence-Predictor
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Generate the dataset

```bash
python data/tools/database_generator.py
```

### 2. Explore the dataset

```bash
python data/tools/database_explore.py
```

### 3. Split into train/validation/test

```bash
python data/tools/database_split.py
```

### 4. Train the model

```bash
python train.py
```

Training normalizes data per-sample, trains the LSTM, validates each epoch, and saves the best-performing model as `best_model.pth`.

### 5. Predict on a new sequence

```bash
python predict.py
```

`predict.py` loads `best_model.pth`, accepts an 8-integer input sequence, applies the same normalization used during training, and outputs the predicted next 3 values restored to their original scale.

### 6. GUI (in progress)

A graphical interface for entering sequences and viewing predictions is under active development in the `gui/` module.

## Evaluation Results

Latest training run:

| Metric | Value |
|---|---|
| Validation Loss | ≈ 0.056 |
| Test Loss | ≈ 0.080 |
| Test MAE | ≈ 0.115 |

**Observations:**
- Training converges successfully.
- Validation and test losses are very close, indicating no significant overfitting.
- Sample predictions closely match target values.

A finite-differences baseline solver is used as a benchmark — if the neural network underperforms it, that signals an issue worth investigating.

## Roadmap

| Stage | Status |
|---|---|
| Dataset Generation | ✅ Done |
| Dataset Exploration | ✅ Done |
| Dataset Split | ✅ Done |
| PyTorch Dataset | ✅ Done |
| DataLoader | ✅ Done |
| Baseline Rule Solver | ✅ Done |
| MLP Model | ⏭️ Skipped |
| Training Pipeline | ✅ Done |
| Validation | ✅ Done |
| Save Best Model | ✅ Done |
| Testing | ✅ Done |
| Prediction Samples | ✅ Done |
| `predict.py` | ✅ Done |
| GUI | 🚧 In Progress |
| Experiments (e.g. Transformer comparison) | 📋 To Do |
| Final Presentation | 📋 To Do |

**Next immediate step:** build the GUI — load the trained model, accept and validate user input, run `predict.py`, and display the predicted continuation.

## Design Decisions

- Fixed input length (8) and target length (3)
- Balanced dataset across all polynomial degrees
- Synthetic data only, with no duplicate sequences
- PyTorch for modeling; scikit-learn used only for utility functions
- Modular, readable codebase with `pathlib`, type hints, and section comments
- Small, incremental development steps — each feature implemented, tested, and committed to Git before moving on

## Tech Stack

- Python 3
- PyTorch
- Pandas
- NumPy
- Scikit-learn
- Git / GitHub
- PyCharm

---

## License

Add your license of choice here (e.g. MIT).
