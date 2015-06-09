

import ROOT
from ROOT import TFile, TTree, TCanvas, TGraph

import os

def get_roc_curve(Zpath = 'Z ntuples path', Hpath= 'H125 ntuple path', mode = 'testing mode', channel = 'channel', **kwargs):
    Zfiles = [Zpath + 'ZtautauNp'+str(i)+'test.root') for i in range(6)]
    Hfiles = [Hpath + 'reco_'+str(mode)+'_'+str(mass)+'_test.root'  for mass in HMasses]

    
    

