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


