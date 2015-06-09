#import BRTmass
import tau
from ROOT import *
import math
import collinearmass
import smirnov
import numpy

smir_mass=125
recoTree=TChain('PowPyth8_AU2CT10_ggH125_tautauhh_mc12a')
recoTree.Add('/cluster/data11/endw/ntuples/prod_v29/hhskim/hhskim.root')
smTree=TChain('Tree')
smTree.Add('/cluster/data04/mquennev/higgs/rootfiles/met/Hmass125.root')

smirnovFile=TFile('smirnov_curves/Smirnov.root')

transform_string='met_phi'

smirnovGraph_par=smirnovFile.Get('sm_reco_smirnov_par_'+str(smir_mass))
smirnovGraph_perp=smirnovFile.Get('sm_reco_smirnov_perp_'+str(smir_mass))
smirnovGraph_et=smirnovFile.Get('sm_reco_smirnov_ET_'+str(smir_mass))
smirnovGraph_phi=smirnovFile.Get('sm_reco_smirnov_phi_'+str(smir_mass))
smirnovGraph_xtrans=smirnovFile.Get('sm_reco_smirnov_Xtrans_'+str(smir_mass))
smirnovGraph_ytrans=smirnovFile.Get('sm_reco_smirnov_Ytrans_'+str(smir_mass))


recoEntries=recoTree.GetEntries()
#recoEntries=10000
smEntries=smTree.GetEntries()
#smEntries=10000

def getPhiWRTAxis(vect,axis):
    phi=vect.Phi()-axis.Phi()
    while phi>math.pi:
        phi-=2*math.pi
    while phi<-math.pi:
        phi+=2*math.pi
    return phi

tv2_Tau1=TVector2()
tv2_Tau2=TVector2()
tv2_diTau=TVector2()
tv2_MET=TVector2()

tv2_Yax=TVector2()
tv2_Xax=TVector2()

tv2_Par=TVector2()
tv2_Perp=TVector2()

Tau1_4vect=TLorentzVector()
Tau2_4vect=TLorentzVector()
MET_2vect=TVector2()

reco_met_et=TH1F('recoMET_et','',25,0.,100.)
reco_met_et.SetLineColor(kRed)
reco_met_et.SetFillStyle(4000)

sm_met_et=TH1F('smMET_et','',25,0.,100.)
sm_met_et.SetLineColor(kBlue)
sm_met_et.SetFillStyle(4000)

truth_met_et=TH1F('truthMET_et','',25,0.,100.)
truth_met_et.SetLineColor(kGreen)
truth_met_et.SetFillStyle(4000)

smirnov_met_et=TH1F('smirnovMET_et','',25,0.,100.)
smirnov_met_et.SetLineColor(kTeal)
smirnov_met_et.SetFillStyle(4000)

reco_met_phi_centrality=TH1F('reco_met_phi_centrality','',50,-1.45,1.45)
reco_met_phi_centrality.SetLineColor(kRed)
reco_met_phi_centrality.SetFillStyle(4000)

sm_met_phi_centrality=TH1F('sm_met_phi_centrality','',50,-1.45,1.45)
sm_met_phi_centrality.SetLineColor(kBlue)
sm_met_phi_centrality.SetFillStyle(4000)

truth_met_phi_centrality=TH1F('truth_met_phi_centrality','',50,-1.45,1.45)
truth_met_phi_centrality.SetLineColor(kGreen)
truth_met_phi_centrality.SetFillStyle(4000)

smirnov_met_phi_centrality=TH1F('smirnov_met_phi_centrality','',50,-1.45,1.45)
smirnov_met_phi_centrality.SetLineColor(kTeal)
smirnov_met_phi_centrality.SetFillStyle(4000)


reco_met_et_cuts=TH1F('recoMET_et_cuts','',25,0.,100.)
reco_met_et_cuts.SetLineColor(kRed)
reco_met_et_cuts.SetFillStyle(4000)

sm_met_et_cuts=TH1F('smMET_et_cuts','',25,0.,100.)
sm_met_et_cuts.SetLineColor(kBlue)
sm_met_et_cuts.SetFillStyle(4000)

truth_met_et_cuts=TH1F('truthMET_et_cuts','',25,0.,100.)
truth_met_et_cuts.SetLineColor(kGreen)
truth_met_et_cuts.SetFillStyle(4000)

smirnov_met_et_cuts=TH1F('smirnovMET_et_cuts','',25,0.,100.)
smirnov_met_et_cuts.SetLineColor(kTeal)
smirnov_met_et_cuts.SetFillStyle(4000)

reco_met_phi_centrality_cuts=TH1F('reco_met_phi_centrality_cuts','',50,-1.45,1.45)
reco_met_phi_centrality_cuts.SetLineColor(kRed)
reco_met_phi_centrality_cuts.SetFillStyle(4000)

sm_met_phi_centrality_cuts=TH1F('sm_met_phi_centrality_cuts','',50,-1.45,1.45)
sm_met_phi_centrality_cuts.SetLineColor(kBlue)
sm_met_phi_centrality_cuts.SetFillStyle(4000)

truth_met_phi_centrality_cuts=TH1F('truth_met_phi_centrality_cuts','',50,-1.45,1.45)
truth_met_phi_centrality_cuts.SetLineColor(kGreen)
truth_met_phi_centrality_cuts.SetFillStyle(4000)

smirnov_met_phi_centrality_cuts=TH1F('smirnov_met_phi_centrality_cuts','',50,-1.45,1.45)
smirnov_met_phi_centrality_cuts.SetLineColor(kTeal)
smirnov_met_phi_centrality_cuts.SetFillStyle(4000)

def passedTauCuts(pt,eta,ntrack):
    return pt>20000 and (abs(eta)<1.37 or 1.52<abs(eta)<2.5) and (ntrack==1 or ntrack==3)

def passedPreselection(v):
    return v['lep1_pt'][4]>35000. and v['lep2_pt'][4]>25000. and 0.8<v['dR_lep_lep'][4]<2.6 and (v['met_phi_centrality'][4]>1. or min(v['dphi_lep1_met'][4],v['dphi_lep2_met'][4])<0.4*math.pi) and v['met_et'][4]>20000.
    #return v['lep1_pt'][4]>35000. and v['lep2_pt'][4]>25000. and (v['met_phi_centrality'][4]>1. or min(v['dphi_lep1_met'][4],v['dphi_lep2_met'][4])<0.4*math.pi) and v['met_et'][4]>20000.

def getMetPhiCentrality(Tau1_phi,Tau2_phi,MET_phi):
    A=math.sin(MET_phi-Tau1_phi)/math.sin(Tau2_phi-Tau1_phi)
    B=math.sin(Tau2_phi-MET_phi)/math.sin(Tau2_phi-Tau1_phi)
    return (A+B)/math.sqrt(A**2+B**2)

def deltaPhi(phi1,phi2):
    dphi=abs(phi1-phi2)
    while dphi>math.pi:
        dphi=dphi-2*math.pi
    return abs(dphi)

def evalVariable(var_name,Tau1,Tau2,met_px,met_py):
    #When adding new variables, they must be added to this function
    if var_name=='lep1_pt':
        return Tau1.pt
    if var_name=='lep1_eta':
        return Tau1.eta
    if var_name=='lep2_pt':
        return Tau2.pt
    if var_name=='lep2_eta':
        return Tau2.eta
    if var_name=='met_et':
        return math.sqrt(met_px**2+met_py**2)
    if var_name=='transverse_mass_lep1_lep2':
        return math.sqrt(2*Tau1.pt*Tau2.pt*(1.-math.cos(deltaPhi(Tau1.phi,Tau2.phi))))
    if var_name=='transverse_mass_lep1_met':
        return math.sqrt(2*Tau1.pt*math.sqrt(met_px**2+met_py**2)*(1.-math.cos(deltaPhi(Tau1.phi,math.atan2(met_py,met_px)))))   
    if var_name=='transverse_mass_lep2_met':
        return math.sqrt(2*Tau2.pt*math.sqrt(met_px**2+met_py**2)*(1.-math.cos(deltaPhi(Tau2.phi,math.atan2(met_py,met_px)))))
    if var_name=='dphi_lep1_met':
        return deltaPhi(Tau1.phi,math.atan2(met_py,met_px))
    if var_name=='dphi_lep2_met':
        return deltaPhi(Tau2.phi,math.atan2(met_py,met_px))
    if var_name=='dphi_lep_lep':
        return deltaPhi(Tau1.phi,Tau2.phi)
    if var_name=='deta_lep_lep':
        return abs(Tau1.eta-Tau2.eta)
    if var_name=='dR_lep_lep':
        return math.sqrt((Tau1.eta-Tau2.eta)**2+deltaPhi(Tau1.phi,Tau2.phi)**2)
    if var_name=='ptsum_lep1_lep2_met':
        return Tau1.pt+Tau2.pt+math.sqrt(met_px**2+met_py**2)
    if var_name=='ptsum_lep1_lep2':
        return Tau1.pt+Tau2.pt
    if var_name=='pttot_lep1_lep2_met':
        return math.sqrt((Tau1.px+Tau2.px+met_px)**2+(Tau1.py+Tau2.py+met_py)**2)/(Tau1.pt+Tau2.pt+math.sqrt(met_px**2+met_py**2))
    if var_name=='pttot_lep1_lep2':
        return math.sqrt((Tau1.px+Tau2.px)**2+(Tau1.py+Tau2.py)**2)/(Tau1.pt+Tau2.pt)
    if var_name=='ptdiff_lep1_lep2':
        return math.sqrt((Tau1.px-Tau2.px)**2+(Tau1.py-Tau2.py)**2)/(Tau1.pt+Tau2.pt)
    if var_name=='met_phi_centrality':
        return getMetPhiCentrality(Tau1.phi,Tau2.phi,math.atan2(met_py,met_px))
    if var_name=='collinear_mass':
        return collinearmass.mass(Tau1,Tau2,met_px,met_py)[1]
    if var_name=='resonance_pt':
        return TVector2(Tau1.px+Tau2.px+met_px,Tau1.py+Tau2.py+met_py).Mod()
    print "Error, unknown variable name. Variable must be added to evalVariable function."
    return 0

def testCentrality(Tau1,Tau2,met_px,met_py):
    phi1=Tau1.phi
    phi2=Tau2.phi
    fact=1./math.sin(phi2-phi1)
    vect=numpy.matrix([[met_px],[met_py]])
    F=numpy.matrix([[fact*math.sin(phi2),-fact*math.cos(phi2)],[-fact*math.sin(phi1),fact*math.cos(phi1)]])
    vectp=F*vect
    #do transformation on vectp
    Fp=numpy.matrix([[math.cos(phi1),math.cos(phi2)],[math.sin(phi1),math.sin(phi2)]])
    return Fp*vectp

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


print recoEntries
for i in xrange(recoEntries):
    if i%10000==0:
    	print i
    ientry=recoTree.LoadTree(i)
    if ientry<0:
   	break
    nb=recoTree.GetEntry(i)
    if nb<=0:
    	continue
    Tau1_numTrack=recoTree.tau1_numTrack
    Tau2_numTrack=recoTree.tau2_numTrack
    if Tau1_numTrack==1:
    	Tau1_4vect.SetPtEtaPhiM(recoTree.tau1_pt,recoTree.tau1_eta,recoTree.tau1_phi,800.)
    elif Tau1_numTrack==3:
        Tau1_4vect.SetPtEtaPhiM(recoTree.tau1_pt,recoTree.tau1_eta,recoTree.tau1_phi,1200.)
    if Tau2_numTrack==1:
    	Tau2_4vect.SetPtEtaPhiM(recoTree.tau2_pt,recoTree.tau2_eta,recoTree.tau2_phi,800.)
    elif Tau2_numTrack==3:
    	Tau2_4vect.SetPtEtaPhiM(recoTree.tau2_pt,recoTree.tau2_eta,recoTree.tau2_phi,1200.)
    Tau1=tau.Tau(Tau1_4vect,Tau1_numTrack)
    Tau2=tau.Tau(Tau2_4vect,Tau2_numTrack)
    MET_2vect.SetMagPhi(recoTree.MET_et,recoTree.MET_phi)
    testCentrality(Tau1,Tau2,MET_2vect.Px(),MET_2vect.Py())
    for k,v in variables.iteritems():
    	variables[k][4]=evalVariable(k,Tau1,Tau2,MET_2vect.Px(),MET_2vect.Py())
    if passedTauCuts(recoTree.tau1_pt,recoTree.tau1_eta,Tau1_numTrack) and passedTauCuts(recoTree.tau2_pt,recoTree.tau2_eta,Tau2_numTrack) and passedPreselection(variables):
        reco_met_et_cuts.Fill(variables['met_et'][4]/1000.)
        reco_met_phi_centrality_cuts.Fill(variables['met_phi_centrality'][4])
    reco_met_et.Fill(variables['met_et'][4]/1000.)
    reco_met_phi_centrality.Fill(variables['met_phi_centrality'][4])

print smEntries
for i in xrange(smEntries):
    if i%10000==0:
    	print i
    ientry=smTree.LoadTree(i)
    if ientry<0:
   	break
    nb=smTree.GetEntry(i)
    if nb<=0:
    	continue
    #Truth
    variables['lep1_pt'][4] = smTree.lep1_pt
    variables['lep1_eta'][4] = smTree.lep1_eta
    variables['lep2_pt'][4] = smTree.lep2_pt
    variables['lep2_eta'][4] = smTree.lep2_eta
    variables['met_et'][4] = smTree.met_et
    variables['transverse_mass_lep1_lep2'][4] = smTree.transverse_mass_lep1_lep2
    variables['transverse_mass_lep1_met'][4] = smTree.transverse_mass_lep1_met
    variables['transverse_mass_lep2_met'][4] = smTree.transverse_mass_lep2_met
    variables['dphi_lep1_met'][4] = smTree.dphi_lep1_met
    variables['dphi_lep2_met'][4] = smTree.dphi_lep2_met
    variables['dphi_lep_lep'][4] = smTree.dphi_lep_lep
    variables['deta_lep_lep'][4] = smTree.deta_lep_lep
    variables['dR_lep_lep'][4] = smTree.dR_lep_lep
    variables['ptsum_lep1_lep2_met'][4] = smTree.ptsum_lep1_lep2_met
    variables['ptsum_lep1_lep2'][4] = smTree.ptsum_lep1_lep2
    variables['pttot_lep1_lep2_met'][4] = smTree.pttot_lep1_lep2_met
    variables['pttot_lep1_lep2'][4] = smTree.pttot_lep1_lep2
    variables['ptdiff_lep1_lep2'][4] = smTree.ptdiff_lep1_lep2
    variables['met_phi_centrality'][4] = smTree.met_phi_centrality
    variables['collinear_mass'][4] = -1.

    if passedTauCuts(variables['lep1_pt'][4],variables['lep1_eta'][4],1) and passedTauCuts(variables['lep2_pt'][4],variables['lep2_eta'][4],1) and passedPreselection(variables):
    	truth_met_et_cuts.Fill(variables['met_et'][4]/1000.)
    	truth_met_phi_centrality_cuts.Fill(variables['met_phi_centrality'][4])
    truth_met_et.Fill(variables['met_et'][4]/1000.)
    truth_met_phi_centrality.Fill(variables['met_phi_centrality'][4])

    #Smeared
    
    variables['lep1_pt'][4] = smTree.lep1_pt_sm
    variables['lep1_eta'][4] = smTree.lep1_eta_sm
    variables['lep2_pt'][4] = smTree.lep2_pt_sm
    variables['lep2_eta'][4] = smTree.lep2_eta_sm
    variables['met_et'][4] = smTree.met_et_sm
    variables['transverse_mass_lep1_lep2'][4] = smTree.transverse_mass_lep1_lep2_sm
    variables['transverse_mass_lep1_met'][4] = smTree.transverse_mass_lep1_met_sm
    variables['transverse_mass_lep2_met'][4] = smTree.transverse_mass_lep2_met_sm
    variables['dphi_lep1_met'][4] = smTree.dphi_lep1_met_sm
    variables['dphi_lep2_met'][4] = smTree.dphi_lep2_met_sm
    variables['dphi_lep_lep'][4] = smTree.dphi_lep_lep_sm
    variables['deta_lep_lep'][4] = smTree.deta_lep_lep_sm
    variables['dR_lep_lep'][4] = smTree.dR_lep_lep_sm
    variables['ptsum_lep1_lep2_met'][4] =smTree.ptsum_lep1_lep2_met_sm
    variables['ptsum_lep1_lep2'][4] = smTree.ptsum_lep1_lep2_sm
    variables['pttot_lep1_lep2_met'][4] = smTree.pttot_lep1_lep2_met_sm
    variables['pttot_lep1_lep2'][4] = smTree.pttot_lep1_lep2_sm
    variables['ptdiff_lep1_lep2'][4] = smTree.ptdiff_lep1_lep2_sm
    variables['met_phi_centrality'][4] = smTree.met_phi_centrality_sm
    variables['collinear_mass'][4] = smTree.collinear_mass_sm
    if passedTauCuts(variables['lep1_pt'][4],variables['lep1_eta'][4],1) and passedTauCuts(variables['lep2_pt'][4],variables['lep2_eta'][4],1) and passedPreselection(variables):
    	sm_met_et_cuts.Fill(variables['met_et'][4]/1000.)
    	sm_met_phi_centrality_cuts.Fill(variables['met_phi_centrality'][4])
    sm_met_et.Fill(variables['met_et'][4]/1000.)
    sm_met_phi_centrality.Fill(variables['met_phi_centrality'][4])

    #Smirnov
    Tau1_numTrack=1
    Tau2_numTrack=1
    if Tau1_numTrack==1:
    	Tau1_4vect.SetPtEtaPhiM(smTree.lep1_pt_sm,smTree.lep1_eta_sm,smTree.lep1_phi_sm,800.)
    elif Tau1_numTrack==3:
        Tau1_4vect.SetPtEtaPhiM(smTree.lep1_pt_sm,smTree.lep1_eta_sm,smTree.lep1_phi_sm,1200.)
    if Tau2_numTrack==1:
    	Tau2_4vect.SetPtEtaPhiM(smTree.lep2_pt_sm,smTree.lep2_eta_sm,smTree.lep2_phi_sm,800.)
    elif Tau2_numTrack==3:
    	Tau2_4vect.SetPtEtaPhiM(smTree.lep2_pt_sm,smTree.lep2_eta_sm,smTree.lep2_phi_sm,1200.)
    Tau1=tau.Tau(Tau1_4vect,Tau1_numTrack)
    Tau2=tau.Tau(Tau2_4vect,Tau2_numTrack)
    tv2_Tau1.SetMagPhi(smTree.lep1_pt_sm,smTree.lep1_phi_sm)
    tv2_Tau2.SetMagPhi(smTree.lep2_pt_sm,smTree.lep2_phi_sm)
    tv2_diTau=tv2_Tau1+tv2_Tau2
    
    tv2_Yax.SetMagPhi(1.,tv2_diTau.Phi())
    tv2_Xax=(tv2_Tau1-tv2_Tau1.Proj(tv2_diTau)).Unit()

    tv2_MET.SetMagPhi(smTree.met_et_sm,smTree.met_phi_sm)
    tv2_Par=tv2_MET.Proj(tv2_Yax)
    tv2_Perp=tv2_MET.Proj(tv2_Xax)
    
    newpar=smirnovGraph_par.Eval(tv2_Par*tv2_Yax/1000.)*1000.
    newperp=smirnovGraph_perp.Eval(tv2_Perp*tv2_Xax/1000.)*1000.
    newphi=math.atan2(newpar,newperp)+tv2_Xax.Phi()
    newmag=math.sqrt(newpar**2+newperp**2)
    
    phi1=tv2_Tau1.Phi()
    phi2=tv2_Tau2.Phi()
    factor=1./math.sin(phi2-phi1)
    vect=numpy.matrix([[tv2_MET.Px()],[tv2_MET.Py()]])
    M=numpy.matrix([[factor*math.sin(phi2),-factor*math.cos(phi2)],[-factor*math.sin(phi1),factor*math.cos(phi1)]])
    vectp=M*vect
    Minv=numpy.matrix([[math.cos(phi1),math.cos(phi2)],[math.sin(phi1),math.sin(phi2)]])
    vectp_trans=numpy.matrix([[smirnovGraph_xtrans.Eval(vectp[0]/1000.)],[smirnovGraph_ytrans.Eval(vectp[1]/1000.)]])
    vect_trans=Minv*vectp_trans
    mag_trans=math.sqrt(vect_trans[0]**2+vect_trans[1]**2)
    phi_trans=math.atan2(vect_trans[1],vect_trans[0])
    #print 'met_phi', smirnovGraph_et.Eval(tv2_MET.Mod()/1000.)*1000., smirnovGraph_phi.Eval(getPhiWRTAxis(tv2_MET,tv2_Yax))+tv2_Yax.Phi()
    #print 'Xtrans_Ytrans', mag_trans*1000.,phi_trans
    #print 'par_perp',newmag,newphi

    if transform_string=='Xtrans_Ytrans':
        MET_2vect.SetMagPhi(mag_trans*1000.,phi_trans)
    elif transform_string=='met_phi':
        MET_2vect.SetMagPhi(smirnovGraph_et.Eval(tv2_MET.Mod()/1000.)*1000.,smirnovGraph_phi.Eval(getPhiWRTAxis(tv2_MET,tv2_Yax))+tv2_Yax.Phi())
    elif transform_string=='par_perp':
        MET_2vect.SetMagPhi(newmag,newphi)
    for k,v in variables.iteritems():
        if 'met' in k:
            variables[k][4]=evalVariable(k,Tau1,Tau2,MET_2vect.Px(),MET_2vect.Py())
    if passedTauCuts(variables['lep1_pt'][4],variables['lep1_eta'][4],1) and passedTauCuts(variables['lep2_pt'][4],variables['lep2_eta'][4],1) and passedPreselection(variables):
    	smirnov_met_et_cuts.Fill(variables['met_et'][4]/1000.)
    	smirnov_met_phi_centrality_cuts.Fill(variables['met_phi_centrality'][4])
    #print ''
    smirnov_met_et.Fill(variables['met_et'][4]/1000.)
    smirnov_met_phi_centrality.Fill(variables['met_phi_centrality'][4])

reco_met_et.Scale(1/reco_met_et.GetEntries())
sm_met_et.Scale(1/sm_met_et.GetEntries())
truth_met_et.Scale(1/truth_met_et.GetEntries())
smirnov_met_et.Scale(1/smirnov_met_et.GetEntries())

legend=TLegend(0.6,0.7,0.8,0.9)
legend.AddEntry(reco_met_et,'Reco')
legend.AddEntry(sm_met_et,'Smeared')
legend.AddEntry(smirnov_met_et,'Smirnov')
legend.AddEntry(truth_met_et,'Truth')

met_et_stack=THStack()
met_et_stack.Add(reco_met_et)
met_et_stack.Add(sm_met_et)
met_et_stack.Add(truth_met_et)
met_et_stack.Add(smirnov_met_et)

canvas=TCanvas()
met_et_stack.Draw('nostack')
legend.Draw('same')
met_et_stack.GetXaxis().SetTitle('MET_et (GeV)')
canvas.SaveAs('new_met/met_et_'+transform_string+'.png')

reco_met_phi_centrality.Scale(1/reco_met_phi_centrality.GetEntries())
sm_met_phi_centrality.Scale(1/sm_met_phi_centrality.GetEntries())
truth_met_phi_centrality.Scale(1/truth_met_phi_centrality.GetEntries())
smirnov_met_phi_centrality.Scale(1/smirnov_met_phi_centrality.GetEntries())



met_phi_centrality_stack=THStack()
met_phi_centrality_stack.Add(reco_met_phi_centrality)
met_phi_centrality_stack.Add(sm_met_phi_centrality)
met_phi_centrality_stack.Add(truth_met_phi_centrality)
met_phi_centrality_stack.Add(smirnov_met_phi_centrality)

canvas.Clear()
met_phi_centrality_stack.Draw('nostack')
legend.Draw('same')
met_phi_centrality_stack.GetXaxis().SetTitle('MET_phi_centrality')
canvas.SaveAs('new_met/met_phi_centrality_'+transform_string+'.png')

reco_met_et_cuts.Scale(1/reco_met_et_cuts.GetEntries())
sm_met_et_cuts.Scale(1/sm_met_et_cuts.GetEntries())
truth_met_et_cuts.Scale(1/truth_met_et_cuts.GetEntries())
smirnov_met_et_cuts.Scale(1/smirnov_met_et_cuts.GetEntries())

met_et_stack_cuts=THStack()
met_et_stack_cuts.Add(reco_met_et_cuts)
met_et_stack_cuts.Add(sm_met_et_cuts)
met_et_stack_cuts.Add(truth_met_et_cuts)
met_et_stack_cuts.Add(smirnov_met_et_cuts)

canvas.Clear()
met_et_stack_cuts.Draw('nostack')
legend.Draw('same')
met_et_stack_cuts.GetXaxis().SetTitle('MET_et (GeV)')
canvas.SaveAs('new_met/met_et_cuts_'+transform_string+'.png')

reco_met_phi_centrality_cuts.Scale(1/reco_met_phi_centrality_cuts.GetEntries())
sm_met_phi_centrality_cuts.Scale(1/sm_met_phi_centrality_cuts.GetEntries())
truth_met_phi_centrality_cuts.Scale(1/truth_met_phi_centrality_cuts.GetEntries())
smirnov_met_phi_centrality_cuts.Scale(1/smirnov_met_phi_centrality_cuts.GetEntries())

met_phi_centrality_stack_cuts=THStack()
met_phi_centrality_stack_cuts.Add(reco_met_phi_centrality_cuts)
met_phi_centrality_stack_cuts.Add(sm_met_phi_centrality_cuts)
met_phi_centrality_stack_cuts.Add(truth_met_phi_centrality_cuts)
met_phi_centrality_stack_cuts.Add(smirnov_met_phi_centrality_cuts)



canvas.Clear()
met_phi_centrality_stack_cuts.Draw('nostack')
legend.Draw('same')
met_phi_centrality_stack_cuts.GetXaxis().SetTitle('MET_phi_centrality')
canvas.SaveAs('new_met/met_phi_centrality_cuts_'+transform_string+'.png')
