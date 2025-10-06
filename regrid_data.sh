#!/bin/bash

# Script to regrid specified dataset type(s) and optionally filter by year/month
# Usage: ./regrid.sh DATASET_ID1 [DATASET_ID2 ...] [YEAR] [MONTH]
# Example: ./regrid.sh OSTIA FMI_SMHI 2023 01
set -euo pipefail

# --- Parse arguments ---
if [ "$#" -lt 4 ]; then
    echo "Usage: $0 START_DATE END_DATE \"ID1 ID2 ...\" HEMISPHERE"
    exit 1
fi

START_DATE=$1
END_DATE=$2
IDS_STR=$3
HS=$4

# Convert space-separated IDs into an array
IFS=' ' read -r -a DATASET_IDS <<< "$IDS_STR"

# --- Debug print ---
echo "Start date : $START_DATE"
echo "End date   : $END_DATE"
echo "IDs        : ${DATASET_IDS[*]}"
echo "Hemisphere : $HS"

#for arg in "$@"; do
#    if [[ "$arg" =~ ^[0-9]{4}$ ]]; then
#        YEAR=$arg
#    elif [[ "$arg" =~ ^[0-9]{2}$ ]]; then
#        MONTH=$arg
#    else
#        DATASET_IDS+=("$arg")
#    fi
#done

#if [ ${#DATASET_IDS[@]} -eq 0 ]; then
#    echo "ERROR: No dataset ID provided."
#    echo "Usage: $0 DATASET_ID [DATASET_ID2 ...] [YEAR] [MONTH]"
#    exit 1
#fi

#target="grid_target"  # Replace with actual grid target if needed

for ID in "${DATASET_IDS[@]}"; do
    echo "Processing dataset: $ID"

    if [ "$ID" == "OSTIA" ]; then
        BASEPATH="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data"
        SAVEPATH="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data"
    else
        BASEPATH="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data"
        SAVEPATH="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data"
    fi

    DATAPATH="$BASEPATH/$ID"
    echo "Data path: $DATAPATH"
    echo "Save path: $SAVEPATH"

    case $ID in
        OSTIA|OSI458_TU|OSI450a_TU|NOAA_NSIDC_v4)
            target=/dmidata/users/ilo/projects/SST_SIC_PIA/bash_scripts/grid_$HS
	    for year_dir in "$DATAPATH"/*; do
                [ -d "$year_dir" ] || continue
                year=$(basename "$year_dir")
                [[ -n "$YEAR" && "$year" != "$YEAR" ]] && continue

                for month_dir in "$year_dir"/*; do
                    [ -d "$month_dir" ] || continue
                    month=$(basename "$month_dir")
                    [[ -n "$MONTH" && "$month" != "$MONTH" ]] && continue
		    if [ "$ID" == "OSTIA" ]; then
		    	specification="$month_dir"/*.nc
		    else
			specification="$month_dir"/*$HS*.nc
		    fi

                    for file in $specification; do
                        filename=$(basename "$file")
			
			if [ "$ID" == "NOAA_NSIDC_v4" ]; then
			    echo "assigning grid and landmask, removing unnesesary varibales"
			    grid=/dmidata/projects/cmems2/C3S/nsidc/regrid/grid_$HS.txt
			    echo $grid
			    cdo -setgrid,$grid $file "${file/.nc/_gridded.nc}"
			    file="${file/.nc/_gridded.nc}"
			    file=$file
			    filename=$(basename "$file")
			    ncks -A -v landmask /dmidata/users/ilo/projects/SST_SIC_PIA/bash_scripts/G02202-cdr-ancillary-$HS.nc $file
                            ncks -x -v melt_onset_day_cdr_seaice_conc,temporal_interpolation_flag,spatial_interpolation_flag $file $SAVEPATH/$ID/out_$HS.nc
			    mv $SAVEPATH/$ID/out_$HS.nc $file
			    
			fi

                        if [ "$ID" == "OSTIA" ]; then
                            echo "Splitting OSTIA file into NH and SH: $file to $SAVEPATH/$ID/NH/$year/$month/$filename"
                            mkdir -p "$SAVEPATH/$ID/NH/$year/$month" "$SAVEPATH/$ID/SH/$year/$month"
                            cdo -sellonlatbox,-180,180,0,90 "$file" "$SAVEPATH/$ID/NH/$year/$month/$filename"
                            cdo -sellonlatbox,-180,180,-90,0 "$file" "$SAVEPATH/$ID/SH/$year/$month/$filename"
		        #elif [ "$ID" == "NOAA_NSIDC_v4" ]; then
                        #    echo "Regridding OSI458_TU file: $file"
                        #    mkdir -p "$SAVEPATH/$ID/$year/$month"
                        #    ofile="$SAVEPATH/$ID/$year/$month/${filename%.*}_orig.nc"
                        #    cdo -remapbil,$target "$file" "$ofile"
                        #    nccopy -d9 "$ofile" "${ofile/_orig.nc/.nc}"
			#    rm $ofile
			else
			    echo "Regridding $ID file: $file"
		      	    mkdir -p "$SAVEPATH/$ID/$year/$month"
			    ofile="$SAVEPATH/$ID/$year/$month/${filename%.*}_orig.nc"
			    cdo -remapbil,$target "$file" "$ofile"
			    nccopy -d9 "$ofile" "${ofile/_orig.nc/.nc}"
			    rm $ofile
                        fi
                    done
                done
            done
            ;;

        FMI_SMHI|BALTIC_SIC)
	    target=/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/FMI_SMHI/2014/ice_conc_baltic_201401011400_comp.nc
            for year_dir in "$DATAPATH"/*; do
                [ -d "$year_dir" ] || continue
                year=$(basename "$year_dir")
                [[ -n "$YEAR" && "$year" != "$YEAR" ]] && continue

                for file in "$year_dir"/*; do
		    echo $file
		    [[ "$file" =~ _\([0-9]+\)\.nc$ ]] && continue  # skip files like _(1).nc
                    echo "Regridding $ID file: $file"
                    filename=$(basename "$file")
                    mkdir -p "$SAVEPATH/$ID/$year"
                    ofile="$SAVEPATH/$ID/$year/$filename"
                    cdo -remapnn,$target "$file" "$ofile"
                    nccopy -d9 "$ofile" "${ofile%.*}.nc"
                done
            done
            ;;

        NIC)
	    target=/dmidata/users/ilo/projects/SST_SIC_PIA/bash_scripts/grid_nh
            for file in "$DATAPATH"/*${YEAR}${MONTH}*; do
                echo "Regridding NIC file: $file"
                mkdir -p "$SAVEPATH/$ID"
		filename=$(basename "$file")
		basename_noext="${filename%.*}"
		tmpfile="$SAVEPATH/$ID/$YEAR/${basename_noext}_tmp.nc"
		finalfile="$SAVEPATH/$ID/$YEAR/${basename_noext}.nc"

		# Remap and compress
		cdo -remapnn,$target "$file" "$tmpfile"
		nccopy -d9 "$tmpfile" "$finalfile"

		# remove the temp file
		rm "$tmpfile"
            done
            ;;

        *)
            echo "ERROR: Unknown dataset ID: $ID"
            exit 2
            ;;
    esac

    echo "Regridding for $ID complete."
done

