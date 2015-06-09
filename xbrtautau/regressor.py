# python imports
import os
# ROOT/rootpy 
from ROOT import TMVA
from rootpy.io import root_open
from rootpy.tree import Cut
import datetime
# local imports
from . import log; log[__name__]
from .variables import VARIABLES
from samples import Higgs
from samples.db import get_file

from rootpy.extern.argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--mode', default='gg', type=str, choices=['VBF', 'gg'])
parser.add_argument('--dry', action='store_true', default=False)
parser.add_argument('--level', default='truth', type=str, choices=['truth', 'reco'])
args = parser.parse_args()

my_datetime = datetime.date.today()
my_datetime = my_datetime.strftime("%m%d%Y")

channels=['hadhad', 'lephad', 'leplep']
class Regressor(TMVA.Factory):
    """
    """
    def __init__(self,
                 output_name,
                 features,
                 factory_name='TMVARegression',
                 verbose='V:!Silent:Color:DrawProgressBar'):

        self.output = root_open(output_name, 'recreate')

        TMVA.Factory.__init__(
            self, factory_name, self.output, verbose)
        self.factory_name = factory_name
        self.features = features

    def set_variables(self):
        """
        Set TMVA formated variables
        from the VARIABLES dict (see variables.py)
        """
        for varName in self.features:
            var = VARIABLES[varName]
            self.AddVariable(
                var['name'], 
                var['root'], 
                var['units'] if 'units' in var.keys() else '',
                var['type'])

    def book_brt(self,
                 ntrees=80,
                 node_size=0.2,
                 depth=8):
        """
        Book the BRT method (set all the parameters)
        """
        params = ["SeparationType=RegressionVariance"]
        params += ["BoostType=AdaBoost"]
        params += ["AdaBoostBeta=0.2"]
        params += ["MaxDepth={0}".format(depth)]
        params += ["MinNodeSize={0}%".format(node_size)]
        params += ["NTrees={0}".format(ntrees)]
        # Do we need those or not ?
        # params += ["PruneMethod=NoPruning"]
        # params += ["UseYesNoLeaf=False"]
        # params += ["DoBoostMonitor"]
        # params += ["nCuts={0}".format(nCuts)]
        # params += ["NNodesMax={0}".format(NNodesMax)]
        # DEPRECATED DEPRECATED
        # params += ["nEventsMin={0}".format(nEventsMin)]
        log.info(params)

        method_name =   "BRT_HiggsMass-" + str(my_datetime)+'_' + str(args.level)+'_' +str(args.mode)+'_'+ channels[1] 
        params_string = "!H:V"
        for param in params:
            params_string+= ":"+param
        self.BookMethod(
            TMVA.Types.kBDT,
            method_name,
            params_string)

    def train(self, mode='gg',level='truth', **kwargs):
        """
        Run, Run !
        """
        self.set_variables()
    
        higgs_array = Higgs(tree_name= 'Tree', mode=mode, level=level, masses=Higgs.MASSES, suffix='_train')

        cut = Cut('lephad==1')
        
        params = ['nTrain_Regression=0']
        params += ['nTest_Regression=1']
        #params = ['SplitMode=Random']
        params += ['NormMode=NumEvents']
        params += ['!V']
        params = ':'.join(params)

        self.PrepareTrainingAndTestTree(cut, params)
        for s in higgs_array.components:
            rfile = get_file(s.ntuple_path, s.student, suffix=s.suffix)
            tree = rfile[s.tree_name]
            self.AddRegressionTree(tree)
        self.AddRegressionTarget('resonance_m')
        # Could reweight samples 
        # self.AddWeightExpression("my_expression")

        # Actual training
        self.book_brt(**kwargs)
        self.TrainAllMethods()
