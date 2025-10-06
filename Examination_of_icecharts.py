import glob
import xarray as xr
import numpy as np
import re
import matplotlib.pyplot as plt
import datetime as dt
from Extrapolate import Extrapolation, extrapolate_2d_data
from plotting_functions import plot_cartopy

def Get_landfast_ice(date, regrid_osisaf_sic_filt, data_SIC, data_SST, sic_source_flag, statusflag, ice_chart_filtering=False, landfast_ice_extrap=False, HS='nh'):
    """
    We use two types of information from the icecharts
    1. We include the landfast ice and sets this to 100% SIC
    2. if two subsequent SIC maps have recorded water for a given location we set the SIC to 0
    """
    year = date[:4]
    
    date = dt.datetime.strptime(date, '%Y%m%d')
    lower = date-dt.timedelta(days=21)
    upper = date+dt.timedelta(days=21)

    # we have a period in 2006/2007 with both SHP and BIN files
    if int(year)<=2007:
        filetype='BIN'
    else:
        filetype='SHP'
    
    # find files in interval
    if HS=='nh':
        if lower.year == upper.year:
            files = glob.glob(f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/NIC/{year}/*{year}*NH*{filetype}*.nc')
        else:
            print('entered different years')
            files = glob.glob(f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/NIC/{lower.year}/*{lower.year}*NH*{filetype}*.nc')
            files += glob.glob(f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/NIC/{upper.year}/*{upper.year}*NH*{filetype}*.nc')
    elif HS=='sh':
        if lower.year == upper.year:
            files = glob.glob(f'/dmidata/projects/cmems2/C3S/FSHEM/regridded/{year}/*{year}*.nc')
        else:
            print('entered different years')
            files = glob.glob(f'/dmidata/projects/cmems2/C3S/FSHEM/regridded/{lower.year}/*{lower.year}*.nc')
            files += glob.glob(f'/dmidata/projects/cmems2/C3S/FSHEM/regridded/{upper.year}/*{upper.year}*.nc')

    ##### day with smallest discrepancy between dates ####
    # find dates and convert to datetime object
    dates = [dt.datetime.strptime(re.findall('\d+',f)[-1], '%Y%m%d') for f in files]
    index = np.argsort(dates)
    # compute time differences
    delta = [abs(date-d) for d in np.array(dates)[index]]
    # make sure that files are in descending order based on temporal distance
    files = np.array(files)[index]

    # find location of minimum difference
    file_index = np.argmin(delta)

    print(f'Temporal Distance between files (SIC-Icechart) are: {delta[file_index]}')
    print(f'closest file is: {files[file_index]}')

    d = xr.open_dataset(files[file_index])

    ## open neighbouring file
    dates = np.array(dates)[index] # order dates

    # if smallest temporal distance was after the SIC/SST date
    if (date-dates[file_index]).total_seconds()<=0:
        # Sea ice chart date after or the same as dataSIC date
        # pick the file before
        d2 = xr.open_dataset(files[file_index-1])
        print(f'Second closest previous file {files[file_index-1]}')
    elif (date-dates[file_index]).total_seconds()>0:
        # Sea ice chart date before dataSIC date
        # pick the file after
        d2 = xr.open_dataset(files[file_index+1])
        print(f'Second closest subsequent file {files[file_index+1]}')

    ## LANDFAST ICE IDENTIFIER IS 92 for SHP files and 108 for BIN files
     ## OPEN WATER IDENTIFIER IS 0
    if HS=='nh': 
        if int(date.year)<2025:
            codes = d.sel(lat=slice(50,90))['codes'].squeeze().to_numpy()
            codes2 = d2.sel(lat=slice(50,90))['codes'].squeeze().to_numpy()
        else:
            try:
                codes = d.sel(lat=slice(50,90))['total_concentration'].squeeze().to_numpy()
            except:
                codes = d.sel(lat=slice(50,90))['codes'].squeeze().to_numpy()
            try:
                codes2 = d2.sel(lat=slice(50,90))['total_concentration'].squeeze().to_numpy()
            except:
                codes2 = d2.sel(lat=slice(50,90))['codes'].squeeze().to_numpy()

    else:
        codes = d.sel(lat=slice(-90,-50))['codes'].squeeze().to_numpy()
        codes2 = d2.sel(lat=slice(-90,-50))['codes'].squeeze().to_numpy()
    # extrapolate code
    if HS=='nh' and landfast_ice_extrap:
        # ADD CODE HERE
        mask = data_SST.sel(lat=slice(50,90))['mask'].squeeze().to_numpy()==2

        lon, lat = np.meshgrid(data_SIC.sel(lat=slice(50,90))['lon'], data_SIC.sel(lat=slice(50,90))['lat'])
        
        #Added SHP file on 13/01/2025 (Can be used in the future - however shapefiles have a finer landmask, therefore this is less important)
        # if 'SHP' in str(files[file_index]):
        #     codes[codes==255]=np.nan
        #     codes2[codes2==255]=np.nan            
        # else: #For BIN files
        if 'BIN' in str(files[file_index]):
            print('entered not correct!')
            codes[codes==254]=np.nan
            codes2[codes2==254]=np.nan

            codes, dummy = extrapolate_2d_data(mask, lon, lat, codes, np.zeros(codes.shape), 'nh')
            codes2, dummy = extrapolate_2d_data(mask, lon, lat, codes2, np.zeros(codes2.shape), 'nh')

        codes[mask]=np.nan
        codes2[mask]=np.nan

    if HS=='nh': # and landfast_ice_extrap:
        # set landfast ice to 100% SIC
        if 'BIN' in str(files[file_index]):
            landfast_ice_code=108
        elif 'SHP' in str(files[file_index]):
            landfast_ice_code=92

        data_SIC.sel(lat=slice(50,90))['ice_conc'].squeeze().to_numpy()[np.logical_and(codes==landfast_ice_code,sic_source_flag!=1)]=100
        regrid_osisaf_sic_filt[np.logical_and(codes==landfast_ice_code,sic_source_flag!=1)]=100
        sic_source_flag[np.logical_and(codes==landfast_ice_code,sic_source_flag!=1)] = (2**1)

    
    # if ice chart filtering is true and the two closest icecharts are on either side of the particular date
    #(date-dates[file_index]).total_seconds()<=0
    #check = True: if files[file_index-1]
    if ice_chart_filtering:
        criteria = ((date>dt.datetime(1986, 3, 28)) and (date<dt.datetime(1986,6,24)))
        criteria2 = ((date>dt.datetime(1987, 12, 3)) and (date<dt.datetime(1988,1,13)))
        # for 1986 do icechart filtering in the whole area because of missing data
        if criteria or criteria2:
            print('in longer period with missing data: doing icechart filtering everywhere (not only in near coastal regions)')
            ow_index = np.logical_and(codes==0, codes2==0)
            # define index of change e.g ow index, but where the previosu SIC was not already 0
            index_of_change = np.logical_and(ow_index, regrid_osisaf_sic_filt!=0)
            # Do not filter if in the Baltic sea
            ow_index = np.logical_and(sic_source_flag!=1, ow_index)
            index_of_change = np.logical_and(sic_source_flag!=1, index_of_change)
            # set sea ice chart open water to open water
            regrid_osisaf_sic_filt[ow_index]=0
            # define areas of change in statusflag and set the source to icechart
            statusflag[index_of_change] += (2**4)
            sic_source_flag[index_of_change] = (2**1)

        else:
            # correct for open water at a distance limit of 75 km from land
            distance_to_land = xr.open_dataset('distance_to_land_nh.nc').sel(lat=slice(50,90))['distance_to_land'].squeeze().to_numpy()
            # define index of open water = openwater in to closest NIC sea ice charts (code=0) & distance to land <= 75 km
            ow_index = np.logical_and(np.logical_and(codes==0, codes2==0), distance_to_land<=75)
            # define index of change e.g ow index, but where the previous SIC was not already 0
            index_of_change = np.logical_and(ow_index, regrid_osisaf_sic_filt!=0)
            # Do not filter if in the Baltic sea
            ow_index = np.logical_and(sic_source_flag!=1, ow_index)
            index_of_change = np.logical_and(sic_source_flag!=1, index_of_change)
            # set sea ice chart open water to open water
            regrid_osisaf_sic_filt[index_of_change]=0
            # define areas of change in statusflag and set the source to icechart
            statusflag[index_of_change] += (2**4)
            sic_source_flag[index_of_change] = (2**1)
    


    return data_SIC, regrid_osisaf_sic_filt, sic_source_flag.reshape(regrid_osisaf_sic_filt.shape), statusflag.reshape(regrid_osisaf_sic_filt.shape)
