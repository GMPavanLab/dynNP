#!/bin/bash

doSimulations(){
    dir=${1%.data}
    file=$1
    (

        lmp -v name "${dir}" \
	    -v dataFile "${file}" \
	    -v Structure "${dir}" \
	    -v seed_v "${seedV}" \
	    -v seed_l "${seedL}" \
	    -log "${dir}.min.log" \
	    -in sim00_minimization.lmp > /dev/null
	
	echo "lmp: minimization ${dir} exited with code $?"
	)
    seedV=$2
    seedL=$3
    for Temp in 300 400 500; do
	simName="${dir}-SV_${seedV}-SL_${seedL}-T_${Temp}"
	(	    
	    lmp -v name "${dir}" \
		-v dataFile "${file}" \
		-v Structure "${dir}" \
		-v simName "${simName}" \
		-v seed_v "${seedV}" \
		-v seed_l "${seedL}" \
		-v Temp "${Temp}" \
		-log "${simName}.eq.log" \
		-in sim01_thermalization.lmp > /dev/null
	    
	    echo "lmp: thermalization ${simName} exited with code $?"

	    lmp -v name "${dir}" \
		-v dataFile "${file}" \
		-v simName "${simName}" \
		-v seed_v "${seedV}" \
		-v seed_l "${seedL}" \
		-v Temp "${Temp}" \
		-log "${simName}.log" \
		-in sim02_start.lmp > /dev/null
	    
	    echo "lmp: production ${simName} exited with code $?"
	) &
    done
}

# for file in *.data; do
#     seedV=$RANDOM
#     seedL=$RANDOM
# 	doSimulations "$file" "$seedV" "$seedL"
# done

#for reproducing the calculation used in this paper, please use
# for ico 309
# 	seedV=18631
# 	seedL=31922
# for to 309_9_4
# 	seedV=2772
# 	seedL=20750
# for dh 348_3_2_3
# 	seedV=27839
# 	seedL=19921

doSimulations ico309.data 18631 31922
doSimulations dh348_3_2_3.data 2772 20750
doSimulations to309_9_4.data 27839 19921