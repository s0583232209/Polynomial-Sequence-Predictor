import torch

print("גרסת PyTorch:", torch.__version__)
print("CUDA זמין:", torch.cuda.is_available())

# יצירת Tensor
x = torch.tensor([[1, 2], [3, 4]])
print("\nTensor:")
print(x)

# פעולת חישוב
y = x * 2
print("\nלאחר הכפלה:")
print(y)

if torch.cuda.is_available():
    print("שם הכרטיס:", torch.cuda.get_device_name(0))
else:
    print("החישובים יתבצעו על המעבד (CPU).")