from torch.utils.data import DataLoader

from data.dataset import PolynomialDataset


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DEFAULT_BATCH_SIZE = 32


# --------------------------------------------------
# Create DataLoaders
# --------------------------------------------------

def create_dataloaders(batch_size=DEFAULT_BATCH_SIZE):

    train_dataset = PolynomialDataset("train")

    validation_dataset = PolynomialDataset("validation")

    test_dataset = PolynomialDataset("test")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
    )

    return (
        train_loader,
        validation_loader,
        test_loader,
    )