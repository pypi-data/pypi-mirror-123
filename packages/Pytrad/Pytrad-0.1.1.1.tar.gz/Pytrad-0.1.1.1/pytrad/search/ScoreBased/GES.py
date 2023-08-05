from pytrad.utils.DAG2CPDAG import dag2cpdag
from pytrad.utils.GESUtils import *
from pytrad.utils.PDAG2DAG import pdag2dag
from pytrad.graph.GeneralGraph import GeneralGraph
from pytrad.graph.GraphNode import GraphNode


def ges(X, score_func, maxP=None, parameters=None):
    '''
    Greedy equivalence search algorithm

    Parameters
    ----------
    X : Data with T*D dimensions
    score_func : the score function you want to use
    maxP : allowed maximum number of parents when searching the graph
    parameters : when using CV likelihood,
                  parameters['kfold']: k-fold cross validation
                  parameters['lambda']: regularization parameter
                  parameters['dlabel']: for variables with multi-dimensions,
                               indicate which dimensions belong to the i-th variable.

    Returns
    -------
    Record['G']: learned causal graph
    Record['update1']: each update (Insert operator) in the forward step
    Record['update2']: each update (Delete operator) in the backward step
    Record['G_step1']: learned graph at each step in the forward step
    Record['G_step2']: learned graph at each step in the backward step
    Record['score']: the score of the learned graph
    '''

    X = np.asmatrix(X)
    if score_func == 'local_score_CV_general':  # % k-fold negative cross validated likelihood based on regression in RKHS
        if parameters is None:
            parameters = {'kfold': 10,  # 10 fold cross validation
                          'lambda': 0.01}  # regularization parameter
        if maxP is None:
            maxP = X.shape[1] / 2  # maximum number of parents
        N = X.shape[1]  # number of variables

    elif score_func == 'local_score_marginal_general':  # negative marginal likelihood based on regression in RKHS
        parameters = {}
        if maxP is None:
            maxP = X.shape[1] / 2  # maximum number of parents
        N = X.shape[1]  # number of variables

    elif score_func == 'local_score_CV_multi':  # k-fold negative cross validated likelihood based on regression in RKHS
        # for data with multi-variate dimensions
        if parameters is None:
            parameters = {'kfold': 10, 'lambda': 0.01, 'dlabel': {}}  # regularization parameter
            for i in range(X.shape[1]):
                parameters['dlabel']['{}'.format(i)] = i
        if maxP is None:
            maxP = len(parameters['dlabel']) / 2
        N = len(parameters['dlabel'])

    elif score_func == 'local_score_marginal_multi':  # negative marginal likelihood based on regression in RKHS
        # for data with multi-variate dimensions
        if parameters is None:
            parameters = {'dlabel': {}}
            for i in range(X.shape[1]):
                parameters['dlabel']['{}'.format(i)] = i
        if maxP is None:
            maxP = len(parameters['dlabel']) / 2
        N = len(parameters['dlabel'])

    elif score_func == 'local_score_BIC':  # Greedy equivalence search with BIC score
        if maxP is None:
            maxP = X.shape[1] / 2
        N = X.shape[1]  # number of variables

    elif score_func == 'local_score_BDeu':  # Greedy equivalence search with BDeu score
        if maxP is None:
            maxP = X.shape[1] / 2
        N = X.shape[1]  # number of variables

    else:
        raise Exception('Unknown function!')

    node_names = [("x%d" % i) for i in range(N)]
    nodes = []

    for name in node_names:
        node = GraphNode(name)
        nodes.append(node)

    G = GeneralGraph(nodes)
    # G = np.matlib.zeros((N, N)) # initialize the graph structure
    score = score_g(X, G, score_func, parameters)  # initialize the score

    G = pdag2dag(G)
    G = dag2cpdag(G)

    ## --------------------------------------------------------------------
    ## forward greedy search
    record_local_score = [[] for i in range(
        N)]  # record the local score calculated each time. Thus when we transition to the second phase,
    # many of the operators can be scored without an explicit call the the scoring function
    # record_local_score{trial}{j} record the local scores when Xj as a parent
    score_new = score
    count1 = 0
    update1 = []
    G_step1 = []
    score_record1 = []
    graph_record1 = []
    while True:
        count1 = count1 + 1
        score = score_new
        score_record1.append(score)
        graph_record1.append(G)
        min_chscore = 1e7
        min_desc = []
        for i in range(N):
            for j in range(N):
                if (G.graph[i, j] == 0 and G.graph[j, i] == 0 and i != j and len(np.where(G.graph[j, :] == 1)[
                                                                                     0]) <= maxP):
                    # find a pair (Xi, Xj) that is not adjacent in the current graph , and restrict the number of parents
                    Tj = np.intersect1d(np.where(G.graph[:, j] == -1)[0],
                                        np.where(G.graph[j, :] == -1)[0])  # neighbors of Xj

                    Ti = np.union1d(np.where(G.graph[:, i] != 0)[0], np.where(G.graph[i, 0] != 0)[0])  # adjacent to Xi

                    NTi = np.setdiff1d(np.arange(N), Ti)
                    T0 = np.intersect1d(Tj, NTi)  # find the neighbours of Xj that are not adjacent to Xi
                    # for any subset of T0
                    sub = Combinatorial(T0.tolist())  # find all the subsets for T0
                    S = np.zeros(len(sub))
                    # S indicate whether we need to check sub{k}.
                    # 0: check both conditions.
                    # 1: only check the first condition
                    # 2: check nothing and is not valid.
                    for k in range(len(sub)):
                        if (S[k] < 2):  # S indicate whether we need to check subset(k)
                            V1 = insert_validity_test1(G, i, j, sub[k])  # Insert operator validation test:condition 1
                            if (V1):
                                if (not S[k]):
                                    V2 = insert_validity_test2(G, i, j,
                                                               sub[k])  # Insert operator validation test:condition 2
                                else:
                                    V2 = 1
                                if (V2):
                                    Idx = find_subset_include(sub[k], sub)  # find those subsets that include sub(k)
                                    S[np.where(Idx == 1)] = 1
                                    chscore, desc, record_local_score = insert_changed_score(X, G, i, j, sub[k],
                                                                                             record_local_score,
                                                                                             score_func,
                                                                                             parameters)
                                    # calculate the changed score after Insert operator
                                    # desc{count} saves the corresponding (i,j,sub{k})
                                    # sub{k}:
                                    if (chscore < min_chscore):
                                        min_chscore = chscore
                                        min_desc = desc
                            else:
                                Idx = find_subset_include(sub[k], sub)  # find those subsets that include sub(k)
                                S[np.where(Idx == 1)] = 2

        if (len(min_desc) != 0):
            score_new = score + min_chscore
            if (score - score_new <= 0):
                break
            G = insert(G, min_desc[0], min_desc[1], min_desc[2])
            update1.append([min_desc[0], min_desc[1], min_desc[2]])
            print(G.graph)
            print(update1)
            G = pdag2dag(G)
            G = dag2cpdag(G)
            G_step1.append(G)
        else:
            score_new = score
            break

    ## --------------------------------------------------------------------
    # backward greedy search
    print('backward')
    count2 = 0
    score_new = score
    update2 = []
    G_step2 = []
    score_record2 = []
    graph_record2 = []
    while True:
        count2 = count2 + 1
        score = score_new
        score_record2.append(score)
        graph_record2.append(G)
        min_chscore = 1e7
        min_desc = []
        for i in range(N):
            for j in range(N):
                if ((G.graph[j, i] == -1 and G.graph[i, j] == -1) or G.graph[j, i] == 1):  # if Xi - Xj or Xi -> Xj
                    Hj = np.intersect1d(np.where(G.graph[:, j] == -1)[0],
                                        np.where(G.graph[j, :] == -1)[0])  # neighbors of Xj
                    Hi = np.union1d(np.where(G.graph[i, :] != 0)[0], np.where(G.graph[:, i] != 0)[0])  # adjacent to Xi
                    H0 = np.intersect1d(Hj, Hi)  # find the neighbours of Xj that are adjacent to Xi
                    # for any subset of H0
                    sub = Combinatorial(H0.tolist())  # find all the subsets for H0
                    S = np.ones(len(sub))  # S indicate whether we need to check sub{k}.
                    # 1: check the condition,
                    # 2: check nothing and is valid;
                    for k in range(len(sub)):
                        if (S[k] == 1):
                            V = delete_validity_test(G, i, j, sub[k])  # Delete operator validation test
                            if (V):
                                # find those subsets that include sub(k)
                                Idx = find_subset_include(sub[k], sub)
                                S[np.where(Idx == 1)] = 2  # and set their S to 2
                        else:
                            V = 1

                        if (V):
                            chscore, desc, record_local_score = delete_changed_score(X, G, i, j, sub[k],
                                                                                     record_local_score, score_func,
                                                                                     parameters)
                            # calculate the changed score after Insert operator
                            # desc{count} saves the corresponding (i,j,sub{k})
                            if (chscore < min_chscore):
                                min_chscore = chscore
                                min_desc = desc

        if (len(min_desc) != 0):
            score_new = score + min_chscore
            if (score - score_new <= 0):
                break
            G = delete(G, min_desc[0], min_desc[1], min_desc[2])
            update2.append([min_desc[0], min_desc[1], min_desc[2]])
            print(G.graph)
            print(update2)
            G = pdag2dag(G)
            G = dag2cpdag(G)
            G_step2.append(G)
        else:
            score_new = score
            break

    Record = {'update1': update1, 'update2': update2, 'G_step1': G_step1, 'G_step2': G_step2, 'G': G, 'score': score}
    return Record
