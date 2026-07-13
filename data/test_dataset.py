"""
Quick test for PolynomialDataset loading and output shapes.
"""
from data.dataset import PolynomialDataset

dataset = PolynomialDataset("train")

print(len(dataset))

x, y = dataset[0]

print(x)
print(y)

print(x.shape)
print(y.shape)