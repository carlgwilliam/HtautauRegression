import numpy as np
import matplotlib.pyplot as plt

def find_sample_number(samples, mass):
    idx = [mass in d for d in samples].index(True)
    return idx

def find_indices(samples, aux, aux_labels, mass):
    isample = aux_labels.index("sample")
    idx = find_sample_number(samples, str(mass))
    return [(a==idx)[isample] for a in aux]

def plot_mass(m = None, mmmc = None, msv = None, mtrue = None, bins = np.linspace(50, 200, 100), 
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
        
        # if scale_true:
        #     counts, _ = np.histogram(mtrue, bins = len(bins), range = (bins[0], bins[-1]))
        #     counts = counts/float(sum(counts))
        #     scale = ymax/max(counts)
        #     mtrue_scaled = mtrue * scale
        
        
        counts, bins2 = np.histogram(mtrue, bins = len(bins), range = (bins[0], bins[-1]))
        counts = counts/(sum(counts) * (bins[1] - bins[0]))
        counts = counts * true_scale
        y, x, polys = plt.hist(bins2[:-1], bins, weights=counts, fill = None, histtype = "step",
                               label = "True" + (rf" $\times$ {true_scale}" if true_scale != 1 else ""))    
        #scale2 = ymax/max(y)
        #print(scale2)
        #polys[0].set_xy([[x,y*scale] for x, y in polys[0].get_xy()])

    plt.xlabel("M [GeV] ")
    plt.ylabel("A.U")
    plt.legend()
    plt.show()