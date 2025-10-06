import xarray as xr
import os
import re
import gzip
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
import pickle
from scipy.interpolate import splrep, BSpline

"""
Function for plotting heatmaps for input data used in DMI-MSC-SIC - allows for plotting both filtered and unfiltered data
Be aware that OSI-458 should possibily be changed with CARRA2 in the list of ID's when plotting filtered data
"""

HS = 'sh'
slice_sst = 0.5 # heatmap steps for SST
slice_sic = 3.0 # heatmap steps for SIC
Product_IDs = ['OSI-450-a', 'SICCI-HR-SIC', 'OSI-458'] # IDs of products to be plotted

year = input("\year? : ").strip()
months = list(map(str, input("\nEnter the Months : ").strip().split()))
filtered = 'combined filtering' # define filtering -either combined filtering or unfiltered

for month in months:
    if filtered=='combined filtering':
        if HS=='nh':
            datapath_OSI458 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/{year}/{month}/'
        else:
            datapath_OSI458 = f'/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/{year}/{month}/'
        sub_figpath = 'figures_filtered_final/'
        var = 'ice_conc'

        datapath_OSI450a = f'/dmidata/projects/cmems2/C3S/OSI450a/{year}/{month}/'
       
        datapath_SICCI = f'/dmidata/projects/cmems2/C3S/SICCI_HR_SIC/{year}/{month}/'

    if filtered=='unfiltered':
        datapath_ref_OSI450a =  f'/dmidata/projects/cmems2/C3S/OSI450a/{year}/{month}/'
        datapath_ref_SICCI = f'/dmidata/projects/cmems2/C3S/SICCI_HR_SIC/{year}/{month}/'
        if HS=='nh':
            datapath_ref_OSI458 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/{year}/{month}/'
        else:
            datapath_ref_OSI458 = f'/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/{year}/{month}/'
        datapath_OSI450a = f'/dmidata/projects/cmems2/C3S/OSI450a_extrap/{year}/{month}/'
        datapath_SICCI = f'/dmidata/projects/cmems2/C3S/SICCI_extrap/{year}/{month}/'
        datapath_OSI458 = f'/dmidata/projects/cmems2/C3S/OSI458_extrap/{year}/{month}/'

        sub_figpath = 'figures_unfiltered/'
        var = 'ice_conc'

    
    path = '/dmidata/projects/cmems2/C3S/CARRA2/heatmaps/'

    # define intervals
    SST_vals = np.arange(-2,13,slice_sst)
    SIC_vals = np.arange(0,100,slice_sic)
    print(SIC_vals)

    tup = [(sst, sic) for sst in SST_vals for sic in SIC_vals]


    def cmap_discretize(cmap, N):
        """Return a discrete colormap from the continuous colormap cmap.
            cmap: colormap instance, eg. cm.jet. 
            N: number of colors.
        """
        if type(cmap) == str:
            cmap = plt.get_cmap(cmap)
            colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
            colors_rgba = cmap(colors_i)
            indices = np.linspace(0, 1., N+1)
            cdict = {}
            for ki,key in enumerate(('red','green','blue')):
                cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in range(N+1) ]
            # Return colormap object.
            return LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)



    columns = [str(i) for i in SST_vals]
    indexes = [str(i) for i in SIC_vals]

    for Product_ID in Product_IDs:
        total_sum = 0
        d = pd.DataFrame(columns=columns, index=indexes).fillna(0)
        print(f'Initial dataframe created \n {d}')
        # loop through files to count occurences of each tuple pair
        means = np.zeros(len(SIC_vals))
        stds = np.zeros(len(SIC_vals))

        if Product_ID == 'SICCI-HR-SIC':
            datapath = datapath_SICCI
            if filtered=='unfiltered':
                datapath_ref = datapath_ref_SICCI
            SENSOR = '' #'SMMR,SSM/I,SSMIS'
            name = 'SICCI'
            with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{month}_{HS}.pkl', 'rb') as ff:
                tck_s3 = pickle.load(ff)


        elif Product_ID == 'OSI-450-a':
            datapath = datapath_OSI450a
            if filtered=='unfiltered':
                datapath_ref = datapath_ref_OSI450a
            SENSOR = '' #'SMMR,SSM/I,SSMIS'
            name = 'OSI'
            with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{month}_{HS}.pkl', 'rb') as ff:
                tck_s3 = pickle.load(ff)
        elif Product_ID == 'OSI-458':
            if filtered=='unfiltered':
                datapath_ref = datapath_ref_OSI458
            datapath = datapath_OSI458
            SENSOR = '' #'AMSR-E/2'
        
        if filtered=='combined filtering':
            datapath_ref = datapath

        files = [f for f in sorted(os.listdir(datapath)) if HS in f]
        print(datapath_ref)
        files_ref = [f for f in sorted(os.listdir(datapath_ref)) if HS in f]
        print(files_ref)
        
        for file, file_ref in zip(files, files_ref):
            print(file, file_ref)
            df = xr.open_dataset(datapath+file)
            
            if HS=='sh' and datapath==datapath_OSI458:
                ice_conc = df[var].sel(lat=slice(-90,0)).squeeze().to_numpy()
            else:
                ice_conc = df[var].squeeze().to_numpy()
                source_flag = xr.open_dataset(datapath_ref+file_ref)['iceconc_source'].squeeze().to_numpy()
                statusflag = xr.open_dataset(datapath_ref+file_ref)['status_flag'].squeeze().to_numpy()

            mask = xr.open_dataset(datapath_ref+file_ref)['mask'].squeeze().to_numpy()
            index = (((mask==1) | (mask==8) | (mask==32)) & (source_flag!=1) & (source_flag!=2) & ~((statusflag == 32) & (ice_conc == 100)) & (ice_conc>0)) #& (~np.isnan(df['ice_conc_orig'].squeeze().to_numpy())))
            data_SST = xr.open_dataset(datapath_ref+file_ref)['analysed_sst'].values.squeeze()[index] - 273.15
            # data_SST = xr.open_dataset(df_SST+file_SST)['analysed_sst'].squeeze().to_numpy()[index] - 273.15
            data_SIC = ice_conc[index]

            total_sum += np.sum(index)

            df.close()

            for i, vsic in enumerate(SIC_vals):
                mask_SIC_i = (data_SIC <= (vsic+slice_sic/2)) & (data_SIC > (vsic-slice_sic/2))
                means[i] += np.nanmean(data_SST[mask_SIC_i])
                # print(f'{vsic}: {np.mean(data_SST[mask_SIC_i])}')
                stds[i] += np.nanstd(data_SST[mask_SIC_i])
                
            
            for t in tup:
                vsst, vsic = t[0], t[1]
                if vsst==SST_vals[-1]:
                    mask_SST = data_SST> (vsst-slice_sst/2)
                else:
                    mask_SST = (data_SST <= (vsst+slice_sst/2)) & (data_SST> (vsst-slice_sst/2))
                mask_SIC = (data_SIC <= (vsic+slice_sic/2)) & (data_SIC > (vsic-slice_sic/2)) # & (data_SIC>15)
                m = np.logical_and(mask_SST, mask_SIC)
        
                d.loc[str(vsic), str(vsst)] += m.sum()

        plt.figure()
        N = 15
        cmap = cmap_discretize('Reds', N)
        svm = sns.heatmap(d.astype(float), linewidth=0.02,
                        linecolor="white",
                        cmap='Reds', #cmap, 
                        norm=LogNorm(vmin=10, vmax=1e7))

        m = means/len(files)
        s=stds/len(files)

        print(m)
        print(s)

        m = m * len(m)/15
        s = s * len(s)/15

        # To plot a box around the heatmap region with high SSTs and intermediate SICs
        # x_start = 8*1.99       # SST lower bound (°C)
        # width = 7*2         # SST span: 6 to 12 -> width = 6
        # y_start = 15/3      # SIC lower bound (%)
        # height = 80/3 - y_start  # height up to 100%

        # # Add rectangle to the heatmap (ax = svm)
        # rect = patches.Rectangle(
        #     (x_start, y_start),  # bottom left corner
        #     width,
        #     height,
        #     linewidth=1.5,
        #     edgecolor='black',
        #     facecolor='none',    # transparent fill
        #     linestyle='--'
        # )
        # svm.add_patch(rect)

        ax2 = svm.twinx()
        ax2.errorbar(m-np.min(m) + 0.5, SIC_vals, c='k', xerr=s, linewidth=0.7, marker='o', markersize=2, capsize=3)
        svm.invert_yaxis()
        ax2.set_yticks([])
        ax2.set_ylim([-1.5, 100.5])
        ax2.set(frame_on=False)
        cbar = svm.collections[0].colorbar  # get the colorbar
        cbar.ax.tick_params(labelsize=13)

        # plt.xlabel(u"SST [\u00b0C]")
        svm.set_ylabel("SIC [%]", fontsize=14)
        svm.set_xlabel(u"SST [\u2103]", fontsize=14)
        ax2.set_ylabel("No. of matchups", fontsize=14)
        svm.tick_params(axis='both', which='major', labelsize=13)

        name = f"{Product_ID}, {filtered}, {year}{month}"
        #name = f"DMI-MSC-SIC[{Product_ID}]{SENSOR}, {year}{month}"
        plt.suptitle(name, fontsize=16)
        plt.title(f'Count SIC>0: {total_sum}', fontsize=14)

        figure = svm.get_figure()
        if not os.path.exists(path + sub_figpath): os.makedirs(path + sub_figpath)
        figure.savefig(path + sub_figpath + Product_ID + f'_{filtered}_{year}{month}_{HS}_v3.png', dpi=400, bbox_inches='tight')

