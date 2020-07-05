import uproot, numpy as np, argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import gc

psr = argparse.ArgumentParser()
psr.add_argument('-p', dest="pd", nargs='+', help="input protondecay root file")
psr.add_argument('-b', dest="bkg", nargs='+', help="input atmosphere neutrino root file")
psr.add_argument("-o", dest="opt", help="output")


args = psr.parse_args()
print(args)
pdqedep = uproot.lazyarray(args.pd, "evtinfo", "Qedep")
bkgqedep = uproot.lazyarray(args.bkg, "evtinfo", "Qedep")
pdf=PdfPages(args.opt)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
pdentries=len(pdqedep)
bkgentries=len(bkgqedep)
# = uproot.lazyarray(args.ipt, "evtinfo", "")
print('100MeV-650MeV:{},{:.4f}'.format(pdqedep[(pdqedep<650)&(pdqedep>100)].shape,pdqedep[(pdqedep<650)&(pdqedep>100)].shape[0]/pdentries))
print('200MeV-600MeV:{},{:.4f}'.format(pdqedep[(pdqedep<600)&(pdqedep>200)].shape,pdqedep[(pdqedep<600)&(pdqedep>200)].shape[0]/pdentries))
print('100MeV-150MeV:{},{:.4f}'.format(pdqedep[(pdqedep<150)&(pdqedep>100)].shape,pdqedep[(pdqedep<150)&(pdqedep>100)].shape[0]/pdentries))
print('150MeV-200MeV:{},{:.4f}'.format(pdqedep[(pdqedep<200)&(pdqedep>150)].shape,pdqedep[(pdqedep<200)&(pdqedep>150)].shape[0]/pdentries))
print('600MeV-650MeV:{},{:.4f}'.format(pdqedep[(pdqedep<650)&(pdqedep>600)].shape,pdqedep[(pdqedep<650)&(pdqedep>600)].shape[0]/pdentries))
print('650MeV-750MeV:{},{:.4f}'.format(pdqedep[(pdqedep<750)&(pdqedep>650)].shape,pdqedep[(pdqedep<750)&(pdqedep>650)].shape[0]/pdentries))

print('100MeV-650MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<650)&(bkgqedep>100)].shape,bkgqedep[(bkgqedep<650)&(bkgqedep>100)].shape[0]/bkgentries))
print('200MeV-600MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<600)&(bkgqedep>200)].shape,bkgqedep[(bkgqedep<600)&(bkgqedep>200)].shape[0]/bkgentries))
print('100MeV-150MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<150)&(bkgqedep>100)].shape,bkgqedep[(bkgqedep<150)&(bkgqedep>100)].shape[0]/bkgentries))
print('150MeV-200MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<200)&(bkgqedep>150)].shape,bkgqedep[(bkgqedep<200)&(bkgqedep>150)].shape[0]/bkgentries))
print('600MeV-650MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<650)&(bkgqedep>600)].shape,bkgqedep[(bkgqedep<650)&(bkgqedep>600)].shape[0]/bkgentries))
print('650MeV-750MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<750)&(bkgqedep>650)].shape,bkgqedep[(bkgqedep<750)&(bkgqedep>650)].shape[0]/bkgentries))
pdqedep=pdqedep[(pdqedep<650)&(pdqedep>150)]
bkgqedep=bkgqedep[(bkgqedep<650)&(bkgqedep>150)]
pdentries=len(pdqedep)
bkgentries=len(bkgqedep)

statisticString = 'pdentries={}\n$\sigma={:.2f}$\nbkgentries={}\n$\sigma={:.2f}$'
print('select in 100-650')
print('100MeV-650MeV:{},{:.4f}'.format(pdqedep[(pdqedep<650)&(pdqedep>100)].shape,pdqedep[(pdqedep<650)&(pdqedep>100)].shape[0]/pdentries))
print('200MeV-600MeV:{},{:.4f}'.format(pdqedep[(pdqedep<600)&(pdqedep>200)].shape,pdqedep[(pdqedep<600)&(pdqedep>200)].shape[0]/pdentries))
print('100MeV-150MeV:{},{:.4f}'.format(pdqedep[(pdqedep<150)&(pdqedep>100)].shape,pdqedep[(pdqedep<150)&(pdqedep>100)].shape[0]/pdentries))
print('150MeV-200MeV:{},{:.4f}'.format(pdqedep[(pdqedep<200)&(pdqedep>150)].shape,pdqedep[(pdqedep<200)&(pdqedep>150)].shape[0]/pdentries))
print('600MeV-650MeV:{},{:.4f}'.format(pdqedep[(pdqedep<650)&(pdqedep>600)].shape,pdqedep[(pdqedep<650)&(pdqedep>600)].shape[0]/pdentries))
print('650MeV-750MeV:{},{:.4f}'.format(pdqedep[(pdqedep<750)&(pdqedep>650)].shape,pdqedep[(pdqedep<750)&(pdqedep>650)].shape[0]/pdentries))

print('100MeV-650MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<650)&(bkgqedep>100)].shape,bkgqedep[(bkgqedep<650)&(bkgqedep>100)].shape[0]/bkgentries))
print('200MeV-600MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<600)&(bkgqedep>200)].shape,bkgqedep[(bkgqedep<600)&(bkgqedep>200)].shape[0]/bkgentries))
print('100MeV-150MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<150)&(bkgqedep>100)].shape,bkgqedep[(bkgqedep<150)&(bkgqedep>100)].shape[0]/bkgentries))
print('150MeV-200MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<200)&(bkgqedep>150)].shape,bkgqedep[(bkgqedep<200)&(bkgqedep>150)].shape[0]/bkgentries))
print('600MeV-650MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<650)&(bkgqedep>600)].shape,bkgqedep[(bkgqedep<650)&(bkgqedep>600)].shape[0]/bkgentries))
print('650MeV-750MeV:{},{:.4f}'.format(bkgqedep[(bkgqedep<750)&(bkgqedep>650)].shape,bkgqedep[(bkgqedep<750)&(bkgqedep>650)].shape[0]/bkgentries))
fig, ax = plt.subplots()

ax.set_title('Qedep distribution')
ax.hist(pdqedep, bins=100, histtype='step',density=True,label='protondecay')
ax.hist(bkgqedep, bins=100, histtype='step',density=True, label='AN background')
ax.set_xlabel('Qedep/MeV')
ax.set_ylabel('entries')
ax.text(0.05,0.95, statisticString.format(len(pdqedep),np.std(np.array(pdqedep)),len(bkgqedep),np.std(np.array(bkgqedep))), transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
ax.legend()
pdf.savefig()
plt.close()

fig, ax = plt.subplots()
ax.set_title('Qedep distribution cdf')
ax.hist(pdqedep, cumulative=True, density=True, bins=100, histtype='step', label='protondecay')
ax.hist(bkgqedep, cumulative=True, density=True, bins=100, histtype='step', label='AN background')
ax.set_xlabel('Qedep/MeV')
ax.set_ylabel('entries')
ax.legend()
pdf.savefig()
plt.close()

pdf.close()


