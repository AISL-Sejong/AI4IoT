import torch
torch.cuda.init()
print('wjjji')
print(torch.randn(1, device='cuda'))