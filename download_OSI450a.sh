#!/bin/bash

# PART 1: DOWNLOAD OSI458 timely update - be aware that this is not an official dataproduct! lagtime 2 days

# read date for processing

years=( 2025 )
months=$(seq 1 12)
days=$(seq 1 31)

# PATHS
OSI458_TU_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU
OSI450a_TU_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450a_TU
NIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NIC/shapefiles
BALTIC_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/BALTIC_SIC
BALTIC_SIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/FMI_SMHI
GLB_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA

for y in $years; do
        echo $y
        mkdir /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450a_TU/$y
        for m in $months; do
                if [ "$m" -lt "10" ]; then
                        m=0$m
                fi
                echo $m
                mkdir /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450a_TU/$y/$m
                cd /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450a_TU/$y/$m
                for d in $days; do
                        if [ "$d" -lt "10" ]; then
                                d=0$d
                        fi
                        echo $d 
                        #url_nh=https://thredds.met.no/thredds/fileServer/carra2sic/$y/$m/ice_conc_nh_ease2-250_dm1-amsr2_"$y$m$d"1200.nc
                        #wget $url_nh
                        url_sh=https://thredds.met.no/thredds/fileServer/carra2sic/$y/$m/ice_conc_sh_ease2-250_dm1-amsr2_"$y$m$d"1200.nc
                        #https://thredds.met.no/thredds/catalog/carra2sic/2025/01/catalog.html
                        wget $url_sh
                done
                cd /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI450aa_TU/
        done
done

