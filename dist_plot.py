import ROOT
import os

ROOT.gROOT.SetBatch(True)

savedFileFormats = ['.pdf']#['.gif', '.jpg', '.pdf']
outputFolderName = 'output'

#ROOT.gROOT.ProcessLine(".x style.C")
#ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetOptStat(1111111)
ROOT.gStyle.SetOptTitle(0)

ROOT.gStyle.SetPadGridX(ROOT.kTRUE);
ROOT.gStyle.SetPadGridY(ROOT.kTRUE);


ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.15)

ROOT.gStyle.SetTickLength(0.03, "XYZ");
ROOT.gStyle.SetNdivisions(510, "XYZ");
ROOT.gStyle.SetPadTickX(1);  # To get tick marks on the opposite side of the frame
ROOT.gStyle.SetPadTickY(1);

ROOT.gStyle.SetLabelColor(1, "XYZ");
ROOT.gStyle.SetLabelFont(42, "XYZ");
ROOT.gStyle.SetLabelOffset(0.007, "XYZ");
ROOT.gStyle.SetLabelSize(0.045); 
ROOT.gStyle.SetTitleSize(0.06); 
ROOT.gStyle.SetTitleOffset(1);

def ScaleHist(hist) :
    integral = hist.Integral()
    if integral != 0. :
        hist.Scale(1. / integral)


def GetCopy(suffix = 'QCD', filename = '', histname = '') :
    afile = ROOT.TFile(filename)
    print 'Content of file'
    afile.ls()
    hist  = afile.Get('demo//' + histname)
    tmp   = hist.Clone(hist.GetName() + suffix)
    print tmp
    print tmp.GetZaxis()

    return tmp

def ProjectOutZ(hist) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
       
    histproj = hist.Project3D("yx"  )
    histproj.Draw()

    filename = 'ProjectionZ' + hist.GetName()
    
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//' + filename + fileFormat)




def DistancesBySubDetSeperate(QCDfilename, ELEfilename, PIONfilename, histname, ptrange = (30., 40.)) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
#    QCD = GetCopy('QCD', QCDfilename, histname) 
#    ELE = GetCopy('ELE', ELEfilename, histname)
    ROOT.TH1.AddDirectory(ROOT.kFALSE) 
    QCDfile = ROOT.TFile(QCDfilename)
    QCDhist  = QCDfile.Get('demo//' + histname)
    QCD   = QCDhist.Clone(QCDhist.GetName() + 'QCD')

    ELEfile = ROOT.TFile(ELEfilename)
    #print 'Content of file'
    #afile.cd('demo')
    #afile.ls()
    ELEhist  = ELEfile.Get('demo//' + histname)
    ELE   = ELEhist.Clone(ELEhist.GetName() + 'ELE')
 
    PIONfile = ROOT.TFile(PIONfilename)
    PIONhist  = PIONfile.Get('demo//' + histname)
    PION   = PIONhist.Clone(PIONhist.GetName() + 'PION')
 

    ELEaxis = ELE.GetZaxis()
    QCDaxis = QCD.GetZaxis()
    PIONaxis = PION.GetZaxis(); 
    
    nameSuffix = '_from_' + str(ptrange[0]) + '_to_' + str(ptrange[1])
    
    QCD.Draw()
    QCDaxis.SetRangeUser(ptrange[0], ptrange[1])
    QCDproj = QCD.Project3D("x" + "QCD" + nameSuffix)
    #axis1.Unzoom()
    ELEaxis.SetRangeUser(ptrange[0], ptrange[1])
    ELEproj = ELE.Project3D("x" + "Signal" + nameSuffix)
    ELEproj.SetLineColor(ROOT.kRed)
    #axis2.Unzoom()

    PIONaxis.SetRangeUser(ptrange[0], ptrange[1])
    PIONproj = PION.Project3D("x" + "pion" + nameSuffix)
    PIONproj.SetLineColor(ROOT.kGreen)
 

    ScaleHist(PIONproj)
    ScaleHist(QCDproj)
    ScaleHist(ELEproj)

    stack = ROOT.THStack("","")

    stack.Add(QCDproj)
    stack.Add(ELEproj)
    stack.Add(PIONproj)
    stack.Draw()
    stack.GetXaxis().SetTitle(ELE.GetXaxis().GetTitle())
    
    stack.Draw("")
    #stack.GetXaxis().SetRangeUser(-0.5, 0.5)
    stack.Draw("NOSTACK")
    
    legend = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
#legSetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
    #histo1->SetLineColor(2);  //histo1 in red
        #histo2->SetLineColor(1);  //histo2 in black
    legend.SetBorderSize(0); # //no border for legend                                                            
    legend.SetFillColor(0);
    legend.AddEntry(QCDproj,"QCD","L");
    legend.AddEntry(ELEproj, "true electron", "L")
    legend.AddEntry(PIONproj, "pion", "L")
    legend.Draw("SAME") 
    
    filename = 'SIGvsBGD' + ELE.GetName() + nameSuffix
    
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//' + filename + fileFormat)



file = ROOT.TFile("output//qcd_hist.root")
file.cd("demo")
file.ls()


def GetCopy(suffix = 'QCD', filename = '', histname = '') :
    afile = ROOT.TFile(filename)
    print 'Content of file'
    afile.ls()
    hist  = afile.Get('demo//' + histname)
    tmp   = hist.Clone(hist.GetName() + suffix)
    print tmp
    print tmp.GetZaxis()

    return tmp


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__PIB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TID', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TIB', ptrange = (0., 100.))
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TOB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__PIE', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TEC', ptrange = (0., 100.)) 


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__PIB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TID', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TIB', ptrange = (0., 100.))
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TOB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__PIE', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TEC', ptrange = (0., 100.)) 


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__PIB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TID', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TIB', ptrange = (0., 100.))
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TOB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__PIE', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TEC', ptrange = (0., 100.)) 





file2 = ROOT.TFile("output//ele_hist.root")

ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__PIB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TID'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TIB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TOB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TEC'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__PIE'))

def DistancesBySubDet1D(QCDfilename, ELEfilename, PIONfilename, histname, ptrange = (30., 40.)) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    ROOT.TH1.AddDirectory(ROOT.kFALSE) 
    QCDfile = ROOT.TFile(QCDfilename)
    QCDhist  = QCDfile.Get('demo//' + histname)
    QCD   = QCDhist.Clone(QCDhist.GetName() + 'QCD')

    ELEfile = ROOT.TFile(ELEfilename)
    ELEhist  = ELEfile.Get('demo//' + histname)
    ELE   = ELEhist.Clone(ELEhist.GetName() + 'ELE')
 
    PIONfile = ROOT.TFile(PIONfilename)
    PIONhist  = PIONfile.Get('demo//' + histname)
    PION   = PIONhist.Clone(PIONhist.GetName() + 'PION')
 

    

    ScaleHist(PION)
    ScaleHist(QCD)
    ScaleHist(ELE)

    ELE.SetLineColor(ROOT.kRed)
    QCD.SetLineColor(ROOT.kBlue)
    PION.SetLineColor(ROOT.kGreen)

    stack = ROOT.THStack("","")

    stack.Add(QCD)
    stack.Add(ELE)
    stack.Add(PION)
    stack.Draw()
    stack.GetXaxis().SetTitle(ELE.GetXaxis().GetTitle())
    
    stack.Draw("")
    #stack.GetXaxis().SetRangeUser(-0.5, 0.5)
    stack.Draw("NOSTACK")
    
    legend = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
#legSetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
    #histo1->SetLineColor(2);  //histo1 in red
        #histo2->SetLineColor(1);  //histo2 in black
    legend.SetBorderSize(0); # //no border for legend                                                            
    legend.SetFillColor(0);
    legend.AddEntry(QCD,"QCD","L");
    legend.AddEntry(ELE, "true electron", "L")
    legend.AddEntry(PION, "pion", "L")
    legend.Draw("SAME") 
    
    filename = 'SIGvsBGD' + ELE.GetName()
    
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//' + filename + fileFormat)


DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__PIB', ptrange = (0., 100.)) 
DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TID', ptrange = (0., 100.)) 
DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TIB', ptrange = (0., 100.))
DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TOB', ptrange = (0., 100.)) 
DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__PIE', ptrange = (0., 100.)) 
DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TEC', ptrange = (0., 100.)) 










file = ROOT.TFile("output//qcd_hist.root")
file.cd("demo")
file.ls()


def GetCopy(suffix = 'QCD', filename = '', histname = '') :
    afile = ROOT.TFile(filename)
    print 'Content of file'
    afile.ls()
    hist  = afile.Get('demo//' + histname)
    tmp   = hist.Clone(hist.GetName() + suffix)
    print tmp
    print tmp.GetZaxis()

    return tmp



qcdtmp = file.Get("demo//h_SignedTransversalDist_Eta_SubDet__GSF")
print "qcdtmp ", qcdtmp
qcd = qcdtmp.Clone(qcdtmp.GetName() + "QCD")
print "b4 close ", qcd
print "qcd name", qcd.GetName()

