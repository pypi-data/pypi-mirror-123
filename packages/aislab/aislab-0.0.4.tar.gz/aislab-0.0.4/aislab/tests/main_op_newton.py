import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from numpy import ndarray

from aislab.op_nlopt.ord12 import *
from aislab.gnrl.sf import *
from aislab.gnrl.measr import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

mdl_types = ['exp2', 'log1', 'exp', 'log', 'lgr', 'lin']
mdl_types = ['exp', 'log', 'lgr', 'lin']
mdl_types = ['log2']
mdl_types = ['exp2', 'log2', 'lin']
# mdl_types = ['exp2']
for mdl_type in mdl_types:

    item = 'AA0878'
    data = pd.DataFrame({'x' : [-0.0, 24.675324675324674, 35.064935064935064], 'y' : [1.04, 1.2608695652173914, 1.45], 'w' : [0.31, 0.35, 0.35]}); item = 'AA0878'
    item = 'AA2257'
    data = pd.DataFrame({'x' : [-0.0, 27.272727272727273, 45.45454545454545, 50.0, 54.54545454545455], 'y' : [2.0, 1.1666666666666667, 1.0, 1.0, 1.1538461538461535], 'w' : [0.15, 0.18, 0.1, 0.2, 0.38]}); item = 'AA2257'
    item =    'AA2297'
    data = pd.DataFrame({'x' : [-0.0, 5.2631578947368425], 'y' : [1.0833333333333333, 1.1666666666666667], 'w' : [0.48, 0.52]}); item = 'AA2297'
    item =    'AA2291'
    data = pd.DataFrame({'x': [-0.0, 46.153846153846146, 61.53846153846154, 69.23076923076923], 'y': [2.0, 1.1162790697674418, 1.175, 1.1395348837209305], 'w': [0.06, 0.31, 0.31, 0.32]});
    # item = 'XXX'
    # data = pd.DataFrame({'x': [30. , 27.5, 25. , 22.5, 20. , 17.5, 10. , -0. ], 'y': [6.70912296, 1.40873016, 6.35330056, 5.65689653, 6.23105281, 6.88002254, 2.08811946, 1.], 'w': [100000., 0., 0.26, 0., 0.09, 0., 0., 0.56]})
    # item = 'XXX'
    # data = pd.DataFrame({'x': [0, 0.05, 0.10, 0.15, 0.20, 0.25 ], 'y': [1, 1.5, 2, 5, 10, 20], 'w': [100, 1, 2, 3, 4, 5]})
    # x = np.array([0, 5, 10, 15, 20, 25]); y = apl_expW(x, [0.9, 0.1, 0.2])
    # data = pd.DataFrame({'x': x, 'y': y, 'w': [100, 1, 2, 3, 4, 5]})

    xx = np.arange(0, np.max(data['x']) + 5, 5)

    # OVERWRITE
    # data['w'] = 1
    x = c_(data.loc[:, 'x'].values); #    x = x[::-1]
    y = c_(data.loc[:, 'y'].values)
    w = c_(data.loc[:, 'w'].values)
    if len(x.shape) == 1: x = c_(x)
    N = len(w)
    if mdl_type == 'lgr': y, st = rnml(y)
    ####################################################
    cnames = 'x'
    metpminit = 'zero' # 'fapp' #
    gcnv = 1e-3
    ####################################################
    # Initial model parameters
    if mdl_type == 'lgr':
        Nw = sum(w)
        my = y.T@w/Nw
        lambda_ = np.log(my/(1 - my))
        if metpminit == 'zero':
            pm0 = np.vstack((c_([lambda_]), [0]))
        elif metpminit == 'fapp':
            model0 = lspm(x, (y - 0.5)*2*lambda_)
            pm0 = model0['Pm']
    elif mdl_type == 'exp':
        pm0 = np.array([y.mean() - 1, 1/np.mean(np.exp(x))]).reshape(2,1)
    elif mdl_type == 'exp2':
        c = 0.1;
        xmax, ind = max1(x.flatten())
        ymax = y[ind, 0]
        b = np.max([np.min([ymax - 1, 100]), 0])/(np.exp(c*xmax) - 1)
        a = 1 - b
        pm0 = c_(np.array([a, b, c]))
    elif mdl_type == 'log':
        pm0 = np.array([y.mean() - 1, 1/np.mean(np.log(abs(x)+1))]).reshape(2,1)
    elif mdl_type == 'log2':
        c = 0.1;
        xmax = np.max(x)
        ymax = np.max(y)
        b = np.max([np.min([ymax - 1, 100]), 0])/(np.log(abs(c*xmax + 1)))
        a = b - 1
        pm0 = c_(np.array([a, b, 5*c]))

    # Arguments for func, grad, hes calculation

    args = {}
    args['data'] = np.hstack((x, y, w, np.zeros((N, 1))))
    args['cnames'] = c_(['a', 'b'])
    args['x'] = pm0
    args['ivi'] = 0
    args['pm0'] = pm0
    args['metpminit'] = metpminit
    #    func = par['func
    #    grad = par['grad
    #    hes = par['hes
    if mdl_type == 'lgr' or mdl_type == 'lin':
        pass
        N = len(w)
        x = np.hstack((ones((N, 1)), x))
        # N = 100
        # x = np.hstack((ones((N, 1)), randn((N, 1))))
        # pm = c_([2, 3])
        # y = lgr_apl(x, pm)
        # pm0 = c_([0, 0])
        # w = ones((100, 1))
        args['data'] = np.hstack((x, y, w, np.zeros((N, 1))))
        # args['pm0'] = pm0
        # args['x'] = pm0

    if mdl_type != 'lin':
        if mdl_type == 'exp2':   pm, F, g, H, Hinv, __ = newton(pm0, f_expW, g_expW, h_expW, args, gcnv, maxiter=1000, rcondH=0, dsp_op=2)
        elif mdl_type == 'lgr1': pm, F, g, H, Hinv, __ = newton(pm0, f_lgr1, g_lgr1, h_lgr1, args, gcnv, rcondH=0, dsp_op=[0])
        elif mdl_type == 'exp':  pm, F, g, H, Hinv, __ = newton(pm0, f_exp, g_exp, h_exp, args, gcnv, rcondH=0, dsp_op=[0])
        elif mdl_type == 'lgr': pm, F, g, H, Hinv, __ = newton(pm0, f_lgr, g_lgr, h_lgr, args, gcnv, rcondH=0, dsp_op=[0])
        elif mdl_type == 'log': pm, F, g, H, Hinv, __ = newton(pm0, f_log, g_log, h_log, args, gcnv, rcondH=0, dsp_op=[0])
        elif mdl_type == 'log2': pm, F, g, H, Hinv, __ = newton(pm0, f_logW, g_logW, h_logW, args, gcnv, maxiter=1000, rcondH=0, dsp_op=0)

        model = {'pm': pm,
                 'st': {'ovr': {'F': F,
                                'g': g,
                                'H': H,
                                'Hinv': Hinv}
                        }
                 }
    else:
        mdl = lspm(x, y)

    pm[pm < 0] = 0
    try:    mdl['Pm'][mdl['Pm'] < 0] = 0
    except: pass


    if mdl_type == 'exp':
        ym = exp_apl(x, pm)
        print('VAF_exp = ', vaf(y, ym), ',   pm =', pm.flatten())
    if mdl_type == 'exp2':
        ym = apl_expW(x, pm)
        print('VAF_exp2 = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'lgr':
        ym = lgr_apl(x, pm)
        print('VAF_lgr = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'log':
        ym = log_apl(x, pm)
        print('VAF_log = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'log2':
        ym = apl_logW(x, pm)
        print('VAF_log = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'lin':
        ym = lspm_apl(x, y, mdl)
        print('VAF_lin = ', vaf(y, ym), ',   pm =', pm.flatten())
    if np.shape(x)[1] > 1: x = c_(x[:,1])
    #xx: ndarray = np.array(range(0, max([25, int(np.ceil(x.max()))+1]) ))
    if mdl_type == 'exp':   ym = exp_apl(xx, pm)
    elif mdl_type == 'exp2': N = len(xx); ym = apl_expW(xx, pm);
    elif mdl_type == 'lgr': N = len(xx); xx = np.hstack((ones((N, 1)), c_(xx))); ym = lgr_apl(xx, pm); xx = xx[:,1]
    elif mdl_type == 'log': ym = log_apl(xx, pm)
    elif mdl_type == 'lin': N = len(xx); xx = np.hstack((ones((N, 1)), c_(xx))); ym = lspm_apl(xx, y, mdl); xx = xx[:,1]
    elif mdl_type == 'log2': N = len(xx); ym = apl_logW(xx, pm);

    if mdl_type == 'lgr': y, st = rnml(y, st['xmin'], st['xmax'])

    plt.scatter(x, y)
    # plt.plot(x, apl_expW(x, pm0), 'k')
    plt.plot(xx, ym, 'r')
    plt.title(item)
    plt.show()
    1;
    #
    # import matplotlib.pyplot as plt
    # plt.plot(y)
    # plt.plot(ym)
    # plt.show
    #
    # # print('Optimal params:')
    # # print(pm)
ym = apl_expW(x, pm0)
print('VAF_exp2(pm0) = ', vaf(y, ym), ',   pm =', pm.flatten())
ym = apl_expW(x, pm)
print('VAF_exp2(pm) = ', vaf(y, ym), ',   pm =', pm.flatten())
