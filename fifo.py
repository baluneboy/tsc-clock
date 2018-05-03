#!/usr/bin/env python

import datetime
#import numpy as np
from operator import mul
from collections import deque


class CheckableFifo(deque):
    
    # def is_stale(self):
    #     """return True if any deltas zero"""
    #     deltas = self.get_deltas()
    #     any_zero_deltas = np.any(deltas == 0)
    #     product = reduce(mul, deltas, 1)
    #     print deltas
    #     print 'any_zero_deltas:', any_zero_deltas
    #     print 'product:', product
    #     return any_zero_deltas
    
    def get_deltas(self):
        t = list(self)
        #old_deltas = np.diff(t)
        deltas = [j-i for i,j in zip(t[:-1], t[1:])]
        # print 'old_deltas:', old_deltas
        # print 'deltas:', deltas
        return deltas


def demo(buff_len):
    d = CheckableFifo([0] * buff_len, buff_len)
    for i in range(9):
        d.append(i)
        print d, d.get_deltas(), d.is_stale()


class TimeCheckableFifo(CheckableFifo):
    
    def get_deltas(self):
        secs = [int((t-datetime.datetime(1970, 1, 1)).total_seconds()) for t in list(self)]
        # old_deltas = np.diff(secs)
        deltas = [j-i for i,j in zip(secs[:-1], secs[1:])]
        # print 'old_deltas:', old_deltas
        # print 'deltas:', deltas
        return deltas
    
    
if __name__ == "__main__":
    demo(3)
