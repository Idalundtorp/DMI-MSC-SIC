#!/bin/bash

# PART 1: DOWNLOAD NSIDC

# read date for processing

years=(2023)
months=$(seq 1 12)
days=$(seq 1 31)

# PATHS
OSI458_TU_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU
OSI450a_TU_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450a_TU
NSIDC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NOAA_NSIDC_v4
NIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NIC/shapefiles
BALTIC_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/BALTIC_SIC
BALTIC_SIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/FMI_SMHI
GLB_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA

for y in "${years[@]}"; do
	echo "$y"
	mkdir -p $NSIDC_BASEPATH/$y
	
	for m in $months; do
		mm=$(printf "%02d" $m)
		echo "$mm"
		mkdir -p $NSIDC_BASEPATH/$y/$mm
		cd $NSIDC_BASEPATH/$y/$mm || exit

		for d in $days; do
			dd=$(printf "%02d" $d)
                	echo "$dd"
			filename="seaice_conc_daily_nh_${y}${mm}${dd}_f17_v04r00.nc"
                	url_sh="https://noaadata.apps.nsidc.org/NOAA/G02202_V4/north/daily/$y/$filename"
			wget $url_sh
		done
	cd $NSIDC_BASEPATH || exit
	done
done



