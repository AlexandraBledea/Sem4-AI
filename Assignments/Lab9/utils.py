from matplotlib import image
from torchvision.transforms import transforms
import torch

PICTURE_SIZE = 64
BATCH_SIZE = PICTURE_SIZE // 2
CUDA_AVAILABLE = False


# Define transformations for the training set, flip the images randomly, crop out and apply mean and std normalization
TRAIN_TRANSFORMATIONS = transforms.Compose([

    transforms.Resize(PICTURE_SIZE),
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(PICTURE_SIZE, padding=PICTURE_SIZE // 8),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Define transformations for the test set
TEST_TRANSFORMATIONS = transforms.Compose([

    transforms.Resize(PICTURE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])