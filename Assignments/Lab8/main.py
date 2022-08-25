from createdb import DBCreator
from trainmodel import ModelTrainer
from model import Net
from utils import Utilities
import numpy as np
import torch

def runAndCompareExamples(NN):
    testArgs = [

        [0.0, 0.0],
        [np.pi/2, 0.0],
        [0.1175, 6.1622],
        [3.1415, 9.8690],
        [5.0, 6.0],
        [8.0, 9.0],
        [-2.34, -4.57]
    ]

    for pair in testArgs:
        print("Input: {} - NN result: {} - Expected result: {}\n".format(str(pair), str(NN(torch.tensor(pair)).item()), str(np.sin(pair[0] + (pair[1] / np.pi))) ))

def main():

    DBCreator().createAndSave()

    trainer = ModelTrainer()
    trainer.trainNN()
    trainer.saveNN()

    neuralNetwork = Net(Utilities.INPUT_LAYER_SIZE, Utilities.HIDDEN_LAYER_SIZE, Utilities.HIDDEN_LAYER_SIZE, Utilities.OUTPUT_LAYER_SIZE)
    neuralNetwork.load_state_dict(torch.load(Utilities.ANN_FILEPATH))
    neuralNetwork.eval()

    runAndCompareExamples(neuralNetwork)


if __name__ == "__main__":
    main()