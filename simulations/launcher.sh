#!/bin/bash

for file in *.data; do
    dir=${file%.data}
    (

	lmp -v name "${dir}" \
	    -v dataFile "${file}" \
	    -v Structure "${dir}" \
	    -v seed_v "${seedV}" \
	    -v seed_l "${seedL}" \
	    -log "${dir}.min.log" \
	    -in minimization.lmp > /dev/null
	
	echo "lmp: minimization ${dir} exited with code $?"

	#for reproducing the calculation used in thes paper use
	# for ico 309
	# 	seedV=18631
    # 	seedL=31922
	# for to 309_9_4
	# 	seedV=2772
    # 	seedL=20750
	# for dh 348_3_2_3
	# 	seedV=27839
    # 	seedL=19921
    seedV=$RANDOM
    seedL=$RANDOM
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
		-in thermalization.lmp > /dev/null
	    
	    echo "lmp: thermalization ${simName} exited with code $?"

	    lmp -v name "${dir}" \
		-v dataFile "${file}" \
		-v simName "${simName}" \
		-v seed_v "${seedV}" \
		-v seed_l "${seedL}" \
		-v Temp "${Temp}" \
		-log "${simName}.log" \
		-in start.lmp > /dev/null
	    
	    echo "lmp: production ${simName} exited with code $?"
	) &
    done
done
