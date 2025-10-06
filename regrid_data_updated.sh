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
	    # Loop through files recursively
            #if [ "$ID" == "OSTIA" ]; then
            #	files=$(find "$DATAPATH" -type f -name "*.nc")
            #else
            #	files=$(find "$DATAPATH" -type f -name "*${HS}*.nc")
            #fi
	    if [ "$ID" == "OSTIA" ]; then
    		# add check to only look for files within start year and end year
		files=$(find "$DATAPATH" -mindepth 3 -maxdepth 3 -type f -regextype posix-extended -regex '.*/[0-9]{4}/[0-9]{2}/.*\.nc')
		# echo $files
	    else
		files=$(find "$DATAPATH" -mindepth 3 -maxdepth 3 -type f -regextype posix-extended -regex ".*/[0-9]{4}/[0-9]{2}/.*${HS}.*\.nc")
    		#files=$(find "$DATAPATH" -type f -regex ".*/[0-9]{4}/.*${HS}.*\.nc")
	    fi
	    #echo "FILES: $files"
	    #printf '%s\n' $files
	    for file in $files; do
            	# Extract YYYYMMDD from filename (adapt this depending on your naming convention)
		filename=$(basename "$file")
            	file_date=$(echo "$filename" | grep -oE '[0-9]{8}' | head -n1)

            	# Convert YYYYMMDD → YYYY-MM-DD
            	file_date_fmt=$(date -d "$file_date" +"%Y-%m-%d")

            	# Compare with START_DATE / END_DATE
		#echo "Checking $file_date_fmt against $START_DATE and $END_DATE"
            	if [[ "$file_date_fmt" < "$START_DATE" || "$file_date_fmt" > "$END_DATE" ]]; then
			continue
            	fi
                #echo "$file_date_fmt"
                year=$(date -d "$file_date_fmt" +%Y)
                month=$(date -d "$file_date_fmt" +%m)
	
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
		if [ "$ID" == "OSTIA" ] && [ "$HS" == "nh" ]; then # run only once and not for both hemispheres
		    # check if file exist - Only continue if the file does NOT exist
		    if [ ! -f "$SAVEPATH/$ID/NH/$year/$month/$filename" ]; then
  		    	echo "Splitting OSTIA file into NH and SH: $file to $SAVEPATH/$ID/NH/$year/$month/$filename"
                    	mkdir -p "$SAVEPATH/$ID/NH/$year/$month" "$SAVEPATH/$ID/SH/$year/$month"	
                    	cdo -sellonlatbox,-180,180,0,90 "$file" "$SAVEPATH/$ID/NH/$year/$month/$filename"
                    	cdo -sellonlatbox,-180,180,-90,0 "$file" "$SAVEPATH/$ID/SH/$year/$month/$filename"
		    fi
		else
	      	    mkdir -p "$SAVEPATH/$ID/$year/$month"
		    ofile="$SAVEPATH/$ID/$year/$month/${filename%.*}_orig.nc"
		    # check if file exist - Only continue if the file does NOT exist
		    if [ ! -f "${ofile/_orig.nc/.nc}" ]; then
			echo "Regridding $ID file: $file"
		    	cdo -remapbil,$target "$file" "$ofile"
		    	nccopy -d9 "$ofile" "${ofile/_orig.nc/.nc}"
		    	rm $ofile
		    else
			echo "Skipping: ${ofile/_orig.nc/.nc} already exists"
		    fi
                fi
            done
            ;;

        FMI_SMHI|BALTIC_SIC)
	    target=$SAVEPATH/FMI_SMHI/2014/ice_conc_baltic_201401011400_comp.nc
            # add check to only look for files within start year and end year
            files=$(find "$DATAPATH" -mindepth 2 -maxdepth 2 -type f -regextype posix-extended -regex '.*/[0-9]{4}/.*\.nc')
	    #echo $files
            for file in $files; do
                # Extract YYYYMMDD from filename (adapt this depending on your naming convention)
                filename=$(basename "$file")
                file_date=$(echo "$filename" | grep -oE '[0-9]{8}' | head -n1)

                # Convert YYYYMMDD → YYYY-MM-DD
                file_date_fmt=$(date -d "$file_date" +"%Y-%m-%d")

                # Compare with START_DATE / END_DATE
                if [[ "$file_date_fmt" < "$START_DATE" || "$file_date_fmt" > "$END_DATE" ]]; then
                        continue
                fi
                echo "$file_date_fmt"
                year=$(date -d "$file_date_fmt" +%Y)
                month=$(date -d "$file_date_fmt" +%m)

		[[ "$file" =~ _\([0-9]+\)\.nc$ ]] && continue  # skip files like _(1).nc
		mkdir -p "$SAVEPATH/$ID/$year"
		ofile="$SAVEPATH/$ID/$year/${filename%.*}_orig.nc"
		if [ ! -f "${ofile/_orig.nc/.nc}" ]; then
                	echo "Regridding $ID file: $file"
                	cdo -remapnn,$target "$file" "$ofile"
                	nccopy -d9 "$ofile" "${ofile/_orig.nc/.nc}"
		else
                        echo "Skipping: "${ofile/_orig.nc/.nc}" already exists"
                fi

            done
            ;;

        NIC)
	    target=/dmidata/users/ilo/projects/SST_SIC_PIA/bash_scripts/grid_nh

            #for file in "$DATAPATH"/*${YEAR}${MONTH}*; do
	    files=$(find "$DATAPATH" -mindepth 1 -maxdepth 1 -type f -regextype posix-extended -regex '.*/.*[0-9]{6}.*\.nc')
	    for file in $files; do
                # Extract YYYYMMDD from filename (adapt this depending on your naming convention)
                filename=$(basename "$file")
                file_date=$(echo "$filename" | grep -oE '[0-9]{8}' | head -n1)

                # Convert YYYYMMDD → YYYY-MM-DD
                file_date_fmt=$(date -d "$file_date" +"%Y-%m-%d")

                # Compare with START_DATE / END_DATE
		# Shift dates - create extended ranges to ensure that we regrid all relecant icecharts (updated biweekly)
		START_EXT=$(date -d "$START_DATE -14 days" +%Y-%m-%d)
		END_EXT=$(date -d "$END_DATE +14 days" +%Y-%m-%d)

                if [[ "$file_date_fmt" < "$START_EXT" || "$file_date_fmt" > "$END_EXT" ]]; then
                        continue
                fi
                year=$(date -d "$file_date_fmt" +%Y)
                month=$(date -d "$file_date_fmt" +%m)

                mkdir -p "$SAVEPATH/$ID"
		filename=$(basename "$file")
		basename_noext="${filename%.*}"
		tmpfile="$SAVEPATH/$ID/$year/${basename_noext}_tmp.nc"
		finalfile="$SAVEPATH/$ID/$year/${basename_noext}.nc"
		
                if [ ! -f $finalfile ]; then
                    echo "Regridding $ID file: $file"
		    cdo -remapnn,$target "$file" "$tmpfile"
                    nccopy -d9 "$tmpfile" "$finalfile"
		    # remove the temp file
                    rm "$tmpfile"
                else
                    echo "Skipping: $finalfile already exists"
		fi

		## Remap and compress
		#cdo -remapnn,$target "$file" "$tmpfile"
		#nccopy -d9 "$tmpfile" "$finalfile"

		## remove the temp file
		#rm "$tmpfile"
            done
            ;;

        *)
            echo "ERROR: Unknown dataset ID: $ID"
            exit 2
            ;;
    esac

    echo "Regridding for $ID complete."
done

