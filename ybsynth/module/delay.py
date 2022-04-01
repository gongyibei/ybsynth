import numpy as np

from .module import Module


class Delay(Module):

    def __init__(self, delay_time=0.5, decay=0.5):
        Module.__init__(self)
        self.delay_time = delay_time
        self.delay_len = int(delay_time * self.sample_rate)
        self.delay_buf = np.zeros(self.delay_len)
        self.decay = decay

    def forward(self, X):
        delay_buf = np.append(self.delay_buf, X)
        X += delay_buf[:self.buf_size] * self.decay
        self.delay_buf = delay_buf[-self.delay_len:]
        return X
