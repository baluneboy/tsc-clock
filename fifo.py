#!/usr/bin/env python

import datetime
import numpy as np
from collections import deque


class CheckableFifo(deque):
    
    def is_stale(self):
        """return True if any deltas zero"""
        deltas = self.get_deltas()
        return np.any(deltas == 0)
    
    def get_deltas(self):
        return np.diff(list(self))


def demo(buff_len):
    d = CheckableFifo([0] * buff_len, buff_len)
    for i in range(9):
        d.append(i)
        print d, d.get_deltas(), d.is_stale()


class TimeCheckableFifo(CheckableFifo):
    
    def get_deltas(self):
        secs = [int((t-datetime.datetime(1970, 1, 1)).total_seconds()) for t in list(self)]
        return np.diff(secs)

if __name__ == "__main__":
    demo(3)
