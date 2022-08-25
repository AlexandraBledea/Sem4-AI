import torch
import torch.nn as nn
import torch.optim as optim
import time
from torch.utils.data import Dataset, DataLoader

# from torchvision import datasets, models, transforms

device = torch.device('cpu')


class ImageClassifierDataset(Dataset):

    def __init__(self, image_list, image_classes, transform):
        # we keep the images
        self.images = []
        # 0 or 1 (1 for human, 0 for others)
        self.labels = []

        # we extract the classes, so we make a list with 0 and 1 as values
        self.classes = list(set(image_classes))
        self.class_to_label = {c: i for i, c in enumerate(self.classes)}

        self.transforms = transform

        for image, image_class in zip(image_list, image_classes):
            transformed_image = self.transforms(image)
            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)

    def __getitem__(self, index):
        return self.images[index], self.labels[index]

    def __len__(self):
        return len(self.images)
