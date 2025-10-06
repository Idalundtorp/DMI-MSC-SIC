#!/bin/bash

# PART 1: DOWNLOAD OSI458 timely update - be aware that this is not an official dataproduct! lagtime 2 days

# read date for processing

years=( 2025 )
months=$(seq 5 12)
days=$(seq 1 31)

# PATHS
OSI458_TU_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU
NIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NIC/shapefiles
BALTIC_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/BALTIC_SIC
BALTIC_SIC_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/FMI_SMHI
GLB_SST_BASEPATH=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA

#for y in $years; do
#        echo $y
#        mkdir /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU/$y
#        for m in $months; do
#                if [ "$m" -lt "10" ]; then
#                        m=0$m
#                fi
#                echo $m
#                mkdir /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU/$y/$m
#                cd /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU/$y/$m
#                for d in $days; do
#                        if [ "$d" -lt "10" ]; then
#                                d=0$d
#                        fi
#                        echo $d 
#                        url_nh=https://thredds.met.no/thredds/fileServer/carra2sic/$y/$m/ice_conc_nh_ease2-250_dm1-amsr2_"$y$m$d"1200.nc
#                        wget $url_nh
#			url_sh=https://thredds.met.no/thredds/fileServer/carra2sic/$y/$m/ice_conc_sh_ease2-250_dm1-amsr2_"$y$m$d"1200.nc
#			#https://thredds.met.no/thredds/catalog/carra2sic/2025/01/catalog.html
#			wget $url_sh
#                done
#                cd /net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/OSI458_TU/
#        done
#done
#
## PART 2: DOWNLOAD NIC icecharts
#
## Spørg Niels eller Matilde om dette er stedet de downloader data fra
## http://wdc.aari.ru/datasets/d0032/arctic/2025/
## THIS IS INCORRECT 
#cd $NIC_BASEPATH || exit
#for year in "${years[@]}"; do
#  for month in $months; do
#    for day in $days; do
#      # Zero-pad month and day
#      mm=$(printf "%02d" "$month")
#      dd=$(printf "%02d" "$day")
#
#      # Check if the date is valid
#      if date -d "$year-$mm-$dd" >/dev/null 2>&1; then
#        yyyymmdd="${year}${mm}${dd}"
#        url="https://noaadata.apps.nsidc.org/NOAA/G10033/north/weekly/shapefile/nh_${yyyymmdd}.zip"
#        echo "Downloading $url"
#        wget -nc "$url"
#      fi
#    done
#  done
#done

# PART 3: DOWNLOAD Baltic SIC, Baltic SST and GBL SST - from copernicus marien data store - using python API

for y in "${years[@]}"; do
    mkdir -p "$BALTIC_SIC_BASEPATH/$y"
    mkdir -p "$BALTIC_SST_BASEPATH/$y"
    for m in $months; do
        mm=$(printf "%02d" "$m")
        for d in $days; do
            dd=$(printf "%02d" "$d")
            mkdir -p "$GLB_SST_BASEPATH/$y/$mm"

            # Run Python downloader script
            python3 /dmidata/users/ilo/projects/SST_SIC_PIA/run_engine/download_baltic.py \
                "$y" "$mm" "$dd" \
                "$BALTIC_SST_BASEPATH/$y" "$BALTIC_SIC_BASEPATH/$y" "$GLB_SST_BASEPATH/$y/$mm"
        done
    done
done

