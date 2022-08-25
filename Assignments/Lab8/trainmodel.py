import torch
import torch.nn.functional as F
import matplotlib.pyplot as plot
import numpy as np

from model import Net
from utils import Utilities

class ModelTrainer:
    
    def __init__(self):

        self._lossFunction = torch.nn.MSELoss()
        self._neuralNetwork = Net(Utilities.INPUT_LAYER_SIZE, Utilities.HIDDEN_LAYER_SIZE, Utilities.HIDDEN_LAYER_SIZE, Utilities.OUTPUT_LAYER_SIZE)

        self._optimizerBatch = torch.optim.SGD(self._neuralNetwork.parameters(), lr=Utilities.LEARNING_RATE)

        data_tensor = torch.load(Utilities.DB_FILEPATH)

        self._inputTensor = data_tensor.narrow(1, 0, 2) 
        self._outputTensor = data_tensor.narrow(1, 2, 1) 


    def trainNN(self):

        averageLosses = []
        batchCount = Utilities.DB_SIZE // Utilities.BATCH_SIZE
        splitInputData = torch.split(self._inputTensor, Utilities.BATCH_SIZE)
        splitOutputData = torch.split(self._outputTensor, Utilities.BATCH_SIZE)

        for epoch in range(Utilities.EPOCH_COUNT):
            
            # We'll compute the average loss for the current epoch, 
            # and after all the epochs, we'll plot these averages.
            lossSum = 0

            for batch in range(batchCount):
                
                # Output for batch
                prediction = self._neuralNetwork(splitInputData[batch].float())

                # Loss for batch (based on the difference between the given output and the expected one)
                loss = self._lossFunction(prediction, splitOutputData[batch].float())

                # Add loss for current batch to the total
                lossSum += loss.item()

                # We set up the gradients for the weights to zero (important in pytorch)
                self._optimizerBatch.zero_grad()

                # We compute automatically the variation for each weight (and bias) of the network
                loss.backward()

                # We compute the new values for the weights 
                self._optimizerBatch.step()

            # We save the average loss for the current epoch
            averageLosses.append(lossSum / batchCount)

            if epoch % 20 == 0:

                prediction = self._neuralNetwork(self._inputTensor.float())
                loss = self._lossFunction(prediction, self._outputTensor)

                print('\repoch index: {} - avg. loss = {:.4f}'.format(epoch, loss))


        plot.plot(averageLosses)
        plot.savefig("averageLosses.png")


    def saveNN(self):
        
        torch.save(self._neuralNetwork.state_dict(), Utilities.ANN_FILEPATH)

