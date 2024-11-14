import numpy as np
import matplotlib.pyplot as plt
import vector

def find_sample_number(samples, mass):
    idx = [f"_{mass}." in d for d in samples].index(True)
    return idx

def find_indices(samples, aux, aux_labels, mass):
    isample = aux_labels.index("sample")
    idx = find_sample_number(samples, str(mass))
    return [(a==idx)[isample] for a in aux]

def plot_mass(m = None, mmmc = None, msv = None, mtrue = None, mvis = None,
              bins = np.linspace(50, 200, 100), 
              title = "", true_scale = 1, logy = False):

    plt.figure()
    if title:
        plt.title(title)
        
    if logy:
        plt.yscale("log")
    
    ymax = 0
    
    if m is not None:
        mean = np.mean(m)
        std = np.std(m)

        y, x, _ = plt.hist(m, bins = bins, fill = None, histtype = "step", density = True,
                           label = f"XGB ($\mu$ = {mean:.1f}, $\sigma$ = {std:.1f})")
        ymax = max(y) if max(y) > ymax else ymax


    if mmmc is not None:
        mean_mmc = np.mean(mmmc)
        std_mmc = np.std(mmmc)
        y, x, _ = plt.hist(mmmc, bins = bins, fill = None, histtype = "step", density = True, 
                           label = f"MMC ($\mu$ = {mean_mmc:.1f}, $\sigma$ = {std_mmc:.1f})")  
        ymax = max(y) if max(y) > ymax else ymax
        
    if msv is not None:
        msv = msv[[not np.isnan(i) for i in msv]]
        
        mean_msv = np.mean(msv)
        std_msv = np.std(msv)
        y, x, _ = plt.hist(msv, bins = bins, fill = None, histtype = "step", density = True, 
                           label = f"SVFit ($\mu$ = {mean_msv:.1f}, $\sigma$ = {std_msv:.1f})")
        ymax = max(y) if max(y) > ymax else ymax
        
    if mtrue is not None:
        
        counts, bins2 = np.histogram(mtrue, bins = len(bins), range = (bins[0], bins[-1]))
        counts = counts/(sum(counts) * (bins[1] - bins[0]))
        counts = counts * true_scale
        y, x, polys = plt.hist(bins2[:-1], bins, weights=counts, fill = None, histtype = "step",
                               label = "True" + (rf" $\times$ {true_scale}" if true_scale != 1 else ""))    

    if mvis is not None:
        mean_vis = np.mean(mvis)
        std_vis = np.std(mvis)
        y, x, _ = plt.hist(mvis, bins = bins, fill = None, histtype = "step", density = True, 
                           label = f"Vis ($\mu$ = {mean_vis:.1f}, $\sigma$ = {std_vis:.1f})")  
        ymax = max(y) if max(y) > ymax else ymax
    
    plt.xlabel("M [GeV] ")
    plt.ylabel("A.U")
    plt.legend()
    plt.show()

def make_four_vector(varname, data, massidx = None):

    # Find variable indices 
    ipt = data.feature_names.index(f"{varname}_Pt")
    ieta = data.feature_names.index(f"{varname}_Eta")
    iphi = data.feature_names.index(f"{varname}_Phi")
    try:
        nme = "M"
        ime = data.feature_names.index(f"{varname}_M")
    except ValueError:
        nme = "E"
        ime = data.feature_names.index(f"{varname}_E")        

    # Get input features
    X = data.X()
    
    if massidx is None:
        vec = vector.array(
            {"pt"  : X[:, ipt], 
             "eta" : X[:, ieta], 
             "phi" : X[:, iphi], 
             nme   : X[:, ime]
            }
        )      
    else:
        vec = vector.array(
            {"pt"  : X[massidx, ipt], 
             "eta" : X[massidx, ieta], 
             "phi" : X[massidx, iphi], 
             nme   : X[massidx, ime]
            }
        )
    
    return vec


def make_met_vector(data, massidx = None):
    ipt  = data.feature_names.index(f"MET_Met")
    iphi = data.feature_names.index(f"MET_Phi")

    if massidx is None:
        vec = vector.array(
            {"pt"  : X[:, ipt],
             "phi" : X[:, iphi]
             }
        )
    else:
        vec = vector.array(
            {"pt"  : X[massidx, ipt],
             "phi" : X[massidx, iphi]
             }
        )

def collinear_mass(tau1, tau2, met):
    """
    Input are `vectors` for the two taus and the met 
    """
    
    pxMiss = met.px
    pyMiss = met.py
    
    pxLept = tau1.px
    pyLept = tau1.py
    pzLept = tau1.pz
    pLept  = tau1.energy
    
    pxTauJet = tau2.px
    pyTauJet = tau2.py
    pzTauJet = tau2.pz
    pTauJet  = tau2.energy
    
    rexy  = pyTauJet/pxTauJet;
    rex   = pxTauJet/pTauJet;
    rcx   = pxLept/pLept;
    rcy   = pyLept/pLept;
    ta    = pyMiss-rexy*pxMiss;
    tb    = rcy-rexy*rcx;
    eNu1  = ta/tb;
    eNu2  = (pxMiss-rcx*eNu1)/rex;

    eTau1 = pLept+eNu1;
    eTau2 = pTauJet+eNu2;
    cosTheta = (pxLept*pxTauJet + pyLept*pyTauJet + pzLept*pzTauJet) / (pLept*pTauJet);
    myTTmassd = 2. * eTau1 * eTau2 * (1. - cosTheta);
    myTTmassd = np.sqrt(myTTmassd);
    myTTmassd = np.nan_to_num(myTTmassd, -1)
    
    #ok = (eNu1 > 0) & (eNu2 > 0)
    
    return myTTmassd
