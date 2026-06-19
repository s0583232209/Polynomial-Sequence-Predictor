import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from utils.dataloaders import create_dataloaders
from models.lstm import PolynomialLSTM
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {device}")
train_loader, validation_loader, test_loader = create_dataloaders()
model = PolynomialLSTM().to(device)
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
)
print(model)
print()

print(f"Train batches: {len(train_loader)}")
print(f"Validation batches: {len(validation_loader)}")
print(f"Test batches: {len(test_loader)}")
NUM_EPOCHS = 20
criterion = nn.MSELoss()
train_losses = []
val_losses = []
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)

            prediction = model(x)
            loss = criterion(prediction, y)

            total_loss += loss.item()

    return total_loss / len(loader)
for epoch in range(NUM_EPOCHS):

    model.train()
    running_loss = 0.0

    for x, y in train_loader:

        x = x.to(device)
        y = y.to(device)

        prediction = model(x)
        loss = criterion(prediction, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    train_loss = running_loss / len(train_loader)
    val_loss = evaluate(model, validation_loader, criterion, device)

    train_losses.append(train_loss)
    val_losses.append(val_loss)

    print(
        f"Epoch {epoch+1}/{NUM_EPOCHS} | "
        f"Train Loss: {train_loss:.6f} | "
        f"Val Loss: {val_loss:.6f}"
    )
    plt.figure()

    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Validation Loss")

    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.yscale("log")
    plt.show()