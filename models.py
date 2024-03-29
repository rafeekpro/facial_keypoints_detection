## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        # Tensor dim: (W-F)/S + 1 = (224 -3)/1 +1 = (221) + 1 = 222 => (16, 222, 222)
        # After Pool 2x2: (16, 111, 111)
        
        self.conv1 = nn.Conv2d(1, 16, 3)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        
        self.pool = nn.MaxPool2d(2, 2)
        
        self.conv2 = nn.Conv2d(16, 32, 3)
        # Tensor dim: (W-F)/S + 1 = (111 -3)/1 +1 = (108) + 1 = 109 => (32, 109, 109)
        # After Pool 2x2: (32, 54, 54)
        
        self.conv3 = nn.Conv2d(32, 64, 3)
        # Tensor dim: (W-F)/S + 1 = (54 -3)/1 +1 = (51) + 1 = 52 => (64, 52, 52)
        # After Pool 2x2: (64, 26, 26)

        self.conv4 = nn.Conv2d(64, 128, 3)
        # Tensor dim: (W-F)/S + 1 = (26 -3)/1 +1 = (23) + 1 = 24 => (128, 24, 24)
        # After Pool 2x2: (128, 12, 12)
        
        self.conv_drop = nn.Dropout(p = 0.2)
        
        self.fc_drop = nn.Dropout(p = 0.3)
        
        # (128, 26, 26) => LINEAR
        #self.fc1 = nn.Linear(128*12*12, 1024)
        self.fc1 = nn.Linear(128*12*12, 1024)
        
        self.fc2 = nn.Linear(1024, 1024)
        
        self.fc3 = nn.Linear(1024, 136)
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        # Drop 0.2
        x = self.conv_drop(x)

        # prep for linear layer
        # flattening 
        x = x.view(x.size(0), -1) 

        # two linear layers with dropout in between
        x = F.relu(self.fc1(x))
        # Drop 0.4
        x = self.fc_drop(x)
        x = self.fc2(x)
        # Drop 0.4
        x = self.fc_drop(x)
        x = self.fc3(x) 
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
