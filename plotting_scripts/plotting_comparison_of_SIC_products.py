#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:19:43 2023

@author: ilo

This script creates geographical comparisons of filtered and untiltered data used as input for DMI-MSC-SIC
"""

__version__ = '0.1'
__author__ = 'Ida Olsen'
__contributers__ = ''
__date__ = '04/08/2023'
__updated__='31/07/2025'


# Build-in modules
import os
import re
# Third-party modules
import numpy as np
import netCDF4 as nc4
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
# Homemade modules 
from Extrapolate import Extrapolation


#%% Functions
def plot_file(self, a, var, mask, orig=False):
    # plotting function - adds a square around the Disco Bay and Uppernarvik areas consistent with MODIS
    # images on ocean.dmi.dk  
    a.set_extent(self.extend, ccrs.PlateCarree())
    if 'ice_conc' in var or 'sic' in var or var=='distance_to_land':
        vmin=0
        vmax=100
    else:
        vmin=0
        vmax=32
    if orig:
        variable = self.dataset_orig[var].squeeze().to_numpy()
        print(variable)
        latitude = self.dataset_orig['lat'].squeeze().to_numpy()
        longitude = self.dataset_orig['lon'].squeeze().to_numpy()
    else:
        variable = self.dataset[var].squeeze().to_numpy()
        latitude = self.dataset['lat'].squeeze().to_numpy()
        longitude = self.dataset['lon'].squeeze().to_numpy()
    # DISCO
    a.plot([-56.5, -49.5], [67.7, 68.2],
            color='limegreen', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-58.0, -50.0], [70.1, 70.9],
            color='limegreen', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-56.5, -58.0], [67.7, 70.1],
            color='limegreen', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-49.5, -50.0], [68.2, 70.9],
            color='limegreen', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    #UPPERNARVIK
    a.plot([-56.5, -50.0], [69.5, 70.0],
            color='orange', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-59.2, -50.9], [71.8, 72.3],
            color='orange', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-56.5, -59.2], [69.5, 71.8],
            color='orange', linestyle='--',
            transform=ccrs.PlateCarree(),
            )
    a.plot([-50.0, -50.9], [70.0, 72.3],
            color='orange', linestyle='--',
            transform=ccrs.PlateCarree(),
            )


    #masked_data = np.ma.masked_where(mask==1, variable)

    variable[mask] = -100

    cmap = plt.cm.Blues_r.copy() 
    cmap.set_under('beige') # Masked land values will be gray

    cs = a.pcolormesh(longitude, latitude, variable, cmap=cmap,# shading='gouraud',
            transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax)
    a.set_title(self.title, fontsize=15)
    # a.gridlines()
    #a.add_feature(cfeature.LAND)
    #a.coastlines(resolution='10m', color='grey')
    # plt.show()
    return cs


class plotting_info:
    def __init__(self, name = str()):
        # specifies data access
        self.data_directory_filt = '/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/' # specify data to examine
        self.data_directory_orig = '/dmidata/projects/cmems2/C3S/' # specify data to examine
        self.output_dir = '/dmidata/projects/cmems2/C3S/CARRA2/figures/'
        self.year = '2007'
        self.month = '07'
        self.day = '29'
        # specify hemisphere
        self.HS = 'nh'
        self.name = name + '_SIC'
        
        # specify location
        self.extend = [-180, 180, 0, 90]

    def read_data(self, product_ID): 
        # Get data
        if product_ID=='OSI-450-a':
            data_directory_orig = self.data_directory_orig + 'OSI450a_extrap/' # specify data to examine
            self.data_directory_filt = self.data_directory_orig + 'OSI450a/' # specify data to examine
        elif product_ID=='OSI-458':
            data_directory_orig = self.data_directory_orig + 'OSI458_extrap/' # specify data to examine
            # for data after 2002 use the carra2 folder defined above instead
            #self.data_directory_filt = self.data_directory_orig + 'OSI458/' # specify data to examine
        elif product_ID=='SICCI-HR-SIC':
            data_directory_orig = self.data_directory_orig + 'SICCI_extrap/' # specify data to examine
            self.data_directory_filt = self.data_directory_orig + 'SICCI_HR_SIC/' # specify data to examine
        elif product_ID=='ASIP':
            data_directory_orig = '/dmidata/projects/asip-cms/reproc/mosaics/level3_0500m_v1/'
        else:
            data_directory_orig = self.data_directory_orig + 'orig_carra2_extrap/' # specify data to examine
        
        # get filtered data
        directory = self.data_directory_filt + f'{self.year}/{self.month}/'
        files = [f for f in os.listdir(directory) if f.endswith('.nc')]
        
        # get unfiltered data
        if product_ID!='ASIP':
            files_orig = [f for f in os.listdir(data_directory_orig + f'{self.year}/{self.month}/') if ((f.endswith('.nc')) and (self.HS in f))]
        else:
            files_orig = [f for f in os.listdir(data_directory_orig)]

        #print(files_orig)
        directory_SST = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SST_data/OSTIA/NH/{self.year}/{self.month}'
        files_SST = [f for f in os.listdir(directory_SST) if f.endswith('.nc')]

        # find dates in filenames
        numbers = [re.findall('[0-9]+', f)[-2] for f in files]
        if product_ID=='CARRA2':
            numbers_orig = [re.findall('[0-9]+', f)[-1] for f in files_orig]
        else:
            numbers_orig = [re.findall('[0-9]+', f)[-1] for f in files_orig]
        # find file belonging to the desired date
        self.file = os.path.join(directory,[f for f,n in zip(files, numbers) if (n==self.year+self.month+self.day in f)][0])
        if product_ID!='ASIP':
            self.file_orig = os.path.join(data_directory_orig + f'{self.year}/{self.month}/',[f for f,n in zip(files_orig, numbers_orig) if (n==self.year+self.month+self.day in f)][0])
            print(self.file_orig)
        else:
            self.file_orig = os.path.join(data_directory_orig,[f for f,n in zip(files_orig, numbers_orig) if (n==self.year+self.month+self.day in f)][0])
            print(self.file_orig)
        # find SST file belonging to the desired date
        self.file_SST = os.path.join(directory_SST,[f for f in files_SST if (self.year+self.month+self.day in f)][0])

        self.dataset = xr.open_dataset(self.file)
        self.dataset_orig = xr.open_dataset(self.file_orig)

    def set_title(self, ID, orig=True):
        if orig==False:
            # set the figure title
            if ID=='CARRA2':
                ID='DMI-MSC [OSI-458]'
            elif ID=='ASIP':
                ID=ID
            else:
                ID=f'DMI-MSC [{ID}]'
        
        self.title = ID + f': ' + self.year + '-' + self.month + '-' + self.day
       
#%% COMPARISON OF SIC PRODUCTS at DISCO BAY, GULF OF OB and BALTIC SEA

# Set date
y='2017' 
m='07'
orig = True # True for unfiltered, False for filtered

#%% SIC products
Product_IDs = ['OSI-458', 'SICCI-HR-SIC', 'OSI-450-a'] # ['ASIP','CARRA2'] #, 'ASIP'] #, 'ASIP'] # , 'SICCI_HR', 'OSI450a'] 
# identifier = ['OSI', 'AMSR2', 'SSMIS']
# Dates to plot
days = ['0' + str(i) if i<10 else str(i) for i in np.arange(1,31)]
for day in ['28']: #, '25']: #, '30']: # ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11',  '12']: # ['01', '06', '10']: # , '10']:
    [disco, Gulf_ob, Baltic] = [plotting_info('Disco_bay'), plotting_info('Gulf_ob'), plotting_info('Baltic')]
    disco.day = day
    Gulf_ob.day = day
    Baltic.day = day

    disco.year = y
    Gulf_ob.year = y
    Baltic.year = y
    
    # Discobay coordinates
    disco.extend = [-61.0, -48.0, 66.5, 73.5] #[-59.7, -49.8, 67.0, 72.9]
    # Gulf ob coordinates
    Gulf_ob.extend = [51, 85, 63, 80]
    # Baltic sea coordinatees
    Baltic.extend = [-180, 180, 50, 90] # [9, 40, 50, 70]

    # loop over areas
    for d in [disco]: #, Gulf_ob, Baltic]:
        # set day
        d.day = day
        # loop over "filtered/unfiltered"
        for var in ['ice_conc']: #ice_conc
            # set month
            d.month = m
            # initiale subplot
            fig, ax = plt.subplots(nrows=1, ncols=3,
                                    subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(d.extend[:2]),
                                                                                            np.mean(d.extend[2:4]))},
                                    figsize=(14.2,10))
            # loop over product IDs
            for ID, a in zip(Product_IDs, ax.flatten()):
                if ID == 'ASIP':
                    var = 'sic'
                else:
                    var = 'ice_conc'
                print('reading data')
                d.read_data(ID)
                if ID == 'ASIP':
                    mask = d.dataset_orig['status_flag'].squeeze().to_numpy() == 1
                else:
                    mask = d.dataset['mask'].squeeze().to_numpy() == 2

                    plt.figure()
                    plt.imshow(mask)
                    plt.savefig('/dmidata/projects/cmems2/C3S/CARRA2/test.png')
                    plt.close()

                # set title 
                d.set_title(ID, orig=orig)
                # plot data to figure
                # if ID=='CARRA2':
                #     cs = plot_file(d, a, var=var, mask=mask, orig=orig)
                # else:
                #     #d.dataset_orig = d.dataset_orig.sel(lat=slice(d.extend[2], d.extend[3]), lon=slice(d.extend[0], d.extend[1]))
          
                cs = plot_file(d, a, var=var, mask=mask, orig=orig)
                print(f'Plotting data for: {ID}')


            
            # Delete the unwanted ax
            # fig.delaxes(ax.flatten()[3])
            # Adjust the location of the subplots on the page to make room for the colorbar
            fig.subplots_adjust(bottom=0.23, top=0.89, left=0.1, right=0.9,
                                    wspace=0.02, hspace=0.1)
            if orig==False: # add colorbar
                # Add a colorbar axis at the bottom of the graph
                cbar_ax = fig.add_axes([0.15, 0.275, 0.7, 0.03])
                # Draw the colorbar
                cbar=fig.colorbar(cs, cax=cbar_ax,orientation='horizontal')
                cbar.ax.tick_params(labelsize=14)
                cbar.set_label('SIC (%)', fontsize=16)
            print('saving figure')
            path = os.path.join(d.output_dir, f'{y}_{m}/')
            if not os.path.exists(path): os.mkdir(path)
            # fig.suptitle(f'SIC comparison for the {d.name}')
            plt.savefig(path + d.title + d.name + f'_{var}.png', bbox_inches='tight')
            # plt.show()
            plt.close()
            