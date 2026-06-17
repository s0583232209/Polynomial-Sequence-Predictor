import pandas as pd


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "data" / "generated" / "polynomial_sequences.csv"

def main():

    df = pd.read_csv(DATASET_PATH)

    print("=" * 50)
    print("DATASET INFORMATION")
    print("=" * 50)

    print(f"\nNumber of samples: {len(df)}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nDegree distribution:")

    degree_counts = df["degree"].value_counts().sort_index()

    for degree, count in degree_counts.items():
        print(f"Degree {degree}: {count}")

    print("\nExample rows:")

    print(df.head())

    print("\nUnique rows:")
    print(len(df.drop_duplicates()))

    duplicate_percentage = (df.duplicated().sum() / len(df)) * 100

    print(f"\nDuplicate percentage: {duplicate_percentage:.2f}%")
    lengths = df["input_sequence"].apply(
    lambda x: len(str(x).split(","))
)


if __name__ == "__main__":
    main()