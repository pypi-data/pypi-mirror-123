import copy

import numpy as np
import pandas as pd

from aislab.gnrl.sf import *
from aislab.gnrl.measr import *

##############################################################################
##############################################################################
def func(X, args):
    # Objective function for credit risk strategy optimization
    # needed for old GA
    case = 1
    if isinstance(X, list):
        case = -1
        X = np.array(X)
    # needed for old GA

    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut

    data = args['data']  # data set
    BRA = args['BRA']  # Desired Bad Rate in AA (less risky) risk zone
    BRR = args['BRR']  # Desired Bad Rate in RR (most risky) risk zone
    TA = args['TA']  # Desired Total number of applications in AA risk zone
    TR = args['TR']  # Desired Total number of applications in RR risk zone
    minNb = args['minNb']  # minimum number of Bad applications in each risk zone
    minNgb = args['minNgb']  # minimum number of Good & Bad applications in each risk zone
    mindBR = args['mindBR']  # minimum change in the Bad Rate moving from one risk zone to a neighbour zone
    w = args['w']  # vector containing the weights of all business requirements included in the objective function
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard
    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = args['minx']  # upper bound for cut-offs of the first scorecard
    maxx = args['maxx']  # upper bound for cut-offs of the second scorecard
    if X.ndim == 1: X = np.array([X])
    N = len(X)
    F = np.full((N,), np.nan)
    i = 0
    for x in X:
        x1, ss = sort(c_(x[:nc1, ]))
        x2, ss = sort(c_(x[nc1:, ]))
        minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
        maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
        x1 = (x1 - minx) / (maxx - minx) * (ub1 - lb1) + lb1
        x2 = (x2 - minx) / (maxx - minx) * (ub2 - lb2) + lb2
        x1 = np.round(x1.flatten())
        x2 = np.round(x2.flatten())
        if len(set(x1)) != len(x1) or len(set(x2)) != len(x2): return case*np.inf  # if there are 2 or more the same GB cut-offs: F = inf
        try:
            GB_zones = cut(data['Score_GB'].values, x1).flatten()
            GBR_zones = cut(data['Score_GBR'].values, x2).flatten()
        except:
            print("In fobj(): Wrong cut-offs...")
        good = confm(-GB_zones, -GBR_zones, w=data['Good'].values).astype(int)  # confusion matrix
        bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values).astype(int)  # confusion matrix
        reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values).astype(int)  # confusion matrix
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        bad_rate = bad / (good + bad) * 100
        total_gb = good + bad
        total = good + bad + reject
        drBR = bad_rate[:, 1:] - bad_rate[:, :-1]  # rowwise delta BR
        dcBR = bad_rate[1:, :] - bad_rate[:-1, :]  # colwise delta BR

        mr, nr = np.shape(drBR)
        mc, nc = np.shape(dcBR)
        drBR1 = copy.deepcopy(drBR)
        for k in range(nr-1, 0, -1):
            for j in range(mr-1, 0, -1):
                if k-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j, k-1]): drBR1[j, k-1] = drBR1[j, k]
                if j-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j-1, k]): drBR1[j-1, k] = drBR1[j, k]
        dcBR1 = copy.deepcopy(dcBR)
        for k in range(nc-1, 0, -1):
            for j in range(mc-1, 0, -1):
                if k-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j, k-1]): dcBR1[j, k-1] = dcBR1[j, k]
                if j-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j-1, k]): dcBR1[j-1, k] = dcBR1[j, k]
        negdrBR = drBR1[drBR1 < mindBR]  # negative trend or not enough change in rowwise delta BR
        negdcBR = dcBR1[dcBR1 < mindBR]  # negative trend or not enough change in colwise delta BR

        # discriminatory power of the strategy  #  min(F1) = 0
        F1 = (((BRA - bad_rate[0, 0]) / max(1e-6, 100 - BRA)) ** 2 + ((TA - total[0, 0]) / max(1e-6, TA)) ** 2) / 2
        F2 = (((BRR - bad_rate[-1, -1]) / max(1e-6, BRR - 0)) ** 2 + ((TR - total[-1, -1]) / max(1e-6, TR)) ** 2) / 2
        # monotonicity of BR  #  min(F2) = 0
        F3 = ((np.sum(mindBR - negdrBR) + np.sum(mindBR - negdcBR)) / (nc1 * nc2)) ** 2
        # mininmum number of Bad and Good & Bad applications per segment  #  min(F4) = min(F5) = 0
        F4 = (np.sum((minNb - bad) * (minNb - bad > 0) * (total_gb > 0)) / max(1e-6,
                                                                               (nc1 + 1) * (nc2 + 1) * minNb)) ** 2
        F5 = (np.sum((minNgb - total_gb)*(minNgb - total_gb > 0)*(total_gb > 0))/max(1e-6, (nc1 + 1)*(nc2 + 1)*minNgb))**2
        # minimum number of NaN cells: min(F6) = 0
        F6 = (np.sum(np.sum(np.isnan(bad_rate))) / ((nc1 + 1) * (nc2 + 1))) ** 2
        # minimum number of records in most populated cell  # min(F7) = 0
        F7 = np.max(np.max(total)) / max(1e-6, sum(sum(total)))
        F[i] = w[0] * F1 + w[1] * F2 + w[2] * F3 + w[3] * F4 + w[4] * F5 + w[5] * F6 + w[6] * F7

        if np.isnan(F[i]):
            F[i] = case * np.inf
            return F
        i += 1
        # needed for old GA
        if len(F) == 1: F = -F[0]
        if isinstance(F, float) and np.isinf(F): F = -np.inf
        # needed for old GA
    return F
##############################################################################
##############################################################################

##############################################################################
def firstgen(pop, par, args):
    F = [func(pop[x], args) for x in range(len(pop))]
    sorted_F = sorted([[pop[x], F[x]] for x in range(len(pop))], key=lambda x: x[1])
    population = [sorted_F[x][0] for x in range(len(sorted_F))]
    F = [sorted_F[x][1] for x in range(len(sorted_F))]
    return {'individuals': population, 'F': sorted(F)}

##############################################################################
def func_sim(max_F, itrConstF):
    result = False
    br = 0
    for i in range(len(max_F) - 1):
        if max_F[i] == max_F[i + 1]:
            br += 1
        else:
            br = 0
    if br == itrConstF - 1: result = True
    return result

##############################################################################
def genopt(par, args):
    itrConstF = par['stop_itrConstF']
    w = args['w']  # Acc  Rej  mt    Nb   Ngb  NaN  min_maxCell
    nc1 = args['nc1']
    w = w/np.sum(w)
    pop = population(par, args, 0)
    gen = []
    gen.append(firstgen(pop, par, args))
    fitness_avg = np.array([sum(gen[0]['F'])/len(gen[0]['F'])])
    fitness_max = np.array([max(gen[0]['F'])])
    finish = False
    itr = 0
    maxiter = 1200
    while finish == False:
        itr += 1
        if itr == maxiter:                              break
        if max(fitness_max) >= 0:                       break
        if max(fitness_avg) >= 0:                       break
        if func_sim(fitness_max, itrConstF) == True:    break
        gen.append(nextgen(gen[-1], par, args, itr))
        fitness_avg = np.append(fitness_avg, sum(gen[-1]['F']) / len(gen[-1]['F']))
        fitness_max = np.append(fitness_max, max(gen[-1]['F']))
        print(itr, 'Fmin = ', -gen[-1]['F'][-1])
    x_opt = gen[-1]['individuals'][-1]
    x1, ss = sort(c_(x_opt[:nc1]))
    x2, ss = sort(c_(x_opt[nc1:]))
    x_opt = np.hstack((x1.flatten(), x2.flatten()))
    F_opt = -gen[-1]['F'][-1]

    return F_opt, x_opt

##############################################################################
def individual(args, mode=1):  # ng - number of genes, lb - lower bound, ub - upper bound
    nc1 = args['nc1']
    ub1 = args['ub1']
    lb1 = args['lb1']
    nc2 = args['nc2']
    ub2 = args['ub2']
    lb2 = args['lb2']
    seed = args['seed1']
    indv_1 = rand((1, nc1), l=lb1, h=ub1, tp='int', seed=seed).flatten().tolist()
    indv_2 = rand((1, nc2), l=lb2, h=ub2, tp='int', seed=seed + nc1 + 1).flatten().tolist()
    indv_1.sort()
    indv_2.sort()
    indv = indv_1 + indv_2
    return indv

##############################################################################
def mating(parents, seed, args, met='Single Point'):
    nc1 = args['nc1']
    if met == 'Single Point':
        cut = rand(l=1, h=len(parents[0]), tp='int', seed=seed)[0, 0]
        child = [parents[0][0:cut] + parents[1][cut:]]
        child.append(parents[1][0:cut] + parents[0][cut:])
    seed = seed + 1
    if met == 'Two Pionts':
        cut_1 = rand(l=1, h=len(parents[0]) - 1, tp='int', seed=seed)
        cut_2 = rand(l=1, h=len(parents[0]), tp='int', seed=seed + cut_1)
        br = 0
        while cut_2 < cut_1:
            br += 1
            cut_2 = rand(l=1, h=len(parents[0]), tp='int', seed=seed + 2 + br)
        child = [parents[0][0:cut_1] + parents[1][cut_1:cut_2] + [parents[0][cut_2:]]]
        child.append([parents[1][0:cut_1] + parents[0][cut_1:cut_2] + [parents[1][cut_2:]]])
    child_1 = child[0][:nc1]
    child_2 = child[0][nc1:]

    child[0] = child_1 + child_2
    child_1 = child[1][:nc1]
    child_2 = child[1][nc1:]

    child[1] = child_1 + child_2
    return child

##############################################################################
def mutation(indv, par, args, seed, i_mut, i):
    if not any(i_mut == i): return indv
    nc1 = args['nc1']
    nc2 = args['nc2']
    minx = args['minx']
    maxx = args['maxx']
    met = par['mut_met']
    mut_strength = par['mut_strength']
    stdev = par['mut_stdev']
    ind = rand(size=(mut_strength,), l=0, h=nc1+nc2-1, tp='int', seed=seed)
    if met == 'Gauss':
        for x in ind:
            seed = seed*x + 1
            indv[x] = int(indv[x] + randn(m=0, s=stdev, seed=seed))
    if met == 'Reset':
        for x in ind:
            seed = seed*x + 1
            indv[x] = rand(l=minx, h = maxx, tp='int', seed=seed)[0, 0]
    return indv # mutated individual


##############################################################################
def nextgen(gen, par, args, itr):
    Nind = par['Nind']
    selection_met = par['select_met']
    pairing_met = par['pairing_met']
    mut_rate = par['mut_rate']
    best = {}
    next_sgen = {}
    best['individuals'] = gen['individuals'].pop(-1)
    best['F'] = gen['F'].pop(-1)
    selected = selection(gen, itr, selection_met)
    parents = pairing(best, selected, itr, met=pairing_met)
    children = [[[mating(parents[i], itr + i + j, args) for i in range(len(parents))]
                 [j][h] for h in range(2)]
                for j in range(len(parents))]
    children1 = [children[i][0] for i in range(len(parents))]
    children2 = [children[i][1] for i in range(len(parents))]
    unmutated = selected['individuals'] + children1 + children2
    n = len(gen['individuals'])
    i_mut = find(rand(size=(n,), seed=itr) < mut_rate / 100)
    mutated = [mutation(unmutated[i], par, args, itr * Nind + i, i_mut, i) for i in range(n)]
    indvs = mutated + [best['individuals']]
    next_gen = [func(mutated[i], args) for i in range(len(mutated))]
    F = [next_gen[x] for x in range(len(gen['F']))] + [best['F']]
    sorted_next_gen = sorted([[indvs[x], F[x]] for x in range(len(indvs))], key=lambda x: x[1])
    next_sgen['individuals'] = [sorted_next_gen[x][0] for x in range(len(sorted_next_gen))]
    next_sgen['F'] = [sorted_next_gen[x][1] for x in range(len(sorted_next_gen))]
    gen['individuals'].append(best['individuals'])
    gen['F'].append(best['F'])
    return next_sgen


##############################################################################
def pairing(best, selected, seed, met='Fbest'):
    indvs = [best['individuals']] + selected['individuals']
    F = [best['F']] + selected['F']
    n = len(indvs)
    if met == 'Fbest':
        parents = [[indvs[i], indvs[i + 1]] for i in range(n // 2)]
    if met == 'rnd':
        parents = []
        n2 = n // 2
        for i in range(n2):
            seed = seed + n2 + i
            parents.append([indvs[rand(l=0, h=n - 1, tp='int', seed=seed)[0, 0]],
                            indvs[rand(l=0, h=n - 1, tp='int', seed=seed + n2)[0, 0]]])
            br = 0
            while parents[i][0] == parents[i][1]:
                br += 1
                seed = seed + 2 * n2 + i + br
                parents[i][1] = indvs[rand(l=0, h=n - 1, tp='int', seed=seed)[0, 0]]
    if met == 'wrnd':
        normalized_F = sorted([F[i] / sum(F) for i in range(n // 2)], reverse=True)
        csum = np.array(normalized_F).cumsum()
        parents = []
        for i in range(n // 2):
            parents.append([indvs[roulette(csum, rand(seed=seed + i))], indvs[roulette(csum, rand(seed=seed + n + i))]])
            j = 0
            while parents[i][0] == parents[i][1]:
                j += 1
                parents[i][1] = indvs[roulette(csum, rand(seed=seed + 2 * n + j))]
    return parents


##############################################################################
def population(par, args, itr):
    Nind = par['Nind']
    pop = []
    for i in range(Nind):
        args['seed1'] = (itr + i) * (args['nc1'] + args['nc2'])
        pop += [individual(args, 1)]
    return pop


##############################################################################
def roulette(cum_sum, chance):
    cumF = list(cum_sum.copy())
    cumF.append(chance)
    cumF = sorted(cumF)
    return cumF.index(chance)


##############################################################################
def selection(gen, seed, met='Fhalf'):
    n = len(gen['individuals'])
    ns = int(np.ceil(n / 2))
    if met == 'roulette':
        ind = 1 - np.isinf(gen['F']) == 1
        if all(ind == 0):
            sF = -1  # !!!!!!!!!!!!!!!! sF = 1
        elif any(ind == 0):
            sF = -1  # !!!!!!!!!!!!!!!! sF = np.max(gen['F'][ind])
        else:
            sF = sum(gen['F'])
        # sorted(F)
        # F1 = copy.deepcopy(F)
        # Fn = rnml(F)
        Fn = sorted([gen['F'][i] / sF for i in range(len(gen['F']))], reverse=True)  # normalization of F
        cumFn = np.array(Fn).cumsum()
        selected = []
        for i in range(n // 2):
            selected.append(roulette(cumFn, rand(seed=seed + i)[0, 0]))
            j = 0
            while len(set(selected)) != len(selected):
                j += 1
                selected[i] = roulette(cumFn, rand(seed + n + j)[0, 0])
        selected = {'individuals': [gen['individuals'][int(selected[i])] for i in range(n // 2)],
                    'F': [gen['F'][int(selected[i])] for i in range(n // 2)]}
    elif met == 'Fhalf':
        selected_indvs = [gen['individuals'][-i - 1] for i in range(ns)]
        Fwinners = [gen['F'][-i - 1] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    elif met == 'rnd':
        selected_indvs = [gen['individuals'][rand(l=0, h=len(gen['F']) - 1, tp='int', seed=seed + i)[0, 0]] for i in
                          range(ns)]
        Fwinners = [gen['F'][rand(l=0, h=len(gen['F']) - 1, tp='int', seed=seed + i)[0, 0]] for i in range(ns)]
        selected = {'individuals': selected_indvs, 'F': Fwinners}
    return selected


##############################################################################
def tables(x, args):
    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut

    # needed for old GA
    case = 1
    if isinstance(x, list):
        case = -1
        x = np.array(x)
    # needed for old GA

    data = args['data']  # data set
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard
    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = np.min([args['minx'], np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([args['maxx'], np.max(x)])  # upper bound for cut-offs of the second scorecard


    if case == 1:
        x1, ss = sort(c_(x[:nc1, ]))
        x2, ss = sort(c_(x[nc1:, ]))
        minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
        maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
        x1 = (x1 - minx)/(maxx - minx)*(ub1 - lb1) + lb1
        x2 = (x2 - minx)/(maxx - minx)*(ub2 - lb2) + lb2
        x1 = np.round(x1.flatten())
        x2 = np.round(x2.flatten())
    else:
        x1 = x[:nc1]
        x2 = x[nc1:]

    GB_zones = cut(data['Score_GB'].values, x1).flatten()
    GBR_zones = cut(data['Score_GBR'].values, x2).flatten()

    names1 = ['GB_A']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('GB_R')
    names2 = ['GBR_A']
    for i in range(nc2 - 1): names2.append('GBR_G' + str(i+1))
    names2.append('GBR_R')
    # confusion matrix
    good = confm(-GB_zones, -GBR_zones, w=data['Good'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)

    # n1 = len(names1)
    # for i in range(n1):
    #     if i not in np.unique(GB_zones):
    #         good = np.hstack((good[:, :i], nans((n1, 1)), good[:, (i+1):]))
    # n2 = len(names2)
    # for i in range(n2):
    #     if i not in np.unique(GBR_zones):
    #         good = np.vstack((good[:i, :], nans((1, n2)), good[(i+1):, :]))


    good = pd.DataFrame(good, index=names1, columns=names2)
    bad = pd.DataFrame(bad, index=names1, columns=names2)
    reject = pd.DataFrame(reject, index=names1, columns=names2)

    bad_rate = bad/(good + bad)*100
    total_gb = good + bad
    total = total_gb + reject
    return good, bad, reject, total_gb, total, bad_rate


##############################################################################
def tables2(G, B, R, TGB, TGBR, BR, args):
    # GB Scorecard
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. first (GB) scorecard
    names1 = ['Accept']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('Reject')
    names1.append('Total')
    names2 = ['Accept']
    for i in range(nc2 - 1): names2.append('GB_G' + str(i+1))
    names2.append('Reject')
    names2.append('Total')
    G1 = np.sum(G, axis=1)
    B1 = np.sum(B, axis=1)
    R1 = np.sum(R, axis=1)
    BadRej = B1 + R1
    TGBR1 = np.sum(TGBR, axis=1)
    TotalPrc = TGBR1 / np.sum(TGBR1) * 100
    BR = B1 / (G1 + B1) * 100
    BadAndRejectRate = BadRej / (G1 + BadRej) * 100
    T1 = np.vstack((G1, B1, R1, BadRej, TGBR1, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B1) / np.sum(G1 + B1)
    BadAndRejectRate1 = np.sum(B1 + R1) / np.sum(G1 + B1 + R1)
    Tot1 = [np.sum(np.sum(G1)), np.sum(np.sum(B1)), np.sum(np.sum(R1)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR1)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 1)
    T1 = np.hstack((T1, Tot))
    T1 = pd.DataFrame(T1, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names1)
    # GBR Scorecard
    G2 = np.sum(G, axis=0)
    B2 = np.sum(B, axis=0)
    R2 = np.sum(R, axis=0)
    BadRej = B2 + R2
    TGBR2 = np.sum(TGBR, axis=0)
    TotalPrc = TGBR2 / np.sum(TGBR2) * 100
    BR = B2 / (G2 + B2) * 100
    BadAndRejectRate = BadRej / (G2 + BadRej) * 100
    T2 = np.vstack((G2, B2, R2, BadRej, TGBR2, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B2) / np.sum(G2 + B2)
    BadAndRejectRate1 = np.sum(B2 + R2) / np.sum(G2 + B2 + R2)
    Tot1 = [np.sum(np.sum(G2)), np.sum(np.sum(B2)), np.sum(np.sum(R2)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR2)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 2)
    T2 = np.hstack((T2, Tot))
    T2 = pd.DataFrame(T2, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names2)
    return T1, T2
###############################################################################
