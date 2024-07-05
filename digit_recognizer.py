from torch import nn
import torch

class DigitRecognizer(nn.Module):
    def __init__(self):
        super(DigitRecognizer, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=2, padding=1, stride=1)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=64, kernel_size=3, padding=1, stride=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1, stride=1)

        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(in_features=128*3*3, out_features=15*10)
        self.fc2 = nn.Linear(in_features=15*10, out_features=15)

        self.dropout = nn.Dropout(p=0.5)
        self.relu = nn.ReLU()

        self.idx_to_class = {0: "+",
                             1: "-",
                             2: "0",
                             3: "1",
                             4: "2",
                             5: "3",
                             6: "4",
                             7: "5",
                             8: "6",
                             9: "7",
                             10: "8",
                             11: "9",
                             12: "=",
                             13: "/",
                             14: "*"}
        

    def forward(self, x):
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.relu(x)

        x = self.conv3(x)
        x = self.maxpool3(x)
        x = self.relu(x)
        
        x = x.view(x.size(0), -1)
        x = self.dropout(x)

        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

    @staticmethod
    def proba_to_predict(proba):
        with torch.no_grad():
            return proba.argmax(1).squeeze(-1)
        
    def predict_to_class(self, predict):
        with torch.no_grad():
            return self.idx_to_class[predict.item()]
            