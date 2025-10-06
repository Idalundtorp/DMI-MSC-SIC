import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('tableau-colorblind10')
import pandas as pd
import zarr
import os
import numpy as np
from sklearn.metrics import root_mean_squared_error, mean_absolute_error #(possible alternative metric)
import glob
import matplotlib.colors as mcolors
import cartopy


def create_dictionary():

    # Column names
    columns = ['landsat', 'osi450a', 'asip', 'carra2',  'osisaf', 'nsidc']
    # asip, carra2, osi458, nsidc, snu

    # Create the nested dictionary
    data = {col: None for col in columns}

    # Print example
    print(data)

    return data

def get_landsat_data():
    # List of seasons as strings
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    name='landsat'
    # Create the nested dictionary
    data = {month: None for month in months}
    zarrs_p1 = []
    for m in data:
        zarrs_p1 = sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????{m}??.zarr'))
        tmp = [zarr.open(f, mode='r').datasets[f'{name}'][:] for f in zarrs_p1]
        tmp_combined = np.stack(tmp, axis=0)
        mask = np.isfinite(tmp_combined).flatten()
        data[m] = tmp_combined.flatten()[mask]
    
    return data

def get_monthly_data():
    # List of seasons as strings
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09'] #, '11', '12']
    columns = ['asip', 'carra2', 'osi450a', 'osisaf', 'nsidc', 'landsat']

    # Create the nested dictionary
    data = {month: {col: None for col in columns} for month in months}

    zarrs_p1 = []
    for m in data:
        print(m)
        for name in data[m]:
            #print(name)
            zarrs_p1 = []
            if name=='carra2':
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_carra2_on_25_km_polstere/????{m}??.zarr')))
                zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
            elif name=='osi450a':
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_OSI450a_on_25_km_polstere/????{m}??.zarr')))
                basenames = [os.path.basename(z) for z in zarrs_p1] 
                zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
            else:
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????{m}??.zarr')))
                files = [os.path.basename(z) for z in zarrs_p1]
            try:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}_sic'][:] for f in zarrs_p1]
            except:
                tmp = [zarr.open(f, mode='r').datasets[f'{name}'][:] for f in zarrs_p1]

            # combine sic fields
            tmp_combined = np.stack(tmp, axis=0)

            if name=='landsat':
                landfast_mask = np.isfinite(tmp_combined).flatten()
            elif name=='asip':
                asip_mask = np.isfinite(tmp_combined).flatten()
            elif name=='osisaf':
                osisaf_mask = np.isfinite(tmp_combined).flatten()
            elif name=='osi450a':
                osi450a_mask = np.isfinite(tmp_combined).flatten()
            elif name=='carra2':
                carra2_mask = np.isfinite(tmp_combined).flatten()
            elif name=='nsidc':
                nsidc_mask = np.isfinite(tmp_combined).flatten()

            data[m][name] = tmp_combined.flatten()

        mask = landfast_mask & asip_mask & osisaf_mask & carra2_mask & osi450a_mask
        for name in data[m]:
            data[m][name] = data[m][name][mask]
    return data

def do_matchup(s='All'):
    data = create_dictionary()
    if s=='Winter':
        months = ['12', '01', '02']
    elif s=='Spring':
        months = ['03', '04', '05']
    elif s=='Summer':
        months = ['06', '07', '08']
    elif s=='Autumn':
        months = ['09', '10', '11']
    elif s=='All':
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # matchup
    for name in data:
        print(name)
        zarrs_p1 = []
        if name=='carra2':
            for m in months:
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_carra2_on_25_km_polstere/????{m}??.zarr')))
            zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
        elif name=='osi450a':
            for m in months:
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/cmems2/C3S/ASIP/daily_OSI450a_on_25_km_polstere/????{m}??.zarr')))
            basenames = [os.path.basename(z) for z in zarrs_p1] 
            zarrs_p1 = [z for z in zarrs_p1 if os.path.basename(z) in files ]
        else:
            for m in months:
                zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????{m}??.zarr')))
            # get valid dates in range from zarr files
            files = [os.path.basename(z) for z in zarrs_p1]
        try:
            tmp = [zarr.open(f, mode='r').datasets[f'{name}_sic'][:] for f in zarrs_p1]
        except:
            tmp = [zarr.open(f, mode='r').datasets[f'{name}'][:] for f in zarrs_p1]

        # combine sic fields
        tmp_combined = np.stack(tmp, axis=0)

        if name=='landsat':
            landfast_mask = np.isfinite(tmp_combined).flatten()
            #mask = landfast_mask.flatten()
        elif name=='asip':
            asip_mask = np.isfinite(tmp_combined).flatten()
        elif name=='osisaf':
            osisaf_mask = np.isfinite(tmp_combined).flatten()
        elif name=='osi450a':
            osi450a_mask = np.isfinite(tmp_combined).flatten()
        elif name=='carra2':
            carra2_mask = np.isfinite(tmp_combined).flatten()
        elif name=='nsidc':
            nsidc_mask = np.isfinite(tmp_combined).flatten()

        data[name] = tmp_combined.flatten()

        

    mask = landfast_mask & asip_mask & osisaf_mask & carra2_mask & osi450a_mask
    for name in data:
        data[name] = data[name][mask]
    return data


def plot_monthly_landsat(data):
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    bin_support = []
    for m in months:
        try:
            bin_support.append(np.sum(np.isfinite(data[m]['landsat'])))
        except:
            bin_support.append(np.sum(np.isfinite(data[m])))

    # Create a DataFrame for bin support
    data_support = {
        'Support': bin_support,
        'Months': months
    }
    df_support_bins = pd.DataFrame(data_support, columns=['Support', 'Months'])

    # Set color palette
    #sns.set_palette(["#FF800E", "#ABABAB", "#5F9ED1", "#C85200", "#595959", "#898989", "#A2C8EC", "#FFBC79", "#CFCFCF", "#006BA4"])
    sns.set_palette(['#4363d8', '#f58231', '#dcbeff', '#800000', '#000075', '#a9a9a9'])

    fig, ax = plt.subplots(figsize=(9, 10))
    b = sns.barplot(x='Months', y='Support', ax=ax, data=df_support_bins)
    #b.axes.set_title("Title",fontsize=50)
    b.set_xlabel("Months",fontsize=18)
    b.set_ylabel("Number of samples",fontsize=18)
    b.tick_params(labelsize=16)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.set_yscale('log', base=10)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/distribution_Landsat_overlap.png', bbox_inches='tight', dpi=300)
    plt.show()

def plot_landsat_geographical():
    zarrs_p1 = []
    zarrs_p1.extend(sorted(glob.glob(f'/dmidata/projects/asip-cms/code/my_dataset_paper/daily_asip_snu_osisaf_nsidc_on_25_km_polstere/????????.zarr')))
    tmp = [zarr.open(f, mode='r').datasets[f'landsat'][:] for f in zarrs_p1] 
    # combine sic fields
    tmp_combined = np.stack(tmp, axis=0)
    print(np.sum(np.isfinite(tmp_combined)))
    finite_counts = np.sum(np.isfinite(tmp_combined), axis=0).astype(float)
    finite_counts[finite_counts==0] = np.nan
    print('computed count of landsat scenes')

    scale = '25'
    cmap = plt.cm.Blues # winter?
    lon = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lon_{scale}km.npy')
    lat = np.load(f'/dmidata/projects/asip-cms/code/my_dataset_paper/lat_{scale}km.npy')

    fig, ax = plt.subplots(1, 1, figsize=(9, 10), subplot_kw={'projection': cartopy.crs.NorthPolarStereo(central_longitude=-65)})

    ax.set_extent([-4e6, 2e6, -2.3e6, 1.5e6], cartopy.crs.NorthPolarStereo())
    ax.add_feature(cartopy.feature.OCEAN, color='black', zorder=100)
    ax.add_feature(cartopy.feature.LAND, zorder=103)
    ax.add_feature(cartopy.feature.COASTLINE, linewidth=0.1, zorder=104)
                
    im = ax.pcolormesh(lon, lat, finite_counts, transform=cartopy.crs.PlateCarree(), vmin=-20, vmax=60, zorder=102, cmap=cmap)

    cbar_ax = fig.add_axes([0.13, 0.10, 0.76, 0.02])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_ticks(np.arange(0, 61, 10))
    cbar.ax.set_xlim(0, 60)
    cbar.ax.tick_params(labelsize=16) #, length=5, width=1)      # tick font size and appearance
    cbar.set_label('Number of samples', fontsize=18)          # colorbar label size

    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/landsat_geographical_distribution', bbox_inches='tight', dpi=300)
    plt.close()



def plot_monthly(data):

    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    # Initialize lists to store RMSE and bias values for each bin
    rmse_asip_bins = []
    rmse_osisaf_bins = []
    rmse_nsidc_bins = []
    rmse_osi450a_bins = []
    rmse_carra2_bins = []
    bin_support = []

    bias_asip_bins = []
    bias_osisaf_bins = []
    bias_nsidc_bins = []
    bias_osi450a_bins = []
    bias_carra2_bins = []

    std_asip_bins = []
    std_osisaf_bins = []
    std_nsidc_bins = []
    std_osi450a_bins = []
    std_carra2_bins = []

    # Calculate RMSE for each bin
    for m in data:
        rmse_asip_bins.append(root_mean_squared_error(data[m]['landsat'], data[m]['asip']))
        rmse_osisaf_bins.append(root_mean_squared_error(data[m]['landsat'], data[m]['osisaf']))
        rmse_carra2_bins.append(root_mean_squared_error(data[m]['landsat'], data[m]['carra2']))
        rmse_osi450a_bins.append(root_mean_squared_error(data[m]['landsat'], data[m]['osi450a']))

        bias_asip_bins.append(data[m]['asip'] - data[m]['landsat'])
        bias_osisaf_bins.append(data[m]['osisaf'] - data[m]['landsat'])
        bias_carra2_bins.append(data[m]['carra2'] - data[m]['landsat'])
        bias_osi450a_bins.append(data[m]['osi450a'] - data[m]['landsat'])

        std_asip_bins.append(np.nanmedian(abs(data[m]['landsat'] - data[m]['asip'])))*1.4826
        std_osisaf_bins.append(np.nanmedian(abs(data[m]['landsat'] - data[m]['osisaf'])))*1.4826
        std_carra2_bins.append(np.nanmedian(abs(data[m]['landsat'] - data[m]['carra2'])))*1.4826
        std_osi450a_bins.append(np.nanmedian(abs(data[m]['landsat'] - data[m]['osi450a'])))*1.4826

        bin_support.append(np.sum(np.isfinite(data[m]['landsat'])))


    # Create a DataFrame for bin support
    data_support = {
        'Support': bin_support,
        'Months': months
    }
    df_support_bins = pd.DataFrame(data_support, columns=['Support', 'Months'])

    # Set color palette
    #sns.set_palette(["#FF800E", "#ABABAB", "#5F9ED1", "#C85200", "#595959", "#898989", "#A2C8EC", "#FFBC79", "#CFCFCF", "#006BA4"])
    sns.set_palette(['#ffe119', '#4363d8', '#f58231', '#dcbeff', '#800000', '#000075', '#a9a9a9'])

    # Create a DataFrame for plotting
    data_rmse = {
        'RMSE': rmse_asip_bins + rmse_osi450a_bins + rmse_osisaf_bins + rmse_carra2_bins,
        'Dataset': ['DMI-ASIP'] * len(rmse_asip_bins) + ['OSI-450-a'] * len(rmse_osi450a_bins) + ['OSI-458'] * len(rmse_osisaf_bins) + ['DMI-MSC-SIC'] * len(rmse_carra2_bins),
        'Months': months * 4
    }

    data_bias = {
        'Difference (%)': bias_asip_bins + bias_osi450a_bins + bias_osisaf_bins + bias_carra2_bins,
        #'Std': std_asip_bins + std_osisaf_bins + std_carra2_bins,
        'Dataset': ['DMI-ASIP'] * len(bias_asip_bins) + ['OSI-450-a'] * len(bias_osi450a_bins) + ['OSI-458'] * len(bias_osisaf_bins) + ['DMI-MSC-SIC'] * len(bias_carra2_bins),
        'Months': months * 4
    }

    df_rmse_bins = pd.DataFrame(data_rmse, columns=['RMSE', 'Dataset', 'Months'])
    df_bias_bins = pd.DataFrame(data_bias, columns=['Difference (%)','Dataset', 'Months'])

    # Explode the Values column to have one value per row
    df_bias_bins_exploded = df_bias_bins.explode('Difference (%)')

    # Plot RMSE line plot
    plt.figure(figsize=(12, 4))
    sns.lineplot(x='Months', y='RMSE', hue='Dataset', data=df_rmse_bins)
    plt.ylabel('RMSE [%]')
    plt.xlabel('Months')
    plt.xticks(rotation=0)
    plt.grid(True, linewidth=0.5)
    plt.legend(loc='upper right')
    plt.ylim(0, 35)



    # Plot bin support bars on a new y-axis
    ax2 = plt.gca().twinx()
    sns.barplot(x='Months', y='Support', data=df_support_bins, alpha=0.2, ax=ax2, color='gray')
    ax2.set_yscale('log', base=10)
    #ax2.set_ylim(100, 40000)
    ax2.set_ylabel('Number of samples', alpha=0.6)
    #ax2.legend(['Support'], loc='upper right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)

    for tl in ax2.get_yticklabels():
        tl.set_alpha(0.6)

    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/rmse_plot_monthly.png', bbox_inches='tight', dpi=300)

    plt.show()

    plt.figure(figsize=(12, 4))
    
    ax = sns.boxplot(x='Months', y='Difference (%)', hue='Dataset', data=df_bias_bins_exploded, width=0.5, linewidth=0.5, flierprops=dict(marker='.',markersize=0.3,markerfacecolor='red',markeredgecolor='red'))
    # add horizontal reference line at y=0
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)

    # Redraw the median lines manually
    for line in ax.artists:
        box = line
        box.set_edgecolor('black')  # box border color

    # Each box has 6 lines: (top, bottom, left, right, median, etc.)
    # But we’ll manually find the median lines and thicken them
    for i, line in enumerate(ax.lines):
        # Median lines occur every 6th line starting from 4
        if i % 6 == 4:
            line.set_linewidth(1)  # thicker median
            #line.set_color('tab:brown')
        else:
            line.set_linewidth(0.5)  # normal lines
    
    plt.grid(True, linewidth=0.3)
    plt.ylabel('Difference (%)')
    plt.xlabel('Months')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.ylim(-60, 60)

    # Plot bin support bars on a new y-axis
    ax2 = plt.gca().twinx()
    sns.barplot(x='Months', y='Support', data=df_support_bins, alpha=0.2, ax=ax2, color='gray')
    ax2.set_yscale('log', base=10)
    #ax2.set_ylim(100, 40000)
    ax2.set_ylabel('Number of samples', alpha=0.6)
    #ax2.legend(['Support'], loc='upper right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)

    for tl in ax2.get_yticklabels():
        tl.set_alpha(0.6)

    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/bias_plot_box_monthly.png', bbox_inches='tight', dpi=300)

    plt.show()


def plot(data, s='All'):
    # Define the bins
    # bins = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 100]
    #bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    bins = [0, 15, 30, 45, 60, 75, 90, 100]
    lim = 90 # set for plotting purposes

    # Initialize lists to store RMSE and bias values for each bin
    rmse_asip_bins = []
    rmse_osisaf_bins = []
    rmse_nsidc_bins = []
    rmse_osi450a_bins = []
    rmse_carra2_bins = []
    bin_support = []

    bias_asip_bins = []
    bias_osisaf_bins = []
    bias_nsidc_bins = []
    bias_osi450a_bins = []
    bias_carra2_bins = []

    std_asip_bins = []
    std_osisaf_bins = []
    std_nsidc_bins = []
    std_osi450a_bins = []
    std_carra2_bins = []

    # Calculate RMSE for each bin
    for i in range(len(bins) - 1):
        if bins[i] == lim:
            mask = (data['landsat'] >= bins[i]) & (data['landsat'] <= bins[i+1]) & (np.isfinite(data['landsat']))
        else:
            mask = (data['landsat'] >= bins[i]) & (data['landsat'] < bins[i+1]) & (np.isfinite(data['landsat']))

        if np.any(mask):
            rmse_asip_bins.append(root_mean_squared_error(data['landsat'][mask], data['asip'][mask]))
            rmse_osisaf_bins.append(root_mean_squared_error(data['landsat'][mask], data['osisaf'][mask]))
            rmse_carra2_bins.append(root_mean_squared_error(data['landsat'][mask], data['carra2'][mask]))
            rmse_osi450a_bins.append(root_mean_squared_error(data['landsat'][mask], data['osi450a'][mask]))

            bias_asip_bins.append(data['asip'][mask] - data['landsat'][mask])
            bias_osisaf_bins.append(data['osisaf'][mask] - data['landsat'][mask])
            bias_carra2_bins.append(data['carra2'][mask] - data['landsat'][mask])
            bias_osi450a_bins.append(data['osi450a'][mask] - data['landsat'][mask])

            std_asip_bins.append(np.std(data['landsat'][mask] - data['asip'][mask]))
            std_osisaf_bins.append(np.std(data['landsat'][mask] - data['osisaf'][mask]))
            std_carra2_bins.append(np.std(data['landsat'][mask] - data['carra2'][mask]))
            std_osi450a_bins.append(np.std(data['landsat'][mask] - data['osi450a'][mask]))

            
            bin_support.append(np.sum(mask))


    # Create a DataFrame for bin support
    data_support = {
        'Support': bin_support,
        'Bin': [f'[{bins[i]}-{bins[i+1]})' if bins[i] != lim else f'[{bins[i]}-{bins[i+1]}]' for i in range(len(bins) - 1)]
    }

    df_support_bins = pd.DataFrame(data_support, columns=['Support', 'Bin'])
    print(df_support_bins)

    # Set color palette
    # Define the tableau-colorblind10 colors
    #tableau_colorblind_palette = list(mcolors.TABLEAU_COLORS.values())  # Get the tableau colors
    #sns.set_palette(["#FF800E", "#ABABAB", "#5F9ED1", "#C85200", "#595959", "#898989", "#A2C8EC", "#FFBC79", "#CFCFCF", "#006BA4"])
    sns.set_palette(['#ffe119', '#4363d8', '#f58231', '#dcbeff', '#800000', '#000075', '#a9a9a9'])

    # Create a DataFrame for plotting
    data_rmse = {
        'RMSE': rmse_asip_bins + rmse_osi450a_bins + rmse_osisaf_bins + rmse_carra2_bins,
        'Dataset': ['DMI-ASIP'] * len(rmse_asip_bins) + ['OSI-450a'] * len(rmse_osi450a_bins) + ['OSI-458'] * len(rmse_osisaf_bins) + ['DMI-MSC-SIC'] * len(rmse_carra2_bins),
        'Bin': [f'[{bins[i]}-{bins[i+1]})' if bins[i] != lim else f'[{bins[i]}-{bins[i+1]}]' for i in range(len(bins) - 1)] * 4
    }

    data_bias = {
        'Difference (%)': bias_asip_bins + bias_osi450a_bins + bias_osisaf_bins + bias_carra2_bins,
        #'Std': std_asip_bins + std_osisaf_bins + std_carra2_bins,
        'Dataset': ['DMI-ASIP'] * len(bias_asip_bins) + ['OSI-450a'] * len(bias_osi450a_bins) + ['OSI-458'] * len(bias_osisaf_bins) + ['DMI-MSC-SIC'] * len(bias_carra2_bins),
        'Bin': [f'[{bins[i]}-{bins[i+1]})' if bins[i] != lim else f'[{bins[i]}-{bins[i+1]}]' for i in range(len(bins) - 1)] * 4
    }

    data_std = {
        'Std': std_asip_bins + std_osi450a_bins + std_osisaf_bins + std_carra2_bins,
        'Dataset': ['DMI-ASIP'] * len(bias_asip_bins) + ['OSI-450a'] * len(bias_osi450a_bins) + ['OSI-458'] * len(bias_osisaf_bins) + ['DMI-MSC-SIC'] * len(bias_carra2_bins),
        'Bin': [f'[{bins[i]}-{bins[i+1]})' if bins[i] != lim else f'[{bins[i]}-{bins[i+1]}]' for i in range(len(bins) - 1)] * 4
    }

    df_rmse_bins = pd.DataFrame(data_rmse, columns=['RMSE', 'Dataset', 'Bin'])
    df_std_bins = pd.DataFrame(data_std, columns=['Std', 'Dataset', 'Bin'])
    df_bias_bins = pd.DataFrame(data_bias, columns=['Difference (%)','Dataset', 'Bin'])

    # Explode the Values column to have one value per row
    df_bias_bins_exploded = df_bias_bins.explode('Difference (%)')

    # # #print(df_rmse_bins)
    # # Plot RMSE line plot
    # plt.figure(figsize=(12, 4))
    # sns.lineplot(x='Bin', y='RMSE', hue='Dataset', data=df_rmse_bins)
    # plt.ylabel('RMSE [%]')
    # plt.xlabel('Sea Ice Concentration [%]')
    # plt.xticks(rotation=0)
    # plt.grid(True, linewidth=0.5)
    # plt.legend(loc='upper right')
    # plt.ylim(0, 35)

    plt.figure(figsize=(12, 4))
    sns.lineplot(x='Bin', y='Std', hue='Dataset', data=df_std_bins)
    plt.ylabel('RSD')
    plt.xlabel('Sea Ice Concentration [%]')
    plt.xticks(rotation=0)
    plt.grid(True, linewidth=0.5)
    plt.legend(loc='upper right')
    plt.ylim(0, 35)


    # Plot bin support bars on a new y-axis
    ax2 = plt.gca().twinx()
    sns.barplot(x='Bin', y='Support', data=df_support_bins, alpha=0.2, ax=ax2, color='gray')
    ax2.set_yscale('log', base=10)
    ax2.set_ylim(100, 40000)
    ax2.set_ylabel('Number of samples', alpha=0.6)
    #ax2.legend(['Support'], loc='upper right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)

    for tl in ax2.get_yticklabels():
        tl.set_alpha(0.6)

    #plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/rmse_plot_{s}.png', bbox_inches='tight', dpi=300)
    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/std_plot_{s}.png', bbox_inches='tight', dpi=300)

    plt.show()

    #print(df_rmse_bins)
    # Plot RMSE line plot
    plt.figure(figsize=(12, 4))
    
    ax = sns.boxplot(x='Bin', y='Difference (%)', hue='Dataset', data=df_bias_bins_exploded, width=0.5, linewidth=0.5, flierprops=dict(marker='.', markersize=0.3,markerfacecolor='red',markeredgecolor='red'))
    # add horizontal reference line at y=0
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    # Redraw the median lines manually
    for line in ax.artists:
        box = line
        box.set_edgecolor('black')  # box border color

    # Each box has 6 lines: (top, bottom, left, right, median, etc.)
    # But we’ll manually find the median lines and thicken them
    for i, line in enumerate(ax.lines):
        # Median lines occur every 6th line starting from 4
        if i % 6 == 4:
            line.set_linewidth(1)  # thicker median
            #line.set_color('tab:brown')
        else:
            line.set_linewidth(0.5)  # normal lines
    plt.grid(True, linewidth=0.5)
    plt.ylabel('Difference (%)')
    plt.xlabel('Sea Ice Concentration [%]')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.ylim(-90, 90)



    # Plot bin support bars on a new y-axis
    ax2 = plt.gca().twinx()
    sns.barplot(x='Bin', y='Support', data=df_support_bins, alpha=0.2, ax=ax2, color='gray')
    ax2.set_yscale('log', base=10)
    ax2.set_ylim(100, 40000)
    ax2.set_ylabel('Number of samples', alpha=0.6)
    #ax2.legend(['Support'], loc='upper right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.3)

    for tl in ax2.get_yticklabels():
        tl.set_alpha(0.6)

    plt.savefig(f'/dmidata/projects/cmems2/C3S/ASIP/bias_plot_box_{s}.png', bbox_inches='tight', dpi=300)

    plt.show()



season = 'All'
data = do_matchup(s=season)
plot(data, s=season)


# data = get_landsat_data()
# plot_monthly_landsat(data)
# plot_landsat_geographical()

# data = get_monthly_data()
# plot_monthly(data)