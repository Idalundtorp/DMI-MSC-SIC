The code presented here was used to produce the Danish Meteorological Institute Multisource Sea Ice Concentration Composite (DMI-MSC-SIC) (https://doi.org/10.5281/zenodo.17100178) along with the figures presented in the associated paper **A new global multi-source sea ice concentration composite**
To produce the DMI-MSC-SIC use the main.sh script. This downloads NIC data, regrid all data and runs the primary code, which selects, combines, filters and extrapolates relevant data.

To run code do: ./main.sh START_DATE END_DATE - e.g. ./main.sh 2025-07-01 2025-07-31

This code runs:

1. Reprojection of NIC icecharts from shapefiles into 12.5 km EASE3 netcdf files
2. Regridding of all data (NIC icecharts, OSI458_TU (temporal update of OSI458 PMW CDR), FMI_SMHI icecharts, BALTIC_SST) from their original grid to a regular 0.05 degree lat/lon grid. It also splits ESA CCI SST data into NH and SH
3. Running processing of DMI-MSC-SIC (main script)
4. Combines NH and SH DMI-MSC-SIC files to create global files.
Steps 2 and 3 runs separately for NH and SH

Each of the input data sources can be downloaded from their respective download scripts.
e.g. to download OSI-450-a data run the download_OSI450a.sh bash script 
