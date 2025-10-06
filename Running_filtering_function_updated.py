#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 09:40:26 2023

@author: ilo
"""

__version__ = '0.2'
__author__ = 'Ida Olsen'
__contributers__ = 'Pia Englyst, Sotirios Skapalezos'
__date__ = '05/09/2023'
__contact__ = ['ilo@dmi.dk']

# Build-in modules
import os
import re

# third party modules
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
import datetime as dt
import sys
import pandas as pd

# Homemade modules
sys.path.append('/dmidata/users/ilo/projects/SST_SIC_PIA/scripts')
from Filter_application import apply_SST_SIC_filtering
from Save_Filtered_SIC_in_nc_file import SaveNCfile
from combination_of_datasets import Combine_Data_Products
from Extrapolate import Extrapolation
from Examination_of_icecharts import Get_landfast_ice
#from Unused.extrap_test import extrapolate_2d_data
#from plotting_functions import plot_cartopy
from missing_SIC_data import missing_SIC_data
from Decide_SIC_source import identify_product_ID
from Fixing_CARRA2_SIC import SIC_post_processing
# =============================================================================
# MAIN SCRIPT
# =============================================================================
# This script calls functions used for the creation of the CARRA2 SST/SIC product
# This includes:
# * Combination of datasets (BALTIC product, OSTIA SST product and SIC product)
#      - The choice of SIC product depends on the given time period. AMSR2 based
#        SIC products are used when available
# * Filtering of SIC products to remove land spillover effects
# * Extrapoaltion of the SIC product into land areas
# * Reapplication of relevant filters (those based on SST)
# * Saving the output file in netCDF format
# =============================================================================

# # Take input from user - made to use tmux and run subsets in parallel
# years = list(map(str, input("\nEnter the Year(s) : ").strip().split()))
# months = list(map(str, input("\nEnter the Months : ").strip().split()))
# HS = str(input("\nEnter the hemisphere (lowercase): "))

# # set hemisphere
# if HS=='sh':
#     latlims =[-90, -87, -40, 0]
# if HS=='nh':
#     latlims =[87, 90, 0, 40]

# ice_chart_filtering = True
# # changed maskfile 26-08-2025 - changed all throughout the script!
# # mask = data_SST['mask'].squeeze().to_numpy()
# # OBS MASK FOR 2025 files - for after 2025 we have no ESACCI SST files
# # SST mask for OSTIA files are different - therefore we must read another mask
# maskfile = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/{HS.upper()}/2020/01/20200101120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR3.0-v02.0-fv01.0.nc'
# mask = xr.open_dataset(maskfile)['mask'].squeeze().to_numpy()

# for y in years:
#     y = int(y)
#     # loop over months and products IDs
#     for m in months:
        # # loop through relevant dates and find belonging files
        # for dd in days:
        #     d = f'{y}{m}{dd}'

# --- Read arguments ---
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} START_DATE END_DATE HEMISPHERE")
    print("Example: script.py 2020-01-01 2020-03-31 nh")
    sys.exit(1)

start_date = sys.argv[1]  # e.g. "20200101"
end_date   = sys.argv[2]  # e.g. "20200331"
HS         = sys.argv[3].lower()

# --- Set hemisphere lat limits ---
if HS == 'sh':
    latlims = [-90, -87, -40, 0]
elif HS == 'nh':
    latlims = [87, 90, 0, 40]
else:
    raise ValueError("Hemisphere must be 'nh' or 'sh'")

ice_chart_filtering = True

# --- Load mask ---
maskfile = f"/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/{HS.upper()}/2020/01/20200101120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR3.0-v02.0-fv01.0.nc"
mask = xr.open_dataset(maskfile)['mask'].squeeze().to_numpy()

# --- Generate full date range ---
dates = pd.date_range(start=pd.to_datetime(start_date, format="%Y-%m-%d"),
                      end=pd.to_datetime(end_date, format="%Y-%m-%d"),
                      freq="D")

# --- Loop over dates ---
for date in dates:
    y = date.strftime("%Y")
    m = date.strftime("%m")
    dd = date.strftime("%d")
    d = date.strftime("%Y%m%d")
    print(d)


    dir_SST = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/{HS.upper()}/{y}/{m}/'
    dir_BALTIC = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/BALTIC_SIC/{y}/'

    # Find files in datafolders
    files_SST = sorted(os.listdir(dir_SST))
    files_BALTIC = sorted(os.listdir(dir_BALTIC))

    ## CHECK for days with missing data - there are no wholes in OSTIA data

    days_in_month = int(files_SST[-1][6:8])   # identify last day
    days = np.arange(1, days_in_month+1)
    days = ['0'+str(i) if i<10 else str(i) for i in days]

    ID = identify_product_ID(int(y), int(m), int(dd))
    #ID = 'OSI450a'
    print(f'year:{y}, month:{m}, day:{dd}, ID:{ID}')
    # define data folders
    dir_SIC = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/{y}/{m}/'
    
    # Find files in datafolders
    files_SIC = sorted(os.listdir(dir_SIC))
    
    # added patch on 02-10-2024 for porcessing incorrect OSI450a files!
    # this must be changed after processing these files
    
    # dates of incorrect OSI450a data
    patch_dates = ['19781025', '19781028', '19790104', '19791206', '19830926', '19840604', '19840906', '19870801', '19870920', '19870922', '19871022', '19880122', '19880128', '19880222', '19880223', '19880830', '19881010', '19881016', '19881201', '19881214', '19881231', '19890205', '19890313', '19890321', '19890324', '19890325', '19890406', '19900202', '19900331', '19900408', '19900808', '19900816', '19900907', '19900922', '19901015', '19901104', '19901112', '19901204', '19910110', '19910112', '19910312', '19910319', '19910325', '19910408', '19910416', '19910506', '19910514', '19910522', '19910524', '19910608', '19910620', '19910627', '19910629', '19910719', '19910726', '19910802', '19910906', '19910911', '19910914', '19910915', '19910918', '19911013', '19911020', '19911021', '19911027']

    # added october 2024
    if d in patch_dates: # read updated regridded file (with the correct atmosphere filter in near coastal areas)
        files_SIC = [f for f in files_SIC if ((HS in f) or (HS.upper() in f) and 'patch' in f)]
    else:
        files_SIC = [f for f in files_SIC if ((HS in f) or (HS.upper() in f))]
    
    #if d in patch_dates:
    # identify files belonging to the relevant date
    if 'SICCI' not in ID:
        identify_dates = [re.findall('\d+', f)[-1][:8] for f in files_SIC]
    else:
        identify_dates = [re.findall('\d+', f)[-3][:8] for f in files_SIC]

    missing_dates = [f'{y}{m}{d}' for d in days if f'{y}{m}{d}' not in identify_dates]
    dat_num = np.array([int(i) for i in identify_dates])

    ## SIC data
    if d in missing_dates and d!='19820101':
        # taking weighted mean of closest days
        data_SIC = missing_SIC_data(d, dat_num, files_SIC, dir_SIC, HS, ID)
    elif d=='19820101': # first date use subsequent days data
        if HS=='nh':
            data_SIC = xr.open_dataset(dir_SIC + 'ice_conc_nh_ease2-250_cdr-v3p0_198201021200.nc')
        elif HS=='sh':
            data_SIC = xr.open_dataset(dir_SIC + 'ice_conc_sh_ease2-250_cdr-v3p0_198201021200.nc')
    else:
        fsic = [f for f in files_SIC if d in f][0]
        file_SIC = dir_SIC + fsic
        data_SIC = xr.open_dataset(file_SIC)

    ## NORTHSEA product
    ## ONLY RELEVANT FOR NH
    # for files after 2025
    fd = dt.datetime.strptime(d, "%Y%m%d").strftime("%Y-%m-%d")
    if (any([d in f for f in files_BALTIC]) or any([fd in f for f in files_BALTIC])) and (HS=='nh'):
        file_BALTIC = [dir_BALTIC + f for f in files_BALTIC if ((d in f) or (fd in f))][0]
    elif HS=='nh': # no file for this specific day
        print('taking next day')
        file_BALTIC = [dir_BALTIC + f for f in files_BALTIC if str(int(d)+1) in f or str(int(d)-1) in f][0]

    # sea surface temperatures from OSTIA
    fsst = [f for f in files_SST if ((d in f) or (fd in f))][0]
    
    # Define complete path filenames
    file_SST = dir_SST + fsst

    # open data
    data_SST = xr.open_dataset(file_SST) # .sel(lat=slice(0.0, 90.0))

    # Define source and status flags
    shape = data_SIC['ice_conc'].squeeze().shape
    statusflag = np.zeros(shape) 
    sst_source_flag = np.zeros(shape)
    sic_source_flag = np.zeros(shape)
    
    sst_source_flag[~data_SST['analysed_sst'].squeeze().isnull()] = (2**1) # OSTIA

    # OSISAF source codes
    if 'OSI458' in ID:
        sic_source_flag[~data_SIC['ice_conc'].squeeze().isnull()] = (2**4) # OSI458
    elif 'SICCI_HR_SIC' in ID:
        sic_source_flag[~data_SIC['ice_conc'].squeeze().isnull()] = (2**3) # SICCI_HR
    else:
        sic_source_flag[~data_SIC['ice_conc'].squeeze().isnull()] = (2**2) # OSI450a
    
    ## lat/lon meshgrid
    lon,lat = np.meshgrid(data_SIC['lon'], data_SIC['lat'])

    
    if HS=='nh':
        # Overlay with DMI BALTIC SST and SIC in the BALTIC SEA
        data_SST, data_SIC, sst_source_flag, sic_source_flag, statusflag = Combine_Data_Products(data_SIC, 
                                                                                                file_SST, 
                                                                                                file_BALTIC, 
                                                                                                d, 
                                                                                                sst_source_flag, 
                                                                                                sic_source_flag, 
                                                                                                statusflag=statusflag, 
                                                                                                plot=False)


    

    # extrapoalte data to the very edges (have been set to nan due to bilinear interpolation)
    lim = data_SIC.sel(lat=slice(latlims[0],latlims[1]))['ice_conc'].shape[1]

    data_SIC['ice_conc'].squeeze().to_numpy()[-lim:, :], dummy = Extrapolation(lat[-lim:, :],
                                                                data_SIC['ice_conc'].squeeze().to_numpy()[-lim:, :], 
                                                                ext_num=3, 
                                                                statusflag=statusflag[-lim:, :],
                                                                mask=mask[-lim:, :], # changed from data_SST to mask 1/09/2025
                                                                lon=lon[-lim:, :],
                                                                HS=HS)
    # Filter pre extrapolation
    regrid_ostia_sst, regrid_osisaf_sic_filt, statusflag = apply_SST_SIC_filtering(lat,
                                                                                    data_SIC, 
                                                                                    data_SST, 
                                                                                    # file_CMC, 
                                                                                    sic_source_flag, 
                                                                                    statusflag=statusflag, 
                                                                                    HS=HS,
                                                                                    filter1=True,
                                                                                    filter2=True, 
                                                                                    filter3=True, 
                                                                                    filter4=False)


    # limit for extrapolation and correction: use only values north of 40 degrees (no ice outside +/-40 degrees)
    lim = data_SIC.sel(lat=slice(latlims[2],latlims[3]))['ice_conc'].shape[1]

    if HS=='nh':
        r1 = lim
        r2 = data_SIC['ice_conc'].squeeze().to_numpy().shape[0]
    elif HS=='sh':
        r1 = 0
        r2 = lim
    
    # filter with ice from ice charts only north of 50 degrees
    # or when we have large data gaps in 1986 and 1987
    date = dt.datetime.strptime(d, '%Y%m%d')
    criteria = ((date>dt.datetime(1986, 3, 28)) and (date<dt.datetime(1986,6,24)))
    criteria2 = ((date>dt.datetime(1987, 12, 3)) and (date<dt.datetime(1988,1,14)))

    # add data before extrapolation, but without extending it into the coastal regions
    if HS=='nh':
        r1_chart = data_SIC.sel(lat=slice(latlims[2],latlims[3]+10))['ice_conc'].shape[1]
        data_SIC, regrid_osisaf_sic_filt[r1_chart:r2, :], sic_source_flag[r1_chart:r2, :], statusflag[r1_chart:r2, :] = Get_landfast_ice(d,
                                                    regrid_osisaf_sic_filt[r1_chart:r2, :],
                                                    data_SIC,
                                                    data_SST,
                                                    sic_source_flag[r1_chart:r2, :],
                                                    statusflag=statusflag[r1_chart:r2, :],
                                                    ice_chart_filtering=True,
                                                    landfast_ice_extrap=False,
                                                    HS=HS)

    elif HS=='sh' and (criteria or criteria2):
        r1_chart = data_SIC.sel(lat=slice(-90,-50))['ice_conc'].shape[1]
        data_SIC, regrid_osisaf_sic_filt[r1:r1_chart, :], sic_source_flag[r1:r1_chart, :], statusflag[r1:r1_chart, :] = Get_landfast_ice(d,
                                                    regrid_osisaf_sic_filt[r1:r1_chart, :],
                                                    data_SIC,
                                                    data_SST,
                                                    sic_source_flag[r1:r1_chart, :],
                                                    statusflag=statusflag[r1:r1_chart, :],
                                                    ice_chart_filtering=ice_chart_filtering,
                                                    landfast_ice_extrap=False,
                                                    HS=HS)
    


    # Extrapolate the filtered SIC into the fjords
    if HS=='sh':
        # requires less extrapolation
        # The value is found by doing a gridoint comparison
        # to check if any values differ by using additional
        # extrap steps
        extrap_num=38
    else:
        extrap_num=50
    regrid_osisaf_sic_filt[r1:r2, :], statusflag[r1:r2, :] = Extrapolation(lat[r1:r2, :],
                                                                regrid_osisaf_sic_filt[r1:r2, :], 
                                                                ext_num=extrap_num, 
                                                                statusflag=statusflag[r1:r2, :], 
                                                                mask=mask[r1:r2, :], # changed from data_SST to mask 1/09/2025
                                                                lon=lon[r1:r2, :],
                                                                HS=HS)
    
    
    
    # Get the landfast ice from ice charts only north of 50 degrees
    # Add open water areas and icechart information extrapolated with NN into coastal regions
    # changed ice chart filter to True
    if HS=='nh':
        r1_chart = data_SIC.sel(lat=slice(latlims[2],latlims[3]+10))['ice_conc'].shape[1]
        data_SIC, regrid_osisaf_sic_filt[r1_chart:r2, :], sic_source_flag[r1_chart:r2, :], statusflag[r1_chart:r2, :] = Get_landfast_ice(d,
                                                    regrid_osisaf_sic_filt[r1_chart:r2, :],
                                                    data_SIC,
                                                    data_SST,
                                                    sic_source_flag[r1_chart:r2, :],
                                                    statusflag=statusflag[r1_chart:r2, :],
                                                    ice_chart_filtering=True,
                                                    landfast_ice_extrap=True)
        
    


    # Filter post extrapolation (currently not used)
    regrid_ostia_sst, regrid_osisaf_sic_filt, statusflag = apply_SST_SIC_filtering(lat,
                                                                                    regrid_osisaf_sic_filt, 
                                                                                    data_SST, 
                                                                                    # file_CMC, 
                                                                                    sic_source_flag, 
                                                                                    statusflag=statusflag, 
                                                                                    filter1=False, 
                                                                                    filter2=False, 
                                                                                    filter3=False, 
                                                                                    filter4=False)


    # apply landmask to data
    regrid_osisaf_sic = data_SIC['ice_conc'].squeeze().to_numpy()
    sst_source_flag[mask==2]=np.nan
    sic_source_flag[mask==2]=np.nan
    statusflag[mask==2]=np.nan
    regrid_osisaf_sic[mask==2]=np.nan
    regrid_osisaf_sic_filt[mask==2]=np.nan
    sic_source_flag[np.isnan(regrid_osisaf_sic_filt)]=np.nan
    statusflag[np.isnan(regrid_osisaf_sic_filt)]=np.nan


    # Save output file
    SaveNCfile(regrid_ostia_sst, 
                regrid_osisaf_sic_filt, 
                regrid_osisaf_sic, 
                sic_source_flag, 
                sst_source_flag, 
                statusflag, 
                file_SST, 
                ID, 
                d,
                HS,
                ice_chart_filtering=ice_chart_filtering)

    SIC_post_processing(HS, y, m, dd)
