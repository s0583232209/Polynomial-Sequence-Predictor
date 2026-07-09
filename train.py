# import torch
# import torch.nn as nn
# import matplotlib.pyplot as plt
# from utils.dataloaders import create_dataloaders
# from models.lstm import PolynomialLSTM
# device = torch.device(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )
#
# print(f"Using device: {device}")
# train_loader, validation_loader, test_loader = create_dataloaders()
# model = PolynomialLSTM().to(device)
# optimizer = torch.optim.Adam(
#     model.parameters(),
#     lr=0.001,
# )
# print(model)
# print()
#
# print(f"Train batches: {len(train_loader)}")
# print(f"Validation batches: {len(validation_loader)}")
# print(f"Test batches: {len(test_loader)}")
# NUM_EPOCHS = 20
# criterion = nn.MSELoss()
# criterion_mae = nn.L1Loss()
# train_losses = []
# val_losses = []
# best_val_loss = float("inf")
# for x, y in train_loader:
#     print("Input min:", x.min().item())
#     print("Input max:", x.max().item())
#     print("Target min:", y.min().item())
#     print("Target max:", y.max().item())
#     break
# def evaluate(model, loader, mse_criterion, mae_criterion, device):
#         model.eval()
#
#         total_mse = 0.0
#         total_mae = 0.0
#
#         with torch.no_grad():
#             for x, y in loader:
#                 x = x.to(device)
#                 y = y.to(device)
#
#                 prediction = model(x)
#
#                 mse = mse_criterion(prediction, y)
#                 mae = mae_criterion(prediction, y)
#
#                 total_mse += mse.item()
#                 total_mae += mae.item()
#
#         return (
#             total_mse / len(loader),
#             total_mae / len(loader),
#         )
# for epoch in range(NUM_EPOCHS):
#
#     model.train()
#     running_loss = 0.0
#
#     for x, y in train_loader:
#
#         x = x.to(device)
#         y = y.to(device)
#
#         prediction = model(x)
#         loss = criterion(prediction, y)
#
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#
#         running_loss += loss.item()
#
#     train_loss = running_loss / len(train_loader)
#     # val_loss = evaluate(model, validation_loader, criterion, device)
#     val_loss, val_mae = evaluate(
#         model,
#         validation_loader,
#         criterion,
#         criterion_mae,
#         device,
#     )
#     train_losses.append(train_loss)
#     val_losses.append(val_loss)
#
#     print(
#         f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
#         f"Train Loss: {train_loss:.6f} | "
#         f"Val Loss: {val_loss:.6f} | "
#         f"Val MAE: {val_mae:.6f}"
#     )
#     if val_loss < best_val_loss:
#         best_val_loss = val_loss
#         torch.save(model.state_dict(), "best_model.pth")
#         print("Best model saved.")
# plt.figure()
#
# plt.plot(train_losses, label="Train Loss")
# plt.plot(val_losses, label="Validation Loss")
# plt.xlabel("Epoch")
# plt.ylabel("MSE Loss")
# plt.title("Training vs Validation Loss")
# plt.legend()
# plt.yscale("log")
# plt.show()
#
# # Load best model
# model.load_state_dict(torch.load("best_model.pth"))
#
# test_loss, test_mae = evaluate(
#     model,
#     test_loader,
#     criterion,
#     criterion_mae,
#     device,
# )
#
# print(f"\nTest MSE: {test_loss:.6f}")
# print(f"Test MAE: {test_mae:.6f}")
#
# print("\nSample predictions:")
#
# model.eval()
#
# with torch.no_grad():
#
#     x, y = next(iter(test_loader))
#
#     x = x.to(device)
#
#     predictions = model(x).cpu()
#
#     for i in range(5):
#
#         print("=" * 40)
#         print(f"Sample {i+1}")
#
#         print("Target:")
#         print(y[i])
#
#         print("Prediction:")
#         print(predictions[i])
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from utils.dataloaders import create_dataloaders
from models.lstm import PolynomialLSTM


# -----------------------------
# Device
# -----------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using device: {device}")


# -----------------------------
# Data
# -----------------------------

train_loader, validation_loader, test_loader = create_dataloaders()

print(f"Train batches: {len(train_loader)}")
print(f"Validation batches: {len(validation_loader)}")
print(f"Test batches: {len(test_loader)}")


# -----------------------------
# Model
# -----------------------------

model = PolynomialLSTM().to(device)

print(model)
print()


# -----------------------------
# Training setup
# -----------------------------

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.001,
    weight_decay=1e-4,
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=5,
)

criterion = nn.MSELoss()
criterion_mae = nn.L1Loss()


NUM_EPOCHS = 200

best_val_loss = float("inf")

patience = 25
epochs_without_improvement = 0


train_losses = []
val_losses = []


# -----------------------------
# Check data range
# -----------------------------

for x, y in train_loader:

    print("Input min:", x.min().item())
    print("Input max:", x.max().item())

    print("Target min:", y.min().item())
    print("Target max:", y.max().item())

    break


# -----------------------------
# Evaluation function
# -----------------------------

def evaluate(model, loader, mse_criterion, mae_criterion, device):

    model.eval()

    total_mse = 0.0
    total_mae = 0.0


    with torch.no_grad():

        for x, y in loader:

            x = x.to(device)
            y = y.to(device)


            prediction = model(x)


            mse = mse_criterion(
                prediction,
                y
            )

            mae = mae_criterion(
                prediction,
                y
            )


            total_mse += mse.item()
            total_mae += mae.item()


    return (
        total_mse / len(loader),
        total_mae / len(loader)
    )


# -----------------------------
# Training loop
# -----------------------------

for epoch in range(NUM_EPOCHS):

    model.train()

    running_loss = 0.0


    for x, y in train_loader:

        x = x.to(device)
        y = y.to(device)


        prediction = model(x)


        loss = criterion(
            prediction,
            y
        )


        optimizer.zero_grad()


        loss.backward()


        # Prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0
        )


        optimizer.step()


        running_loss += loss.item()



    train_loss = running_loss / len(train_loader)



    val_loss, val_mae = evaluate(
        model,
        validation_loader,
        criterion,
        criterion_mae,
        device
    )


    scheduler.step(val_loss)



    train_losses.append(train_loss)
    val_losses.append(val_loss)



    current_lr = optimizer.param_groups[0]["lr"]


    print(
        f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
        f"LR: {current_lr:.6f} | "
        f"Train Loss: {train_loss:.6f} | "
        f"Val Loss: {val_loss:.6f} | "
        f"Val MAE: {val_mae:.6f}"
    )



    # -----------------------------
    # Save best model
    # -----------------------------

    if val_loss < best_val_loss:

        best_val_loss = val_loss

        epochs_without_improvement = 0


        torch.save(
            model.state_dict(),
            "best_model.pth"
        )


        print("Best model saved.")


    else:

        epochs_without_improvement += 1



    # -----------------------------
    # Early stopping
    # -----------------------------

    if epochs_without_improvement >= patience:

        print(
            "Early stopping triggered."
        )

        break



# -----------------------------
# Plot losses
# -----------------------------

plt.figure()

plt.plot(
    train_losses,
    label="Train Loss"
)

plt.plot(
    val_losses,
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title(
    "Training vs Validation Loss"
)

plt.legend()

plt.yscale("log")

plt.show()



# -----------------------------
# Load best model
# -----------------------------

model.load_state_dict(
    torch.load(
        "best_model.pth",
        weights_only=True
    )
)



# -----------------------------
# Test
# -----------------------------

test_loss, test_mae = evaluate(
    model,
    test_loader,
    criterion,
    criterion_mae,
    device
)


print(
    f"\nTest MSE: {test_loss:.6f}"
)

print(
    f"Test MAE: {test_mae:.6f}"
)



# -----------------------------
# Sample predictions
# -----------------------------

print("\nSample predictions:")


model.eval()


with torch.no_grad():

    x, y = next(iter(test_loader))


    x = x.to(device)


    predictions = model(x).cpu()



    for i in range(5):

        print("=" * 40)

        print(
            f"Sample {i+1}"
        )

        print(
            "Target:"
        )

        print(
            y[i]
        )


        print(
            "Prediction:"
        )

        print(
            predictions[i]
        )