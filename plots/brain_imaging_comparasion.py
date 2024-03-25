import matplotlib.pyplot as plt
import numpy as np

values = np.array([
    (0,0,"EEG/MEG", 1, 1),
    (1,1,"EEG Wewnątrzczaszkowe", 1, 1), 
    (2,2,"Obrazowanie optyczne", 1, 1), 
    (3,3,"Ultrasonograf funkcjonalny",1, 1), 
    (4,4,"fNIRS",1, 1),
    (5,5,"fMRI",1, 1),
    (6,6,"PET",1, 1)
    ])


plt.xlim(1e-2, 1e6)
plt.ylim(1e-3, 1e2)
plt.yscale('log')
plt.xscale('log')
plt.scatter(values[:, 0], values[:, 1], c='black')
for x, y, label, yrange, xrange in values:
    x = int(x)
    y = int(y)
    xrange = int(xrange)
    yrange = int(yrange)
    plt.errorbar(x, y, yerr=int(yrange), xerr=int(xrange), fmt='o', ecolor='black')
    plt.annotate(label, xy=(x, y))
plt.show()