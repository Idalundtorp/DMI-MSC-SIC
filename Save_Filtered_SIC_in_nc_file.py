#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.2'
__author__ = 'Ida Olsen'
__contributers__ = 'Pia Englyst, Sotirios Skapalezos'
__date__ = '14/09/2023'

# Build-in modules
from datetime import datetime
import os

# Third-party modules
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt 

# Homemade modules

def SaveNCfile(regrid_ostia_sst, regrid_osisaf_sic_filt3, regrid_osisaf_sic, sic_source_flag, sst_source_flag, statusflag, file_SST, ID, d, HS, ice_chart_filtering=False):
    """

    Parameters
    ----------
    regrid_ostia_sst : TYPE
        OSTIA SST
    regrid_osisaf_sic_filt3 : TYPE
        SIC after filtration
    regrid_osisaf_sic : TYPE
        SIC before filtration
    file_SST : TYPE
        Opened original SST file - used to get dims and coordinates of NC file
    file_SIC : TYPE
        Original SIC file - used to name the output file
    ID : TYPE
        Product ID identifier (due to product combination and comparison)

    Returns
    -------
    None.

    """
    # =============================================================================
    # WRITE TO NETCDF FILE - WRITE TO NETCDF FILE - WRITE TO NETCDF FILE - WRITE TO
    # =============================================================================
    print('Writing to netCDF file...')
    # Create a netCDF Dataset object
    # ------------------------------
    
    # set nan values to -99
    sst_source_flag[np.isnan(sst_source_flag)]=-99 
    sic_source_flag[np.isnan(sic_source_flag)]=-99 
    statusflag[np.isnan(statusflag)]=-99

    # Redefine mask values
    # choose fixed mask for 2020-01-01 due to changing SST files:
    # added 26-08-2025
    maskfile = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/{HS.upper()}/2020/01/20200101120000-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR3.0-v02.0-fv01.0.nc'
    mask = xr.open_dataset(maskfile)['mask'].squeeze().to_numpy()
    try:
        file_SST = xr.open_dataset(file_SST)
    except:
        # file already opened
        pass
    # mask =  file_SST['mask'].squeeze().to_numpy()

    # water
    mask[regrid_osisaf_sic_filt3<15] = 2**0
    # sea ice 
    mask[regrid_osisaf_sic_filt3>70] = 2**3
    # marginal ice zone
    mask[(regrid_osisaf_sic_filt3>=15) & (regrid_osisaf_sic_filt3<=70)] = 2**5
    
    # changed file_SST['mask'].squeeze().to_numpy() to mask 26-08-2025
    # land
    mask[mask==2] = 2**1
    # river
    mask[mask==4] = 2**2
    # lake
    mask[mask==16] = 2**4


    regrid_osisaf_sic_filt3[np.logical_and(mask==1, np.isnan(regrid_osisaf_sic_filt3))]=0
    # assign water to non extrapolated ocean locations (e.g. south/north of 40/-40)
    # regrid_osisaf_sic_filt3[np.logical_and(np.isnan(regrid_osisaf_sic_filt3), mask==1)]=0
    # add plotting routine
    plt.figure(figsize=(6,5))
    plt.imshow(regrid_osisaf_sic_filt3, origin='lower')
    plt.title("SIC after landmask")
    plt.colorbar(label="Concentration")
    plt.tight_layout()
    #plt.show()
    
    # Create the dataset
    ds = xr.Dataset(
        data_vars = dict(
            analysed_sst = (['time','lat','lon'],np.expand_dims(regrid_ostia_sst.astype(np.float32),axis=0)),
            ice_conc = (['time','lat','lon'],np.expand_dims(regrid_osisaf_sic_filt3.astype(np.float32),axis=0)),
            ice_conc_orig = (['time','lat','lon'],np.expand_dims(regrid_osisaf_sic.astype(np.float32),axis=0)),
            mask = (['time','lat','lon'],np.expand_dims(mask.astype(np.int8),axis=0)),
            analysed_sst_source =  (['time','lat','lon'],np.expand_dims(sst_source_flag.astype(np.int8),axis=0)),
            iceconc_source =  (['time','lat','lon'],np.expand_dims(sic_source_flag.astype(np.int8),axis=0)),
            status_flag =  (['time','lat','lon'],np.expand_dims(statusflag.astype(np.int8),axis=0))
        ),
        coords = file_SST.coords,
        attrs = dict(title = 'CARRA Sea Surface Temperature and Sea Ice Concentration',
                      institution = 'DMI',
                      source = os.path.basename(__file__),
                      history = 'created ' + datetime.today().strftime('%Y-%m-%d %H:%M'),
                      conventions = 'CF-1.6')
    )
        
    # Add variable attributes
    ds['status_flag'].attrs['standard_name'] = 'status flag'
    ds['status_flag'].attrs['long_name'] = 'filtering/extrapolation status flag '
    ds['status_flag'].attrs['flag values'] = '0UB 1UB 2UB 4UB 8UB 16UB 32UB'
    ds['status_flag'].attrs['flag meaning'] = 'original, filter1: near-land minimum SIC correction, filter2: near-land SST correction,  filter3: Global SST correction, filter4: inter-sensor bias correction, filter5: sea ice chart correction, filter6: extrapolated'
    ds['status_flag'].encoding['_FillValue'] = -99
    ds['status_flag'].encoding['missing_value'] = -99

    ds['iceconc_source'].attrs['standard_name'] = 'sic data source'
    ds['iceconc_source'].attrs['long_name'] = 'sea ice concentration data source'
    ds['iceconc_source'].attrs['flag values'] = '0UB 1UB 2UB 4UB 8UB 16UB'
    ds['iceconc_source'].attrs['flag meaning'] = 'No_Input_Data NSB_SIC NIC_ice_charts OSI450a SICCI_HR_SIC OSI458 '
    ds['iceconc_source'].encoding['_FillValue'] = -99
    ds['iceconc_source'].encoding['missing_value'] = -99


    ds['analysed_sst_source'].attrs['standard_name'] = 'sst data source'
    ds['analysed_sst_source'].attrs['long_name'] = 'sea surface temperature data source'
    ds['analysed_sst_source'].attrs['flag values'] = '1UB 2UB'
    ds['analysed_sst_source'].attrs['flag meaning'] = 'NSB_SST OSTIA_SST'
    ds['analysed_sst_source'].encoding['_FillValue'] = -99
    ds['analysed_sst_source'].encoding['missing_value'] = -99

    ds['mask'].attrs['FillValue'] = '-128UB'
    ds['mask'].attrs['long_name'] = "land sea_ice lake bit mask" 
    ds['mask'].attrs['flag_masks'] = '1UB 2UB 4UB 8UB 16UB 32UB'
    ds['mask'].attrs['flag_meanings'] = "open_water land optional_lake_surface sea_ice optional_river_surface marginal_ice_zone" 
    # ds['mask'].attrs['source'] = "NAVOCEANO_landmask_v1.0 EUMETSAT_OSI-SAF_icemask ARCLake_lakemask" 
    ds['mask'].attrs['comment'] = " Land/ open ocean/ sea ice /lake mask" 
    ds['mask'].encoding['_FillValue'] = -99
    ds['mask'].encoding['missing_value'] = -99
    
    ds['analysed_sst'].attrs['standard_name'] = 'sea_surface_foundation_temperature'
    ds['analysed_sst'].attrs['long_name'] = 'analysed sea surface temperature'
    ds['analysed_sst'].attrs['units'] = 'kelvin'
    ds['analysed_sst'].encoding['_FillValue'] = -9999
    ds['analysed_sst'].encoding['missing_value'] = -9999
    
    ds['ice_conc'].attrs['standard_name'] = 'sea ice concentration'
    ds['ice_conc'].attrs['long_name'] = 'regridded concentration of sea ice filtered by F12345 and extrapolated towards land'
    ds['ice_conc'].attrs['units'] = '%'
    ds['ice_conc'].encoding['_FillValue'] = -9999
    ds['ice_conc'].encoding['missing_value'] = -9999
    
    ds['ice_conc_orig'].attrs['standard_name'] = 'original sea ice concentration '
    ds['ice_conc_orig'].attrs['long_name'] = 'regridded concentration of original sea ice'
    ds['ice_conc_orig'].attrs['units'] = '%'
    ds['ice_conc_orig'].encoding['_FillValue'] = -9999
    ds['ice_conc_orig'].encoding['missing_value'] = -9999
    
    ds['lat'].attrs['standard_name'] = 'lat'
    ds['lat'].attrs['long_name'] = 'latitude'
    ds['lat'].attrs['units'] = 'degrees_north'
    ds['lat'].attrs['axis'] = 'Y'
    
    ds['lon'].attrs['standard_name'] = 'lon'
    ds['lon'].attrs['long_name'] = 'longitude'
    ds['lon'].attrs['units'] = 'degrees_east'
    ds['lon'].attrs['axis'] = 'X'
    
    ds['time'].attrs['standard_name'] = 'time'
    ds['time'].attrs['long_name'] = 'reference time of sst field'
    ds['time'].encoding['units'] = 'seconds since 1981-01-01 00:00:00'
    ds['time'].encoding['calendar'] = 'standard'
    
    # Write dataset to netCDF file
    year = d[:4]
    month = d[4:6]
    day = d[6:]
    print(f'{year}, {month}, {day}')
    if ice_chart_filtering:
        #path_out = f'/dmidata/projects/cmems2/C3S/{ID}/{year}/{month}/'
        if HS=='sh':
            path_out = f'/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/{year}/{month}/'
            #path_out = f'/dmidata/projects/cmems2/C3S/{ID}/{year}/{month}/'
        else:
            path_out = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/{year}/{month}/'
            #path_out = f'/dmidata/projects/cmems2/C3S/{ID}/{year}/{month}/'
    else:
        path_out = f'/dmidata/projects/asip-cms/SIC/CARRA2_data/filtered_SIC_data/{ID}/{year}/{month}/'
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    if HS == 'sh':
        ofile = path_out + 'dmigbl_sic' + f'{year}{month}{day}_{HS}.nc'
    else:
        ofile = path_out + 'CARRA2_' + f'{year}{month}{day}_{HS}_v3.nc'
    if os.path.exists(ofile):
        os.remove(ofile)
    
    # define compression
    # scale_factor=0.01,
    comp = dict( zlib=True, complevel=6)
    encoding = {varname: comp for varname, da in ds.data_vars.items()}

    for var in ds: 
        ds[var].encoding.update(dict(zlib=True, complevel=6))
    ds.to_netcdf(ofile, format="NETCDF4", mode="w")
    ds.close()
    
    print(f'File {ofile} created')

