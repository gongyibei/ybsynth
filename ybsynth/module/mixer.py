import numpy as np

from .module import Module


class Mixer(Module):

    def __init__(self):
        Module.__init__(self)

    def forward(self, buf_list, max_num=6):
        return sum(buf_list) / min(len(buf_list), max_num)


class RationMixer(Module):

    def __init__(self):
        Module.__init__(self)

    def forward(self, buf_list, ration):
        s = sum(ration)
        X = np.zeros(self.buf_size, dtype=self.dtype)
        for buf, r in zip(buf_list, ration):
            if r > 0:
                X += buf * r / s
        return X
