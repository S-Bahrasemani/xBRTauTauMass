
## A Module to help harmonize tree branches  
## A List of intresting branches from truth-level trees to harmonize with reco-level trees 
## BRANCHES = {Oldbranch_name:{new_branch_name : value}, ...}

import os
import shutil

import ROOT
import math
from rootpy.io import root_open
from rootpy.tree import TreeModel, FloatCol, IntCol
from rootpy.stl import vector
from brtautau import parallel
import logging
from multiprocessing import Process
import array
from brtautau.parallel import run_pool
from brtautau.categories.features import FEATURES
log = logging.getLogger('apply-bdt-weights')

from ROOT import TLorentzVector

from rootpy.tree import TreeModel, FloatCol, IntCol, BoolCol
from rootpy.vector import LorentzRotation, LorentzVector, Vector3, Vector2
from rootpy import log
ignore_warning = log['/ROOT.TVector3.PseudoRapidity'].ignore(
    '.*transvers momentum.*')




variables = {}
variables['lep1_pt']                   = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['lep1_eta']                  = [''   ,'F',-10.00,10.00,  0.,TBranch(), -2.5,2.5,   40]
variables['lep2_pt']                   = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['lep2_eta']                  = [''   ,'F',-10.00,10.00,  0.,TBranch(), -2.5,2.5,   40]
variables['met_et']                    = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['transverse_mass_lep1_lep2'] = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,250000., 40]
variables['transverse_mass_lep1_met']  = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,250000., 40]
variables['transverse_mass_lep2_met']  = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,250000., 40]
variables['dphi_lep1_met']             = ['rad','F',  0.00, 3.15,  0.,TBranch(),   0.00, 3.15,   20]
variables['dphi_lep2_met']             = ['rad','F',  0.00, 3.15,  0.,TBranch(),   0.00, 3.15,   20]
variables['dphi_lep_lep']              = ['rad','F',  0.00, 3.15,  0.,TBranch(),   0.00, 3.15,   20]
variables['deta_lep_lep']              = ['',   'F',  0.00,20.00,  0.,TBranch(),   0.00,3.15,   40]
variables['dR_lep_lep']                = ['',   'F',  0.00,25.00,  0.,TBranch(),   0.00,3.15,   40]
variables['ptsum_lep1_lep2_met']       = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,300000., 30]
variables['ptsum_lep1_lep2']           = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,250000., 25]
variables['pttot_lep1_lep2_met']       = ['',   'F',  0.00, 2.00,  0.,TBranch(),   0.00, 1.10,   22]
variables['pttot_lep1_lep2']           = ['',   'F',  0.00, 2.00,  0.,TBranch(),   0.00, 1.10,   22]
variables['ptdiff_lep1_lep2']          = ['',   'F',  0.00, 2.00,  0.,TBranch(),   0.00, 1.10,   22]
variables['met_phi_centrality']        = ['',   'F', -1.45, 1.45,  0.,TBranch(),  -1.45, 1.45,   40]
variables['collinear_mass']            = ['',   'F', 0.00, 9999999,0.,TBranch(),   0.00,200000., 40]
