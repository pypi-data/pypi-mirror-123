import time
from pytrad.utils.PCUtils import Algorithm1, Algorithm2, Algorithm3


def pc(data, alpha, indep_test, stable, uc_rule, uc_priority):
    '''
    Perform Peter-Clark algorithm for causal discovery

    Parameters
    ----------
    data : data set (numpy ndarray)
    alpha : desired significance level (float) in (0, 1)
    test_name : name of the independence test being used
            [fisherZ, chisq, gsq, mvfisherZ, KCI]
           - "Fisher_Z": Fisher's Z conditional independence test
           - "Chi_sq": Chi-squared conditional independence test
           - "G_sq": G-squared conditional independence test
           - "MV_Fisher_Z": Missing-value Fishers'Z conditional independence test
           - "KCI": kernel-based conditional independence test
    stable : run stabilized skeleton discovery if True (default = True)
    uc_rule : how unshielded colliders are oriented
           0: run uc_sepset
           1: run maxP
           2: run definiteMaxP
    uc_priority : rule of resolving conflicts between unshielded colliders
           -1: whatever is default in uc_rule
           0: overwrite
           1: orient bi-directed
           2. prioritize existing colliders
           3. prioritize stronger colliders
           4. prioritize stronger* colliers

    Returns
    -------
    cg : a CausalGraph object

    '''

    start = time.time()
    cg_1 = Algorithm1.skeleton_discovery(data, alpha, indep_test, stable)

    if uc_rule == 0:
        if uc_priority != -1:
            cg_2 = Algorithm2.uc_sepset(cg_1, uc_priority)
        else:
            cg_2 = Algorithm2.uc_sepset(cg_1)
        cg = Algorithm3.meek(cg_2)

    elif uc_rule == 1:
        if uc_priority != -1:
            cg_2 = Algorithm2.maxp(cg_1, uc_priority)
        else:
            cg_2 = Algorithm2.maxp(cg_1)
        cg = Algorithm3.meek(cg_2)

    elif uc_rule == 2:
        if uc_priority != -1:
            cg_2 = Algorithm2.definite_maxp(cg_1, alpha, uc_priority)
        else:
            cg_2 = Algorithm2.definite_maxp(cg_1, alpha)
        cg_before = Algorithm3.definite_meek(cg_2)
        cg = Algorithm3.meek(cg_before)
    end = time.time()

    cg.PC_elapsed = end - start

    return cg

