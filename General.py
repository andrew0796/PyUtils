import functools
import operator

def flattenList(l,*m):
    ''' 
    flatten a list l, along with optionally expanding other list of the same length as l in the same fashion, for instance if we want to flatten l and m is another list where each entry corresponds to an entry in l, then we would expand m by duplicating the nth entry for each entry we extract from the nth entry of l

    assumes each entry in l is either a list (must be flattend) or not a list, and all entries are of the same class (ie list or not list) 
    '''
    
    if len(m) == 0:
        if len(l) == 0:
            return l
        while type(l[0]) is list:
            l = functools.reduce(operator.add, l)
        return l

    if len(l) == 0:
        return l,[None for i in m]
    mMap = {i:1 for i in range(len(l))}
    while type(l[0]) is list:
        _l = []
        for i in range(len(l)):
            temp = functools.reduce(operator.add, l[i])
            if type(temp) is list:
                mMap[i] = len(temp)
                _l += temp
            else:
                _l.append(temp)
        l = _l
    _m = []
    for i in m:
        temp = []
        for j in range(len(i)):
            temp += mMap[j]*[i[j]]
        _m.append(temp)
    return l, _m
