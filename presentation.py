import ROOT
import os

ROOT.gROOT.SetBatch(True)

savedFileFormats = ['.pdf']#['.gif', '.jpg', '.pdf']
outputFolderName = 'output'

#ROOT.gROOT.ProcessLine(".x style.C")
#ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetOptTitle(0)
#
#ROOT.gStyle.SetPadGridX(ROOT.kTRUE);
#ROOT.gStyle.SetPadGridY(ROOT.kTRUE);
#
#
#ROOT.gStyle.SetPadBottomMargin(0.13)
#ROOT.gStyle.SetPadLeftMargin(0.15)
#
#ROOT.gStyle.SetTickLength(0.03, "XYZ");
#ROOT.gStyle.SetNdivisions(510, "XYZ");
#ROOT.gStyle.SetPadTickX(1);  # To get tick marks on the opposite side of the frame
#ROOT.gStyle.SetPadTickY(1);
#
#ROOT.gStyle.SetLabelColor(1, "XYZ");
#ROOT.gStyle.SetLabelFont(42, "XYZ");
ROOT.gStyle.SetLabelOffset(0.007, "XYZ");
#ROOT.gStyle.SetLabelSize(0.045); 
#ROOT.gStyle.SetTitleSize(0.06); 
#ROOT.gStyle.SetTitleOffset(1);


def setTDRStyle() :
    tdrStyle = ROOT.TStyle("tdrStyle","Style for P-TDR");
    tdrStyle.SetHistMinimumZero(ROOT.kTRUE) #start y axis at 0
    tdrStyle.SetLabelOffset(0.7, "XYZ");

#    // For the Canvas:
    tdrStyle.SetCanvasBorderMode(0);
    tdrStyle.SetCanvasColor(ROOT.kWhite);
    tdrStyle.SetCanvasDefH(550)#; //Height of canvas
    tdrStyle.SetCanvasDefW(550)#; //Width of canvas
    tdrStyle.SetCanvasDefX(0)#;   //POsition on screen
    tdrStyle.SetCanvasDefY(0)#;

 #   // For the Pad:
    tdrStyle.SetPadBorderMode(0);
    #tdrStyle->SetPadBorderSize(Width_t size = 1);
    tdrStyle.SetPadColor(ROOT.kWhite);
    tdrStyle.SetPadGridX(False);
    tdrStyle.SetPadGridY(False);
    tdrStyle.SetGridColor(0);
    tdrStyle.SetGridStyle(3);
    tdrStyle.SetGridWidth(1);

  #  // For t. frame:
    tdrStyle.SetFrameBorderMode(0);
    tdrStyle.SetFrameBorderSize(1);
    tdrStyle.SetFrameFillColor(0);
    tdrStyle.SetFrameFillStyle(0);
    tdrStyle.SetFrameLineColor(1);
    tdrStyle.SetFrameLineStyle(1);
    tdrStyle.SetFrameLineWidth(1);

   # // For t. histo:
    tdrStyle.SetHistFillColor(0);
    tdrStyle.SetHistFillStyle(0);
    tdrStyle.SetHistLineColor(1);
    tdrStyle.SetHistLineStyle(0);
    tdrStyle.SetHistLineWidth(1);


setTDRStyle()
def SaveScatterplot(hist, subdetectorLabel = "", showCorrelation=False, showEntries = True) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 700 )   

    print hist

    hist.Draw()
    hist.GetYaxis().SetTitleOffset(1.2)
    #hist.SetHistMinimumZero(ROOT.kTRUE)
    box1 = ROOT.TPaveText(0.15,0.92,0.35,0.92, "NDC") #//NDC sets coords relative to pad
    box1.SetTextSize(0.04)
    box1.SetFillColor(0) #white background 
    box1.SetTextFont(42)
    box1.SetTextAlign(12)

    box2 = ROOT.TPaveText(0.60,0.85,0.85,0.85, "NDC") #//NDC sets coords relative to pad
    box2.SetTextSize(0.04)
    box2.SetFillColor(0) #white background 
    box2.SetTextFont(42)
    
    box2.SetTextAlign(12)

    box3 = ROOT.TPaveText(0.15,0.85,0.35,0.85, "NDC") #//NDC sets coords relative to pad
    box3.SetTextSize(0.04)
    box3.SetFillColor(0) #white background 
    box3.SetTextFont(42)
    box3.SetTextAlign(12)



    if subdetectorLabel is not "" :
        #sub = ROOT.TPaveText(0.15,0.75,0.35,0.85, "NDC") #//NDC sets coords relative to pad
        #sub.SetTextSize(0.04)
        #sub.SetFillColor(0) #white background 
        #sub.SetTextAlign(12)
        subtmp = box1.AddText("#bf{" + subdetectorLabel + "}")     
        box1.Draw("SAME")
    
    if showCorrelation is True :
        corrtmp = box3.AddText("#it{#rho = " + "{0:.2f}".format(hist.GetCorrelationFactor()) + "}")     
        box3.Draw("SAME")

    if showEntries is True :
        entrtmp = box2.AddText("#it{Entries: " + "{:.0f}".format(hist.GetEntries()) + "}")
        

    box2.Draw("SAME")
    filename = hist.GetName()
    
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//' + currSample + filename + fileFormat)

afile = ROOT.TFile("output//ele_hist.root")
afile.cd("demo")
afile.ls()
currSample = "ele_"

SaveScatterplot(afile.Get("demo//h_fbremMC_fbremSignificance__Central"), subdetectorLabel = 'central |#eta| < 0.9', showCorrelation = True)
SaveScatterplot(afile.Get("demo//h_fbremMC_UncertMeanPout__Central"), subdetectorLabel = 'central |#eta| < 0.9', showCorrelation = True)
SaveScatterplot(afile.Get("demo//h_fbremMC_UncertMeanPin__Central"), subdetectorLabel = 'central |#eta| < 0.9', showCorrelation = True)

SaveScatterplot(afile.Get("demo//h_fbremMC_fbremSignificance__Forward"), subdetectorLabel = 'forward |#eta| > 0.9', showCorrelation = True)
SaveScatterplot(afile.Get("demo//h_fbremMC_UncertMeanPout__Forward"), subdetectorLabel = 'forward |#eta| > 0.9', showCorrelation = True)
SaveScatterplot(afile.Get("demo//h_fbremMC_UncertMeanPin__Forward"), subdetectorLabel = 'forward |#eta| > 0.9', showCorrelation = True)

SaveScatterplot(afile.Get("demo//h_UncertMeanPin_UncertMeanPout__Forward"), subdetectorLabel = 'forward |#eta| > 0.9', showCorrelation = True)
SaveScatterplot(afile.Get("demo//h_UncertMeanPin_UncertMeanPout__Central"), subdetectorLabel = 'central |#eta| < 0.9', showCorrelation = True)

SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPin"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPinCov"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPinPDiff"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPin__5HITS"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPinCov__5HITS"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPinPDiff__5HITS"))


SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPout"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPoutCov"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPoutPDiff"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPout__5HITS"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPoutCov__5HITS"))
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPoutPDiff__5HITS"))


afile = ROOT.TFile("output//qcd_hist.root")
afile.cd("demo")
afile.ls()
currSample = "qcd_"


SaveScatterplot(afile.Get("demo//h_GsfElectronPt"))
SaveScatterplot(afile.Get("demo//h_GsfElectronEta"))#.SetHistMinimumZero(ROOT.kTRUE))

afile = ROOT.TFile("output//pion_hist.root")
afile.cd("demo")
afile.ls()
currSample = "pion_"
SaveScatterplot(afile.Get("demo//h_eta_UncertMeanPout"))




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




def DistancesBySubDetSeperate(QCDfilename, ELEfilename, PIONfilename, histname, subdetectorLabel = 'det', ptrange = (30., 40.)) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 700 )

    isLog = True

    if isLog is True :
        canvas.SetLogy()

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
    if isinstance(QCD, ROOT.TH3D) :
        QCDaxis.SetRangeUser(ptrange[0], ptrange[1])
        QCDproj = QCD.Project3D("x" + "QCD" + nameSuffix)
    else :
        QCDproj = QCD
    if isinstance(ELE, ROOT.TH3D) :
        ELEaxis.SetRangeUser(ptrange[0], ptrange[1])
        ELEproj = ELE.Project3D("x" + "Signal" + nameSuffix)
    else :
        ELEproj = ELE
    ELEproj.SetLineColor(ROOT.kRed)
    #axis2.Unzoom()

    if isinstance(PION, ROOT.TH3D) :
        PIONaxis.SetRangeUser(ptrange[0], ptrange[1])
        PIONproj = PION.Project3D("x" + "pion" + nameSuffix)
    else :
        PIONproj = PION
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

    box1 = ROOT.TPaveText(0.15,0.92,0.35,0.92, "NDC") #//NDC sets coords relative to pad
    box1.SetTextSize(0.04)
    box1.SetFillColor(0) #white background 
    box1.SetTextFont(42)
    box1.SetTextAlign(12)

    box2 = ROOT.TPaveText(0.60,0.85,0.85,0.85, "NDC") #//NDC sets coords relative to pad
    box2.SetTextSize(0.04)
    box2.SetFillColor(0) #white background 
    box2.SetTextFont(42)
    
    box2.SetTextAlign(12)

    box3 = ROOT.TPaveText(0.15,0.85,0.35,0.85, "NDC") #//NDC sets coords relative to pad
    box3.SetTextSize(0.04)
    box3.SetFillColor(0) #white background 
    box3.SetTextFont(42)
    box3.SetTextAlign(12)



    #if subdetectorLabel is not "" :
        #sub = ROOT.TPaveText(0.15,0.75,0.35,0.85, "NDC") #//NDC sets coords relative to pad
        #sub.SetTextSize(0.04)
        #sub.SetFillColor(0) #white background 
        #sub.SetTextAlign(12)
    subtmp = box1.AddText("#bf{" + subdetectorLabel + "}")     
    
#    if showCorrelation is True :
#        corrtmp = box3.AddText("#it{#rho = " + "{0:.2f}".format(hist.GetCorrelationFactor()) + "}")     
#        box3.Draw("SAME")

 #   if showEntries is True :
 #       entrtmp = box2.AddText("#it{Entries: " + "{:.0f}".format(hist.GetEntries()) + "}")
        

    box2.Draw("SAME")





    stack.Draw("")
    #stack.GetXaxis().SetRangeUser(-0.5, 0.5)
    stack.Draw("NOSTACK")
    
    box1.Draw("SAME")
    legend = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
#legSetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
    #histo1->SetLineColor(2);  //histo1 in red
        #histo2->SetLineColor(1);  //histo2 in black
    legend.SetBorderSize(0); # //no border for legend                                                            
    legend.SetFillColor(0);
    legend.AddEntry(QCDproj,"QCD","L");
    legend.AddEntry(ELEproj, "electron", "L")
    legend.AddEntry(PIONproj, "pion", "L")
    legend.Draw("SAME") 
    
    filename = 'SIGvsBGD' + ELE.GetName() + nameSuffix
    if isLog is True :
        filename += 'Log'


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

DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'pixel barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__TID', ptrange = (0., 100.), subdetectorLabel = 'inner disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__TIB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__TOB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__PIE', ptrange = (0., 100.), subdetectorLabel = 'pixel disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PPhiDiffPredFPredB_Eta_Pt__GSF__TEC', ptrange = (0., 100.), subdetectorLabel = 'TEC')           

DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'pixel barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__TID', ptrange = (0., 100.), subdetectorLabel = 'inner disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__TIB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__TOB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__PIE', ptrange = (0., 100.), subdetectorLabel = 'pixel disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_PDiffPredFPredB__GSF__TEC', ptrange = (0., 100.), subdetectorLabel = 'TEC')           


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'Pixel barrel') 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TID', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TIB', ptrange = (0., 100.))
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TOB', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__PIE', ptrange = (0., 100.)) 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_SignedTransversalDist_Eta_Pt__GSF__TEC', ptrange = (0., 100.)) 


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'pixel barrel') 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TID', ptrange = (0., 100.), subdetectorLabel = 'inner disks') 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TIB', ptrange = (0., 100.), subdetectorLabel = 'inner barrel')
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TOB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel') 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__PIE', ptrange = (0., 100.), subdetectorLabel = 'pixel disks') 
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFPredB_Eta_Pt__GSF__TEC', ptrange = (0., 100.), subdetectorLabel = 'TEC') 


DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'pixel barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TID', ptrange = (0., 100.), subdetectorLabel = 'inner disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TIB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TOB', ptrange = (0., 100.), subdetectorLabel = 'outer barrel')  
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__PIE', ptrange = (0., 100.), subdetectorLabel = 'pixel disks')   
DistancesBySubDetSeperate(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPhiPredFMeas_Eta_Pt__GSF__TEC', ptrange = (0., 100.), subdetectorLabel = 'TEC')           





file2 = ROOT.TFile("output//ele_hist.root")

ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__PIB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TID'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TIB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TOB'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__TEC'))
ProjectOutZ(file2.Get('demo//h_DiffPredMeas_DiffPredUp_Eta__GSF__PIE'))

def DistancesBySubDet1D(QCDfilename, ELEfilename, PIONfilename, histname, ptrange = (30., 40.), subdetectorLabel = 'det') :

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
   
    box1 = ROOT.TPaveText(0.15,0.92,0.35,0.92, "NDC") #//NDC sets coords relative to pad
    box1.SetTextSize(0.04)
    box1.SetFillColor(0) #white background 
    box1.SetTextFont(42)
    box1.SetTextAlign(12)

    box2 = ROOT.TPaveText(0.60,0.85,0.85,0.85, "NDC") #//NDC sets coords relative to pad
    box2.SetTextSize(0.04)
    box2.SetFillColor(0) #white background 
    box2.SetTextFont(42)
    
    box2.SetTextAlign(12)

    box3 = ROOT.TPaveText(0.15,0.85,0.35,0.85, "NDC") #//NDC sets coords relative to pad
    box3.SetTextSize(0.04)
    box3.SetFillColor(0) #white background 
    box3.SetTextFont(42)
    box3.SetTextAlign(12)



    if subdetectorLabel is not "" :
        #sub = ROOT.TPaveText(0.15,0.75,0.35,0.85, "NDC") #//NDC sets coords relative to pad
        #sub.SetTextSize(0.04)
        #sub.SetFillColor(0) #white background 
        #sub.SetTextAlign(12)
        subtmp = box1.AddText("#bf{" + subdetectorLabel + "}")     
        box1.Draw("SAME")
 


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


#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__PIB', ptrange = (0., 100.), subdetectorLabel = 'Pixel barrel') 
#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TID', ptrange = (0., 100.)) 
#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TIB', ptrange = (0., 100.))
#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TOB', ptrange = (0., 100.)) 
#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__PIE', ptrange = (0., 100.)) 
#DistancesBySubDet1D(QCDfilename = 'output//qcd_hist.root', ELEfilename = 'output//ele_hist.root', PIONfilename = 'output//pion_hist.root', histname =  'h_DiffPredFPredB__GSF__TEC', ptrange = (0., 100.)) 










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

def SetColors(hist, color) :

    #hist.SetFillColor(color)
    hist.SetLineColor(color)
    hist.SetMarkerColor(color)

def SliceHistogram(hist, sliceAxis, numberOfSlices) :

    histList = []
    axis = None
    projectionString = ''
    print sliceAxis
    projectionFunction = None
    if sliceAxis == 'x' :
        axis = hist.GetXaxis()
        projectionString = 'zy'
        projectionFunction = hist.ProjectionY
    elif sliceAxis == 'y' :
        axis = hist.GetYaxis()
        projectionString = 'zx'
        projectionFunction = hist.ProjectionX
    elif sliceAxis == 'z' :
        axis = hist.GetZaxis()
        projectionString = 'yx'
    else :
        print 'No reasonable axis for slicing specified'

    lastBin = axis.GetLast()
    firstBin = axis.GetFirst()
    numberOfBins = lastBin - firstBin + 1
    widthInBins = numberOfBins // numberOfSlices
    #print 'firstBin: ', firstBin
    #print 'lastBin: ', lastBin
    #print '#bins: ', numberOfBins
    #print 'width in bins: ', widthInBins

    for i in range(0, numberOfSlices) :
        
        lowerBin = firstBin + i * widthInBins
        upperBin = firstBin + (i+1) * widthInBins - 1
        lowerValue = axis.GetBinLowEdge(lowerBin)
        upperValue = axis.GetBinUpEdge(upperBin)
        #print 'Producing slice# ', i
        #print 'Range in bin#: ' , lowerBin, ' - ', upperBin
        #print 'Range in axis value:', lowerValue, ' - ', upperValue 
        
        nameSuffix = '_from_' + str(lowerValue) + '_to_' + str(upperValue)
        if isinstance(hist, ROOT.TH3) :
            axis.SetRangeUser(lowerBin, upperBin)
            projectedHist = hist.Project3D(projectionString + nameSuffix)
            axis.Unzoom()
        elif isinstance(hist, ROOT.TH2) :
            projectedHist = projectionFunction(hist.GetName() + sliceAxis + nameSuffix, lowerBin, upperBin)
        else :
            print 'Unknown kind of hosto!'
            return None

def SaveSuperpositionSlicePlots(histos, numberOfSlices = 10, normalization = 'none', etaRanges = [(-2.5, 2.5)], XaxisUserRange = [],  histoColors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kYellow, ROOT.kBlack, ROOT.kGreen+2]) :

    if len(histos) > len(histoColors) :
        print 'Need more colors do plot all data'
        return 0
    for erange in etaRanges :
        sliceCollection = {}
        for aSlice in range(0, numberOfSlices) :
            sliceCollection[aSlice] = []

        etaString = "_eta[" + str(erange[0]) + "," + str(erange[1]) + "]"
        filename = histos[0].GetName() + etaString
        if normalization == 'one' :
            filename += '_Normalized'
        if normalization == 'both' :
            filename += '_Both'

        for i in range(0, len(histos)) :
            histos[i].GetZaxis().SetRangeUser(erange[0], erange[1])
            h = histos[i].Project3D("yx")
            histos[i].GetZaxis().UnZoom()
            SetColors(h, histoColors[i])
            _slices = SliceHistogram(h, 'x', numberOfSlices)
            for sliceNumber in range(0, numberOfSlices) :
                sliceCollection[sliceNumber].append(_slices[sliceNumber])
  

         #hist1.GetZaxis().SetRangeUser(erange[0], erange[1])
         #h1 = hist1.Project3D("yx")
         #hist1.GetZaxis().UnZoom()
         #SetColors(h1, ROOT.kRed)
         #slices1 = SliceHistogram(h1, 'x', 10)


         #hist2.GetZaxis().SetRangeUser(erange[0], erange[1])
         #h2 = hist2.Project3D("yx2")
         #hist2.GetZaxis().UnZoom()
         #SetColors(h2, ROOT.kBlue)
         #slices2 = SliceHistogram(h2, 'x', 10)

         #name1 = hist1.GetName()
         #name2 = hist2.GetName()

         #commonName = (lcs(name1, name2))
         #lenCommonName = len(commonName)
         #
         #rest1 = name1[lenCommonName:]
         #rest2 = name2[lenCommonName:]
         
        for aSlice in range(0, len(sliceCollection)) :
            
            canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
            canvas.SetLogy()
            if normalization == 'both' :
                canvas.Divide(0, 2, 0, 0)
                pad = canvas.cd(1)
                print 'Set log'
                pad.SetLogy()
            legend  = ROOT.TLegend(.6,.15,.95,.35);  #//geometry of legend
            legend.SetBorderSize(0); # //no border for legend
            legend.SetFillColor(0);  #//fill color is white
            legend.Draw()
             
            stack = ROOT.THStack("tmp","tmp")
           
            firstSlice = sliceCollection[aSlice][1]
            sliceName = firstSlice.GetName()
            #print 'index: ', sliceName.find('_from')
            sliceName = sliceName[sliceName.find('_from'):]
            #print 'sliceName: ', sliceName

          
            for aData in sliceCollection[aSlice] :
                
                legend.AddEntry(aData, aData.GetName(),"L");#  // see *http://root.cern.ch/root/html/TLegend.html *  for details
                if normalization == 'one' :
                    NormalizeHisto(aData)
                    stack.SetMaximum(1.0)
         
                stack.Add(aData)
            stack.Draw("nostack")
            #axis = stack.GetXaxis()
            #axis.SetRange(0, axis.GetNbins() + 1)
            legend.Draw("SAME")

            if normalization == 'both' :
                pad2 = canvas.cd(2)
                pad2.SetLogy()
                secondStack = ROOT.THStack("tmp2", "tmp2")
                
                for aData in sliceCollection[aSlice] :
                    tmp = aData.Clone(aData.GetName() + "tmp")
                    NormalizeHisto(tmp)
                    #secondStack.SetMaximum(0.3)
            
                    secondStack.Add(tmp)
                if len(XaxisUserRange) is not 0 :
                    print 'Modifying axis range'        
def GetRebin(name, rebin) :
    return afile.Get("demo/" + name).RebinY(rebin, name + '_rebin' + str(rebin))

afile = ROOT.TFile("output//ele_hist.root")
afile.cd("demo")
afile.ls()
#SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__1HITS',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__2HITS',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
#                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
#                            numberOfSlices = 1,
#                            normalization = 'one')
#

