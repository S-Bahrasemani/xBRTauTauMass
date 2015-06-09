import logging
import os
import rootpy

MMC_VERSION = 1
MMC_MASS = 'mmc%d_resonance_m' % MMC_VERSION
MMC_PT = 'mmc%d_resonance_pt' % MMC_VERSION
Coll_MASS = 'mass_collinear_tau1_tau2'

DEFAULT_STUDENT = 'flat'
DEFAULT_TREE = 'Tree'
NTUPLE_PATH = 'ntuples'
UNMERGED_NTUPLE_PATH = '/cluster/data03/sbahrase/BrtStudies/PracticeDesk/TRUTH_LEVEL_BRT/flat_ntuples/running'

import ROOT

log = logging.getLogger('brtautau')
if not os.environ.get("DEBUG", False):
    log.setLevel(logging.INFO)
rootpy.log.setLevel(logging.INFO)

ROOT.gROOT.SetBatch(True)

ATLAS_LABEL = os.getenv('ATLAS_LABEL', 'Internal').strip()
