import ROOT 
from ROOT import TFile, TTree
#import collinearmass
#import tau
import os
import sys
import math
import random
import glob


masses=[110,115,120,125,130,135,140,145,150]
ifilepath='/cluster/data03/sbahrase/BrtStudies/PracticeDesk/TRUTH_LEVEL_BRT/BRTauTauMass/SAMPLES/HADHAD/H/'
ofilepath='/cluster/data03/sbahrase/BrtStudies/PracticeDesk/TRUTH_LEVEL_BRT/BRTauTauMass/SAMPLES/HADHAD/'

# tlv_tau1=TLorentzVector()
# tlv_tau2=TLorentzVector()
# tv2_met=TVector2()
masses = range(100, 155, 5)

for mass in masses:
    iFileName=ifilepath+'reco_gg_'+str(mass)+'_test_v0.root' 
    oFileName=ofilepath+'reco_gg_'+str(mass)+'_test_v0.root'
    _TreeNameInput='tau'
    _TreeNameOutput='Tree'

    print "<--  input file: "+iFileName
    print "--> output file: "+oFileName
    iFile = TFile.Open(iFileName)
    iTree = iFile.Get(_TreeNameInput)
    #    oDirName = oFileName[::-1].split("/",1)[-1][::-1]
#os.system("mkdir -p "+oDirName)
    oFile = TFile(oFileName,"RECREATE")
    oTree = iTree.CloneTree(0)
    oTree.SetName(_TreeNameOutput)
    nEntries = iTree.GetEntries()
    print "number of entries in original tree = %s" %nEntries
    for ientry in xrange(nEntries):
    ## Get the next tree in the chain and verify.
        if iTree.LoadTree(ientry) <  0: break
    ## Copy next entry into memory and verify.
        if iTree.GetEntry(ientry) <= 0: continue
        oTree.Fill()
    oTree.AutoSave()
    iFile.Close()
    oFile.Close()
