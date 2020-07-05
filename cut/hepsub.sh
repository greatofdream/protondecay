hepsub=$1
echo ${hepsub}
shift 1
echo $@
scriptfile=$1
shift 1
heplog=$1
shift 1
# scriptfile=$2
# scriptfile="${scriptfile%.*}.sh"
echo "ulimit -v" >${scriptfile}
echo $@ >> ${scriptfile}
chmod +x ${scriptfile}
echo "${hepsub} ${scriptfile} ${heplog}"
${hepsub} ${scriptfile} ${heplog}
