import numpy as np
from params import *
from zq import Zq

def sample_matrix(test=False):
    if test:
        lu = np.array([11, 16, 16, 6])
        ru = np.array([3, 6, 4, 9])
        lb = np.array([1, 10, 3, 5])
        rb = np.array([15, 9, 1, 6])
        return np.array([lu, ru, lb, rb])
    
    A = np.random.randint(low=0, high=q, size=(k*k,n))
    return A

def sample_private(test=False):
    if test:
        sl = np.array([0, 1, -1, -1])
        sr = np.array([0, -1, 0, -1])
        return np.array([sl, sr])
    
    s = np.random.randint(low=-1, high=2, size=(k, n))
    return s

def sample_vec_error(test=False):
    if test:
        el = np.array([0, 0, 1, 0])
        er = np.array([0, -1, 1, 0])
        return np.array([el, er])
    
    e = np.random.randint(low=-1, high=2, size=(k, n))
    return e
###
def sample_r(test=False):
    if test:
        rl = np.array([0, 0, 1, -1])    
        rr = np.array([-1, 0, 1, 1])
        return np.array([rl, rr])
    
    r = np.random.randint(low=-1, high=2, size=(k, n))
    return r

def sample_e1(test=False):
    if test:
        e1l = np.array([0, 1, 1, 0])
        e1r = np.array([0, 0, 1, 0])
        return np.array([e1l, e1r])
    
    return np.random.randint(low=0, high=2, size=(k, n))
    
def sample_e2(test=False):
    if test:
        e2 = np.array([0, 0, -1, -1])
        return e2
    
    e2 = np.random.randint(low=-1, high=1, size=n)
    return e2


# In[10]:


def convert(data, to):
    Zq_list = []
    if to == 'vector':
        for i in range(k):
            Zq_list.append(Zq(n, q, data[i]))
        
        Zq_list = np.array([Zq_list]).T
        
    elif to == 'matrix':
        for i in range(k*k):
            Zq_list.append(Zq(n, q, data[i, :]))
        
        Zq_list = np.array([Zq_list])
        Zq_list = Zq_list.reshape((k, k))
            
    elif to == 'scalar':
        Zq_list = Zq(n, q, data)
        
    return Zq_list
####
def gen_matrix(test=False):
    A = sample_matrix(test)
    return convert(A, to='matrix')

def gen_private(test=False):
    s = sample_private(test)
    return convert(s, to='vector')

def gen_vec_error(test=False):
    e = sample_vec_error(test)
    return convert(e, to='vector')

def gen_r(test=False):
    r = sample_r(test)
    return convert(r, to='vector')

def gen_e1(test=False):
    e1 = sample_e1(test)
    return convert(e1, to='vector')

def gen_e2(test=False):
    e2 = sample_e2(test)
    return convert(e2, to='scalar')
    e2 = Zq(n, q, e2)
    return e2

def keygen(test=False):
    A = gen_matrix(test)
    private = gen_private(test)
    error = gen_vec_error(test)

    public = A @ private + error
    return private, public, A

