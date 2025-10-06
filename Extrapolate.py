#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.2'
__author__ = 'Ida Olsen, Sotirios Skapalezos'
__contributers__ = 'Pia Englyst'
__date__ = '14/09/2023'

# Build-in modules

# Third-party modules
import numpy as np
import matplotlib.pyplot as plt
from plotting_functions import plot_cartopy
from scipy.interpolate import griddata

# Homemade modules

def Extrapolation(lat, grid, ext_num, statusflag, mask=None, lon=None, HS='nh'):
    # =============================================================================
    # EXTRAPOLATION - EXTRAPOLATION - EXTRAPOLATION - EXTRAPOLATION - EXTRAPOLATION
    # =============================================================================
    # Extrapolation into the fjords based on an average of the 8 nearest gridcelss
    # The extrapolation number decides how far into the fjords that we extrapolate
    # * Each iteration moves one pixel further into the fjord
    print('Extrapolation')
    print('-------------')

    # Find land pixels
    if mask is not None:
            if (mask==2).any():
                # convert into boolean array with True at land (2) and False everywhere else
                mask = mask == 2
            # pad mask
            mask = np.pad(mask, pad_width=1, mode='constant', constant_values=-999)
            mask[mask == -999] = np.nan
    # Find indices of NaN on the final_grid_pad (eg. land and areas to extrapolate to)
    idx_land = np.argwhere(np.isnan(grid))
    # assign "extrapolated value" statusflag
    statusflag[idx_land[:,0],idx_land[:,1]] += (2**5) # extrapolated + land

    # save original grid
    grid_out = np.copy(grid)
    
    # Pad array 
    final_grid_pad = np.pad(grid, pad_width=1, mode='constant', constant_values=-999)
    final_grid_pad[final_grid_pad == -999] = np.nan
    
    # perform extrapolation
    for i in np.arange(ext_num):
        if i%5==0: # print iteration number
            print(f'iteration: {i}')
        # Create the 8 shifted grids
        final_grid_pad_l = np.roll(final_grid_pad,-1,axis=1)
        # first collumn
        final_grid_pad_l[:,0] = np.nan
        
        final_grid_pad_r = np.roll(final_grid_pad,1,axis=1)
        # last collumn
        final_grid_pad_r[:,-1] = np.nan

        final_grid_pad_u = np.roll(final_grid_pad,-1,axis=0)
        # first row
        final_grid_pad_u[0,:] = np.nan

        final_grid_pad_d = np.roll(final_grid_pad,1,axis=0)
        # last row
        final_grid_pad_d[-1,:] = np.nan

        final_grid_pad_lu = np.roll(final_grid_pad_l,-1,axis=0)
        final_grid_pad_lu[0,:] = np.nan

        final_grid_pad_ld = np.roll(final_grid_pad_l,1,axis=0)
        final_grid_pad_ld[-1,:] = np.nan
        
        final_grid_pad_ru = np.roll(final_grid_pad_r,-1,axis=0)
        final_grid_pad_ru[0,:] = np.nan
        
        final_grid_pad_rd = np.roll(final_grid_pad_r,1,axis=0)
        final_grid_pad_rd[-1,:] = np.nan
        
        # Stack them together with the initial grid and calculate nanmean along the 3rd dimension
        final_grid_pad_stack = np.stack((final_grid_pad,
                                         final_grid_pad_l,
                                         final_grid_pad_r,
                                         final_grid_pad_u,
                                         final_grid_pad_d,
                                         final_grid_pad_lu,
                                         final_grid_pad_ld,
                                         final_grid_pad_ru,
                                         final_grid_pad_rd
                                         ),axis=2)
        
        # Calculate nanmean for the land + nearland pixels
        final_grid_pad_mean = np.nanmean(final_grid_pad_stack,axis=2)
        # assign those values which now have a value
        if i<(ext_num-10): 
            final_grid_pad[np.isnan(final_grid_pad)] = final_grid_pad_mean[np.isnan(final_grid_pad)]
        # smooth the output for the last 10 extrapolation iterations
        elif i>=(ext_num-10): 
            final_grid_pad = final_grid_pad_mean
        # apply land mask - this avoids extrapolating over land 
        if mask is not None:
            try:
                final_grid_pad[mask] = np.nan
            except: # no land 
                pass
    
    # restore original size of grid
    final_grid_pad = final_grid_pad[1:-1,1:-1]
    try: # resize mask
        mask = mask[1:-1,1:-1]
    except:
        pass
    # Replace the extrapolated pixels in the original grid
    grid_out[idx_land[:,0],idx_land[:,1]] = final_grid_pad[idx_land[:,0],idx_land[:,1]]

    # for any non filled out values we do nearest neighbour extrapolation
    if lon is not None:
        grid_out, statusflag = extrapolate_2d_data(mask, lon, lat, grid_out, statusflag, HS)
    print('Extrapolation complete\n')
    
    return grid_out, statusflag

def extrapolate_2d_data(land_mask, lon, lat, regrid_osisaf_sic_filt, statusflag, HS, method='nearest', subset='all'):
    """
    Extrapolate 2D gridded data to new points using cubic interpolation.

    Parameters:
    - x: 1D array-like, x-coordinates of the original grid.
    - y: 1D array-like, y-coordinates of the original grid.
    - z: 1D array-like, values at the original grid points.
    - x_new: 1D array-like, x-coordinates of the points to extrapolate to.
    - y_new: 1D array-like, y-coordinates of the points to extrapolate to.
    
    Returns:
    - Extrapolated values at the new points.
    """
    # we do not expect any sea ice between 0 and 40 degrees lattitude

    # Identify NaN values in the ice_conc variable
    nan_mask = np.isnan(regrid_osisaf_sic_filt)

    # Create a mask for coastal points
    
    if HS=='nh':
        latlim = lat >= 40
    else:
        latlim = lat <= -40
    try:
        coastal_points = ((nan_mask) & (~land_mask) & (latlim))
    except:
        print('not using landmask')
        coastal_points = ((nan_mask) & (latlim))
    
    if subset=='SIC>0':
        lat_in, lon_in = lat[((~nan_mask) & (regrid_osisaf_sic_filt>0))], lon[((~nan_mask) & (regrid_osisaf_sic_filt>0))]
        SIC = regrid_osisaf_sic_filt[((~nan_mask) & (regrid_osisaf_sic_filt>0))]
    else:
        # create meshgrid
        lat_in, lon_in = lat[~nan_mask], lon[~nan_mask]
        SIC = regrid_osisaf_sic_filt[~nan_mask]
    
    lat_out, lon_out = lat[coastal_points], lon[coastal_points]

    # Perform nearest interpolation only with non-NaN values
    coastal_sic = griddata((lon_in,
                            lat_in),
                            SIC,
                            (lon_out,
                            lat_out),
                            method=method)
    
    regrid_osisaf_sic_filt[coastal_points] = coastal_sic
    statusflag[coastal_points] = (2**5)

    return regrid_osisaf_sic_filt, statusflag