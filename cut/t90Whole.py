import uproot, numpy as np, argparse, h5py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import gc
'''
t90 whole use global maximum value as peak.
'''
def getT90WholeWalk(hcount, hbins, delta=1, pdf=None):
    smoothCount = np.zeros(hcount.shape)
    dt = hbins[1]-hbins[0]
    for i in range(delta, len(hcount)-delta):
        smoothCount[i] = np.mean(hcount[(i-delta):(i+delta+1)])
    smoothBin = (hbins[0:len(hcount)]+hbins[1:])/2
    maxPeakIndex = np.argmax(smoothCount)
    maxPeak = smoothCount[maxPeakIndex]
    flag = 0
    t1 = 0
    # just set a default big value to avoid extreme event. 
    t9 = 79
    for i in range(delta, maxPeakIndex+1):
        if smoothCount[i] >= 0.1*maxPeak:
            t1 = i
            break
    for i in range(maxPeakIndex, delta, -1):
        if smoothCount[i]<=0.9*maxPeak:
            t9 = i+1
            break

    if pdf:
        fig, ax = plt.subplots()
        ax.step(smoothBin,smoothCount,where='mid', color='b',label='smooth')
        ax.plot(smoothBin, hcount, color='k', alpha=0.5, label='origin wave')
        for p in peakPos:
            ax.vlines(p, 0, 10, label='estimate peak', color='g')
        ax.text(0.05,0.95, 'estimate peak:{}'.format(peakPos), verticalalignment='top')
        ax.set_title('smooth hitTime')
        ax.set_xlabel('hitTime/ns')
        ax.set_ylabel('entries')
        ax.set_xlim(left=0, right=1500)
        ax.legend()
        pdf.savefig()
        plt.close()
    return (t9-t1)*dt
psr = argparse.ArgumentParser()
psr.add_argument('-p', dest="pd", nargs='+', help="input protondecay root file")
psr.add_argument("-o", dest="opt", help="output")
psr.add_argument('-l', dest="log", help='whether direct log the result', default=False, type=bool)

args = psr.parse_args()
print(args)
iptFiles = args.pd
qedep = uproot.lazyarray(iptFiles[0], "evtinfo", "Qedep")
hitTimeSingle = uproot.lazyarray(iptFiles, "evtinfo", "HitTimeSingle", basketcache=uproot.cache.ThreadSafeArrayCache("5 MB"))
entries=len(hitTimeSingle)
if not args.log:
    pdf=PdfPages(args.opt)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    t90 = np.zeros((entries,))

    for i, ht in enumerate(hitTimeSingle):
        hc, hbins = np.histogram(ht, bins=10000, range=(0, 10000))
        # smooth the wave and get the num and hit
        t0 = getT90WholeWalk(hc, hbins, delta=0)

        t90[i] = t0
    fig, ax = plt.subplots()
    ax.set_title('T90 distribution')
    ax.hist(t90, bins=80, range=[0,80], histtype='step',label='w/o energy cut')
    ax.hist(t90[(qedep<600)&(qedep>200)], bins=80, range=[0,80], histtype='step',label='energy cut')
    ax.set_xlabel('t/ns')
    ax.set_ylabel('entries')
    ax.legend()
    pdf.savefig()
    plt.close()
    pdf.close()

    with h5py.File(args.opt+'.h5', 'w') as opt:
        opt.create_dataset('t90', data=t90, compression='gzip')
else:
    with h5py.File(args.opt+'.h5', 'r') as ipt:
        t90 = ipt['t90'][:]
EselectNum = len(qedep[(qedep<600)&(qedep>200)])

selectNum = len(t90[(t90>=13)&(qedep<600)&(qedep>200)])
print('total entries:{};select {} t90>=13: {:.4f};t90<13: {:.4f}'.format(entries, selectNum, selectNum/entries, 1-selectNum/entries))
print('total entries:{};select {} t90>=13: {:.4f};t90<13: {:.4f}'.format(EselectNum, selectNum, selectNum/EselectNum, 1-selectNum/EselectNum))
selectNum = len(t90[(t90>=9)&(qedep<600)&(qedep>200)])
print('total entries:{};select {} t90>=9: {:.4f};t90<9: {:.4f}'.format(entries, selectNum, selectNum/entries, 1-selectNum/entries))
print('total entries:{};select {} t90>=9: {:.4f};t90<9: {:.4f}'.format(EselectNum, selectNum, selectNum/EselectNum, 1-selectNum/EselectNum))
selectNum = len(t90[(t90>=10)&(qedep<600)&(qedep>200)])
print('total entries:{};select {} t90>=10: {:.4f};t90<10: {:.4f}'.format(entries, selectNum, selectNum/entries, 1-selectNum/entries))
print('total entries:{};select {} t90>=10: {:.4f};t90<10: {:.4f}'.format(EselectNum, selectNum, selectNum/EselectNum, 1-selectNum/EselectNum))
selectNum = len(t90[(t90>=11)&(qedep<600)&(qedep>200)])
print('total entries:{};select {} t90>=11: {:.4f};t90<11: {:.4f}'.format(entries, selectNum, selectNum/entries, 1-selectNum/entries))
print('total entries:{};select {} t90>=11: {:.4f};t90<11: {:.4f}'.format(EselectNum, selectNum, selectNum/EselectNum, 1-selectNum/EselectNum))
selectNum = len(t90[(t90>=12)&(qedep<600)&(qedep>200)])
print('total entries:{};select {} t90>=12: {:.4f};t90<12: {:.4f}'.format(entries, selectNum, selectNum/entries, 1-selectNum/entries))
print('total entries:{};select {} t90>=12: {:.4f};t90<12: {:.4f}'.format(EselectNum, selectNum, selectNum/EselectNum, 1-selectNum/EselectNum))

'''
total entries:10000;select 4511 t90>=13: 0.4511;t90<13: 0.548
total entries:9671;select 4511 t90>=13: 0.4664;t90<13: 0.5336

total entries:9671;select 4893 t90>13: 0.5059;t90<13: 0.4941
'''

