# aux_functions.py
import numpy as np

class Data:
    def __init__(self, x_coord, y_coord, label, category=None):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.label = label
        self.category = category
        if len(x_coord) != len(y_coord):
            raise Warning("x_coord and y_coord have different dimensions")

def load_data(file_path, label):
    data = np.loadtxt(file_path, delimiter=',', dtype=float)
    x_coord, y_coord = data[:, 0], data[:, 1]
    return Data(x_coord, y_coord, label)


