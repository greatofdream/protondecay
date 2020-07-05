.PHONY: all plot
psudoshell:=hep_sub -mem 
pdpath:=$(wildcard /junofs/users/junoprotondecay/guoyh/offlines/offline3745/simulation_result/SIG/ana/RawData/PDRawData_*.root)
bkgpath:=$(wildcard /junofs/users/junoprotondecay/guoyh/offlines/offline3745/simulation_result/BKG/ana/RawData/ANRawData_*.root)

all: python/p2vk.pdf
#	hep_sub -mem 2000 plot.sh
root/bkg.pdf:
	mkdir -p $(dir $@)
	$(psudoshell) rootscript.sh -argu "root/plotSpectrum.C" -o $@.log -e $@.err
energy/energy.pdf:
	./hepsub.sh "$(psudoshell) 4000" "-o $@.log -e $@.err" python3 energy.py -o $@ -p $(pdpath) -b $(bkgpath) >$@.log 2>&1

pulseNum/sigpulseNum.pdf:
	./hepsub.sh "$(psudoshell) 4096" $(notdir $@.sh) "-o $@.log -e $@.err" python3 pulse.py -o $@ -p $(pdpath) >$@.log 2>&1

pulseNum/bkgpulseNum.pdf:
	./hepsub.sh "$(psudoshell) 8192" $(notdir $@.sh) "-o $@.log -e $@.err" python3 pulse.py -o $@ -p $(bkgpath) >$@.log 2>&1


python/hit.pdf:
	$(psudoshell) ../script/hitTime.sh -argu '$@ $(datapath)' -o $@.log -e $@.err
