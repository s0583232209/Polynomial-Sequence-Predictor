import torch

from models.lstm import PolynomialLSTM

model = PolynomialLSTM()

x = torch.randn(32, 8, 1)

prediction = model(x)

print(x.shape)
print(prediction.shape)