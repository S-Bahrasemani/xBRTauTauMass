from .mixins import *
from .taudecay import TauDecay
from . import log; log = log[__name__]

def define_objects(tree):

    tree.define_collection(
        name="taus",
        prefix="tau_pi0_",
        size="tau_pi0_n",
        mix=MCTauParticle)

    # tree.define_collection(
    #     name="mc",
    #     prefix="mc_",
    #     size="mc_n",
    #     mix=MCParticle)

    # tree.define_collection(
    #     name="higgs",
    #     prefix="mc_",
    #     size="mc_n",
    #     mix=MCParticle)

    tree.define_collection(
        name="jets",
        prefix="jet_antikt4truth_",
        size="jet_antikt4truth_n",
        mix=FourMomentum)
    
