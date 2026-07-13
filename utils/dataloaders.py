"""
Create PyTorch DataLoaders for the polynomial sequence dataset.

This module:
    1. Loads the training, validation, and test datasets.
    2. Wraps each dataset with a PyTorch DataLoader.
    3. Returns loaders that can be used during model training
       and evaluation.
"""

from torch.utils.data import DataLoader

from data.dataset import PolynomialDataset


# ==========================================================
# Configuration
# ==========================================================

DEFAULT_BATCH_SIZE = 32


# ==========================================================
# DataLoader Creation
# ==========================================================

def create_dataloaders(batch_size=DEFAULT_BATCH_SIZE):
    """
    Create DataLoaders for training, validation, and testing.

    Each DataLoader provides batches of polynomial sequences
    that can be efficiently processed by the neural network.

    Args:
        batch_size:
            Number of samples processed together in one batch.

    Returns:
        tuple:
            (
                train_loader,
                validation_loader,
                test_loader
            )
    """

    train_dataset = PolynomialDataset("train")

    validation_dataset = PolynomialDataset("validation")

    test_dataset = PolynomialDataset("test")


    # Shuffle training data so that the model does not learn
    # from the original ordering of samples.
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
    )


    # Validation and test data keep their original order
    # because they are only used for evaluation.
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