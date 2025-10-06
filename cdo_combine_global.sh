#!/bin/bash

#years=$(seq 2013 2023)
years=("2025")
months=$(seq 1 5)
#months=("7") # "4" "5" "6")
for y in $years; do
	#rm -r /dmidata/projects/nckf-sat/SIC/CARRA2_data/filtered_SIC_data/with_icechart_filtering/GLOBAL_final/$y
	#mkdir /dmidata/projects/asip-cms/SIC/CARRA2_data/filtered_SIC_data/with_icechart_filtering/GLOBAL_final/$y
        #if [ "$y" -eq "1983" ]; then
	#	mkdir /dmidata/projects/cmems2/C3S/OSI450a/$y
        #        squashfuse /dmidata/projects/cmems2/C3S/OSI450a/$y.sqfs /dmidata/projects/cmems2/C3S/OSI450a/$y
	#fi
	
	for m in $months; do
		echo $m	
		if [ "$m" -lt "10" ]; then
			m=0"$m"
		fi

		outputdir=/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final_GBL/$y/$m
		mkdir -p $outputdir
		
		input_directory_NH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/$y/$m
		input_directory_SH=/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/$y/$m

		files_nh=( $( ls $input_directory_NH/*nh*) )
		files_sh=( $( ls $input_directory_SH/*sh*) )
		
		for index in "${!files_nh[@]}"; do
			echo $index
			#if [[ "$index" -gt "9" ]] && [[ "$index" -lt "11" ]] ; then
			#if [ "$index" -gt "29" ] ; then

				file_nh="${files_nh[index]}"
				file_sh="${files_sh[index]}"
		
				echo $file_nh
				echo $file_sh

                		## Description of gridsize
                		echo enlargegrid
				myentiregrid=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/GLOBAL_GRID.nc
				cdo enlargegrid,$myentiregrid  $file_nh $outputdir/tmpfile	
		
				day_count=$(($index + 1))
				if [ "$day_count" -lt "10" ]; then
					day=0"$day_count"
				else
					day="$day_count"
				fi
				echo $day
				echo mergegrid
				ofile=$outputdir/dmisic_gbl_$y$m.nc
				if [ -f "$ofile" ]; then
					rm $ofile
				fi
				cdo mergegrid $outputdir/tmpfile $file_sh $ofile
				#cdo selname,lat_bnds $ofile ${ofile%.*}o.nc
				#ncatted -O -a bounds,,d,, $ofile

				nccopy -d9 $ofile ${ofile%.*}${day}_test.nc
				
				#ncks -C -O -x -v lat_bnds,lon_bnds ${ofile%.*}$day.nc ${ofile%.*}$day.nc
				#cdo selname,lat_bnds ${ofile%.*}$day.nc ${ofile%.*}o.nc
				#ncatted -O -a bounds,,d,, ${ofile%.*}$day.nc 
				rm -r $ofile
				rm -r $outputdir/tmpfile
			#fi

		done
	done
done

