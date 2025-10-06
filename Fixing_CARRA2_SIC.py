from scipy.ndimage import gaussian_filter, uniform_filter
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import os
from Save_Filtered_SIC_in_nc_file import SaveNCfile
from Decide_SIC_source import identify_product_ID
import pickle
from scipy.interpolate import splrep, BSpline

# Steps to do
# 1 implement SIC sensor bias correction
# 2 FIX SICCI HR SIC pole hole
# 3 set nan values to 0
# 4 1986 ? Not happening..'


def SIC_post_processing(HS, y, m, dd):
        if HS=='nh':
            dir = f"/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/{y}/{m}/"
        if HS=='sh':
            dir = f"/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/{y}/{m}/"
        # Find files in datafolders
        files = sorted(os.listdir(dir))
        #print(files)
        # loop through relevant dates and find belonging files
        #for dd in days:
        # identify source
        ID = identify_product_ID(int(y), int(m), int(dd))
        print(ID)
    
        #try:
        d = f'{y}{m}{dd}'
        # added the 4/10/2024 to processes wrong files for OSI450a
        #if d in patch_dates:
        
        # added 'test' the 4/10/2024 to processes wrong files for OSI450a
        # removed 'test' the 26/08/2025
        # changes to look for newest file 4/9/2025
        matches = [f for f in files if d in f]
        # pick the newest created file
        fsic = max(matches, key=lambda f: os.path.getctime(os.path.join(dir, f)))
        print(fsic)

        if HS=='sh':
            data_SIC = xr.open_dataset(dir + fsic).sel(lat=slice(-90,0))
        else:
            data_SIC = xr.open_dataset(dir + fsic)
        # load SIC, source and statusflag
        ice_conc = data_SIC['ice_conc'].squeeze().to_numpy()
        source_flag = data_SIC['iceconc_source'].squeeze().to_numpy()
        statusflag = data_SIC['status_flag'].squeeze().to_numpy()

        extend=[-180, 180, 60, 90]
        
        # fig, ax = plt.subplots(nrows=1, ncols=1,
        #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
        #                                                                         np.mean(extend[2:4]))},
        #                 figsize=(10,10))
        # ax.set_extent(extend, ccrs.PlateCarree())
        # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
        #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
        # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
        # ax.set_title(f'SIC pole hole for {d}')
        # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
        # plt.savefig(f'SIC_original_{d}.png', bbox_inches='tight')


        # FIX WIERD POLE HOLE FOR SICCI HR
        if ID == 'SICCI_HR_SIC' and HS=='nh':
            print('SICCI HR PERIOD FIXING POLE HOLE')
        #if ((np.logical_and(y>1991, y<2003)) or (y==2012)):
            file2 = f"/dmidata/projects/cmems2/C3S/OSI450a_extrap/{y}/{m}/OSI450a_{d}_{HS}.nc"
            ice_conc_OSI450a = xr.open_dataset(file2).sel(lat=slice(87,90))['ice_conc'].squeeze().to_numpy()
            # replace pole hole in SICCI HR SIC with OSI450a SIC
            ice_conc[-ice_conc_OSI450a.shape[0]:,:]=ice_conc_OSI450a

            # apply filter to smooth the transfer between the products
            result = uniform_filter(ice_conc[-ice_conc_OSI450a.shape[0]-20:-ice_conc_OSI450a.shape[0]+20,:], size=(5,100), mode='nearest')
            ice_conc[-ice_conc_OSI450a.shape[0]-20:-ice_conc_OSI450a.shape[0]+20,:]=result

            # change SIC source to OSI450a
            source_flag[-ice_conc_OSI450a.shape[0]:,:] = (2**2) # OSI450a

            # extend=[-180, 180, 75, 90]
        
            # fig, ax = plt.subplots(nrows=1, ncols=1,
            #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #                                                                         np.mean(extend[2:4]))},
            #                 figsize=(10,10))
            # ax.set_extent(extend, ccrs.PlateCarree())
            # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #         vmin=70, vmax=100, transform=ccrs.PlateCarree())
            # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            # ax.set_title(f'SIC pole hole for {d}')
            # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            # plt.savefig(f'SIC_pole_hole_{d}.png', bbox_inches='tight')


        #######################################

        #######################################
        # DO SIC correction OSI450a
        if ID == 'OSI450a':
            print('OSI450a PERIOD doing sensor correction')
        #if y<1992:
            # Third degree polynomia 
            def func(x, b, c, d, e):
                return b * x**3 + c * x**2 + d* x + e

            # Get coefficients
            name = 'OSI'
            with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl', 'rb') as f:
                tck_s3 = pickle.load(f)
            # # adjust SIC between 2 and 97 % but not in the Baltic
            crit = np.logical_and(np.logical_and(ice_conc<=97, ice_conc>2), source_flag!=1)
            ice_conc[crit] = ice_conc[crit] - BSpline(*tck_s3)(ice_conc[crit])

            # # Get coefficients
            # popt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_function_coefficients_NAME.npy')
            
            # # adjust SIC between 0 and 60 % but not in the Baltic
            # crit = np.logical_and(np.logical_and(ice_conc<=60, ice_conc>0), source_flag!=1)
            # ice_conc[crit] = ice_conc[crit] - func(ice_conc[crit], *popt)
            
            # # adjust SIC between 60 and 90% but not in the Baltic
            # crit2 = np.logical_and(np.logical_and(ice_conc>60, ice_conc<90), source_flag!=1)
            # ice_conc[crit2] = ice_conc[crit2] - func(60, *popt)
            
            # Change values outside valid bounds
            ice_conc[ice_conc>=100]=100
            ice_conc[ice_conc<=0]=0

            # set statusflag to "sensor bias correction"
            statusflag[crit] += (2**3)

            # Set name of flag
            statusflag_name = 'inter-sensor bias correction'

            # extend=[-180, 180, 60, 90]
            
            # fig, ax = plt.subplots(nrows=1, ncols=1,
            #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #                                                                         np.mean(extend[2:4]))},
            #                 figsize=(10,10))
            # ax.set_extent(extend, ccrs.PlateCarree())
            # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
            # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            # ax.set_title(f'SIC pole hole for {d}')
            # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            # plt.savefig(f'SIC_corrected_{d}.png', bbox_inches='tight')
        #######################################
        #######################################
        # DO SIC correction SICCI HR
        if ID == 'SICCI_HR_SIC':
            print('SICCI HR PERIOD doing sensor correction')
        #if ((np.logical_and(y>1991, y<2003)) or (y==2012)):
            # Third degree polynomia 
            def func(x, b, c, d, e):
                return b * x**3 + c * x**2 + d* x + e
            # Get coefficients
            name = 'SICCI'
            with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl', 'rb') as f:
                tck_s3 = pickle.load(f)
            # # adjust SIC between 2 and 97 % but not in the Baltic
            crit = np.logical_and(np.logical_and(ice_conc<=97, ice_conc>2), source_flag!=1)
            ice_conc[crit] = ice_conc[crit] - BSpline(*tck_s3)(ice_conc[crit])
            
            # popt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl')
            
            # # adjust SIC between 0 and 60 % but not in the Baltic
            # crit = np.logical_and(np.logical_and(ice_conc<=60, ice_conc>0), source_flag!=1)
            # ice_conc[crit] = ice_conc[crit] - func(ice_conc[crit], *popt)
            
            # # adjust SIC between 60 and 90% but not in the Baltic
            # crit2 = np.logical_and(np.logical_and(ice_conc>60, ice_conc<90), source_flag!=1)
            # ice_conc[crit2] = ice_conc[crit2] - func(60, *popt)
            
            # Change values outside valid bounds
            ice_conc[ice_conc>=100]=100
            ice_conc[ice_conc<=0]=0

            # set statusflag to "sensor bias correction"
            statusflag[crit] += (2**3)

            # Set name of flag
            statusflag_name = 'inter-sensor bias correction'

            # extend=[-180, 180, 60, 90]
            
            # fig, ax = plt.subplots(nrows=1, ncols=1,
            #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #                                                                         np.mean(extend[2:4]))},
            #                 figsize=(10,10))
            # ax.set_extent(extend, ccrs.PlateCarree())
            # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
            # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            # ax.set_title(f'SIC pole hole for {d}')
            # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            # plt.savefig(f'SIC_corrected_{d}.png', bbox_inches='tight')
        #######################################

        #######################################
        # Set nan values to 0 where there are ocean
        # landmask = data_SIC['mask'].squeeze().to_numpy()
        # ice_conc[np.logical_and(landmask==1, np.isnan(ice_conc))]=0
        
        extend=[-180, 180, 60, 90]
        
        # fig, ax = plt.subplots(nrows=1, ncols=1,
        #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
        #                                                                         np.mean(extend[2:4]))},
        #                 figsize=(10,10))
        # ax.set_extent(extend, ccrs.PlateCarree())
        # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), data_SIC['analysed_sst'].squeeze().to_numpy(), cmap='RdBu',
        #         transform=ccrs.PlateCarree())
        # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
        # ax.set_title(f'SST {d}')
        # plt.colorbar(mappable=cs, ax=ax, label='SST', format="%d", shrink=0.7)
        # plt.savefig(f'SST_{d}.png', bbox_inches='tight')
        #######################################
        # Save the new files using nc save function 

        if HS=='sh':
            file = xr.open_dataset(dir + fsic).sel(lat=slice(-90,0))
        else:
            file = xr.open_dataset(dir + fsic)
        
        SaveNCfile(data_SIC['analysed_sst'].squeeze().to_numpy(), 
                    ice_conc, 
                    regrid_osisaf_sic=data_SIC['ice_conc_orig'].squeeze().to_numpy(), 
                    sic_source_flag=source_flag, 
                    sst_source_flag=data_SIC['analysed_sst_source'].squeeze().to_numpy(), 
                    statusflag=statusflag, 
                    file_SST=file, 
                    ID='CARRA2', 
                    d=d, 
                    HS=HS,
                    ice_chart_filtering=True)

        data_SIC.close()


###########################################################
# HS='nh'

# # # Take input from user - made to use tmux and run subsets in parallel
# years = list(map(str, input("\nEnter the Year(s) : ").strip().split()))
# # y = sys.argv[1]
# months = list(map(str, input("\nEnter the Months : ").strip().split()))

# days =np.arange(1,32)
# days = [str(d) if d>=10 else '0'+str(d) for d in days]

# patch_dates = ['19781025', '19781028', '19790104', '19791206', '19830926', '19840604', '19840906', '19870801', '19870920', '19870922', '19871022', '19880122', '19880128', '19880222', '19880223', '19880830', '19881010', '19881016', '19881201', '19881214', '19881231', '19890205', '19890313', '19890321', '19890324', '19890325', '19890406', '19900202', '19900331', '19900408', '19900808', '19900816', '19900907', '19900922', '19901015', '19901104', '19901112', '19901204', '19910110', '19910112', '19910312', '19910319', '19910325', '19910408', '19910416', '19910506', '19910514', '19910522', '19910524', '19910608', '19910620', '19910627', '19910629', '19910719', '19910726', '19910802', '19910906', '19910911', '19910914', '19910915', '19910918', '19911013', '19911020', '19911021', '19911027']
# for y in years:
#     y = int(y)
#     print(HS)
#     # loop over months and products IDs
#     for m in months:

#         print(f'year:{y}, month:{m}')
#         # define data folders
#         dir = f"/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/output/CARRA2_final/post_processed_v2/{y}/{m}/"
#         if HS=='sh':
#             dir = f"/net/isilon/ifs/arch/home/sstdev/Projects/C3S/GBL_0.05_REAN/GBL_sea_ice_conc/final/{y}/{m}/"
#         # Find files in datafolders
#         files = sorted(os.listdir(dir))
#         print(files)
#         # loop through relevant dates and find belonging files
#         for dd in days:
#                 SIC_post_processing(HS, y, m, dd)

            #     # identify source
            #     ID = identify_product_ID(int(y), int(m), int(dd))
            #     print(ID)
       
            # #try:
            #     d = f'{y}{m}{dd}'
            #     # added the 4/10/2024 to processes wrong files for OSI450a
            #     if d in patch_dates:
            #         print(d)
            #         # added 'test' the 4/10/2024 to processes wrong files for OSI450a
            #         fsic = [f for f in files if d in f and 'test' in f][0]
            #         if HS=='sh':
            #             data_SIC = xr.open_dataset(dir + fsic).sel(lat=slice(-90,0))
            #         else:
            #             data_SIC = xr.open_dataset(dir + fsic)
            #         # load SIC, source and statusflag
            #         ice_conc = data_SIC['ice_conc'].squeeze().to_numpy()
            #         source_flag = data_SIC['iceconc_source'].squeeze().to_numpy()
            #         statusflag = data_SIC['status_flag'].squeeze().to_numpy()

            #         extend=[-180, 180, 60, 90]
                    
            #         # fig, ax = plt.subplots(nrows=1, ncols=1,
            #         #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #         #                                                                         np.mean(extend[2:4]))},
            #         #                 figsize=(10,10))
            #         # ax.set_extent(extend, ccrs.PlateCarree())
            #         # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #         #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
            #         # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            #         # ax.set_title(f'SIC pole hole for {d}')
            #         # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            #         # plt.savefig(f'SIC_original_{d}.png', bbox_inches='tight')


            #         # FIX WIERD POLE HOLE FOR SICCI HR
            #         if ID == 'SICCI_HR_SIC' and HS=='nh':
            #             print('SICCI HR PERIOD FIXING POLE HOLE')
            #         #if ((np.logical_and(y>1991, y<2003)) or (y==2012)):
            #             file2 = f"/dmidata/projects/cmems2/C3S/OSI450a_extrap/{y}/{m}/OSI450a_{d}_{HS}.nc"
            #             ice_conc_OSI450a = xr.open_dataset(file2).sel(lat=slice(87,90))['ice_conc'].squeeze().to_numpy()
            #             # replace pole hole in SICCI HR SIC with OSI450a SIC
            #             ice_conc[-ice_conc_OSI450a.shape[0]:,:]=ice_conc_OSI450a

            #             # apply filter to smooth the transfer between the products
            #             result = uniform_filter(ice_conc[-ice_conc_OSI450a.shape[0]-20:-ice_conc_OSI450a.shape[0]+20,:], size=(5,100), mode='nearest')
            #             ice_conc[-ice_conc_OSI450a.shape[0]-20:-ice_conc_OSI450a.shape[0]+20,:]=result

            #             # change SIC source to OSI450a
            #             source_flag[-ice_conc_OSI450a.shape[0]:,:] = (2**2) # OSI450a

            #             # extend=[-180, 180, 75, 90]
                    
            #             # fig, ax = plt.subplots(nrows=1, ncols=1,
            #             #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #             #                                                                         np.mean(extend[2:4]))},
            #             #                 figsize=(10,10))
            #             # ax.set_extent(extend, ccrs.PlateCarree())
            #             # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #             #         vmin=70, vmax=100, transform=ccrs.PlateCarree())
            #             # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            #             # ax.set_title(f'SIC pole hole for {d}')
            #             # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            #             # plt.savefig(f'SIC_pole_hole_{d}.png', bbox_inches='tight')


            #         #######################################

            #         #######################################
            #         # DO SIC correction OSI450a
            #         if ID == 'OSI450a':
            #             print('OSI450a PERIOD doing sensor correction')
            #         #if y<1992:
            #             # Third degree polynomia 
            #             def func(x, b, c, d, e):
            #                 return b * x**3 + c * x**2 + d* x + e

            #             # Get coefficients
            #             name = 'OSI'
            #             with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl', 'rb') as f:
            #                 tck_s3 = pickle.load(f)
            #             # # adjust SIC between 2 and 97 % but not in the Baltic
            #             crit = np.logical_and(np.logical_and(ice_conc<=97, ice_conc>2), source_flag!=1)
            #             ice_conc[crit] = ice_conc[crit] - BSpline(*tck_s3)(ice_conc[crit])

            #             # # Get coefficients
            #             # popt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_function_coefficients_NAME.npy')
                        
            #             # # adjust SIC between 0 and 60 % but not in the Baltic
            #             # crit = np.logical_and(np.logical_and(ice_conc<=60, ice_conc>0), source_flag!=1)
            #             # ice_conc[crit] = ice_conc[crit] - func(ice_conc[crit], *popt)
                        
            #             # # adjust SIC between 60 and 90% but not in the Baltic
            #             # crit2 = np.logical_and(np.logical_and(ice_conc>60, ice_conc<90), source_flag!=1)
            #             # ice_conc[crit2] = ice_conc[crit2] - func(60, *popt)
                        
            #             # Change values outside valid bounds
            #             ice_conc[ice_conc>=100]=100
            #             ice_conc[ice_conc<=0]=0

            #             # set statusflag to "sensor bias correction"
            #             statusflag[crit] += (2**3)

            #             # Set name of flag
            #             statusflag_name = 'inter-sensor bias correction'

            #             # extend=[-180, 180, 60, 90]
                        
            #             # fig, ax = plt.subplots(nrows=1, ncols=1,
            #             #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #             #                                                                         np.mean(extend[2:4]))},
            #             #                 figsize=(10,10))
            #             # ax.set_extent(extend, ccrs.PlateCarree())
            #             # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #             #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
            #             # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            #             # ax.set_title(f'SIC pole hole for {d}')
            #             # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            #             # plt.savefig(f'SIC_corrected_{d}.png', bbox_inches='tight')
            #         #######################################
            #         #######################################
            #         # DO SIC correction SICCI HR
            #         if ID == 'SICCI_HR_SIC':
            #             print('SICCI HR PERIOD doing sensor correction')
            #         #if ((np.logical_and(y>1991, y<2003)) or (y==2012)):
            #             # Third degree polynomia 
            #             def func(x, b, c, d, e):
            #                 return b * x**3 + c * x**2 + d* x + e
            #             # Get coefficients
            #             name = 'SICCI'
            #             with open(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl', 'rb') as f:
            #                 tck_s3 = pickle.load(f)
            #             # # adjust SIC between 2 and 97 % but not in the Baltic
            #             crit = np.logical_and(np.logical_and(ice_conc<=97, ice_conc>2), source_flag!=1)
            #             ice_conc[crit] = ice_conc[crit] - BSpline(*tck_s3)(ice_conc[crit])
                        
            #             # popt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/scripts/dokumentation/correction_p2_{name}_tck_s3_{m}_{HS}.pkl')
                        
            #             # # adjust SIC between 0 and 60 % but not in the Baltic
            #             # crit = np.logical_and(np.logical_and(ice_conc<=60, ice_conc>0), source_flag!=1)
            #             # ice_conc[crit] = ice_conc[crit] - func(ice_conc[crit], *popt)
                        
            #             # # adjust SIC between 60 and 90% but not in the Baltic
            #             # crit2 = np.logical_and(np.logical_and(ice_conc>60, ice_conc<90), source_flag!=1)
            #             # ice_conc[crit2] = ice_conc[crit2] - func(60, *popt)
                        
            #             # Change values outside valid bounds
            #             ice_conc[ice_conc>=100]=100
            #             ice_conc[ice_conc<=0]=0

            #             # set statusflag to "sensor bias correction"
            #             statusflag[crit] += (2**3)

            #             # Set name of flag
            #             statusflag_name = 'inter-sensor bias correction'

            #             # extend=[-180, 180, 60, 90]
                        
            #             # fig, ax = plt.subplots(nrows=1, ncols=1,
            #             #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #             #                                                                         np.mean(extend[2:4]))},
            #             #                 figsize=(10,10))
            #             # ax.set_extent(extend, ccrs.PlateCarree())
            #             # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), ice_conc, cmap='RdBu',
            #             #         vmin=0, vmax=100, transform=ccrs.PlateCarree())
            #             # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            #             # ax.set_title(f'SIC pole hole for {d}')
            #             # plt.colorbar(mappable=cs, ax=ax, label='SIC', format="%d", shrink=0.7)
            #             # plt.savefig(f'SIC_corrected_{d}.png', bbox_inches='tight')
            #         #######################################

            #         #######################################
            #         # Set nan values to 0 where there are ocean
            #         # landmask = data_SIC['mask'].squeeze().to_numpy()
            #         # ice_conc[np.logical_and(landmask==1, np.isnan(ice_conc))]=0
                    
            #         extend=[-180, 180, 60, 90]
                    
            #         # fig, ax = plt.subplots(nrows=1, ncols=1,
            #         #                 subplot_kw={'projection':ccrs.LambertAzimuthalEqualArea(np.mean(extend[:2]),
            #         #                                                                         np.mean(extend[2:4]))},
            #         #                 figsize=(10,10))
            #         # ax.set_extent(extend, ccrs.PlateCarree())
            #         # cs = ax.pcolormesh(data_SIC['lon'].squeeze().to_numpy(), data_SIC['lat'].squeeze().to_numpy(), data_SIC['analysed_sst'].squeeze().to_numpy(), cmap='RdBu',
            #         #         transform=ccrs.PlateCarree())
            #         # ax.coastlines(resolution='50m', color='grey', linewidth=0.7)
            #         # ax.set_title(f'SST {d}')
            #         # plt.colorbar(mappable=cs, ax=ax, label='SST', format="%d", shrink=0.7)
            #         # plt.savefig(f'SST_{d}.png', bbox_inches='tight')
            #         #######################################
            #         # Save the new files using nc save function 

            #         if HS=='sh':
            #             file = xr.open_dataset(dir + fsic).sel(lat=slice(-90,0))
            #         else:
            #             file = xr.open_dataset(dir + fsic)
                    
            #         SaveNCfile(data_SIC['analysed_sst'].squeeze().to_numpy(), 
            #                     ice_conc, 
            #                     regrid_osisaf_sic=data_SIC['ice_conc_orig'].squeeze().to_numpy(), 
            #                     sic_source_flag=source_flag, 
            #                     sst_source_flag=data_SIC['analysed_sst_source'].squeeze().to_numpy(), 
            #                     statusflag=statusflag, 
            #                     file_SST=file, 
            #                     ID='CARRA2', 
            #                     d=d, 
            #                     HS=HS,
            #                     ice_chart_filtering=True)

            #         data_SIC.close()
            #     #except:
            #     #    print(f'no data for {d}')
