import numpy as np
import sympy
from neuroimaging.modalities.fmri import formula, utils, hrf

# hrf 

h = sympy.Function('hrf')
t = formula.Term('t')

# Session 1

t1 = formula.Term('t1')
c11 = utils.events([3,7,10], f=h); c11 = c11.subs(t, t1)
c21 = utils.events([1,3,9], f=h); c21 = c21.subs(t, t1)
c31 = utils.events([2,4,8], f=h); c31 = c31.subs(t, t1)
d1 = utils.fourier_basis([0.3,0.5,0.7]); d1 = d1.subs(t, t1)
tval1 = np.linspace(0,20,101)

f1 = formula.Formula([c11,c21,c31]) + d1
f1.aliases['hrf'] = hrf.glover

# Session 2

t2 = formula.Term('t2')
c12 = utils.events([3.3,7,10], f=h); c12 = c12.subs(t, t2)
c22 = utils.events([1,3.2,9], f=h); c22 = c22.subs(t, t2)
c32 = utils.events([2,4.2,8], f=h); c32 = c32.subs(t, t2)
d2 = utils.fourier_basis([0.3,0.5,0.7]); d2 = d2.subs(t, t2)
tval2 = np.linspace(0,10,51)

f2 = formula.Formula([c12,c22,c32]) + d2
f2.aliases['hrf'] = hrf.glover

session = np.array([1]*tval1.shape[0] + [2]*tval2.shape[0])
sess_factor = formula.Factor('sess', [1,2])

ttval1 = np.hstack([tval1, np.zeros(tval2.shape)])
ttval2 = np.hstack([np.zeros(tval1.shape), tval2])

f = formula.Formula([sess_factor.terms[0]]) * f1 + formula.Formula([sess_factor.terms[1]]) * f2
f.aliases['hrf'] = hrf.glover
d = formula.Design(f)

rec = np.array([(t1,t2, s) for t1, t2, s in zip(ttval1, ttval2, session)], 
               np.dtype([('t1', np.float),
                         ('t2', np.float),
                         ('sess', np.int)]))
contrast = formula.Formula([sess_factor.terms[0]*c11-sess_factor.terms[1]*c12])
contrast.aliases['hrf'] = hrf.glover

X = d(rec, return_float=True)

d2 = formula.Design(contrast, return_float=True)
preC = d2(rec)

C = np.dot(np.linalg.pinv(X), preC)
print C
