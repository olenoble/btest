#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 15:37:52 2018

@author: olivier
"""

import numpy as np
import pandas as pd
from scipy import optimize as spo
import portfolioOptimization as po


data = pd.read_csv('data_etf.csv', date_parser='%Y-%m-%d').set_index('Date').sort_index()
data_ret = data / data.shift() - 1
C = (data_ret.cov() * 252).as_matrix()

### Optimization - 0
po0 = po.PortfolioOptimization(C, data_ret.columns)
po0.run_allOptimization()

po0._risk_allocation(po0.allwgt, po0.covariance_matrix).plot(kind='bar')
pd.Series(np.diag(np.dot(po0.allwgt.T, np.dot(C, po0.allwgt))), index=po0.allwgt.columns).plot(kind='bar')
pd.Series([po0._maxdiv_objfunc(po0.allwgt.values[:,i], C) for i in range(3)], index=po0.allwgt.columns).plot(kind='bar')
