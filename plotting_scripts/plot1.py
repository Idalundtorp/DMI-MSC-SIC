# Cartopy plot
import matplotlib
import numpy as np
import cartopy
import calendar
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import zarr
import os

def days_in_month(year, month):
    """
    Returns the number of days in a given month for a specified year.

    Parameters:
    - year (int): The year (between 2014 and 2024).
    - month (int): The month (1-12).

    Returns:
    - int: Number of days in the month.
    """
    if not (2014 <= year <= 2024):
        raise ValueError("Year must be between 2014 and 2024")
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")

    return calendar.monthrange(year, month)[1]  # Returns (weekday, num_days), we extract num_days


def create_nested_dictionary():
    # List of months as strings
    months = [f"{i:02d}" for i in range(1, 13)]  # ['01', '02', ..., '12']

    # Column names
    columns = ['asip', 'carra2', 'osi450a', 'osisaf', 'nsidc', 'landsat']
    # asip, carra2, osi458, nsidc, snu

    # Create the nested dictionary
    monthly_avg = {month: {col: None for col in columns} for month in months}

    # Print example
    print(monthly_avg)

    return monthly_avg


def create_nested_dictionary_season():
    # List of seasons as strings
    seasons = ['Winter (DJF)', 'Spring (MAM)', 'Summer (JJA)', 'Autumn (SON)']

    # Column names
    columns = ['asip', 'carra2', 'osi450a', 'osisaf', 'nsidc', 'landsat']
    # asip, carra2, osi458, nsidc, snu

    # Create the nested dictionary
    season_avg = {season: {col: None for col in columns} for season in seasons}

    # Print example
    print(season_avg)

    return season_avg

def compute_monthly_means():

    monthly_avg = create_nested_dictionary()

    # get all matches for the given month for each dataset
    for m in monthly_avg:
        print(f'Month: {m}')
        for name in monthly_avg[m]:
            #print(name)
            # get file
            if name=='carra2':   
                zarrs_p1 = sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_carra2_on_25_km_polstere/????{m}??.zarr'))
            else: 
                zarrs_p1 = sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????{m}??.zarr'))
        
            try:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}_sic'][:] for f in zarrs_p1]
            except:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}'][:] for f in zarrs_p1]
            
            # combine sic fields
            tmp_combined = np.stack(tmp, axis=0)

            # # read days in month
            # days = days_in_month(2014, int(m))

            # # slice tmp_combined into days in month
            # slices = np.split(tmp_combined, len(tmp_combined[:,0,0])/days)

            # #print(np.shape(slices))

            # # find valid datapoints per slice: Count finite elements along dimension 0
            # finite_counts = np.sum(np.isfinite(slices), axis=1)
            
            # #print(finite_counts.shape)
            # # replace where below limit

            # mask = finite_counts<15

            # for i in np.arange(0,days):
            #     slices = np.array(slices)
            #     slices_reshaped = slices.transpose(1, 0, 2, 3)
            #     slices_reshaped[i,mask] = np.nan

            # slices = slices_reshaped.reshape(slices.shape[0] * slices.shape[1], *slices.shape[2:])
            # #print(slices.shape)

            # # combine data # new version
            # tmp_combined = np.stack(slices, axis=0) 

            finite_counts = np.sum(np.isfinite(tmp_combined), axis=0)
            mask = finite_counts <=20

            # get monthly mean
            tmp_monthly = np.nanmean(tmp_combined,axis=0)
            tmp_monthly[mask] = np.nan

            monthly_avg[m][name] = tmp_monthly
    

    print('computed monthly means')

    return monthly_avg


def compute_seasonal_means():

    season_avg = create_nested_dictionary_season()

    # get all matches for the given month for each dataset
    for s in season_avg:
        print(f'Season: {s}')
        for name in season_avg[s]:

            if s=='Winter (DJF)':
                months = ['12', '01', '02']
            elif s=='Spring (MAM)':
                months = ['03', '04', '05']
            elif s=='Summer (JJA)':
                months = ['06', '07', '08']
            elif s=='Autumn (SON)':
                months = ['09', '10', '11']

            # get file
            if name=='carra2':
                zarrs_p1 = []
                for m in months:
                    zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_carra2_on_25_km_polstere/????{m}??.zarr')))
                zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
            elif name=='osi450a':
                zarrs_p1 = []
                for m in months:
                    zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_OSI450a_on_25_km_polstere/????{m}??.zarr')))
                zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
            else: 
                zarrs_p1 = []
                for m in months:
                    zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????{m}??.zarr')))
                files = [os.path.basename(z) for z in zarrs_p1]

        
            try:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}_sic'][:] for f in zarrs_p1]
            except:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}'][:] for f in zarrs_p1]
            
            # combine sic fields
            tmp_combined = np.stack(tmp, axis=0)
            finite_counts = np.sum(np.isfinite(tmp_combined), axis=0)
            mask = finite_counts <100
            tmp_combined[: , mask] = np.nan

            season_avg[s][name] = tmp_combined
    

    print('computed seasonal means')

    return season_avg

def plot(monthly_avg):

    scale = '25'
    months = [f"{i:02d}" for i in range(1, 13)]
    cmap = plt.cm.bwr

    lon = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lon_{scale}km.npy')
    lat = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lat_{scale}km.npy')

    fig, axes = plt.subplots(3, 4, figsize=(13, 11), subplot_kw={'projection': cartopy.crs.NorthPolarStereo(central_longitude=-65)})
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.03, hspace=0.13)
    for i, ax in enumerate(axes.flat):
        if i < len(months):
            month = str(months[i]).zfill(2)
            diff = monthly_avg[month]['asip'] - monthly_avg[month]['carra2']

            ax.set_extent([-4e6, 2e6, -2.3e6, 1.5e6], cartopy.crs.NorthPolarStereo())
            ax.add_feature(cartopy.feature.OCEAN, color='black', zorder=100)
            ax.add_feature(cartopy.feature.LAND, zorder=103)
            ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.1, zorder=104)
            
            im = ax.pcolormesh(lon, lat, diff, transform=cartopy.crs.PlateCarree(), zorder=102, cmap=cmap, vmin=-50, vmax=50)

            mean_diff = np.nanmean(diff)
            ax.text(0.61, 0.98, f'Mean diff: {mean_diff:.2f}%', transform=ax.transAxes, fontsize=8, horizontalalignment='left', verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), zorder=105)

            ax.set_title(f'{datetime.strptime(month, "%m").strftime("%B")}')
        else:
            ax.axis('off')

    cbar_ax = fig.add_axes([0.1, 0.013, 0.8, 0.02])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal', label='Mean Difference [%]')
    cbar.set_ticks(np.arange(-50, 51, 10))

    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/asip_v_carra2_monthly_diff_{scale}km.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_season(season_avg):

    scale = '25'
    seasons = ['Winter (DJF)', 'Spring (MAM)', 'Summer (JJA)', 'Autumn (SON)']
    cmap = plt.cm.seismic

    lon = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lon_{scale}km.npy')
    lat = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lat_{scale}km.npy')

    for name in ['osisaf', 'osi450a', 'carra2']:
        fig, axes = plt.subplots(1, 4, figsize=(12, 4), subplot_kw={'projection': cartopy.crs.NorthPolarStereo(central_longitude=-65)})
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.03, hspace=0.13)
        for i, ax in enumerate(axes.flat):
            if i < len(seasons):
                season = str(seasons[i])
                diff = season_avg[season][name] - season_avg[season]['asip']

                # get mean
                diff = np.nanmean(diff,axis=0)


                ax.set_extent([-4e6, 2e6, -2.3e6, 1.5e6], cartopy.crs.NorthPolarStereo())
                ax.add_feature(cartopy.feature.OCEAN, color='black', zorder=100)
                ax.add_feature(cartopy.feature.LAND, zorder=103)
                ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.1, zorder=104)
                
                im = ax.pcolormesh(lon, lat, diff, transform=cartopy.crs.PlateCarree(), zorder=102, cmap=cmap, vmin=-50, vmax=50)

                mean_diff = np.nanmean(abs(diff))
                ax.text(0.025, 0.98, f'Mean abs diff: {mean_diff:.2f}%', transform=ax.transAxes, fontsize=8, horizontalalignment='left', verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.95), zorder=105)

                ax.set_title(f'{season}')

                if i % 4 == 0:  # First column only (or wherever you want it)
                    if name=='carra2':
                        title = '[DMI-MSC-SIC] - [ASIP]'
                    elif name=='osisaf':
                        title = '[OSI458] - [ASIP]'
                    elif name=='osi450a':
                        title = '[OSI450a] - [ASIP]'
                    ax.text(-0.1, 0.5, title,
                            transform=ax.transAxes,
                            rotation='vertical',
                            va='center', ha='center',
                            fontsize=10)
                    
            else:
                ax.axis('off')

        if name=='osi450a':
            cbar_ax = fig.add_axes([0.1, 0.013, 0.8, 0.02])
            cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal', label='Mean Difference [%]')
            cbar.set_ticks(np.arange(-50, 51, 10))
            
        plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/asip_v_{name}_season_diff_{scale}km.png', bbox_inches='tight', dpi=300)
        plt.close()


# run
#monthly_avg = compute_monthly_means()
season_avg = compute_seasonal_means()
plot_season(season_avg)