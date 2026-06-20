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
criterion_mae = nn.L1Loss()
train_losses = []
val_losses = []
best_val_loss = float("inf")
for x, y in train_loader:
    print("Input min:", x.min().item())
    print("Input max:", x.max().item())
    print("Target min:", y.min().item())
    print("Target max:", y.max().item())
    break
def evaluate(model, loader, mse_criterion, mae_criterion, device):
        model.eval()

        total_mse = 0.0
        total_mae = 0.0

        with torch.no_grad():
            for x, y in loader:
                x = x.to(device)
                y = y.to(device)

                prediction = model(x)

                mse = mse_criterion(prediction, y)
                mae = mae_criterion(prediction, y)

                total_mse += mse.item()
                total_mae += mae.item()

        return (
            total_mse / len(loader),
            total_mae / len(loader),
        )
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
    # val_loss = evaluate(model, validation_loader, criterion, device)
    val_loss, val_mae = evaluate(
        model,
        validation_loader,
        criterion,
        criterion_mae,
        device,
    )
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    print(
        f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
        f"Train Loss: {train_loss:.6f} | "
        f"Val Loss: {val_loss:.6f} | "
        f"Val MAE: {val_mae:.6f}"
    )
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), "best_model.pth")
        print("Best model saved.")
plt.figure()

plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.yscale("log")
plt.show()