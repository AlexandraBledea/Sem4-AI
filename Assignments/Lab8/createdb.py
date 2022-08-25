import torch
import numpy as np
from utils import Utilities

class DBCreator:

    def createAndSave(self):

        function_args_tensor = torch.rand(Utilities.DB_SIZE, 2) * (Utilities.DATA_HIGHER_BOUND - Utilities.DATA_LOWER_BOUND) - Utilities.DATA_HIGHER_BOUND

        results = []

        for pair in function_args_tensor.cpu().numpy():
            
            sin_arg = pair[0] + (pair[1] / torch.pi)
            results.append(np.sin(sin_arg))

        results_tensor = torch.tensor(results)

        data_tensor = torch.column_stack((function_args_tensor, results_tensor))
        
        torch.save(data_tensor, Utilities.DB_FILEPATH)
