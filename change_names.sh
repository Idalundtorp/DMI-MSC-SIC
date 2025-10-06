
path="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/NH/2025/04"
for file in $path/*.nc; do
    file=$( basename "$file")
    # Extract date (YYYY-MM-DD)
    date_part=$(basename "$file" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
    date_formatted=$(echo "$date_part" | tr -d '-')  # e.g., 20250101

    # Decide on filename based on pattern
    if [[ "$file" == METOFFICE* ]]; then
        new_name="${date_formatted}120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_ICDR3.0-v02.0-fv01.0.nc"

    elif [[ "$file" == DMI* ]]; then
        new_name="${date_formatted}000000-DMI-L4_GHRSST-SSTfnd-DMI_OI-NSEABALTIC-v02.0-fv01.0.nc"

    elif [[ "$file" == FMI-BAL-SEAICE_CONC* ]]; then
        new_name="ice_conc_baltic_${date_formatted}1400.nc"

    else
        echo "Skipping unknown file type: $file"
        continue
    fi

    mv "$path/$file" "$path/$new_name"
    echo "Renamed $file → $new_name"
done
