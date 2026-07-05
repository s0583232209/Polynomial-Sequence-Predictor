from pathlib import Path

import torch

from models.lstm import PolynomialLSTM

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_model = None


def model_available() -> bool:
    return MODEL_PATH.exists()


def load_model() -> PolynomialLSTM:
    global _model

    if _model is None:
        model = PolynomialLSTM().to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.eval()
        _model = model

    return _model


def predict_sequence(sequence: list[float]) -> list[float]:
    """Predict the next 3 values given 8 input values."""

    if len(sequence) != 8:
        raise ValueError("Exactly 8 numbers are required.")

    model = load_model()

    x = torch.tensor(sequence, dtype=torch.float32)
    mean = x.mean()
    std = x.std()

    if std < 1e-8:
        std = torch.tensor(1.0)

    x = (x - mean) / std
    x = x.unsqueeze(-1)
    x = x.unsqueeze(0)
    x = x.to(device)

    with torch.no_grad():
        prediction = model(x)

    prediction = prediction.cpu().squeeze(0)
    prediction = prediction * std + mean

    return [value.item() for value in prediction]


if __name__ == "__main__":
    print(f"Using device: {device}")

    if not model_available():
        print(f"Model file not found at {MODEL_PATH}")
        exit()

    load_model()
    print("Model loaded successfully!")

    user_input = input("Enter 8 numbers separated by commas:\n")

    try:
        sequence = [float(x.strip()) for x in user_input.split(",")]
        result = predict_sequence(sequence)
    except ValueError as e:
        print(f"Input error: {e}")
        exit()

    print("Predicted next values:")
    for value in result:
        print(round(value, 2))
