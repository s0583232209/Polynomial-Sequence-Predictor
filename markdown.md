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

PyTorch Dataset             DONE

DataLoader                  DONE

Baseline Rule Solver        DONE

MLP Model                   DONE

Training Pipeline           DONE

Validation                  DONE

Save Best Model             DONE

Testing                     DONE

Prediction Samples          DONE

predict.py                  TODO

GUI                         TODO

Experiments                 TODO

Final Presentation          TODO
```

---

# Next Immediate Step

Create

```
predict.py
```

Responsibilities:

- load best_model.pth
- receive a new input sequence
- normalize the input
- predict the next three values
- display the prediction

```
x = input sequence

y = target sequence
```

---

# Current Model

Architecture:

```
Input (8)

↓

LSTM
(2 layers, hidden size = 64)

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

Current implementation:

- LSTM
- Fully Connected output layer

Future comparison:

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

Build LSTM

↓

4.

Normalize Data

↓

5.

Train

↓

6.

Validate

↓

7.

Save Best Model

↓

8.

Test

↓

9.

Display Sample Predictions

↓

10.

predict.py

↓

11.

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

The dataset and training infrastructure are complete.

Implemented:

- Dataset generation
- Dataset exploration
- Dataset split
- PyTorch Dataset
- DataLoader
- LSTM model
- Training pipeline
- Per-sample normalization
- Validation
- Test evaluation
- Best model saving
- Loss visualization
- Sample prediction evaluation

The next development task is implementing

```
predict.py
```

which will load the trained model and predict the next three values of a new polynomial sequence.

---

# Current Evaluation Results

Latest run:

```
Validation Loss ≈ 0.056

Test Loss ≈ 0.080

Test MAE ≈ 0.115
```

Observation:

- Training converges successfully.
- Validation and Test losses are very similar.
- No significant overfitting observed.
- Sample predictions closely match the target values.
