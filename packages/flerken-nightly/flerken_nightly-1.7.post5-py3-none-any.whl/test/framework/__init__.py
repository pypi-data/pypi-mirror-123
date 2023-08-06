import torch
from numpy import nan, inf
from flerken.framework import train, val


class toy_example(torch.nn.Module):
    def __init__(self, isnan=False, isinf=False):
        super(toy_example, self).__init__()
        self.module1 = torch.nn.Conv2d(1, 10, 3)
        self.module2 = torch.nn.Conv2d(10, 10, 3)
        self.isnan = isnan
        self.isinf = isinf

    def forward(self, x):
        x = self.module1(x)
        if self.isnan:
            x += torch.tensor(nan)

        x = self.module2(x)
        if self.isinf:
            x += torch.tensor(inf)
        return torch.sigmoid(x)


class database(torch.utils.data.Dataset):
    def __len__(self):
        return 30

    def __getitem__(self, idx):
        return torch.randint(0, 2, (10, 6, 6)).float(), [torch.randint(0, 5, (1, 10, 10)).float()], []


