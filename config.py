from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

GENERATED_DIR = BASE_DIR / "generated"

TRAIN_PATH = GENERATED_DIR / "train.csv"
VALIDATION_PATH = GENERATED_DIR / "validation.csv"
TEST_PATH = GENERATED_DIR / "test.csv"
DATASET_PATH = GENERATED_DIR / "polynomial_sequences.csv"
BASE_DIR = Path(__file__).resolve().parents[1]

