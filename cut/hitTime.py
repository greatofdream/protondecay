import uproot, numpy as np, argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

psr = argparse.ArgumentParser()
psr.add_argument("ipt", nargs='+', help="input root file")
psr.add_argument("-o", dest="opt", help="output")

args = psr.parse_args()
print(args)
evtID = uproot.lazyarray(args.ipt, "evtinfo", "evtID")
hitTimeSingle = uproot.lazyarray(args.ipt, "evtinfo", "HitTimeSingle", basketcache=uproot.cache.ThreadSafeArrayCache("5 MB"))
r0 = uproot.lazyarray(args.ipt, 'evtinfo', 'r0')
print('hitTimeSingle.shape:{}'.format(len(hitTimeSingle)))

pdf = PdfPages(args.opt)
statisticString = 'entries={}\n$\mu={:.2f}$\n$\sigma={:.2f}$'
entries = len(evtID)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

for i, (eid, ht, r) in enumerate(zip(evtID, hitTimeSingle, r0)):
    if i>100:
        break
    ht = np.array(ht)
    fig, ax = plt.subplots()
    ax.hist(ht[ht<5000], bins=500)
    ax.set_title("evtID:{} r:{} hitTime distribution".format(eid, r))
    ax.set_xlabel('hitTime/ns')
    ax.set_ylabel('entries')
    ax.text(0.65,0.95, statisticString.format(entries,np.mean(ht[ht<5000]), np.std(ht[ht<5000])), transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    ax.set_yscale('log')
    pdf.savefig()
    plt.close()

pdf.close()



