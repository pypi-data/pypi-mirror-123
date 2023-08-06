import torch.nn as nn


class ExampleNet(nn.Module):
    """
    The example net
    """

    def __init__(self):
        super(ExampleNet, self).__init__()
        self.seq_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),

            nn.Conv2d(8, 16, kernel_size=5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),

        )  # 1 1 1 2
        self.fc = nn.Sequential(
            nn.Linear(144, 72),
            nn.Linear(72, 10)
        )

    def feed_forward(self, x):
        x = self.seq_block(x).flatten(start_dim=1)
        x = self.fc(x)
        x = nn.Dropout(0.2)(x)
        # x = F.normalize(x, p=2, dim=1)
        # return nn.LogSoftmax(dim=-1)(x)
        return nn.Softmax(dim=-1)(x)

    def forward(self, x):
        return self.feed_forward(x)
