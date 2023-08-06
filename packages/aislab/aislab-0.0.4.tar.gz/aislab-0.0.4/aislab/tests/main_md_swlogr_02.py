# S T E P W I S E   L O G I S T I C   R E G R E S S I O N
#--------------------------------------
# Author: Alexander Efremov
# Date:   05.09.2009
# Course: Multivariable Control Systems
#--------------------------------------

import numpy as np
import pandas as pd
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_bn.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_fsel.swlogr import *
from aislab.gnrl.sf import *
from aislab.md_reg import *
# from aislab.md_swlogr import *
# from aislab.op_nlopt import *

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

# Load data
dat = pd.read_csv(dpath)
x = dat.iloc[:,  :-2].values
w = c_(dat['w'].values)
y = c_(dat['y'].values)

cnames = dat.columns.tolist()[:-2]
# cnames = ['var_' + s for s in list(map(str, range(1, x.shape[1] + 1)))]

# CONFIG FOR STEP-WISE LOGISTIC REGRESSION
###############################################################################
#--------------------------
# Author: Alexander Efremov
# Date:   12.11.2012
#--------------------------

# Initial model parameters and func(), grad(), hes() names
#    par['func'] = f_lgr
#    par['grad'] = g_lgr
#    par['hes'] = H_lgr
#    par['mdl_apl'] = lgr_apl

# Cofig parameters for newton()
par = {}
par['cnames'] = cnames
# modelling params
par['meth'] = 'newt'
par['gcnv'] = 1e-8
par['fcnv'] = 0
par['afcnv'] = 0
par['xcnv'] = 0
par['maxiter'] = 100
par['smin'] = 1e-12
par['dsp_op'] = np.array([1,2])

# par['dsp_ls = 1;      # za vizualizacia, kogato se izpolzva 'newtls'
# ako metodat e newtonls /t.e. newton with linr search/ dolnite parametri sa zadaljitelni => default values sa:
par['dcnv'] = 1
par['incrPrec'] = 1e-05
par['invmet'] = 'EVD'
par['invtype'] = 'PDMR'
par['inv.smin'] = 1e-16
# sledvashtite parametri sa za dopalnitelna nastroika na daljinata na stapkata. Default vals sa
par['smeth'] = 'fprev' # 'gang' # 'none'

par['p_incr'] = 1.2
par['p_decr'] = 0.6
par['sl'] = 1e-12
par['su'] = 1
par['sc'] = []

# swr params
par['SLE'] = 0.05
par['SLS'] = 0.05
par['pm0'] = 1
par['dsp'] = 'all' # 'no' # 'ovr'
par['nbm_crit'] = np.array([])
par['mtp'] = 'full' # 'empty' # 'init'
par['met'] = 'SWR' # 'BR' # 'FR'
par['metpminit'] = 'zero' # 'fapp'

# todo: implement par['metpminit'] = 'prev'
###############################################################################

par['met'] =  'SWR' # 'BR' # 'FR' #
par['mtp'] = 'empty' # 'full' # 'init' # 
par['ivi'] = c_(np.arange(1,int(np.floor(x.shape[1] / 3))+1))

tic()
model = swlogr(x, y, w, par)
toc()
