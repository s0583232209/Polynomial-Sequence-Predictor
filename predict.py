"""
Load a trained LSTM model and use it to predict the next three values
of a polynomial sequence.

This script:
    1. Loads the saved model from disk.
    2. Normalizes an input sequence of 8 values.
    3. Uses the trained model to predict the next 3 values.
    4. Converts the predictions back to the original scale.
    5. Allows interactive prediction from the command line.
"""

from pathlib import Path

import torch

from models.lstm import PolynomialLSTM


# ==========================================================
# Paths and Device Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cache the loaded model so it is only loaded once.
_model = None


# ==========================================================
# Model Utilities
# ==========================================================

def model_available() -> bool:
    """
    Check whether the trained model file exists.

    Returns:
        True if the model file exists, otherwise False.
    """
    return MODEL_PATH.exists()


def load_model() -> PolynomialLSTM:
    """
    Load the trained model into memory.

    The model is loaded only once and then cached for future
    predictions.

    Returns:
        The trained PolynomialLSTM model.
    """

    global _model

    if _model is None:
        model = PolynomialLSTM().to(device)

        model.load_state_dict(
            torch.load(
                MODEL_PATH,
                map_location=device,
            )
        )

        model.eval()

        _model = model

    return _model


# ==========================================================
# Prediction Function
# ==========================================================

def predict_sequence(sequence: list[float]) -> list[float]:
    """
    Predict the next three values of a polynomial sequence.

    The input sequence is normalized using its own mean and
    standard deviation before being passed to the model.
    The predictions are then converted back to the original scale.

    Args:
        sequence:
            A list containing exactly 8 numbers.

    Returns:
        A list containing the predicted next 3 values.

    Raises:
        ValueError:
            If the input does not contain exactly 8 numbers.
    """

    if len(sequence) != 8:
        raise ValueError("Exactly 8 numbers are required.")

    model = load_model()

    x = torch.tensor(sequence, dtype=torch.float32)

    mean = x.mean()
    std = x.std()

    # Prevent division by zero when all input values are equal.
    if std < 1e-8:
        std = torch.tensor(1.0)

    # Normalize the input using the same preprocessing
    # performed during training.
    x = (x - mean) / std

    # Convert to the expected LSTM input shape:
    # (batch_size, sequence_length, features)
    x = x.unsqueeze(-1)
    x = x.unsqueeze(0)
    x = x.to(device)

    with torch.no_grad():
        prediction = model(x)

    # Convert predictions back to the original scale.
    prediction = prediction.cpu().squeeze(0)
    prediction = prediction * std + mean

    return [value.item() for value in prediction]


# ==========================================================
# Command-Line Interface
# ==========================================================

if __name__ == "__main__":

    print(f"Using device: {device}")

    if not model_available():
        print(f"Model file not found at {MODEL_PATH}")
        exit()

    load_model()
    print("Model loaded successfully!")

    user_input = input(
        "Enter 8 numbers separated by commas:\n"
    )

    try:
        sequence = [
            float(x.strip())
            for x in user_input.split(",")
        ]

        result = predict_sequence(sequence)

    except ValueError as e:
        print(f"Input error: {e}")
        exit()

    print("Predicted next values:")

    for value in result:
        print(round(value, 2))