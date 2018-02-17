#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:55:50 2018

@author: olivier
"""

import numpy as np
import pandas as pd
from scipy import optimize as spo


class PortfolioOptimization():
    
    def __init__(self, C, undl_names):
        self.covariance_matrix = C
        self.underlyings = undl_names
        self.num_undl = len(C)
        
        self.start_x = [1.0 / self.num_undl] * self.num_undl
        self.boundaries =[(0, 1)] * self.num_undl

        self.optim_constraints = {'type': 'eq', 
                                  'fun': lambda x: x.sum() - 1}

        self.optimization_results = {'minvar': None,
                                     'maxdiv': None,
                                     'rp': None}

        self.allwgt = pd.DataFrame()

    @staticmethod
    def _minvar_objfunc(w, cov):
        return np.dot(w, np.dot(cov, w))

    @staticmethod
    def _maxdiv_objfunc(w, cov):
        return np.dot(w, np.dot(cov, w)) / np.dot(np.diag(cov), w)

    @staticmethod
    def _risk_allocation(w, cov):
        return np.dot(cov, w) * w

    @staticmethod
    def _rp_objfunc(w, cov):
        return PortfolioOptimization._risk_allocation(w, cov).std()

    def run_singleOptimization(self, method):
        res_optim = spo.minimize(method, 
                                 self.start_x, 
                                 args=(self.covariance_matrix, ),
                                 constraints=self.optim_constraints,
                                 method='SLSQP',
                                 bounds=self.boundaries,
                                 options={'maxiter': 500},
                                 tol=1e-12)
        return res_optim

    def run_allOptimization(self):
        self.optimization_results = {'minvar': self.run_singleOptimization(self._minvar_objfunc),
                                     'maxdiv': self.run_singleOptimization(self._maxdiv_objfunc),
                                     'rp': self.run_singleOptimization(self._rp_objfunc)}
        
        [print(x + ' - ' + self.optimization_results[x]['message']) for x in self.optimization_results]
        
        self.allwgt = pd.DataFrame({x: self.optimization_results[x]['x'] for x in self.optimization_results},
                                    index=self.underlyings)


