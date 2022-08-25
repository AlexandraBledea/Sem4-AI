from PIL import Image
import os
import torch
import torch.nn as nn
from torchvision.datasets import CIFAR10
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.autograd import Variable
import numpy as np
from dataset import ImageClassifierDataset
from utils import PICTURE_SIZE

class Unit(nn.Module):
    def __init__(self,in_channels,out_channels):

        super(Unit,self).__init__()
        
        self.conv = nn.Conv2d(in_channels=in_channels,kernel_size=3,out_channels=out_channels,stride=1,padding=1)
        self.bn = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU()


    def forward(self,input):

        output = self.conv(input)
        output = self.bn(output)
        output = self.relu(output)

        return output


class SimpleNet(nn.Module):

    def __init__(self,num_classes=2):

        super(SimpleNet,self).__init__()

        #Create 14 layers of the unit with max pooling in between
        # Input layer has 3 inputs because rgb tuple
        self.unit1 = Unit(in_channels=3, out_channels=PICTURE_SIZE // 2)

        self.unit2 = Unit(in_channels=PICTURE_SIZE // 2, out_channels=PICTURE_SIZE // 2)
        self.unit3 = Unit(in_channels=PICTURE_SIZE // 2, out_channels=PICTURE_SIZE // 2)

        self.pool1 = nn.MaxPool2d(kernel_size=2)

        self.unit4 = Unit(in_channels=PICTURE_SIZE // 2, out_channels=PICTURE_SIZE)
        self.unit5 = Unit(in_channels=PICTURE_SIZE, out_channels=PICTURE_SIZE)
        self.unit6 = Unit(in_channels=PICTURE_SIZE, out_channels=PICTURE_SIZE)
        self.unit7 = Unit(in_channels=PICTURE_SIZE, out_channels=PICTURE_SIZE)

        self.pool2 = nn.MaxPool2d(kernel_size=2)

        self.unit8 = Unit(in_channels=PICTURE_SIZE, out_channels=PICTURE_SIZE * 2)
        self.unit9 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)
        self.unit10 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)
        self.unit11 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)

        self.pool3 = nn.MaxPool2d(kernel_size=2)

        self.unit12 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)
        self.unit13 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)
        self.unit14 = Unit(in_channels=PICTURE_SIZE * 2, out_channels=PICTURE_SIZE * 2)

        self.avgpool = nn.AvgPool2d(kernel_size=4)
        
        #Add all the units into the Sequential layer in exact order
        self.net = nn.Sequential(self.unit1, self.unit2, self.unit3, self.pool1, self.unit4, self.unit5, self.unit6
                                 ,self.unit7, self.pool2, self.unit8, self.unit9, self.unit10, self.unit11, self.pool3,
                                 self.unit12, self.unit13, self.unit14, self.avgpool)

        self.fc = nn.Linear(in_features=PICTURE_SIZE * 2 * 4, out_features=num_classes)


    def forward(self, input):

        output = self.net(input)
        output = output.view(-1, PICTURE_SIZE * 2 * 4)
        output = self.fc(output)
        return output

