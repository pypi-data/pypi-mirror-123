import os, sys
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(BASE_DIR)
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from pytrad.utils.KCI.KCI import KCI_UInd
from pytrad.utils.KCI import GaussianKernel


class MLP(nn.Module):
    """
    Python implementation MLP, which is the same of G1 and G2
    Input: X (x1 or x2)
    """
    def __init__(self, n_inputs, n_outputs, n_layers=1, n_units=100):
        """ The MLP must have the first and last layers as FC.
        :param n_inputs: input dim
        :param n_outputs: output dim
        :param n_layers: layer num = n_layers + 2
        :param n_units: the dimension of hidden layers
        :param nonlinear: nonlinear function
        """
        super(MLP, self).__init__()
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_layers = n_layers
        self.n_units = n_units

        # create layers
        layers = [nn.Linear(n_inputs, n_units)]
        for i in range(n_layers):
            layers.append(nn.ReLU())
            layers.append(nn.Linear(n_units, n_units))
        layers.append(nn.ReLU())
        layers.append(nn.Linear(n_units, n_outputs))
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        x = self.layers(x)
        return x


class MixGaussianLayer(nn.Module):
    def __init__(self, Mix_K=5):
        super(MixGaussianLayer, self).__init__()
        self.Mix_K = Mix_K
        self.Pi = nn.Parameter(torch.randn(self.Mix_K,1))
        self.Mu = nn.Parameter(torch.randn(self.Mix_K,1))
        self.Var = nn.Parameter(torch.randn(self.Mix_K,1))

    def forward(self, x):
        Constraint_Pi = F.softmax(self.Pi, 0)
        # -(x-u)**2/(2var**2)
        Middle1 = -((x.expand(len(x),self.Mix_K) - self.Mu.T.expand(len(x),self.Mix_K)).pow(2)).div(2*(self.Var.T.expand(len(x),self.Mix_K)).pow(2))
        # sum Pi*Middle/var
        Middle2 = torch.exp(Middle1).mm(Constraint_Pi.div(torch.sqrt(2*math.pi*self.Var.pow(2))))
        # log sum
        out = sum(torch.log(Middle2))

        return out


class PNL(object):
    """
    Use of constrained nonlinear ICA for distinguishing cause from effect.
    Python Version 3.7
    PURPOSE:
          To find which one of xi (i=1,2) is the cause. In particular, this
          function does
            1) preprocessing to make xi rather clear to Gaussian,
            2) learn the corresponding 'disturbance' under each assumed causal
            direction, and
            3) performs the independence tests to see if the assumed cause if
            independent from the learned disturbance.
    """
    def __init__(self, maxlag=2):
        self.maxlag = maxlag

    def nica_mnd(self, X, TotalEpoch, KofMix):
        """
        Use of "Nonlinear ICA with MND for Matlab" for distinguishing cause from effect
        PURPOSE: Performing nonlinear ICA with the minimal nonlinear distortion or smoothness regularization.
        INPUTS: X (n*T): a matrix containing multivariate observed data. Each row of the matrix x is a observed signal.
        OUTPUTS: Y (n*T): the separation result.
        """
        trpattern = X
        trpattern = trpattern - np.tile(np.mean(trpattern, axis=1).reshape(2,1), (1, len(trpattern[0])))
        trpattern = np.dot(np.diag(1.5 / np.std(trpattern, axis=1)), trpattern)
        # --------------------------------------------------------
        x1 = torch.from_numpy(trpattern[0,:]).type(torch.FloatTensor).reshape(-1,1)
        x2 = torch.from_numpy(trpattern[1,:]).type(torch.FloatTensor).reshape(-1,1)
        length = len(x1)
        y1 = x1

        Final_y2 = x2
        Min_loss = float('inf')

        for epoch in range(TotalEpoch):
            # print('This is the {}-th epoch'.format(epoch))
            G1 = MLP(1, 1, n_layers=3, n_units=20)
            G2 = MLP(1, 1, n_layers=3, n_units=20)
            y2 = G2(x2) - G1(x1)

            MixGaussian = MixGaussianLayer(Mix_K=KofMix)
            loss_pdf = -MixGaussian(y2)

            x2.retain_grad()
            y2.backward(torch.ones(length,1), retain_graph=True)

            jacob = x2.grad
            loss_jacob = -sum(torch.log(torch.abs(jacob)+1e-10))

            loss = 0.1*loss_jacob + loss_pdf

            if loss[0]<Min_loss:
                Min_loss = loss[0]
                Final_y2 = y2

            if epoch % 100 == 0:
                print('---------------------------{}-th epoch-------------------------------'.format(epoch))
                print('The Total loss is {}'.format(loss))
                print('The jacob loss is {}'.format(loss_jacob))
                print('The pdf loss is {}'.format(loss_pdf))

            optimizer = torch.optim.Adam([
                    {'params': G1.parameters()},
                    {'params': G2.parameters()},
                    {'params': MixGaussian.parameters()}
                    ], lr=1e-4, betas=(0.9,0.99))

            optimizer.zero_grad()
            loss[0].backward(retain_graph=True)
            optimizer.step()

        return y1, Final_y2

    def cause_or_effect(self, x):
        """
        INPUTS:
                x (T*2): has two columns, each of them corresponds to a continuous
                variable. T is the sample size.
        OUTPUTS:
                The statistical tests results will be printed by this function.
         ----------------------------------------------------------------------------
          We are given x
          To avoid local optima and accelerate the learning process, we first try
          to transform the data to make them seem regular.
          The automatic procedure will be provided in future.
          Currently this procedure is done by you...
        print('Please use nonlinear transformations to make the transformed variables closer to Gaussian before running the program.')
         ----------------------------------------------------------------------------
         If you want to test other data sets, please let 'data' contain the original data and 'temp' contain the transformed data.
        """
        N = x.shape[0]
        data = x.T
        kernelX = GaussianKernel()
        kernelY = GaussianKernel()
        kci = KCI_UInd(N, kernelX, kernelY)

        # Now let's see if x1 -> x2 is plausible
        y1, y2 = self.nica_mnd(data, 5000, 3)
        print('To see if x2 -> x1...')

        y1_np = np.squeeze(y1.detach().numpy().T)
        y2_np = np.squeeze(y2.detach().numpy().T)

        pval_foward, _ = kci.compute_pvalue(y1_np, y2_np)

        # Now let's see if x2 -> x1 is plausible
        y1, y2 = self.nica_mnd(data[[1, 0], :], 5000, 3)
        print('To see if x2 -> x1...')

        y1_np = np.squeeze(y1.detach().numpy().T)
        y2_np = np.squeeze(y2.detach().numpy().T)

        pval_backward, _ = kci.compute_pvalue(y1_np, y2_np)

        return pval_foward, pval_backward