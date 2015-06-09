from ROOT import *
import numpy

masses=[100,105,110,115,120,125,130,135,140,145,150]

files=[TFile('smirnov_curves/smirnov_'+str(mass)+'.root') for mass in masses]

graphs=[ifile.Get('sm_reco_smirnov') for ifile in files]

points=[[ipoint for ipoint in range(igraph.GetN())] for igraph in graphs]
npoints=sum([igraph.GetN() for igraph in graphs])
xpoints=[]
ypoints=[]
zpoints=[]
for i,igraph in enumerate(graphs):
    xlist=igraph.GetX()
    ylist=igraph.GetY()
    for j in range(igraph.GetN()):
        xpoints.append(float(xlist[j]))
        ypoints.append(float(masses[i]))
        zpoints.append(float(ylist[j]))

graph2d=TGraph2D(npoints,numpy.asarray(xpoints),numpy.asarray(ypoints),numpy.asarray(zpoints))
graph2d.SetName('SmirnovCurve')
outfile=TFile('Smirnov.root','Recreate')
outfile.cd()
graph2d.Write()
outfile.Close()
