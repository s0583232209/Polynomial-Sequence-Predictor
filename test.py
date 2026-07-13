import torch

# Basic sanity check: verify PyTorch is installed and report CUDA availability.
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

# Create a small 2x2 tensor to confirm basic operations work.
x = torch.tensor([[1, 2], [3, 4]])
print("\nTensor:")
print(x)

# Apply an element-wise operation to verify computation runs correctly.
y = x * 2
print("\nAfter multiplication:")
print(y)

# Report whether training will use the GPU or fall back to CPU.
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("No GPU found — computations will run on CPU.")