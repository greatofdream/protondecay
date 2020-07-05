import uproot, numpy as np, argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import gc

def getPeakWalk(hcount, hbins, delta=1, pdf=None):
    smoothCount = np.zeros(hcount.shape)
    smoothBin = (hbins[0:len(hcount)]+hbins[1:])/2
    deltaCount = np.zeros(hcount.shape)
    peakPos = []
    for i in range(delta, len(hcount)-delta):
        smoothCount[i] = np.mean(hcount[(i-delta):(i+delta+1)])
        deltaCount[i-1] = smoothCount[i] - smoothCount[i-1]
    cursor = smoothCount[delta]
    flag = 0
    for i in range(delta, len(hcount)-delta):
        if flag==0:
            if (deltaCount[(i-2):i]>2).all():
                flag = 1
        elif flag==1:
            if np.sum((deltaCount[i:(i+3)]<0)!=0)>2:
                flag = 0
                peakPos.append(smoothBin[i])
    if pdf:
        fig, ax = plt.subplots()
        ax.plot(smoothBin,smoothCount,color='b',label='smooth')
        ax.plot(smoothBin, hcount, color='k', alpha=0.5, label='origin wave')
        for p in peakPos:
            ax.axvline(p, label='estimate peak', color='g')
        ax.text(0.05,0.95, 'estimate peak:{}'.format(peakPos), verticalalignment='top')
        ax.set_title('smooth hitTime')
        ax.set_xlabel('hitTime/ns')
        ax.set_ylabel('entries')
        ax.set_xlim(left=0, right=1500)
        ax.legend()
        pdf.savefig()
        plt.close()
    return peakPos
psr = argparse.ArgumentParser()
psr.add_argument('-p', dest="pd", nargs='+', help="input protondecay root file")
psr.add_argument("-o", dest="opt", help="output")


args = psr.parse_args()
print(args)
iptFiles = args.pd
qedep = uproot.lazyarray(iptFiles[0], "evtinfo", "Qedep")
hitTimeSingle = uproot.lazyarray(iptFiles[0], "evtinfo", "HitTimeSingle", basketcache=uproot.cache.ThreadSafeArrayCache("5 MB"))
r0 = uproot.lazyarray(iptFiles[0], 'evtinfo', 'r0')
kaonStopTime = uproot.lazyarray(iptFiles[0], 'evtinfo', 'KaonStopTime')
decayTime = uproot.lazyarray(iptFiles[0], 'evtinfo', 'DecayTime')
michelStartT = uproot.lazyarray(iptFiles[0], 'evtinfo', 'MichelStartT')
pdf=PdfPages(args.opt)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
entries=len(qedep)

statisticString = 'Qedep={:.2f}\nkaonStopTime={:.2f}\ndecayTime={:.2f}\nmicheleTime={}'
for i,(qe, ht, r, kst, dt, mst) in enumerate(zip(qedep, hitTimeSingle, r0, kaonStopTime, decayTime, michelStartT)):
    if i>20:
        break
    fig, ax = plt.subplots()
    ht = ht[(ht<10000)&(ht>0)]
    ax.set_title('r:{:.2f} hitTime(<10000) distribution'.format(r))
    hc, hbins = np.histogram(ht, bins=5000, range=(0, 10000))
    # smooth the wave and get the num and hit
    peakPos = getPeakWalk(hc, hbins, pdf=pdf)
    ax.hist(ht, bins=500, histtype='step',density=True,label='protondecay')
    ax.set_xlabel('hitTime/ns')
    ax.set_ylabel('entries')
    ax.text(0.05,0.95, statisticString.format(qe, kst, dt, mst), transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)
    for p in peakPos:
        ax.axvline(p, label='estimate peak', color='g')
    ax.legend()
    pdf.savefig()
    plt.close()

pdf.close()


