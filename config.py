from pathlib import Path

# Root of the project (two levels up from this file).
BASE_DIR = Path(__file__).resolve().parent

# Directory where all generated CSV files are stored.
GENERATED_DIR = BASE_DIR / "data" / "generated"

# Paths to the three dataset splits.
TRAIN_PATH = GENERATED_DIR / "train.csv"
VALIDATION_PATH = GENERATED_DIR / "validation.csv"
TEST_PATH = GENERATED_DIR / "test.csv"

# Path to the full unsplit dataset.
DATASET_PATH = GENERATED_DIR / "polynomial_sequences.csv"
