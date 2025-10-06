#!/bin/bash
# For an overview of production and for further information see the confluence page called
# SIC (DMI_MSC_SIC) overview of production

# ========================
# INPUTS
# ========================

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 START_DATE END_DATE"
    echo "Example: $0 2023-01-01 2023-01-31"
    exit 1
fi

START_DATE=$1
END_DATE=$2

# Activate python environment
# Initialize conda in this shell
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate CARRA

DATA_BASEPATH="/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2"
CODE_BASEPATH="/dmidata/users/ilo/projects/SST_SIC_PIA/run_engine"

echo "Running pipeline from $START_DATE to $END_DATE"

# ========================
# STEP 1: DOWNLOAD RELEVANT DATA
# ========================
# CDS data is transferred from AURORA including: OSI-458-TU, FMI/SMHI icecharts, BALTIC SST, and ESACCI SST/OSTIA SST
# Download NIC icecharts

# Shift dates - create extended ranges to ensure that we get an icechart (updated biweekly)
START_EXT=$(date -d "$START_DATE -14 days" +%Y-%m-%d)
END_EXT=$(date -d "$END_DATE +14 days" +%Y-%m-%d)

echo "Downloading NIC data"
#python download_nic.py "$START_EXT" "$END_EXT" "$DATA_BASEPATH/original_SIC_data/NIC/shapefiles" #: this script downloads the data between two given dates and unzips the downloaded data, path=download path
python Read_NIC_shapefiles.py "$START_EXT" "$END_EXT" "$DATA_BASEPATH/original_SIC_data/NIC" # reprojects NIC shapefiles from .sig file to an .nc file in EASE3 grid

# ========================
# STEP 2: REGRID RELEVANT DATA
# ========================
echo "Regridding data"
# regrids all of the listed datasources
#./regrid_data_updated.sh "$START_DATE" "$END_DATE" "OSI458_TU OSTIA BALTIC_SIC FMI_SMHI NIC" "nh" #"OSI458_TU OSTIA BALTIC_SIC FMI_SMHI NIC" "nh" # modify script to take start date and end date and HS
#./regrid_data_updated.sh "$START_DATE" "$END_DATE" "OSI458_TU OSTIA" "sh" # modify script to take start date and end date and HS

# ========================
# STEP 3: RUN PRODUCTION OF DMI-MSC-SIC
# ========================
echo "Run processing of DMI-MSC-SIC"
# Runs processing chain for each HS
python "$CODE_BASEPATH/Running_filtering_function_updated.py" "$START_DATE" "$END_DATE" "nh" # modify to take start_date, end date and HS
#python $COSE_BASEPATH/Running_filtering_function_updated.py START_DATE END_DATE SH

# ========================
# STEP 4: COMBINE DMI-MSC-SIC NH AND SH
# ========================
echo "combining NH and SH SIC"
./cdo_combine_global.sh # must be updated to take dates
