import numpy as np
# import numpy.matlib
from aislab.gnrl.sf import *

###################################################################################
def dspl(flg, **kwargs):
    if flg == 2:
        ivi = kwargs['args']['ivi']
        x = kwargs['x']
        F = kwargs['F']
        itr = kwargs['itr']
        cnames = c_(kwargs['args']['cnames'])

        s = kwargs['s']
        spc = '   '
        if itr == 0:
            print('---------- Newton-Raphson Method Log ------------')
            print('[Iter][  Step  ][Objective Function]', cnames[:, 0])
            print(itr, 'initial', s, F, x.T)
        else:
            meth = kwargs['meth']
            print(itr, meth, s, F, x.T)
    elif flg == 1:
            x = kwargs['x']
            xx = kwargs['xx']
            F = kwargs['F']
            FF = kwargs['FF']
            g = kwargs['g']
            H = kwargs['H']
            itr = kwargs['itr']
            msg = kwargs['msg']
            print(' ')
            if not len(FF) == 0:
                print('Last Change of F: ', (F - FF[0])[0])
            print('Last Gradient')
            print(g)
            if 'A' == msg:
                print('Convergence criterion (FCONV = ', kwargs['fcnv'], ') satisfied. /Initial model/')
            elif 'B' == msg:
                print('Stopping Rule (MaxIter = ', kwargs['maxiter'], ') satisfied. /', itr, '/')
            elif 'C' == msg:
                print('Convergence criterion (FCONV = ', kwargs['fcnv'], ') satisfied. /',
                      np.abs(F - FF[0])/(np.abs(FF[0]) + 1e-6), '/')
            elif 'D' == msg:
                print('Convergence criterion (ABSFCONV = ', kwargs['afcnv'], ') satisfied. /', np.abs(F - FF[0]), '/')
            elif 'E' == msg:
                print('Convergence criterion (XCONV = ', kwargs['xcnv'], ') satisfied. /', (x - xx[:, 0]).T/x, '/')
            elif 'F' == msg:
                print('Convergence criterion (GCONV = ', kwargs['gcnv'], ') satisfied. /',
                      -g.T@H@g/(np.abs(F) + 1e-6), '/')
            elif 'G' == msg:
                print('Termination: reaching the uncretainty level...')
            elif 'H' == msg:
                print('Termination: Hessian is a zero matrix...')
            else:
                print('Termination is caused by unknown reason...')
            print('----------------------------------------------------------')
            print('\n')
###################################################################################
def f_exp(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp1(args):
   # F for exponential model: ym = a + b*exp(c*x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp1_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = 0.01
    c = 1e6
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_expW(args):
   # F for exponential model: ym = a + b*exp(c*x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = apl_expW(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = 1e-2
    c = 1e6
    d1 = pm.flatten()
    d2 = (1 - (pm[0, 0] + pm[1, 0]))**2*c
    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def f_lgr(args):
    # F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    ym = lgr_apl(x, pm)
    ym[ym > 1 - 1e-10] = 1 - 1e-10
    ym[ym < 1e-10] = 1e-10
    m = pm.shape[1]
    yy = np.matlib.repmat(y, 1, m)
    ww = np.matlib.repmat(w, 1, m)
    F = -sum(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww)
    args['data'][:, -1] = ym.flatten()

    # pm = args['x']
    # b = 0.01
    # c = 1e6
    # A = np.diag((pm.flatten() < b))*c
    # F = F + pm.T@A@pm
    return F, args
###################################################################################
def f_log(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log1(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_logW(args):
    # F for exponential model: ym = a + b*ln(c*x + 1)
    pm = args['x']
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = apl_logW(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = 0.01
    c = 1e6
    d1 = pm.flatten()
    d2 = (pm[0, 0] - 1)**2*c

    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def g_exp(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.exp(x))[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x + pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e).T@tmp)[0]

    b = 0.01
    c = 1e6
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_expW(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x*pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e*x).T@tmp)[0]

    b = 0.01
    c = 1e6
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    g = g + 2*A@pm + np.array([[-2*(1 - (pm[0,0] + pm[1,0]))*c], [-2*(1 - (pm[0,0] + pm[1,0]))*c], [0]])
    return g
###################################################################################
def g_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    g = -x.T@((y - ym)*w)

    # pm = args['x']
    # b = 0.01
    # c = 1e6
    # A = np.diag((pm.flatten() < b))*c
    # g = g + 2*A@pm
    return g
###################################################################################
def g_log(args=None):
    # gradient of F for log model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(x) + 1))[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_logW(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(pm[2]*x) + 1))[0]
    g[2] = ((-2*pm[1]*(w*e/(abs(pm[2]*x) + 1)).T@x)*np.sign(pm[2]*x + 1))[0]  # !!!: np.sign(0) = 0

    b = 1e-2
    c = 1e6
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    d2 = (pm[0, 0] - 1)**2*c
    g = g + 2*A@pm + np.array([[2*(pm[0,0] - 1)*c], [0], [0]])
    return g
###################################################################################
def h_exp(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.exp(x)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A

    return H
###################################################################################
def h_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x + pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp).T@tmp)[0] - 2*((w*e).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp).T@tmp)[0] - 2*pm[1]*((w*e).T@tmp)[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    H = H + 2*A
    return H
    dd = pm.flatten()
    A = np.diag((dd < b))*c
###################################################################################
def h_expW(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x*pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*((w*x).T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp*x).T@tmp)[0] - 2*((w*e*x).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp*x**2).T@tmp)[0] - 2*pm[1]*((w*e*x**2).T@tmp)[0]

    pm = args['x']
    b = 1e-2
    c = 1e6
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 2*c, 0], [2*c, 2*c, 0], [0, 0, 0]])
    return H
###################################################################################
def h_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    n = x.shape[1]
    H = (x*np.matlib.repmat(ym*(1 - ym)*w, 1, n)).T@x

    # pm = args['x']
    # b = 0.01
    # c = 1e6
    # A = np.diag((pm.flatten() < b))*c
    # H = H + 2*A
    return H
###################################################################################
def h_log(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.log(abs(x) + 1)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A
    return H
###################################################################################
def h_logW(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.log(abs(pm[2]*x + 1))
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = (2*pm[1]*((w/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = (2*pm[1]*((w*tmp/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1) - 2*((w*e/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w/abs(pm[2]*x + 1)*x).T@x)[0] - 2*pm[1]*((w*e*x/abs(pm[2]*x + 1)).T@x)[0]

    pm = args['x']
    b = 0.01
    c = 1e6
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 0, 0], [0, 0, 0], [0, 0, 0]])
    return H
###################################################################################
def exp_apl(x, pm):
    ym = pm[0] + pm[1]*np.exp(x)
    return ym
###################################################################################
def exp1_apl(x, pm):
    ym = pm[0] + pm[1]*np.exp(x + pm[2])
    return ym
###################################################################################
def apl_expW(x, pm):
    ym = pm[0] + pm[1]*np.exp(x*pm[2])
    return ym
###################################################################################
def lgr_apl(x, pm):
    # logistic regression function
    if not isinstance(x, np.ndarray): x = np.array([[x]])
    if not isinstance(pm, np.ndarray): pm = np.array([[pm]])
    ym = 1/(1 + np.exp(-x@pm))
    return ym
###################################################################################
def log_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(x) + 1)
    return ym
###################################################################################
def log1_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)
    return ym
###################################################################################
def apl_logW(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))
    return ym
###################################################################################
def optOmit(x, xx, F, FF, g, g_1, H, H_1, Hinv, Hinv_1, iterate, s, tmp, sc, smeth, dsp_op):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    msg = 0
    flg = 0
    # tmp['F'] = np.inf
    sc = None
    if smeth == 'fprev2' or smeth == 'fprev3':
        if iterate == 1 and F > FF[0]:
            if F < tmp['F']:
                sc = s/2
                tmp['F'] = F
                tmp['x'] = x
                tmp['g'] = g
                tmp['H'] = H
                tmp['Hinv'] = Hinv
                x = c_(xx[:, 0])
                F = FF[0]
                g = g_1
                H = H_1
                Hinv = Hinv_1
            else:
                if np.any(dsp_op == 2): print('The uncertainty level has been reached and the precision could not be increased. Note: it is assumed that the objective function is unimodal. The optimization is terminated.')
                if FF[0] < tmp['F']:
                    F = FF[0]
                    x = c_(xx[:, 0])
                    g = g_1
                    H = H_1
                    Hinv = Hinv_1
                else:
                    x = tmp['x']
                    F = tmp['F']
                    g = tmp['g']
                    H = tmp['H']
                    Hinv = tmp['Hinv']
                iterate = 0
                msg = 'G'
            flg = 1
    return x, F, g, H, Hinv, tmp, sc, iterate, msg, flg
###################################################################################
def stepPar(s, F, FF, g, g_1, iter, flg, sc, smeth, su, p_decr, p_incr):
    # Stepsize Determination
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    if not sc is None:
        s = sc
    elif smeth == 'fprev2' or smeth == 'fprev3':
        #    smax = par['s_max']
        nn = len(FF)
        FF[np.arange(nn, 3)] = np.nan
        c = nans((3,))
        c[0] = FF[1] < FF[2]
        c[1] = FF[0] < FF[1]
        c[2] = F < FF[0]
        if (iter == 1 or iter == 2) and c[2] == 0:
            s1 = p_decr*s
        elif iter > 1 and smeth == 'fprev2':
            if np.all(c[2] == 1):
                s1 = p_incr*s
            else:
                s1 = p_decr*s
        elif iter > 2 and smeth == 'fprev3':
            if np.all(c == np.array([1, 1, 1])):
                s1 = p_incr*s
            elif np.all(c == np.array([1, 1, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([1, 0, 1])):
                s1 = s
            elif np.all(c == np.array([1, 0, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([0, 1, 1])):
                s1 = s
            elif np.all(c == np.array([0, 1, 0])):
                s1 = p_decr*s
            elif np.all(c == np.array([0, 0, 1])):
                s1 = s
            elif np.all(c == np.array([0, 0, 0])):
                s1 = p_decr*s
        else:
            s1 = s
        s = min([s1, su*np.abs(p_incr - 1)/5 + s])
        if s > su:   s = su
        if flg == 1: s = s/2
    elif smeth == 'gang':
        if iter < 1:
            s = 1
        else:
            norm2g = np.sqrt(g.T@g)
            norm2g_1 = np.sqrt(g_1.T@g_1)
            s = 1e-10 + (np.pi - np.arccos(min(1, g_1.T@g/max(norm2g_1*norm2g, 1e-06))))/np.pi*(su - 1e-10)
    elif smeth == 'none':
        s = 1
    return s
###################################################################################
def stopcrt(x=None, F=None, xx=None, FF=None, g=None, H=None, itr=None, maxiter=None, fcnv=None, afcnv=None, xcnv=None,
            gcnv=None, sc=None):
    # Stopping Criteria
    # Contains a set of convergence criteria for NR, NRLS, NRPI, SD, etc.
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    if FF is None:
        F_1 = None
    elif isinstance(FF, (int, float)):
        F_1 = FF
    else:
        F_1 = FF[0, 0]
    if isinstance(xx, list) and len(xx) == 0:
        x_1 = None
    elif isinstance(xx, (int, float)):
        x_1 = xx
    else:
        x_1 = xx[:, 0]
    iterate = 1
    msg = '0'
    if maxiter is not None and itr >= maxiter:
        iterate = 0
        msg = 'B'
        return iterate, msg
    if fcnv is not None and not F_1 and np.abs(F - F_1)/min(np.array([1e12, np.abs(F_1) + 1e-6])) < fcnv:
        iterate = 0
        msg = 'C'
        return iterate, msg
    if afcnv is not None and not F_1 is None and np.abs(F - F_1) < afcnv:
        iterate = 0
        msg = 'D'
        return iterate, msg
    if xcnv is not None and not x_1 is None:
        x_1 = c_(x_1)
        d = nans(x.shape)
        ind1 = np.argwhere(np.abs(x_1) < 0.01)
        ind2 = np.argwhere(np.abs(x_1) >= 0.01)
        d[ind1, 0] = x[ind1, 0] - x_1[ind1, 0]
        d[ind2, 0] = (x[ind2, 0] - x_1[ind2, 0])/x_1[ind2, 0]
        if np.all(np.abs(d) <= xcnv):
            iterate = 0
            msg = 'E'
            return iterate, msg
    if gcnv is not None and np.abs(g.T@H@g)/(np.abs(F) + 1e-6) < gcnv:
        iterate = 0
        msg = 'F'
        return iterate, msg
    return iterate, msg
###################################################################################
# import copy
# import numpy as np
# import pandas as pd
# def model_apply(mdl_type, X, pm):
#     if mdl_type == 'logistic':
#         return 1/(1 + np.exp(-np.dot(X, pm)))
#
#     if mdl_type == 'exp':
#         return (pm[0] + pm[1]*np.exp(X)).reshape((len(X), 1))
#
#     if mdl_type == 'log':
#         return (pm[0] + pm[1]*np.log(abs(X) + 1)).reshape((len(X), 1))
#
#     if mdl_type == 'logB':
#         pass
#         # return pm[0] + np.log(abs(x) + 1)/np.log(pm[2])
# def grad(mdl_type, ym, x, y, w):
#     if mdl_type == 'logistic':
#         return np.dot(-x.T, ((y - ym)*w))
#
#     else:
#         e = y - ym.reshape((len(y), 1))
#         g = np.zeros(shape=(2, 1))
#         g[0] = (-2*np.dot(w.T, e))[0, 0]
#
#     if mdl_type == 'exp':
#         g[1] = (-2*np.dot((w*e).T, np.exp(x)))[0]
#
#     if mdl_type == 'log':
#         g[1] = (-2*np.dot((w*e).T, np.log(abs(x) + 1)))[0]
#
#     if mdl_type == 'logB':
#         pass
#         # lnb = np.log(pm(2))
#         # g[1] = 2/(pm(2)*lnb)*np.dot((w*e).T, np.log(abs(x) + 1)/lnb)
#
#     return g
#
#
# def hes(mdl_type, ym, x, y, w):
#     if mdl_type == 'logistic':
#         return np.dot((x*np.tile(ym*(1 - ym)*w, (1, x.shape[1]))).T, x)
#
#     else:
#         H = np.zeros(shape=(2, 2))
#
#     if mdl_type == 'exp' or mdl_type == 'log':
#
#         if mdl_type == 'exp':
#             tmp = np.exp(x)
#
#         if mdl_type == 'log':
#             tmp = np.log(abs(x) + 1)
#
#         H[0, 0] = 2*w.sum()
#         H[0, 1] = (2*np.dot(w.T, tmp))[0]
#         H[1, 0] = H[0, 1]
#         H[1, 1] = (2*np.dot(w.T*tmp, tmp))[0]
#
#     if mdl_type == 'logB':
#         pass
#         # lnb = log(pm(2));
#         # logbc = log(abs(x) + 1)/log(pm(2));  % = logb(c) = logb(abs(x) + 1)
#         # H11 = 2*sum(w);
#         # H12 = -2/(pm(2)*lnb)*w'*logbc;
#         # H21 = H12;
#         # H22 = 2/(pm(2)*lnb)^2*((lnb + 3)*logbc' - (lnb + 2)*(y - pm(1))')*(w.*logbc);
#
#     return H
#
#
# def func(mdl_type, pm, x, y, w):
#     # Model Output
#     ym = model_apply(mdl_type, x, pm)
#
#     # Capping
#     ym[ym > 1 - 1e-10] = 1 - 1e-10
#     ym[ym < 1e-10] = 1e-10
#
#     if mdl_type == 'logistic':
#         yy = np.tile(y, (1, pm.shape[1]))
#         ww = np.tile(w, (1, pm.shape[1]))
#         F = -(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww).sum().T
#
#     else:
#
#         ym = model_apply(mdl_type, x, pm)
#         e = y - ym
#         F = np.dot(e.T, (e*w))[0, 0]
#
#     return [F, ym]
