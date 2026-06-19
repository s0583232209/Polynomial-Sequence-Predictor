# Polynomial-sequence-Predictor - Project Context

## Project Overview

**Project Name:** PolySeqNet

**Description:**

PolySeqNet is an AI-powered system for learning and predicting polynomial integer sequences.

The project uses a synthetic dataset of polynomial sequences and trains a PyTorch neural network to predict the next values of a sequence.

The project is developed as a Computer Science / Artificial Intelligence university project.

---

# Main Goal

Given an input sequence:

```
5, 8, 13, 20, 29, 40, 53, 68
```

predict:

```
85, 104, 125
```

without explicitly being given the polynomial formula.

The AI should learn the mathematical pattern from data.

---

# Technologies

- Python 3
- PyTorch
- Pandas
- NumPy
- Scikit-learn
- Git
- GitHub
- PyCharm

---

# Project Structure

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

---

# Dataset Design

The dataset is completely synthetic.

## Polynomial degree

Degrees:

```
1
2
3
4
5
```

Exactly 10,000 samples for each degree.

Total:

```
50,000 samples
```

---

# Polynomial Properties

General polynomial:

```
a0
+ a1*n
+ a2*n²
+ ...
+ a5*n⁵
```

Features:

- positive coefficients
- negative coefficients
- random coefficients
- leading coefficient always non-zero

---

# Sequence Properties

Input sequence length:

```
8 numbers
```

Target sequence length:

```
3 numbers
```

Random starting index:

```
start_n ∈ [-20, 30]
```

The target sequence is a direct continuation of the input sequence.

---

# Duplicate Handling

Duplicate sequences are NOT allowed.

Implementation:

Python set()

```
generated_sequences
```

Generation uses

```
while True
```

instead of recursion.

---

# CSV Structure

Columns:

```
degree
formula
coefficients
start_n
input_length
target_length
input_sequence
target_sequence
```

Example:

| degree | formula | input_sequence        | target_sequence |
| ------ | ------- | --------------------- | --------------- |
| 2      | n²+2n+7 | 4,7,12,19,28,39,52,67 | 84,103,124      |

---

# Tools Already Implemented

## database_generator.py

Creates balanced synthetic dataset.

Features:

- no duplicates
- balanced degrees
- configurable parameters
- automatic CSV creation

Status:

DONE

---

## database_explore.py

Checks:

- number of samples
- duplicates
- missing values
- degree distribution
- example rows

Status:

DONE

---

## database_split.py

Creates:

```
train.csv
validation.csv
test.csv
```

Recommended split:

```
80%
10%
10%
```

Status:

DONE

---

# Git

Repository:

Polynomial-Sequence-Predictor

Generated CSV files are NOT tracked.

.gitignore ignores:

```
.idea/
__pycache__/
venv/
*.pt
*.pth
data/generated/*.csv
```

except

```
.gitkeep
```

---

# Architecture Roadmap

Current status:

```
Dataset Generation          DONE

Dataset Exploration         DONE

Dataset Split               DONE

PyTorch Dataset             TODO

DataLoader                  TODO

Baseline Rule Solver        TODO

MLP Model                   TODO

Training Pipeline           TODO

Validation                  TODO

Prediction                  TODO

GUI                         TODO

Experiments                 TODO

Final Presentation          TODO
```

---

# Next Immediate Step

Create

```
data/dataset.py
```

Implement

```
class PolynomialDataset(Dataset)
```

Responsibilities:

- load CSV
- convert string sequences to lists
- convert lists to torch.FloatTensor
- return

```
x = input sequence

y = target sequence
```

---

# Planned Model

Initial architecture:

```
Input (8)

↓

Linear

↓

ReLU

↓

Linear

↓

ReLU

↓

Linear

↓

Output (3)
```

Simple MLP first.

Future comparison:

- LSTM
- Transformer

---

# Baseline Solver

Before training AI,

implement a mathematical solver using finite differences.

Purpose:

Provide a benchmark.

If AI performs worse than the mathematical solver,
the implementation should be investigated.

---

# Training Plan

1.

Load Dataset

↓

2.

Create DataLoader

↓

3.

Build MLP

↓

4.

Train

↓

5.

Validate

↓

6.

Save Best Model

↓

7.

Test

↓

8.

Predict

↓

9.

GUI

---

# Evaluation Metrics

Training Loss

Validation Loss

Test Loss

MAE

MSE

Prediction Accuracy

---

# Coding Style

Always:

- readable code
- pathlib instead of relative paths
- configuration variables at top
- type hints when possible
- comments for major sections
- modular design
- no duplicated logic

---

# Important Design Decisions

- Fixed input length (8)
- Fixed target length (3)
- Balanced dataset
- Synthetic data only
- No duplicate sequences
- PyTorch implementation
- Scikit-learn allowed only for utilities
- Modular architecture
- Git after every completed feature

---

# Development Philosophy

Take very small steps.

Every step should:

1.

Implement one feature.

2.

Run successfully.

3.

Be tested.

4.

Be committed to Git.

Only then continue.

Never implement multiple large features simultaneously.

---

# Current Status

Project foundation is complete.

The dataset infrastructure is finished.

The next development task is implementing the PyTorch Dataset class and verifying that it correctly loads train.csv and returns tensors suitable for DataLoader and model training.
