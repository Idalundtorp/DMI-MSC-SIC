#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.2'
__author__ = 'Ida Olsen'
__contributers__ = 'Pia Englyst'
__date__ = '14/09/2023'

# Build-in modules

# Third-party modules
import numpy as np
import xarray as xr
import scipy
import matplotlib.pyplot as plt

# Homemade modules 
from plotting_functions import plot_cartopy
from Extrapolate import Extrapolation
from Get_Baltic_SIC import Get_ice_chart_information

def Combine_Data_Products(data_SIC, file_SST, file_BALTIC, date, sst_source_flag, sic_source_flag, statusflag, plot=False):

    # =============================================================================
    # COMBINING
    # =============================================================================
    print('=========')
    print('COMBINING')
    print('=========\n')

    # AREA OF INTEREST
    # To avoid having too many interfaces we use only the Area of the Baltic region where 
    # the ocean interface is as small as possible (e.g. north of Jutland)
    # This region fits with 40.1<=lat<=86.1 and -110.1<=lon<=30.1

    data = xr.open_dataset(file_BALTIC).sel(lat=slice(53.0, 66.1), lon=slice(9.2,30.2))
    sst_bal = data['analysed_sst'].squeeze().to_numpy()
    
    # Get SIC data from FMI/SMHI icecharts
    # EXCEPT FOR JUNE-DEC 2000, where we have no sea ice charts! (this is taken care of later)
    SIC_BAL_file = Get_ice_chart_information(date)
    print(SIC_BAL_file)
    try:
        sic_bal = xr.open_dataset(SIC_BAL_file)['ice_concentration'].squeeze().to_numpy()
        # there are small faults in some icecharts! [20110305, 20110306, 20110311] - set these to nan
        sic_bal[sic_bal>100] = np.nan
        sic_bal[sic_bal<0] = np.nan
    except: # sic replaced with zeros, when no sea ice information available (which is the case for summer months)
        sic_bal = SIC_BAL_file

    # ------------------------------------
    # Overlay Baltic SST and SIC
    # ------------------------------------
    # Filter description: For the North Sea / Baltic Sea region, we use the DMI L4 product.
    print('Overlay Baltic SST and SIC')
    print('------------------------------------')
    
    # Load dataset
    # data_SIC = xr.open_dataset(file_SIC)
    data_SST = xr.open_dataset(file_SST)
    
    sst = data_SST['analysed_sst'].squeeze().to_numpy().flatten()
    sic = data_SIC['ice_conc'].squeeze().to_numpy().flatten()

    # set undefined areas to nan
    print(sst_bal.shape)
    print(sic_bal.shape)
    sst_bal[sic_bal<0] = np.nan
    sic_bal[sic_bal<0] = np.nan
    
    # Extrapolate Baltic data into the surrondings fjords
    statusflag_out = np.copy(statusflag)
    sic_bal, dummy = Extrapolation(data['lat'].squeeze().to_numpy(), sic_bal, 5, statusflag=statusflag)
    sst_bal, dummy = Extrapolation(data['lat'].squeeze().to_numpy(), sst_bal, 5, statusflag=statusflag)

    # Define output arrays
    sst_out = np.copy(sst)
    sic_out = np.copy(sic)
    
    # to get "square" area of Baltic region
    mask0 = (
            (data_SST.coords["lat"] >= 53.0) &
            (data_SST.coords["lat"] <= 66.1) &
            (data_SST.coords["lon"] >= 9.2)  &
            (data_SST.coords["lon"] <= 30.2)
            ).to_numpy().flatten()

    
    sst_out[mask0] = sst_bal.flatten()
    sic_out[mask0] = sic_bal.flatten()
    print('Baltic region grid overlayed\n')

    # fill status flags to assign sst and sic sources
    # flag 1 = Baltic
    sst_source_flag[mask0.reshape(sst_source_flag.shape)] = (2**0) # Baltic
    sic_source_flag[mask0.reshape(sst_source_flag.shape)] = (2**0) # Baltic

    # reapply the SST mask and fill with OSTIA lakes
    landmask_OSTIA = data_SST['mask'].squeeze().to_numpy().flatten()==2
    # set OSTIA land areas to nan
    sst_out[landmask_OSTIA] = np.nan
    sic_out[landmask_OSTIA] = np.nan

    # to get area North of Norway
    mask1 = (
            (data_SST.coords["lat"] >= 62.0) &
            (data_SST.coords["lat"] <= 66.1) &
            (data_SST.coords["lon"] >= 9.2)  &
            (data_SST.coords["lon"] <= 15.0)
            ).to_numpy().flatten()

    # bool index for Baltic sea
    a = np.array(mask0, dtype=bool)
    # bool index for nan areas in sic data
    b = np.logical_or(np.isnan(sic_out),np.array(mask1, dtype=bool))
    # find values that are true in both
    index = np.logical_and(a, b)

    # assign OSTIA source flag
    sst_source_flag[index.reshape(sic_source_flag.shape)] = (2**1) # Ostia
    sic_source_flag[index.reshape(sic_source_flag.shape)] = np.max(sic_source_flag) # OSI SAF or SSMIS SIC

    # fill nan areas with OSTIA data ( to get OSTIA data in lakes + north of norway)
    sst_out[index]=data_SST['analysed_sst'].squeeze().to_numpy().flatten()[index]
    sic_out[index]=data_SIC['ice_conc'].squeeze().to_numpy().flatten()[index]
    
    # remove source assigned in areas where we have no SIC data
    sic_source_flag[np.isnan(sic_out).reshape(sic_source_flag.shape)] = 0 # We have no data

    # plot data products and regions 
    if plot:
        lon = data_SST['lon']
        lat = data_SST['lat']
        for v, V, n in zip([sst_out, sic_out],[data_SST['analysed_sst'], data_SIC['ice_conc']], ['sst','sic']):
            var = v.reshape(data_SST['analysed_sst'].squeeze().shape)
            plot_cartopy(lon, lat, var, subplots=1, extend=[9, 40, 50, 70], title='OSTIA_BALTIC_AREA_' + str(date) + n, square=True)
            plot_cartopy(data_SST['lon'], data_SST['lat'], V.squeeze().to_numpy(), subplots=1, extend=[9, 40, 50, 70], title='OSTIA_'+ str(date) + n)
            
    # ------------------------------------
    # SMOOTH DATA IN INTERFACE REGION 
    # ------------------------------------
    
    # Interface area definition
    mask_interface = (
            (data_SST.coords["lat"] >= 57.1) &
            (data_SST.coords["lat"] <= 59.0) &
            (data_SST.coords["lon"] >= 9.2-0.5)  &
            (data_SST.coords["lon"] <= 9.2+0.5)
            ).to_numpy()
    
    # Define mean filter - we use a 5 by 5 square kernel
    mean_filter = np.ones((5,5))/(5**2)
    
    out = []
    for d, D in zip([sst_out, sic_out], [data_SST['analysed_sst'], data_SIC['ice_conc']]):
        # get data in region of interest
        conv = d[mask_interface.flatten()]
        # Replace nan with mean value of interface values
        # If this is not done we get affected by nan values (the land mask spreads)
        conv[np.isnan(conv)]=np.nanmean(conv)
        # find dimensions of area of interest - used to reshape
        index = np.where(mask_interface==True)
        length, width = len(np.unique(index[0])), len(np.unique(index[1]))
        
        # apply the mean filter and flatten the output
        a = scipy.signal.convolve2d(conv.reshape(length, width),
                                    mean_filter,
                                    boundary='symm',
                                    mode='same').flatten()
        
        # restore land mask 
        a[np.isnan(d[mask_interface.flatten()])]=np.nan
        
        # assign smoothed values to SST data
        d[mask_interface.flatten()] = a
        D = xr.DataArray(d.reshape(D.shape), 
                         coords=D.coords, 
                         dims={'time': 1, 'lat': 1800, 'lon': 7200})
        
        print('Interface smoothed \n')
        out.append(D)
        # plot output
        if plot:
            plot_cartopy(data_SST['lon'], data_SST['lat'], D.squeeze(), subplots=1, extend=[8, 14, 55, 59], title='OSTIA_BALTIC_INTERFACE_' + str(date), square=True)

    # assign final data to the output
    data_SST['analysed_sst'] = out[0]

    # EXCEPT FOR JUNE-DEC 2000, where we have no sea ice charts!
    y=date[:4]
    m=date[4:6]
    print(y)
    print(m)
    if int(y)!=2000 or int(m)<6:
        data_SIC['ice_conc'] = out[1]
    else: # revert ice source flag
        print('NOT USING ICECHARTS AS DATA IS MISSING')
        sic_source_flag[mask0.reshape(sst_source_flag.shape)] = np.max(sic_source_flag) # OSI SAF or SSMIS SIC

    return data_SST, data_SIC, sst_source_flag, sic_source_flag, statusflag_out
