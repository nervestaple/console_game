# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 11:31:02 2012

@author: jamcgee
"""

import numpy as np
from scipy import ndimage

class Cellular:
    def __init__(self, dim, kernel_type='normal'):
        self.dim = dim
        if kernel_type == 'normal':    
            self.kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
        elif kernel_type == 'orthogonal':            
            self.kernel = np.array([[0,1,0],[1,0,1],[0,1,0]])
            
        self.dtype = np.int8    
        self.state = np.random.binomial(1, 0.6, size=self.dim).astype(self.dtype)
        self.old_state = np.ndarray(self.dim, dtype=self.dtype)
        self.tmp = np.ndarray(self.dim, dtype=self.dtype)
        self.cell_bounds1 = np.ndarray(self.dim, dtype=np.bool)
        self.cell_bounds2 = np.ndarray(self.dim, dtype=np.bool)
    
    def cellular_next_step(self, min_n, max_n, birth_n):
        self.old_state = self.state.copy()
        neighbors = self.tmp
        ndimage.convolve(self.state, self.kernel, output=neighbors)
        np.greater_equal(neighbors, min_n, out=self.cell_bounds1)
        np.less_equal(neighbors, max_n, out=self.cell_bounds2)
        np.multiply(self.cell_bounds1, self.cell_bounds2, out=self.cell_bounds1)
        np.multiply(self.state, self.cell_bounds1, out=self.state)
        np.equal(neighbors, birth_n, out=self.cell_bounds1)
        np.add(self.state, self.cell_bounds1, out=self.state)
        np.clip(self.state + self.cell_bounds1, 0, 1, out=self.state)
        return np.sum(self.old_state - self.state)**2