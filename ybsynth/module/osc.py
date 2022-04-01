import numpy as np
import scipy

from .module import Module


class MetaOSC(Module):

    def __init__(self, freq):
        Module.__init__(self)
        self.freq = freq
        self.idx = 0
        self.period = self.sample_rate // self.freq

    def forward(self):
        X = self._make_wav()
        return X

    def _make_wav(self):
        self.idx = (self.idx + self.buf_size) % self.period
        X = np.arange(self.idx, self.idx + self.buf_size)
        X = self._table(X)
        return X

    def _table(self, X):
        raise NotImplementedError("Derived classes must override this method")


class SineOSC(MetaOSC):

    def __init__(self, freq):
        MetaOSC.__init__(self, freq)

    def _table(self, X):
        return np.cos(2 * np.pi * (1 / self.period) * X)


class SquareOSC(MetaOSC):

    def __init__(self, freq, duty=0.5):
        MetaOSC.__init__(self, freq)
        self.duty = duty

    def _table(self, X):
        return scipy.signal.square(2 * np.pi * (1 / self.period) * X,
                                   duty=self.duty)


class SawtoothOSC(MetaOSC):

    def __init__(self, freq, width=0.5):
        MetaOSC.__init__(self, freq)
        self.width = width

    def _table(self, X):
        return scipy.signal.sawtooth(2 * np.pi * (1 / self.period) * X,
                                     width=self.width)
