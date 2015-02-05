import ROOT
import os

ROOT.gROOT.SetBatch(True)
file = ROOT.TFile("output//histo.root")

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









file.cd("demo")
file.ls()

def lcs(s1, s2):
  m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
  longest, x_longest = 0, 0
  for x in xrange(1, 1 + len(s1)):
    for y in xrange(1, 1 + len(s2)):
      if s1[x - 1] == s2[y - 1]:
        m[x][y] = m[x - 1][y - 1] + 1
        if m[x][y] > longest:
          longest = m[x][y]
          x_longest = x
      else:
        m[x][y] = 0
  return s1[x_longest - longest: x_longest]


def SetColors(hist, color) :

    #hist.SetFillColor(color)
    hist.SetLineColor(color)
    hist.SetMarkerColor(color)


def SaveElectronClassificationPlot(histo, normalization = 'one') :

    filename = histo.GetName()
    
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    histo.GetXaxis().SetRangeUser(0., 5.)

    classes = {-1:'unknown', 0:'golden', 1:'big brem', 2:'bad track', 3:'showering', 4:'gap'}
    colors  = {-1:ROOT.kRed, 0:ROOT.kYellow, 1:ROOT.kMagenta, 2:ROOT.kBlack, 3:ROOT.kBlue, 4:ROOT.kCyan}
    histList = []

    numberOfClasses = histo.GetYaxis().GetNbins()

    if(len(classes) is not numberOfClasses) :
        print 'Number of classes in electron classification does not match!, exiting'

    stack = ROOT.THStack('tmp', 'tmp')

    for i in range(1, numberOfClasses + 1) :
        xbin = histo.GetYaxis().GetBinLabel(i)
        print 'Looking up bin label ', i
        catName = classes[i - 2]
        print 'Category name ', catName
        tmp = histo.ProjectionX(catName, i, i)
        if(normalization is 'one') :
            totNumber = histo.Integral()
            intCat    = tmp.Integral()
            tmp.SetLineColor(colors[i - 2])
            if(intCat > 0) :
                tmp.Scale(1. / intCat)
                histList.append(tmp)


    canvas.SetLogy()
    legend = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
    #legend.SetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
    #histo1->SetLineColor(2);  //histo1 in red
    #histo2->SetLineColor(1);  //histo2 in black
    legend.SetBorderSize(0); # //no border for legend                                                            
    legend.SetFillColor(0);  #//fill color is white


    for hist in histList :
        stack.Add(hist)

        legend.AddEntry(hist, hist.GetName(),"L");#  // see *http://root.cern.ch/root/html/TLegend.html *  for details


    stack.Draw("NOSTACK")
    stack.GetYaxis().SetTitle("Entries")
    if(normalization is 'one') :
        stack.GetYaxis().SetTitle("normalized per category")
    stack.GetXaxis().SetTitle(histo.GetXaxis().GetTitle())
    stack.Draw("NOSTACK")

    legend.Draw("SAME")

    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + filename + fileFormat)

SaveElectronClassificationPlot(file.Get("demo/h_EeleClusterOverPout_Classification"))
SaveElectronClassificationPlot(file.Get("demo/h_EseedOverPout_Classification"))
SaveElectronClassificationPlot(file.Get("demo/h_InvSFPout_Classification"))


def SaveMaterialBudgetPlot(profile) :
    filename = 'MaterialBudget'
    hist = profile.ProjectionX()

    graph = ROOT.TGraph(hist)

    func = ROOT.TF2("f2","TMath::LogE() * TMath::Log(y)",0,50,0,8);

    graph.Apply(func)
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    graph.Draw()
   
    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + filename + fileFormat)

SaveMaterialBudgetPlot(file.Get("demo/p_EinOverEoutGeant_eta"))


def SaveRadiationLengthPlot(profile) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )

    hist = profile.ProjectionX()

    graph = ROOT.TGraph(hist)

    
def SaveAllProjectionSuperposition(hist1, hist2, normalization='none') :

    histos = [hist1, hist2]

    SetColors(hist1, ROOT.kRed)
    SetColors(hist2, ROOT.kBlue)

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    canvas.SetRightMargin(0.3)  

    projection1 = []
    projection2 = []
    
    projHist = []
    projections = ["x", "y", "z"]
    for proj in projections :
        projHist.append((hist1.Project3D(proj), hist2.Project3D(proj)))

    hist1Name = hist1.GetName()
    hist2Name = hist2.GetName()
    hist1Rest = hist1Name[hist1Name.rfind('__'):]
    hist2Rest = hist2Name[hist2Name.rfind('__'):]

    filename = 'SupPos_' + hist1Name[:hist1Name.rfind('__')] 

    subfolderName = outputFolderName + '//' + filename
    if not os.path.exists(subfolderName):
        os.makedirs(subfolderName)


    for p in projHist :
        stack = ROOT.THStack(hist1.GetTitle(),"Barrel;" +p[0].GetXaxis().GetTitle())
        p[0].Draw()
        ROOT.gPad.Update()
        st1 = p[0].FindObject("stats");
        st1.SetTextColor(ROOT.kRed) 
        
        p[1].Draw();
        ROOT.gPad.Update();
        st2 = p[1].FindObject("stats");
        st2.SetTextColor(ROOT.kBlue)
        st1.SetX1NDC(0.7);
        st1.SetX2NDC(0.95);
        st1.SetY1NDC(0.7);
        st1.SetY2NDC(0.9);
        st2.SetX1NDC(0.7);
        st2.SetX2NDC(0.95);
        st2.SetY1NDC(0.5);
        st2.SetY2NDC(0.7);
        if normalization == 'one' :
           p[0].Scale(1. /p[0].Integral())
           p[1].Scale(1. /p[1].Integral())
 
        stack.Add(p[0])
        stack.Add(p[1])

        stack.Draw("nostack")
        st1.Draw("SAME")
        st2.Draw("SAME")

        projectedName = p[0].GetName()

        for fileFormat in savedFileFormats :
            canvas.Print(subfolderName + '//'  +projectedName +  '_' + hist1Rest + '_vs_' + hist2Rest + fileFormat)


#SaveAllProjectionSuperposition(
#        file.Get("demo/h_numberOfValidTrackerHits_trackerLayersWithMeasurement_trackerLayersWithoutMeasurement__BARREL__POUTSMALL"), 
#        file.Get("demo/h_numberOfValidTrackerHits_trackerLayersWithMeasurement_trackerLayersWithoutMeasurement__BARREL__POUTBIG"),
#        normalization='one')
#
#SaveAllProjectionSuperposition(
#        file.Get("demo/h_numberOfBadHits_numberOfLostPixelHits_numberOfLostStripHits__BARREL__POUTSMALL"), 
#        file.Get("demo/h_numberOfBadHits_numberOfLostPixelHits_numberOfLostStripHits__BARREL__POUTBIG"),
#        normalization='one')


def SaveScatterPlotProjection(histo, projection="xy") :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )

    proj = histo.Project3D( projection)

    proj.Draw()

    filename = proj.GetName()
    
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//' + filename + fileFormat)


#SaveScatterPlotProjection(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__3HITS"), ""
SaveScatterPlotProjection(file.Get("demo/h_Eta_MeanRelErrorIn_MeanRelErrorOut"), "zx")
SaveScatterPlotProjection(file.Get("demo/h_Eta_MeanRelErrorIn_MeanRelErrorOut"), "yx")



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

        projectedHist.SetTitle('Only entries with ' + axis.GetTitle() + ' in [' + str(lowerValue) + ',' + str(upperValue) + ')' )
        histList.append(projectedHist)

    
    return histList



def SaveGeantTPEnergySpectrum(histGeant, histTP) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    histTP.SetLineColor(ROOT.kRed)
    histTP.SetStats(ROOT.kFALSE)
    histTP.Draw()
    histGeant.SetLineColor(ROOT.kBlue)
    histGeant.SetStats(ROOT.kFALSE)
    histGeant.Draw("SAME")
    
    histTP.Draw()
    ROOT.gPad.Update()
    #st1 = histTP.FindObject("stats");
    #st1.SetTextColor(ROOT.kRed) 
    
    histGeant.Draw();
    ROOT.gPad.Update();
    #st2 = histGeant.FindObject("stats");
    #st2.SetTextColor(ROOT.kBlue)
    #st1.SetX1NDC(0.5);
    #st1.SetX2NDC(0.7);
    #st1.SetY1NDC(0.7);
    #st1.SetY2NDC(0.9);
    #st2.SetX1NDC(0.7);
    #st2.SetX2NDC(1.0);
    #st2.SetY1NDC(0.7);
    #st2.SetY2NDC(0.9);
    
    histTP.Draw()
    histTP.GetXaxis().SetTitle("Energy of #gamma_{brem}")
    histTP.GetYaxis().SetTitle("Entries")
    histTP.GetYaxis().SetTitleOffset(1.6)
    histGeant.Draw("SAME")

    legend  = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
    #legend.SetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
    #histo1->SetLineColor(2);  //histo1 in red
    #histo2->SetLineColor(1);  //histo2 in black
    legend.AddEntry(histTP,"TrackingParticle #gamma","L");#  // see *http://root.cern.ch/root/html/TLegend.html *  for details
    legend.AddEntry(histGeant,"Geant tracklet deltas","L");
    legend.SetBorderSize(0); # //no border for legend                                                            
    legend.SetFillColor(0);  #//fill color is white

    legend.Draw("SAME")                                                                                                
    for fileFormat in savedFileFormats : 
        canvas.Print(outputFolderName + '//Geant_vs_TP_EnergySpectra' + fileFormat)

SaveGeantTPEnergySpectrum(file.Get("demo/h_GeantBremEnergySpectrum") ,file.Get("demo/h_TPBremEnergySpectrum"))

def SaveHistogramByEta(hist) :

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    EtaRanges = [(-2.5,2.5), (-2.5,-1.0), (-1.0,1.0), (1.0,2.5)]

    xName = hist.GetXaxis().GetTitle()
    yName = hist.GetYaxis().GetTitle()


    for range in EtaRanges :
        upper = range[1]
        lower = range[0]
        rangeString = '(' + str(lower) + ',' + str(upper) + ')'
        hist.GetZaxis().SetRangeUser(lower,upper)
       
        ProjectZ = hist.Project3D("yx")
         
        histIntX = ProjectZ.ProjectionX()
        histIntY = ProjectZ.ProjectionY()
    
        histos = [histIntX, histIntY]    
    
        for rangedHist in histos :
        
            #print 'Eta range =', rangeString, rangedHist.GetCorrelationFactor(), " with Nentries: ", rangedHist.GetEntries()
            fileName = rangedHist.GetName() + '_eta_' + str(lower) + '_' + str(upper)#rangeString
            #fileName = 'corrCoeff_' + xName + '_' + yName + '_eta_' + str(lower) + '_' + str(upper)#rangeString
            title = '#eta in ' + rangeString
            rangedHist.SetTitle(title)
            rangedHist.Draw()

            canvas.Print('output//'+ fileName + '.gif')
    hist.GetZaxis().UnZoom()

SaveHistogramByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta"))

def SaveCorrelationPlotsByEta(hist, EtaRanges = [(-2.5,2.5), (-2.5,-1.0), (-1.0,1.0), (1.0,2.5)], folderName = "" ) :
    if folderName is not "" :
        folderName = "//" + folderName
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    

    hist.SetStats(ROOT.kFALSE)

    print 'Computing correlations for histogram:', hist.GetName()
    xName = hist.GetXaxis().GetTitle()
    yName = hist.GetYaxis().GetTitle()   
   
    for range in EtaRanges :
        upper = range[1]
        lower = range[0]
        rangeString = '(' + str(lower) + ',' + str(upper) + ')'
        hist.GetZaxis().SetRangeUser(lower,upper)
        rangedHist = hist.Project3D("yx")
        histoname = hist.GetName()
        rangedHist.SetStats(ROOT.kFALSE) 
        print 'Eta range =', rangeString, rangedHist.GetCorrelationFactor(), " with Nentries: ", rangedHist.GetEntries()
        filename = hist.GetName() + '_eta_' + str(lower) + '_' + str(upper)#rangeString
        #fileName = 'corrCoeff_' + xName + '_' + yName + '_eta_' + str(lower) + '_' + str(upper)#rangeString
        title = '#rho(' + xName + ',' + yName + ') limited to #eta in ' + rangeString
        rangedHist.SetTitle(title)
        #rangedHist.GetYaxis().SetRangeUser(0., 2.4)
        rangedHist.Draw()

        myText = ROOT.TPaveText(0.2,0.7,0.4,0.85, "NDC") #//NDC sets coords relative to pad
        myText.SetTextSize(0.04)
        myText.SetFillColor(0) #white background 
        myText.SetTextAlign(12)
        myTextEntry = myText.AddText("#rho = " + "{0:.2f}".format(rangedHist.GetCorrelationFactor()))       #str(rangedHist.GetCorrelationFactor()) ) 
        myText.Draw("SAME");

        subfolderName = outputFolderName + folderName + '//' + histoname
        if not os.path.exists(subfolderName):
            os.makedirs(subfolderName)
        for fileFormat in savedFileFormats :
            canvas.Print(subfolderName + '//' + filename + fileFormat)



    hist.GetZaxis().UnZoom()

#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])

#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSCONT40__4ORMOREHITS__NOCONV"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSCONT40__4ORMOREHITS"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSCONT40"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__4ORMOREHITS__NOCONV"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__4ORMOREHITS"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__3ORMOREHITS"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")

SaveCorrelationPlotsByEta(file.Get("demo/h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS__NOCONV"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_SFfbrem_SFPout_eta__ABSBIG40"),        EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_SFfbrem_SFPout_eta"),        EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta"),        EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__1HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__2HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])


SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__1HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__2HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG60__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG60__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG60__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG60__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__HITASS"), EtaRanges = [(-1.0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__4ORMOREHITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")
SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40__4ORMOREHITS__NOCONV"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)], folderName = "FbremCorr")





#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__3HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__4HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__5HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
#SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__6HITS"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])

SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_ModePtout_eta"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_6MinWeightPtout_eta"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_1MinPtout_eta"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])
SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_1MinWeightPtout_eta"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])

#SaveCorrelationPlotsByEta(file.Get("demo/h_MCPtout_1MinWeightPtout_eta"), EtaRanges = [(-0.5, 0.5), (1.0, 1.5), (1.5, 2.0), (2.0,2.5)])


SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_GSFchi2red_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_MeanFbrem_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbremTimesRelErrorModePtIn_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbremOverRelErrorModePtIn_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_ModeFbrem_eta__CONT60"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_MeanfbremOverRelErrorPout_eta"))

SaveCorrelationPlotsByEta(file.Get("demo/h_Gfbrem_MeanfbremSignificance_eta"))
                                        
def SaveScatterplotSuperposition(hist1, hist2) :

    hist1 = hist1.Project3D("yx")
    hist2 = hist2.Project3D("yx")

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    
    SetColors(hist1, ROOT.kRed)
    SetColors(hist2, ROOT.kBlue)
    
    hist1.Draw()
    ROOT.gPad.Update()
    st1 = hist1.FindObject("stats");
    st1.SetTextColor(ROOT.kRed) 
    
    hist2.Draw();
    ROOT.gPad.Update();
    st2 = hist2.FindObject("stats");
    st2.SetTextColor(ROOT.kBlue)
    st1.SetX1NDC(0.1);
    st1.SetX2NDC(0.3);
    st1.SetY1NDC(0.7);
    st1.SetY2NDC(0.9);
    st2.SetX1NDC(0.3);
    st2.SetX2NDC(0.5);
    st2.SetY1NDC(0.7);
    st2.SetY2NDC(0.9);
    
    hist1.Draw()
    hist2.Draw("SAME")
    
    filename = 'Superposition_'  + hist1.GetName() + '+' + hist2.GetName()

    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + filename + fileFormat)


#SaveScatterplotSuperposition(file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG"), file.Get("demo/h_Gfbrem_ModeFbrem_eta__CONT"))

def NormalizeHisto(histo) :
    integral = histo.Integral()
    if integral != 0. :
        histo.Scale(1. / integral)

def SaveSummaryPlots(histo1, title = "No requirements ", axis = "y", normalization = 'none', etaRanges = [(-2.5, 2.5), (1.0, 1.5)],  histoColors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kYellow, ROOT.kBlack, ROOT.kGreen+2]) :

    histos = []
    filename = histo1.GetName()

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    legend  = ROOT.TLegend(.8,.15,.95,.35);  #//geometry of legend
    for erange in etaRanges :
        etaString = "_eta[" + str(erange[0]) + "," + str(erange[1]) + "]"
        filename += etaString

        histo1.GetZaxis().SetRangeUser(erange[0], erange[1])
        aHist = histo1.Project3D(axis + etaString)
        histos.append(aHist)
        histo1.GetZaxis().UnZoom()
  
        legend.AddEntry(aHist, "#eta in ["  + str(erange[0]) + ", " + str(erange[1]) + "]","L");#  // see *http://root.cern.ch/root/html/TLegend.html *  for details
    if normalization == 'one' :
        filename += '_Normalized'
    if normalization == 'both' :
        filename += '_Both'

     
       
        for i in range(0, len(histos)) : 
            SetColors(histos[i], histoColors[i])

        stack = ROOT.THStack("tmp","tmp")
        

        canvas.SetLogy()
        secondStack = ROOT.THStack("tmp2", "tmp2")
    
        fractionAbove2 = []
        numberAroundPeak = []
        statistics = []
        for aHisto in histos :
        
            #numberAroundPeak.append(number)
            stack.Add(aHisto)
            tmp = aHisto.Clone(aHisto.GetName() + "tmp")
            NormalizeHisto(tmp)
                    #secondStack.SetMaximum(0.3)
            fractionAbove2.append(tmp.GetBinContent(21))
            secondStack.Add(tmp)
            
            FOR = "{:.0f}"
            FOR2 = "{:.1f}"
            xmin = 0.8
            xmax = 1.19
            bmin = aHisto.GetXaxis().FindBin(xmin)
            bmax = aHisto.GetXaxis().FindBin(xmax)
            number = aHisto.Integral(bmin, bmax) #9,12
            
            fractionPeak = 100. * tmp.Integral(bmin, bmax)
            print "bmin ", bmin
            print "bmax ", bmax
            if axis is "y" :
                text = "In peak [" + FOR2.format(xmin) + ", " + FOR2.format(xmax) + ") " + str(number) + " (" + FOR.format(fractionPeak)+ "%)"  +"; in [2, #infty) " + FOR.format(100. * tmp.GetBinContent(21)) + "%"
            if axis is "x" :
                text = "In peak [" + FOR2.format(xmin) + ", " + FOR2.format(xmax) + ") " + str(number) + " (" + FOR.format(fractionPeak)+ "%)"#  +"; in [2, #infty) " + FOR.format(100. * tmp.GetBinContent(21)) + "%"
            statistics.append(text)

        if normalization == 'both' :
            canvas.Divide(0, 2, 0, 0)
            pad = canvas.cd(1)
            print 'Set log'
            pad.SetLogy()
            stack.Draw("nostack") 
            stack.GetYaxis().SetTitle("electrons")
            legend.SetBorderSize(0); # //no border for legend
            legend.SetFillColor(0);  #//fill color is white
            legend.Draw("SAME")

            pad2 = canvas.cd(2)
            pad2.SetLogy()
            stats = ROOT.TPaveText(.6,.35,1.0,.55,"brNDC")#.8, .35, .95, .65)
            stats.SetBorderSize(0)
            stats.SetFillColor(0)           
            for s in statistics :
                stats.AddText(s)

            lines = []
            lines.append(stats.GetLine(0))
            lines.append(stats.GetLine(1))
            for i in range(0, len(lines)):
                line = lines[i]
                line.SetTextColor(histoColors[i])
                line.SetTextAlign(11)
                line.SetTextSize(.04)
            #stats.GetLine(1).SetTextColor(histoColors[1])           
        
            secondStack.Draw("nostack")
            secondStack.GetXaxis().SetTitle(aHisto.GetXaxis().GetTitle())    
            secondStack.GetYaxis().SetTitle("normalized")
            secondStack.Draw("nostack")

            stats.Draw("SAME")
        if normalization == 'one' :
            NormalizeHisto(aHisto)
            stack.SetMaximum(1.0)
         

        if normalization is not 'both' :
            stack.Draw("nostack")
            #axis = stack.GetXaxis()
            #axis.SetRange(0, axis.GetNbins() + 1)
            legend.Draw("SAME")

                
               #legend.Draw("SAME")   

        subfolderName = outputFolderName + '//' + 'Summary'
        if not os.path.exists(subfolderName):
            os.makedirs(subfolderName)
        for fileFormat in savedFileFormats :
            canvas.Print(subfolderName + '//' + filename + fileFormat)

def GetRebin(name, rebin) :
    return file.Get("demo/" + name).RebinY(rebin, name + '_rebin' + str(rebin))


SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta',2), normalization = 'both', axis = "x")
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40',2), normalization = 'both', axis = "x")
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS',2), normalization = 'both', axis = "x")
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS__NOCONV',2), normalization = 'both', axis = "x")

SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta',2), normalization = 'both', axis = "x", etaRanges = [(-1.0, 1.0), (1.0, 1.5)])
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40',2), normalization = 'both', axis = "x" , etaRanges = [(-1.0, 1.0), (1.0, 1.5)])
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS',2), normalization = 'both', axis = "x", etaRanges = [(-1.0, 1.0), (1.0, 1.5)])
SaveSummaryPlots(GetRebin('h_SFfbrem_SFPout_eta__ABSBIG40__4ORMOREHITS__NOCONV',2), normalization = 'both', axis = "x", etaRanges = [(-1.0, 1.0), (1.0, 1.5)])




SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta',1), normalization = 'both')
SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1), normalization = 'both')
SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5ORMOREHITS__NOCONV',1), normalization = 'both')
SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5ORMOREHITS',1), normalization = 'both')

SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4ORMOREHITS__NOCONV',1), normalization = 'both')
SaveSummaryPlots(GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4ORMOREHITS',1), normalization = 'both')


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
         

         #filename = 'Slices_' + commonName + rest1 + '_vs_' + rest2 +etaString 
         #print 'name1: ', name1
         #print 'name2: ', name2
         #print 'common part: ', commonName
         #print 'rest1: ', rest1
         #print 'rest2: ' ,rest2
         #print 'filename: ', filename

        
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
                    secondStack.Draw()
                    print XaxisUserRange
                    #axis =  secondStack.GetXaxis()
                    #secondStack.GetXaxis().SetRange(0, axis.GetNbins() + 1)#XaxisUserRange[0], XaxisUserRange[1])
                secondStack.Draw("nostack")
               #legend.Draw("SAME")   

            subfolderName = outputFolderName + '//' + filename
            if not os.path.exists(subfolderName):
                os.makedirs(subfolderName)
            for fileFormat in savedFileFormats :
                canvas.Print(subfolderName + '//' + filename + sliceName + fileFormat)

             

def SaveSuperpositionPlots(hist1, hist2, normalization = 'none') :

    SetColors(hist1, ROOT.kRed)
    SetColors(hist2, ROOT.kBlue)

    name1 = hist1.GetName()
    name2 = hist2.GetName()

    commonName = (lcs(name1, name2))
    lenCommonName = len(commonName)
    
    rest1 = name1[lenCommonName:]
    rest2 = name2[lenCommonName:]
    
    filename = commonName + rest1 + '_vs_' + rest2
    print 'name1: ', name1
    print 'name2: ', name2
    print 'common part: ', commonName
    print 'rest1: ', rest1
    print 'rest2: ' ,rest2
    print 'filename: ', filename
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    if normalization == 'one' :
        filename += '_Normalized'
        hist1.Scale(1. /hist1.Integral())
        hist1.Scale(1. /hist2.Integral())
    
    hist1.SetStats(True)

    hist2.SetStats(True)
    stack = ROOT.THStack("hs","stack;" + hist1.GetXaxis().GetTitle() + ";" + hist1.GetYaxis().GetTitle())
    stack.Add(hist1)
    stack.Add(hist2)
    hist1.Draw()
    ROOT.gPad.Update()
    st1 = hist1.FindObject("stats")
    st1.SetTextColor(ROOT.kRed)

    hist2.Draw();
    ROOT.gPad.Update();
    st2 = hist2.FindObject("stats")
    st2.SetTextColor(ROOT.kBlue)
    canvas.SetRightMargin(0.3)
    st1.SetX1NDC(0.7);
    st1.SetX2NDC(0.95);
    st1.SetY1NDC(0.7);
    st1.SetY2NDC(0.9);
    
    st2.SetX1NDC(0.7);
    st2.SetX2NDC(0.95);
    st2.SetY1NDC(0.5);
    st2.SetY2NDC(0.7);

   #slice1.Draw()
    #slice2.Draw("SAME")
    stack.Draw("nostack")
    
    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + filename + fileFormat)





SaveSuperpositionPlots( file.Get("demo/h_PinFromCurvilinearOverPinMC"), 
                        file.Get("demo/h_PinFromCartesianOverPinMC"))
SaveSuperpositionPlots( file.Get("demo/h_PoutFromCurvilinearOverPoutMC"), 
                        file.Get("demo/h_PoutFromCartesianOverPoutMC"))

def SaveEtaSuperpositionSlicePlots(hist1, hist2, normalization = 'none', etaRange1 = [(-2.5, -1.0)], etaRange2=[(-1.0,1.0)]) :

    for erange in range(0, len(etaRange1)) :

         hist1.GetZaxis().SetRangeUser(etaRange1[erange][0], etaRange1[erange][1])
         etaString1 = "_eta1[" + str(etaRange1[erange][0]) + "," + str(etaRange1[erange][1]) + "]"
         h1 = hist1.Project3D("yx" + etaString1)
         hist1.GetZaxis().UnZoom()
         SetColors(h1, ROOT.kRed)
         slices1 = SliceHistogram(h1, 'x', 10)


         hist2.GetZaxis().SetRangeUser(etaRange2[erange][0], etaRange2[erange][1])
         etaString2 = "_eta2[" + str(etaRange2[erange][0]) + "," + str(etaRange2[erange][1]) + "]"
         h2 = hist2.Project3D("yx" +etaString2)
         hist2.GetZaxis().UnZoom()
         SetColors(h2, ROOT.kBlue)
         slices2 = SliceHistogram(h2, 'x', 10)

         name1 = hist1.GetName()
         name2 = hist2.GetName()

         commonName = (lcs(name1, name2))
         lenCommonName = len(commonName)
         
         rest1 = name1[lenCommonName:]
         rest2 = name2[lenCommonName:]
         
         etaString = etaString1 + etaString2 
         filename = 'Slices_' + commonName + rest1 + '_vs_' + rest2 +etaString 
         print 'name1: ', name1
         print 'name2: ', name2
         print 'common part: ', commonName
         print 'rest1: ', rest1
         print 'rest2: ' ,rest2
         print 'filename: ', filename
         canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
         if normalization == 'one' :
             filename += '_Normalized'
         for i in range(0, 10) :
             slice1 = slices1[i]
             slice2 = slices2[i]
             if normalization == 'one' :
                 slice1.Scale(1. /slice1.Integral())
                 slice2.Scale(1. /slice2.Integral())
             #ROOT.gStyle.SetOptStat(0)
 
             slice1.SetStats(False)
             slice2.SetStats(False)
             stack = ROOT.THStack("hs","Slice;" + slice1.GetXaxis().GetTitle() + ";" + slice1.GetYaxis().GetTitle())
             stack.Add(slice1)
             stack.Add(slice2)
             slice1.Draw()
             ROOT.gPad.Update()
             #st1 = slice1.FindObject("stats")
             #st1.SetTextColor(ROOT.kRed)

             slice2.Draw();
             ROOT.gPad.Update();
             #st2 = slice2.FindObject("stats")
             #st2.SetTextColor(ROOT.kBlue)
             #canvas.SetRightMargin(0.3)
             #st1.SetX1NDC(0.7);
             #st1.SetX2NDC(0.95);
             #st1.SetY1NDC(0.7);
             #st1.SetY2NDC(0.9);
             
             #st2.SetX1NDC(0.7);
             #st2.SetX2NDC(0.95);
             #st2.SetY1NDC(0.5);
             #st2.SetY2NDC(0.7);

            #slice1.Draw()
             #slice2.Draw("SAME")
             #stack.SetStats(ROOT.kFALSE)
             stack.Draw("nostack")

    
             legend  = ROOT.TLegend(.7,.75,.89,.89);  #//geometry of legend
             
             #legend.SetHeader(histTP.GetName());  #//leg. header (name of histogram or sth. else)
             #histo1->SetLineColor(2);  //histo1 in red
             #histo2->SetLineColor(1);  //histo2 in black
             legend.AddEntry(slice1, "#eta in [" + str(etaRange1[erange][0]) + "," + str(etaRange1[erange][1]) + "]","L");#  // see *http://root.cern.ch/root/html/TLegend.html *  for details
             legend.AddEntry(slice2,"#eta in [" + str(etaRange2[erange][0]) + "," + str(etaRange2[erange][1]) + "]","L");
             legend.SetBorderSize(0); # //no border for legend                                                            
             legend.SetFillColor(0);  #//fill color is white

             legend.Draw("SAME")






             slice1name = slice1.GetName()
             sliceName = slice1name[slice1name.find('_from'):]

             subfolderName = outputFolderName + '//' + filename
             if not os.path.exists(subfolderName):
                     os.makedirs(subfolderName)
             for fileFormat in savedFileFormats :
                canvas.Print(subfolderName + '//' + filename + sliceName + fileFormat)


h_Gfbrem_ModeFbrem_eta__BIG40_rebin = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__BIG40_rebin")
h_Gfbrem_ModeFbrem_eta__CONT40_rebin = file.Get("demo/h_Gfbrem_ModeFbrem_eta__CONT40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__CONT40_rebin")

h_Gfbrem_ModeFbrem_eta__ABSBIG40_rebin = file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__ABSBIG40_rebin")
h_Gfbrem_ModeFbrem_eta__ABSCONT40_rebin = file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSCONT40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__ABSCONT40_rebin")


h_Gfbrem_ModeFbrem_eta__BIG40_rebin2 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__BIG40_rebin2")
h_Gfbrem_ModeFbrem_eta__CONT40_rebin2 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__CONT40").RebinY(5, "h_Gfbrem_ModeFbrem_eta__CONT40_rebin2")
#SaveSuperpositionSlicePlots(h_Gfbrem_ModeFbrem_eta__ABSBIG40_rebin, h_Gfbrem_ModeFbrem_eta__ABSCONT40_rebin, 'one')

SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG40_rebin, h_Gfbrem_ModeFbrem_eta__CONT40_rebin], normalization = 'none')
SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG40_rebin2, h_Gfbrem_ModeFbrem_eta__CONT40_rebin2])
SaveSuperpositionSlicePlots([file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSBIG40"), file.Get("demo/h_Gfbrem_ModeFbrem_eta__ABSCONT40")])
#SaveEtaSuperpositionSlicePlots([file.Get("demo/h_Gfbrem_ModeFbrem_eta"), file.Get("demo/h_Gfbrem_ModeFbrem_eta")], normalization='one')

h_Gfbrem_ModeFbrem_eta__BIG40__3HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__3HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG40__3HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG40__5HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__5HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG40__5HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG40__4HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__4HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG40__4HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG40__6HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG40__6HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG40__6HITS_rebin1")

h_Gfbrem_ModeFbrem_eta__BIG60__3HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__3HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG60__3HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG60__5HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__5HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG60__5HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG60__4HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__4HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG60__4HITS_rebin1")
h_Gfbrem_ModeFbrem_eta__BIG60__6HITS_rebin1 = file.Get("demo/h_Gfbrem_ModeFbrem_eta__BIG60__6HITS").RebinY(4,"h_Gfbrem_ModeFbrem_eta__BIG60__6HITS_rebin1")

SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG60__3HITS_rebin1,
                             h_Gfbrem_ModeFbrem_eta__BIG60__4HITS_rebin1, 
                             h_Gfbrem_ModeFbrem_eta__BIG60__5HITS_rebin1, 
                             h_Gfbrem_ModeFbrem_eta__BIG60__6HITS_rebin1], 
                             normalization = 'both',
                             etaRanges = [(-2.5, 2.5), (-1.0, 1.0), (1.0, 1.5)])


SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG40__3HITS_rebin1, 
                             h_Gfbrem_ModeFbrem_eta__BIG40__4HITS_rebin1, 
                             h_Gfbrem_ModeFbrem_eta__BIG40__5HITS_rebin1, 
                             h_Gfbrem_ModeFbrem_eta__BIG40__6HITS_rebin1], 
                             normalization = 'none')


SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__1HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta'       ,8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__2HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__3HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__4HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__5HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__6HITS',8)],
                            normalization = 'one',
                            etaRanges = [(-1.0, 1.0), (1.0, 1.5)])

SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__1HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta'       ,8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__2HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__3HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__4HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__5HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__6HITS',8)],
                            normalization = 'none',
                            etaRanges = [(-1.0, 1.0), (1.0, 1.5)])








SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__1HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__2HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__3HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__4HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__5HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__6HITS',4)],
                            normalization = 'one',
                            etaRanges = [(-2.5, 2.5), (-1.0, 1.0), (1.0, 1.5)])

SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__1HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__2HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__3HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__4HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__5HITS',4),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__6HITS',4)],
                            normalization = 'none',
                            etaRanges = [(-2.5, 2.5), (-1.0, 1.0), (1.0, 1.5)])


SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__1HITS',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__2HITS',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__3HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__4HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__5HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__6HITS',8)],
                            normalization = 'one')

SaveSuperpositionSlicePlots([
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__1HITS',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__2HITS',1),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__3HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__4HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__5HITS',8),
                            GetRebin('h_Gfbrem_ModeFbrem_eta__ABSBIG40__6HITS',8)],
                            normalization = 'none')

SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__1HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__2HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'one')

SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__1HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__2HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'none')

SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'one')

print 'h_MCPtout_ModePoutOverMCPout_eta__3HITS'
SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'none')
print 'END h_MCPtout_ModePoutOverMCPout_eta__3HITS'
SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSCONT40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            normalization = 'both')
SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSCONT40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'one')
SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSCONT40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            numberOfSlices = 1,
                            normalization = 'none')

SaveSuperpositionSlicePlots([GetRebin('h_MCPtout_ModePoutOverMCPout_eta__BIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__3HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__4HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__5HITS',1),
                            GetRebin('h_MCPtout_ModePoutOverMCPout_eta__ABSBIG40__6HITS',1)],
                            normalization = 'both')
                            #XaxisUserRange = [0, 4])
#SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG40__4HITS_rebin1, h_Gfbrem_ModeFbrem_eta__BIG40__5HITS_rebin1], 'one')

#SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG60__3HITS_rebin1, h_Gfbrem_ModeFbrem_eta__BIG60__4HITS_rebin1], 'one')
#SaveSuperpositionSlicePlots([h_Gfbrem_ModeFbrem_eta__BIG60__3HITS_rebin1, h_Gfbrem_ModeFbrem_eta__BIG60__4HITS_rebin1], 'one')



def ProduceCorrelationPlots(hist, projections = ['xy', 'zx', 'zy']) :

    histList = []
    for proj in projections :
        histList.append(hist.Project3D(proj))
    #projectYX = hist.Project3D("yx")
    #projectZX = hist.Project3D("zx")
    #projectYZ = hist.Project3D("zy")

    #histList = [projectYX, projectZX, projectYZ]

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    for h in histList :
        filename = h.GetName()
        h.Draw()
        myText = ROOT.TPaveText(0.2,0.7,0.4,0.85, "NDC") #//NDC sets coords relative to pad
        myText.SetTextSize(0.04)
        myText.SetFillColor(0) #white background
        myText.SetTextAlign(12)
        myTextEntry = myText.AddText("#rho = " + str(h.GetCorrelationFactor()) )
        myText.Draw("SAME")

        for fileFormat in savedFileFormats :
            canvas.Print(outputFolderName + '//' + filename + fileFormat)



ProduceCorrelationPlots(file.Get("demo/h_GSFEstimate_KFEstimate_GSFTrajMeasMaxEstimate"), ['yx', 'zx', 'zy'])
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_ModeFbrem_GSFTrajMeasMaxEstimate"), ['yx', 'zx', 'zy'])
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_SFFbrem_GSFTrajMeasMaxEstimate"), ['yx', 'zx', 'zy'])

ProduceCorrelationPlots(file.Get("demo/h_Modefbrem_MeanRelErrorIn_MeanRelErrorOut"))
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MeanRelErrorIn_MeanRelErrorOut"))
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MeanRelErrorIn_MeanRelErrorOut__Barrel"))
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MeanRelErrorIn_MeanRelErrorOut__Endcap"))
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MeanOut_MeanRelErrorOut__eta_05_07"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_Eta_MeanOut_MeanRelErrorOut"), ['yx', 'zx', 'zy'])

ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MomentumRelErrorOutMaxWeight_eta"), ['xy', 'zx', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_MomentumOutMaxWeight_eta"), ['xy', 'zx', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MomentumRelErrorOutMaxWeight_MomentumOutMaxWeight_eta__PoPtrue_09_11"), ['xy', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_RelGSFpdiff_ModeOut_eta"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtOut_eta"), ['xy', 'xz', 'yz'])


ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__3HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__4HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__5HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG40__6HITS"), ['yx', 'xz', 'yz'])

ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__3HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__4HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__5HITS"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_MCPtout_ModePtout_eta__BIG60__6HITS"), ['yx', 'xz', 'yz'])



ProduceCorrelationPlots(file.Get("demo/h_MCPout_ModeOut_eta"), ['yx', 'xz', 'yz'])
ProduceCorrelationPlots(file.Get("demo/h_Gfbrem_ModeOut_eta"), ['yx', 'zx', 'yz'])


def SaveSlicePlots(hist, projectionAxis="yx") :

    result = SlicePlots(hist, projectionAxis) 

    subfolderName = outputFolderName + '//' + hist.GetName()

    if not os.path.exists(subfolderName):
                os.makedirs(subfolderName)

    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    for h in result :
        h.Draw()
        filename = h.GetName()
        for fileFormat in savedFileFormats :
            canvas.Print(subfolderName +  '//' + filename + fileFormat)


def SlicePlots(hist, projectionAxis = 'yx', numberOfSlices = 10) :
    if projectionAxis == '' :
        projectedHisto = hist
        result = SliceHistogram(projectedHisto,'z', numberOfSlices)
    else :
        projectedHisto = hist.Project3D(projectionAxis)
        result = SliceHistogram(projectedHisto,'x', numberOfSlices)
    
    return result


def SuperimposePeaks(hist1, hist2, projectionAxis = 'yz', numberOfSlices = 10, windowForIntegral = 0.1) :

    colorList = [ROOT.kRed, ROOT.kBlue]
    SetColors(hist1, colorList[0])
    SetColors(hist2, colorList[1])

    slices1 = SlicePlots(hist1, projectionAxis, numberOfSlices)
    slices2 = SlicePlots(hist2, projectionAxis, numberOfSlices)
    
    print slices1
    print slices2
    slices = [slices1, slices2]
    
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )
    for sliceNumber in range(0, numberOfSlices) :
        statsboxList = [] 
        stack = ROOT.THStack("stack", "test")
        for histSlice in range(0,2):# len(slices) - 1) :
            print 'sliceNumber ', sliceNumber, ' histSLice ', histSlice
            temp = slices[histSlice]
            hist = temp[sliceNumber]
            mean = hist.GetMean()
            beta = 0;1 - hist.GetXaxis().GetBinCenter(hist.GetMaximumBin())
            alpha = 1. /  hist.GetXaxis().GetBinCenter(hist.GetMaximumBin())  #mean
            
            nbins = hist.GetXaxis().GetNbins();
            newHist = hist.Clone()
            newHist.Reset()
            newHist.Rebin(4)
            print 'Smoothing'
            #newHist.Smooth(100)
            for ibin in range(0, nbins - 1) : 
                y = hist.GetBinContent(ibin)
                x = hist.GetXaxis().GetBinCenter(ibin)
                xnew = alpha*x + beta
                newHist.Fill(xnew,y)
            stack.Add(newHist)
            newHist.Draw()
            #plotSlices.append(newHist)
            canvas.Update()
            statsbox = newHist.GetListOfFunctions().FindObject("stats")
            statsboxList.append(statsbox)

        subfolderName = outputFolderName + '//SupPos_' + hist1.GetName()
        #for h in plotSlices :
        stack.Draw("HISTNOSTACK")
        
        #rootList = stack.GetHists()

        #print rootList.At(0)

        #->Update(); //to for the generation of the 'stat" boxes 
        for i in range(0, len(statsboxList) ) :
            box = statsboxList[i]
            box.SetX1NDC(.7 - i * .3)
            box.SetX2NDC(.5 - i * .3)
            box.SetTextColor(colorList[i])
            box.Draw("SAME")


        #st1 = rootList.At(0).GetListOfFunctions().FindObject("stats"); 
        #st2 = rootList.At(1).GetListOfFunctions().FindObject("stats"); 
        #st1.SetX1NDC(.5); st1.SetX2NDC(.7); 
        #st2.SetX1NDC(.2); st2.SetX2NDC(.4); 
        #canvas.Modified(); 

        
        filename = slices[0][sliceNumber].GetName()
        if not os.path.exists(subfolderName):
            os.makedirs(subfolderName)
        
        for fileFormat in savedFileFormats :
            canvas.Print(subfolderName +  '//' + filename + fileFormat)


SuperimposePeaks(file.Get("demo/h_Gfbrem_1MinPoutOverMCPout_eta"),
                 file.Get("demo/h_MCPtout_ModePoutOverMCPout_eta"),
                 projectionAxis = 'yz')

SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__3HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__4HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__5HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG40__6HITS"), projectionAxis = 'yz')

SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__3HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__4HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__5HITS"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_Gfbrem_ModePoutOverMCPout_eta__BIG60__6HITS"), projectionAxis = 'yz')

SaveSlicePlots(file.Get("demo/h_Gfbrem_1MinPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_2MinPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_3MinPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_4MinPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_5MinPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_6MinPoutOverMCPout_eta"), projectionAxis = 'yz' )

SaveSlicePlots(file.Get("demo/h_Gfbrem_1MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_2MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_3MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_4MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_5MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )
SaveSlicePlots(file.Get("demo/h_Gfbrem_6MaxWeightPoutOverMCPout_eta"), projectionAxis = 'yz' )

SaveSlicePlots(file.Get("demo/h_MCPtout_ModePoutOverMCPout_eta"), projectionAxis = 'yz')
SaveSlicePlots(file.Get("demo/h_RecHitsOfConversionLeg_BBInvPtIn_eta"), projectionAxis = 'xz')

SaveSlicePlots(file.Get("demo/h_Gfbrem_ModeFbrem_eta"))

SaveSlicePlots(file.Get("demo/h_Gfbrem_GSFchi2red_eta"))


SaveSlicePlots(file.Get("demo/h_Eta_MeanRelErrorIn_MeanRelErrorOut"), projectionAxis = "zy")

def SaveScatterPlot(hist) :

    filename = hist.GetName()
    canvas= ROOT.TCanvas( 'c1', 'Test', 200, 10, 700, 500 )    

    hist.Draw('CONT')
    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + filename + fileFormat)

def SaveScatterPlotYX(hist) :
    histYX = hist.Project3D("yx")
    SaveScatterPlot(histYX)

SaveScatterPlotYX(file.Get("demo/h_Gfbrem_ModeFbrem_eta"))



histo = file.Get("demo/p_fbremMC_ptintModeRelError")

def SaveVertexPositionPlot() :
    histo = file.Get("demo/h_VertexPosition_Z_R")
    histo.SetStats(False)
    canvas = ROOT.TCanvas( 'c1', 'Test', 200, 10, 2000, 1000 )
    histo.SetMarkerSize(0.04)
    histo.Draw()
    histo.GetYaxis().SetTitleOffset(0.75)
    histo.GetYaxis().SetRangeUser(0.,130.)
    histo.Draw()
    for fileFormat in savedFileFormats :
        canvas.Print(outputFolderName + '//' + histo.GetName() + fileFormat)


SaveVertexPositionPlot()
