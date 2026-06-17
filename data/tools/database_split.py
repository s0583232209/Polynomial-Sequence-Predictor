import pandas as pd

from sklearn.model_selection import train_test_split

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

GENERATED_DIR = BASE_DIR / "generated"

TRAIN_PATH = GENERATED_DIR / "train.csv"
VALIDATION_PATH = GENERATED_DIR / "validation.csv"
TEST_PATH = GENERATED_DIR / "test.csv"
DATASET_PATH = GENERATED_DIR / "polynomial_sequences.csv"


def main():

    df = pd.read_csv(DATASET_PATH)

    train_df, temp_df = train_test_split(

        df,

        test_size=0.2,

        random_state=42,

        shuffle=True,

        stratify=df["degree"]

    )

    validation_df, test_df = train_test_split(

        temp_df,

        test_size=0.5,

        random_state=42,

        shuffle=True,

        stratify=temp_df["degree"]

    )

    train_df.to_csv(TRAIN_PATH, index=False)

    validation_df.to_csv(VALIDATION_PATH, index=False)

    test_df.to_csv(TEST_PATH, index=False)

    print()

    print("Dataset successfully split!")

    print(f"Train samples: {len(train_df)}")

    print(f"Validation samples: {len(validation_df)}")

    print(f"Test samples: {len(test_df)}")


if __name__ == "__main__":
    main()