# DMI Multisource Sea Ice Concentration Composite (DMI-MSC-SIC)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17100178.svg)](https://doi.org/10.5281/zenodo.17100178)
[![Made with Bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](#)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](#)

> **Authors:** Olsen, I. et al., Danish Meteorological Institute (DMI)  
> **Associated Publication (Preprint):** *A new global multi-source sea ice concentration composite*  
> **Dataset DOI:** [https://doi.org/10.5281/zenodo.17100178](https://doi.org/10.5281/zenodo.17100178)

---

## Overview

The **DMI Multisource Sea Ice Concentration Composite (DMI-MSC-SIC)** is a *global daily sea ice concentration dataset spanning 1982 through 2024*. It combines several input data sources including passive microwave data and sea ice charts.  

This repository contains the full workflow for producing the DMI-MSC-SIC ([DOI link](https://doi.org/10.5281/zenodo.17100178)) along with the figures presented in the associated paper **A new global multi-source sea ice concentration composite**. These are available from the plotting_scripts folder.

To produce the DMI-MSC-SIC, use the `main.sh` script. This downloads NIC data, regrids all data, and runs the primary code, which selects, combines, filters, and extrapolates relevant data.

---

## Running the Code

To run the code:

```bash
./main.sh START_DATE END_DATE

Example: 
./main.sh 2025-07-01 2025-07-31

This code runs:

1. Reprojection of NIC icecharts from shapefiles into 12.5 EASE3 netcdf files
2. Regridding of all data (NIC icecharts, OSI458_TU (temporal update of OSI458 PMW CDR), FMI_SMHI icecharts, BALTIC_SST) from their original grid to a regular 0.05 degree lat/lon grid. It also splits ESA CCI SST data into NH and SH
3. Running processing of DMI-MSC-SIC (main script)
4. Combines NH and SH DMI-MSC-SIC files to create global files.

Steps 2 and 3 runs separately for NH and SH


**Input Data**

Each of the input data sources can be downloaded using their respective download scripts.

Example: ./download_OSI450a.sh



