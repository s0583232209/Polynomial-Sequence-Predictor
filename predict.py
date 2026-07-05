import torch

from models.lstm import PolynomialLSTM

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {device}")

model = PolynomialLSTM().to(device)

model.load_state_dict(
    torch.load("best_model.pth", map_location=device)
)

model.eval()
print("Model loaded successfully!")

user_input = input("Enter 8 numbers separated by commas:\n")

try:
    sequence = [float(x.strip()) for x in user_input.split(",")]

    if len(sequence) != 8:
        raise ValueError("Exactly 8 numbers are required.")

except ValueError as e:
    print(f"Input error: {e}")
    exit()

x = torch.tensor(sequence, dtype=torch.float32)
mean = x.mean()
std = x.std()

if std < 1e-8:
    std = 1.0

x = (x - mean) / std
x = x.unsqueeze(-1)
x = x.unsqueeze(0)
x = x.to(device)

with torch.no_grad():
    prediction = model(x)

prediction = prediction.cpu().squeeze(0)

prediction = prediction * std + mean

print("Predicted next values:")

for value in prediction:
    print(round(value.item(), 2))