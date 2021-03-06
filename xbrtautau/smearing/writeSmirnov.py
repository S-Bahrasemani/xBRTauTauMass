#import BRTmass
import tau
from ROOT import *
import math
import collinearmass
import smirnov
import sys
import numpy

mass=int(sys.argv[1])
recoTree=TChain('PowPyth8_AU2CT10_ggH'+str(mass)+'_tautauhh_mc12a')
recoTree.Add('/cluster/data11/endw/ntuples/prod_v29/hhskim/hhskim.root')
smTree=TChain('Tree')
smTree.Add('/cluster/data04/mquennev/higgs/rootfiles/met/final_smearing/Hmass'+str(mass)+'.root')


recoEntries=recoTree.GetEntries()
#recoEntries=100
smEntries=smTree.GetEntries()
#smEntries=100

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

recoPar=TH1F('recoPar','',100,-150,150)
recoPerp=TH1F('recoPerp','',100,-150,150)
recoET=TH1F('recoET','',100,20,150)
recoPhi=TH1F('recoPhi','',100,0.,2*math.pi)
recoXtrans=TH1F('recoXtrans','',100,-150,150)
recoYtrans=TH1F('recoYtrans','',100,-150,150)
recoPar.SetLineColor(kRed)
recoPerp.SetLineColor(kRed)
recoET.SetLineColor(kRed)
recoPhi.SetLineColor(kRed)
recoXtrans.SetLineColor(kRed)
recoYtrans.SetLineColor(kRed)
recoPar.SetFillStyle(4000)
recoPerp.SetFillStyle(4000)
recoET.SetFillStyle(4000)
recoPhi.SetFillStyle(4000)
recoXtrans.SetFillStyle(4000)
recoYtrans.SetFillStyle(4000)

smPar=TH1F('smPar','',100,-150,150)
smPerp=TH1F('smPerp','',100,-150,150)
smET=TH1F('smET','',100,20,150)
smPhi=TH1F('smPhi','',100,0.,2*math.pi)
smXtrans=TH1F('smXtrans','',100,-150,150)
smYtrans=TH1F('smYtrans','',100,-150,150)
smPar.SetLineColor(kBlue)
smPerp.SetLineColor(kBlue)
smET.SetLineColor(kBlue)
smPhi.SetLineColor(kBlue)
smXtrans.SetLineColor(kBlue)
smYtrans.SetLineColor(kBlue)
smPar.SetFillStyle(4000)
smPerp.SetFillStyle(4000)
smET.SetFillStyle(4000)
smPhi.SetFillStyle(4000)
smXtrans.SetFillStyle(4000)
smYtrans.SetFillStyle(4000)

truthPar=TH1F('truthPar','',100,-150,150)
truthPerp=TH1F('truthPerp','',100,-150,150)
truthET=TH1F('truthET','',100,20,150)
truthPhi=TH1F('truthPhi','',100,0.,2*math.pi)
truthXtrans=TH1F('truthXtrans','',100,-150,150)
truthYtrans=TH1F('truthYtrans','',100,-150,150)
truthPar.SetLineColor(kGreen)
truthPerp.SetLineColor(kGreen)
truthET.SetLineColor(kGreen)
truthPhi.SetLineColor(kGreen)
truthXtrans.SetLineColor(kGreen)
truthYtrans.SetLineColor(kGreen)
truthPar.SetFillStyle(4000)
truthPerp.SetFillStyle(4000)
truthET.SetFillStyle(4000)
truthPhi.SetFillStyle(4000)
truthXtrans.SetFillStyle(4000)
truthYtrans.SetFillStyle(4000)

def getPhiWRTAxis(vect,axis):
    phi=vect.Phi()-axis.Phi()
    while phi>math.pi:
        phi-=2*math.pi
    while phi<-math.pi:
        phi+=2*math.pi
    return phi

def passedBRTCuts(v):
    return v['lep1_pt'][4]>35000. and v['lep2_pt'][4]>25000. and v['met_et'][4]>20000. and abs(v['lep1_eta'][4])<2.5 and abs(v['lep2_eta'][4])<2.5

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

variables = {}
variables['lep1_pt']                   = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['lep1_eta']                  = [''   ,'F',-10.00,10.00,  0.,TBranch(), -2.5,2.5,   40]
variables['lep2_pt']                   = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['lep2_eta']                  = [''   ,'F',-10.00,10.00,  0.,TBranch(), -2.5,2.5,   40]
variables['met_et']                    = ['MeV','F',  0.00,9999999,0.,TBranch(),   0.00,200000., 25]
variables['dR_lep_lep']                = ['',   'F',  0.00,25.00,  0.,TBranch(),   0.00,3.15,   40]
variables['met_phi_centrality']        = ['',   'F', -1.45, 1.45,  0.,TBranch(),  -1.45, 1.45,   40]


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
    Tau1_4vect.SetPtEtaPhiM(recoTree.tau1_pt,recoTree.tau1_eta,recoTree.tau1_phi,0.)
    Tau2_4vect.SetPtEtaPhiM(recoTree.tau2_pt,recoTree.tau2_eta,recoTree.tau2_phi,0.)
    Tau1=tau.Tau(Tau1_4vect,1)
    Tau2=tau.Tau(Tau2_4vect,1)
    tv2_MET.SetMagPhi(recoTree.MET_et,recoTree.MET_phi)
    for k,v in variables.iteritems():
	variables[k][4]=evalVariable(k,Tau1,Tau2,tv2_MET.Px(),tv2_MET.Py())
    if not(passedBRTCuts(variables)):
	continue
    tv2_Tau1.SetMagPhi(recoTree.tau1_pt,recoTree.tau1_phi)
    tv2_Tau2.SetMagPhi(recoTree.tau2_pt,recoTree.tau2_phi)
    tv2_diTau=tv2_Tau1+tv2_Tau2

    tv2_Yax.SetMagPhi(1.,tv2_diTau.Phi())
    
    tv2_Xax=(tv2_Tau1-tv2_Tau1.Proj(tv2_diTau)).Unit()

    tv2_Par=tv2_MET.Proj(tv2_Yax)
    tv2_Perp=tv2_MET.Proj(tv2_Xax)

    phi1=tv2_Tau1.Phi()
    phi2=tv2_Tau2.Phi()
    factor=1./math.sin(phi2-phi1)
    vect=numpy.matrix([[tv2_MET.X()],[tv2_MET.Y()]])
    M=numpy.matrix([[factor*math.sin(phi2),-factor*math.cos(phi2)],[-factor*math.sin(phi1),factor*math.cos(phi1)]])
    vectp=M*vect

    recoPar.Fill(tv2_Par*tv2_Yax/1000.)
    recoPerp.Fill(tv2_Perp*tv2_Xax/1000.)
    recoET.Fill(tv2_MET.Mod()/1000.)
    recoPhi.Fill(getPhiWRTAxis(tv2_MET,tv2_Yax))
    recoXtrans.Fill(vectp[0]/1000.)
    recoYtrans.Fill(vectp[1]/1000.)

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

    Tau1_4vect.SetPtEtaPhiM(smTree.lep1_pt,smTree.lep1_eta,smTree.lep1_phi,0.)
    Tau2_4vect.SetPtEtaPhiM(smTree.lep2_pt,smTree.lep2_eta,smTree.lep2_phi,0.)
    Tau1=tau.Tau(Tau1_4vect,1)
    Tau2=tau.Tau(Tau2_4vect,1)
    tv2_MET.SetMagPhi(smTree.met_et,smTree.met_phi)
    for k,v in variables.iteritems():
	variables[k][4]=evalVariable(k,Tau1,Tau2,tv2_MET.Px(),tv2_MET.Py())
    if passedBRTCuts(variables):
    	tv2_Tau1.SetMagPhi(smTree.lep1_pt,smTree.lep1_phi)
    	tv2_Tau2.SetMagPhi(smTree.lep2_pt,smTree.lep2_phi)
    	tv2_diTau=tv2_Tau1+tv2_Tau2

    	tv2_Yax.SetMagPhi(1.,tv2_diTau.Phi())
    	tv2_Xax=(tv2_Tau1-tv2_Tau1.Proj(tv2_diTau)).Unit()

    	tv2_Par=tv2_MET.Proj(tv2_Yax)
    	tv2_Perp=tv2_MET.Proj(tv2_Xax)

    	phi1=tv2_Tau1.Phi()
    	phi2=tv2_Tau2.Phi()
    	factor=1./math.sin(phi2-phi1)
    	vect=numpy.matrix([[tv2_MET.X()],[tv2_MET.Y()]])
    	M=numpy.matrix([[factor*math.sin(phi2),-factor*math.cos(phi2)],[-factor*math.sin(phi1),factor*math.cos(phi1)]])
    	vectp=M*vect

    	truthPar.Fill(tv2_Par*tv2_Yax/1000.)
    	truthPerp.Fill(tv2_Perp*tv2_Xax/1000.)
    	truthET.Fill(tv2_MET.Mod()/1000.)
    	truthPhi.Fill(getPhiWRTAxis(tv2_MET,tv2_Yax))
    	truthXtrans.Fill(vectp[0]/1000.)
    	truthYtrans.Fill(vectp[1]/1000.)

    #Smeared
    Tau1_4vect.SetPtEtaPhiM(smTree.lep1_pt_sm,smTree.lep1_eta_sm,smTree.lep1_phi_sm,0.)
    Tau2_4vect.SetPtEtaPhiM(smTree.lep2_pt_sm,smTree.lep2_eta_sm,smTree.lep2_phi_sm,0.)
    Tau1=tau.Tau(Tau1_4vect,1)
    Tau2=tau.Tau(Tau2_4vect,1)
    tv2_MET.SetMagPhi(smTree.met_et_sm,smTree.met_phi_sm)
    for k,v in variables.iteritems():
	variables[k][4]=evalVariable(k,Tau1,Tau2,tv2_MET.Px(),tv2_MET.Py())
    if passedBRTCuts(variables):
    	tv2_Tau1.SetMagPhi(smTree.lep1_pt_sm,smTree.lep1_phi_sm)
    	tv2_Tau2.SetMagPhi(smTree.lep2_pt_sm,smTree.lep2_phi_sm)
    	tv2_diTau=tv2_Tau1+tv2_Tau2
    
    	tv2_Yax.SetMagPhi(1.,tv2_diTau.Phi())
    	tv2_Xax=(tv2_Tau1-tv2_Tau1.Proj(tv2_diTau)).Unit()

    	tv2_Par=tv2_MET.Proj(tv2_Yax)
    	tv2_Perp=tv2_MET.Proj(tv2_Xax)

    	phi1=tv2_Tau1.Phi()
    	phi2=tv2_Tau2.Phi()
    	factor=1./math.sin(phi2-phi1)
    	vect=numpy.matrix([[tv2_MET.X()],[tv2_MET.Y()]])
    	M=numpy.matrix([[factor*math.sin(phi2),-factor*math.cos(phi2)],[-factor*math.sin(phi1),factor*math.cos(phi1)]])
    	vectp=M*vect

    	smPar.Fill(tv2_Par*tv2_Yax/1000.)
    	smPerp.Fill(tv2_Perp*tv2_Xax/1000.)
    	smET.Fill(tv2_MET.Mod()/1000.)
   	smPhi.Fill(getPhiWRTAxis(tv2_MET,tv2_Yax))
    	smXtrans.Fill(vectp[0]/1000.)
    	smYtrans.Fill(vectp[1]/1000.)
print recoXtrans.Integral(),smXtrans.Integral()
outfile=TFile('smirnov_curves/smirnov_'+str(mass)+'.root','Recreate')
"""smirnovgraph=smirnov.Smirnov(smPar,recoPar)
smirnovgraph.SetName('sm_reco_smirnov_par_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(smPerp,recoPerp)
smirnovgraph.SetName('sm_reco_smirnov_perp_'+str(mass))
smirnovgraph.Write()"""
smirnovgraph=smirnov.Smirnov(smET,recoET)
smirnovgraph.SetName('sm_reco_smirnov_ET_'+str(mass))
smirnovgraph.Write()
"""
smirnovgraph=smirnov.Smirnov(smPhi,recoPhi)
smirnovgraph.SetName('sm_reco_smirnov_phi_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(smXtrans,recoXtrans)
smirnovgraph.SetName('sm_reco_smirnov_Xtrans_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(smYtrans,recoYtrans)
smirnovgraph.SetName('sm_reco_smirnov_Ytrans_'+str(mass))
smirnovgraph.Write()

smirnovgraph=smirnov.Smirnov(truthPar,recoPar)
smirnovgraph.SetName('truth_reco_smirnov_par_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(truthPerp,recoPerp)
smirnovgraph.SetName('truth_reco_smirnov_perp_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(truthET,recoET)
smirnovgraph.SetName('truth_reco_smirnov_ET_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(truthPhi,recoPhi)
smirnovgraph.SetName('truth_reco_smirnov_phi_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(truthXtrans,recoXtrans)
smirnovgraph.SetName('truth_reco_smirnov_Xtrans_'+str(mass))
smirnovgraph.Write()
smirnovgraph=smirnov.Smirnov(truthYtrans,recoYtrans)
smirnovgraph.SetName('truth_reco_smirnov_Ytrans_'+str(mass))
smirnovgraph.Write()
"""
outfile.Close()
recoXtrans.Scale(1/recoXtrans.Integral())
smXtrans.Scale(1/smXtrans.Integral())
truthXtrans.Scale(1/truthXtrans.Integral())
stack=THStack()
stack.Add(recoXtrans)
stack.Add(truthXtrans)
stack.Add(smXtrans)
canvas=TCanvas()
stack.Draw('nostack')
canvas.SaveAs('xtest.png')
