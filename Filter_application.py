#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.2'
__author__ = 'Sotirios Skapalezos'
__contributers__ = 'Ida Olsen, Pia Englyst'
__date__ = '14/09/2023'

# Build-in modules
# Third-party modules
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.ndimage import minimum_filter
# Homemade modules 
from make_minimum_filter import make_minimum_filter

def apply_SST_SIC_filtering(latitude,
                            data_SIC, 
                            data_SST, 
                            # data_SST_CMC, 
                            sic_source_flag, 
                            statusflag, 
                            HS='nh',
                            filter1=True, 
                            filter2=True, 
                            filter3=True, 
                            filter4=True):

    # =============================================================================
    # FILTERING - FILTERING - FILTERING - FILTERING - FILTERING - FILTERING - FILTE
    # =============================================================================
    print('=========')
    print('FILTERING')
    print('=========\n')
    # -------------------------------------------------------
    # Filter 1: Land spillover correction over the OSISAF SIC
    # -------------------------------------------------------
    # Filter description: A "1" value in the near_land array indicates land within
    # the mask around that pixel. Whenever a "1" is detected in the walt_dist
    # array, and the minimum SIC that is found within the 15x15 SIC area around it 
    # is zero, i.e. there is open water in the grid, then the SIC value is replaced
    # with zero, i.e. we replace ice with water.
    print('Filter 1: Land spillover correction over the OSISAF SIC')
    print('-------------------------------------------------------')
    
    # read near landmask and replace nan values with 0 and land values with 1
    # near_land_SSMIS = np.load('15x15_land_identifier.npy').squeeze()
    # near_land_AMSR = np.load('5x5_land_identifier.npy').squeeze()
    if HS=='nh':
        distance_to_land = xr.open_dataset('distance_to_land_nh.nc')['distance_to_land'].squeeze().to_numpy()
    elif HS=='sh':
        distance_to_land = xr.open_dataset('distance_to_land_sh.nc')['distance_to_land'].squeeze().to_numpy()

    
    # resolution of AMSR2, which we also use for SSMIS
    near_land = distance_to_land<25
    resolution = 25
    
    # convert near land
    near_land[near_land] = 1

    # # We want to avoid filtering Landfast ice, which has been extrapolated to land
    # landfast_mask = np.copy(sic_source_flag)
    # bool_mask = sic_source_flag==2
    # landfast_mask[bool_mask] = -1
    # landfast_mask[~bool_mask] = 0
    # # make a mask to see if there and landfast ice close to point
    # landfast_mask = minimum_filter(landfast_mask,size=window_size)
    
    # define data
    try:
        regrid_osisaf_sic = data_SIC['ice_conc'].squeeze().to_numpy()
    except: # post processing
        regrid_osisaf_sic = data_SIC
    
    ## SST data 
    regrid_ostia_sst = data_SST['analysed_sst'].squeeze().to_numpy()
    # regrid_cmc_sst = xr.open_dataset(data_SST_CMC)['analysed_sst'].squeeze().to_numpy()
    
    if filter1:
        # Pad the image with 1000 around, otherwise it has unwanted behavior around the edges
        # See https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html
    
        # regrid_osisaf_sic_min = np.pad(regrid_osisaf_sic, pad_width=half_window, mode='constant', constant_values=1000)
        # # Replace nan (land) with a large value (e.g. 1000) in regrid_osisaf_sic_min because minimum_filter cannot handle nan
        # regrid_osisaf_sic_min[np.isnan(regrid_osisaf_sic_min)==True] = 1000
        
        # Find minimum SIC within a window window for every pixel
        # longitude,latitude = np.meshgrid(data_SIC['lon'], data_SIC['lat'])
    
        # regrid_osisaf_sic_min = minimum_filter(regrid_osisaf_sic, latitude, longitude)
        # get region of interest e.g. where we believe we will find non zero sic
        if HS=='nh':
            r1 = data_SIC.sel(lat=slice(0,40))['ice_conc'].shape[1]
            r2 = data_SIC['ice_conc'].squeeze().to_numpy().shape[0]
        elif HS=='sh':
            r1 = 0
            r2 = data_SIC.sel(lat=slice(-40,0))['ice_conc'].shape[1]
        regrid_osisaf_sic_min = np.ones(regrid_osisaf_sic.shape)*np.nan
        regrid_osisaf_sic_min[r1:r2, :] = make_minimum_filter(regrid_osisaf_sic[r1:r2, :], latitude[r1:r2, :], resolution=resolution, HS=HS)
  
        # Find where near_land = 1 and regrid_osisaf_sic_min = 0 and not Baltic or landfast ice
        idx_filt1 = np.argwhere((near_land==1) & (regrid_osisaf_sic_min==0) & (regrid_osisaf_sic!=0) & (sic_source_flag!=2) & (sic_source_flag!=1)
                                )
    else:
        idx_filt1 = np.array([])
    # -----------------------------------------------------
    # Filter 1: SIC correction based on land
    # -----------------------------------------------------
    if idx_filt1.size != 0:
        # Create regrid_osisaf_sic_filt3 (create a copy of regrid_osisaf_sic_filt1 and modify it)
        regrid_osisaf_sic_filt1 = np.copy(regrid_osisaf_sic) # Copy it
        regrid_osisaf_sic_filt1[idx_filt1[:,0],idx_filt1[:,1]] = 0 # Replace sea ice with open water
        #assign flag value
        statusflag[idx_filt1[:,0],idx_filt1[:,1]] += (2**0) # Assign filter1 flag
        # Restore regridded OSISAF land mask
        regrid_osisaf_sic_filt1[np.isnan(regrid_osisaf_sic)==True] = np.nan
        
        # Statistics:
        print(f'Filtered out {len(idx_filt1)} pixels')
        print(f'Mean SIC filtered out: {np.nanmean(regrid_osisaf_sic[idx_filt1[:,0],idx_filt1[:,1]])}\n')

    else:
        print('Land spillover filtering resulted in no corrections\n')
        regrid_osisaf_sic_filt1 = np.copy(regrid_osisaf_sic)

    # -----------------------------------------------------
    # Filter 2: SIC correction based on near-land OSTIA SST
    # -----------------------------------------------------
    # Filter description: Within the near_land mask, whenever a OSTIA SST value is
    # larger than 3 deg. Celcius, we set the corresponding OSISAF SIC pixel to zero.
    print('Filter 2: SIC correction based on near-land OSTIA and CMC SST')
    print('-----------------------------------------------------')
    
    # Find where near_land = 1 and OSTIA or CMC SST > 3 deg. Celcius (276.15 K)
    # idx_filt2_test = np.argwhere((near_land==1) & ((regrid_ostia_sst > 276.15) | (regrid_cmc_sst > 276.15)) & (regrid_osisaf_sic_filt1 !=0) & (np.isnan(regrid_osisaf_sic_filt1)==False))
    idx_filt2 = np.argwhere((near_land==1) & (regrid_ostia_sst > 276.15) & (regrid_osisaf_sic !=0) & (np.isnan(regrid_osisaf_sic)==False)
                            & (sic_source_flag!=2) & (sic_source_flag!=1))
    # Check if the above filtering condition is met at any pixel
    if idx_filt2.size != 0 and filter2:
        # Create regrid_osisaf_sic_filt2 (create a copy of regrid_osisaf_sic_filt1 and modify it)
        regrid_osisaf_sic_filt2 = np.copy(regrid_osisaf_sic_filt1) # Copy it
        regrid_osisaf_sic_filt2[idx_filt2[:,0],idx_filt2[:,1]] = 0 # Replace sea ice with open water
        #assign flag value
        statusflag[idx_filt2[:,0],idx_filt2[:,1]] += (2**1) # Assign filter2 flag
        
        # Statistics:
        print(f'Filtered out {len(idx_filt2)} pixels')
        print(f'Mean SIC filtered out: {regrid_osisaf_sic_filt1[idx_filt2[:,0],idx_filt2[:,1]].mean()}\n')
    else:
        print('No OSTIA near-land pixels are above 276.15 K - SST filtering resulted in no corrections\n')
        regrid_osisaf_sic_filt2 = np.copy(regrid_osisaf_sic_filt1)


    # --------------------------------------------------
    # Filter 3: SIC correction based on global OSTIA SST
    # --------------------------------------------------
    # Filter description: For every OSTIA SST value that is above 8 deg. Celcius
    # (281.15 K), we set the corresponding OSISAF SIC pixel to zero.
    print('Filter 3: SIC correction based on global OSTIA SST')
    print('--------------------------------------------------')
    
    # Find where OSTIA SST > 8 deg. Celcius (281.15 K)
    # idx_filt3_test = np.argwhere(((regrid_ostia_sst > 281.15) | (regrid_cmc_sst > 281.15)) & (regrid_osisaf_sic_filt2 !=0) & (np.isnan(regrid_osisaf_sic_filt2)==False))
    idx_filt3 = np.argwhere((regrid_ostia_sst > 281.15) & (regrid_osisaf_sic !=0) & (np.isnan(regrid_osisaf_sic)==False)
                            & (sic_source_flag!=2) & (sic_source_flag!=1))

    if idx_filt3.size != 0 and filter3:
        # Create regrid_osisaf_sic_filt3 (create a copy of regrid_osisaf_sic_filt1 and modify it)
        regrid_osisaf_sic_filt3 = np.copy(regrid_osisaf_sic_filt2) # Copy it
        regrid_osisaf_sic_filt3[idx_filt3[:,0],idx_filt3[:,1]] = 0 # Replace sea ice with open water
        #assign flag value
        statusflag[idx_filt3[:,0],idx_filt3[:,1]] += (2**2) # Assign filter3 flag
        
        # Statistics:
        print(f'Filtered out {len(idx_filt3)} pixels')
        print(f'Mean SIC filtered out: {regrid_osisaf_sic_filt2[idx_filt3[:,0],idx_filt3[:,1]].mean()}\n')
    else:
        print('No OSISAF SIC corresponds to OSTIA SST above 281.15 K - SST filtering resulted in no corrections\n')
        regrid_osisaf_sic_filt3 = np.copy(regrid_osisaf_sic_filt2)     



    idx_filt4 = np.argwhere((regrid_osisaf_sic < 15)  & (regrid_osisaf_sic!=0)
                            & (sic_source_flag!=2)) # & (sic_source_flag!=1)
    
    if idx_filt4.size != 0 and filter4:
        # -------------------------------------------
        # Filter 4: Replace all SIC < 15 with SIC = 0
        # -------------------------------------------
        # Filter description: Apply the common practice of considering all SIC < 15 as
        # open water.
        print('Filter 4: Replace SIC < 15 with SIC = 0')
        print('---------------------------------------')
        # Create regrid_osisaf_sic_filt5 (create a copy of regrid_osisaf_sic_filt4 and modify it)
        regrid_osisaf_sic_filt4 = np.copy(regrid_osisaf_sic_filt3) # Copy it
        regrid_osisaf_sic_filt4[idx_filt4[:,0],idx_filt4[:,1]] = 0 # Replace sea ice with open water
        #assign flag value
        statusflag[idx_filt4[:,0],idx_filt4[:,1]] += (2**3) # Assign filter1 flag
        
        # Statistics:
        print(f'Filtered out {len(idx_filt4)} pixels')
        print(f'Mean SIC filtered out: {regrid_osisaf_sic_filt3[idx_filt4[:,0],idx_filt4[:,1]].mean()}\n')
        
    else:
        # print('No SIC < 15 found in grid - Filter 4 resulted in no corrections\n')
        regrid_osisaf_sic_filt4 = np.copy(regrid_osisaf_sic_filt3)
        
    print('Filtering complete\n')

    return regrid_ostia_sst, regrid_osisaf_sic_filt4, statusflag
