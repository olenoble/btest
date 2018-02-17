import numpy as np
import pandas as pd
from scipy import optimize as spo


data = pd.read_csv('data_etf.csv', date_parser='%Y-%m-%d').set_index('Date').sort_index()

data_ret = data / data.shift() - 1
C = (data_ret.cov() * 252).as_matrix()


##############################################################
## Objective Functions
def minvar_objfunc(w, cov):
    return np.dot(w, np.dot(cov, w))

def maxdiv_objfunc(w, cov):
    return np.dot(w, np.dot(cov, w)) / np.dot(np.diag(C), w)

def risk_allocation(w, cov):
    return np.dot(cov, w) * w

def rp_objfunc(w, cov):
    return risk_allocation(w, cov).std()

N = len(C)
start_x = [1.0 / N] * N
boundaries =[(0, 1)] * N

optim_constraints = {'type': 'eq', 
                     'fun': lambda x: x.sum() - 1}

## Minimum Variance
res_mv = spo.minimize(minvar_objfunc, 
                      start_x, 
                      #args=(caps, 10.0, 0.05),
                      args=(C, ),
                      constraints=optim_constraints,
                      method='SLSQP',
                      bounds=boundaries,
                      options={'maxiter': 500},
                      tol=1e-12)

#if False:
#    onevec = np.array([1] * N).reshape(N,1)
#    fact = np.dot(onevec.T, np.dot(np.linalg.inv(C), onevec))[0][0]
#    res_test = (np.dot(np.linalg.inv(C), np.array([1] * N).reshape(N,1)) / fact).T[0]
#    
#    cmp_method_mv = pd.DataFrame({'sp': res_mv['x'], 'test': res_test})

## Max Diversification
res_md = spo.minimize(maxdiv_objfunc, 
                      start_x, 
                      #args=(caps, 10.0, 0.05),
                      args=(C, ),
                      constraints=optim_constraints,
                      method='SLSQP',
                      bounds=boundaries,
                      options={'maxiter': 500},
                      tol=1e-12)

## Risk Parity
res_rpd = spo.minimize(rp_objfunc, 
                      start_x, 
                      #args=(caps, 10.0, 0.05),
                      args=(C, ),
                      constraints=optim_constraints,
                      method='SLSQP',
                      bounds=boundaries,
                      options={'maxiter': 500},
                      tol=1e-12)



#### Comparison 
compare_wgt = pd.DataFrame({'minvar': res_mv['x'],
                            'maxdiv': res_md['x'],
                            'rp': res_rpd['x']},
                            index=data.columns)

risk_allocation(compare_wgt, C).plot(kind='bar')
pd.Series(np.diag(np.dot(compare_wgt.T, np.dot(C, compare_wgt))), index=compare_wgt.columns).plot(kind='bar')
pd.Series([maxdiv_objfunc(compare_wgt.values[:,i], C) for i in range(3)], index=compare_wgt.columns).plot(kind='bar')
