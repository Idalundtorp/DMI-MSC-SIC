import glob
import os
import numpy as np
import xarray as xr
from itertools import chain
import matplotlib.pyplot as plt
from scipy import stats

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
#colors = ['#ffe119', '#4363d8', '#f58231', '#dcbeff', '#800000', '#000075', '#a9a9a9', '#ffffff', '#000000']
colors = ['#000000', '#ffe119', '#4363d8', '#f58231', '#dcbeff', '#800000', '#000075', '#a9a9a9']

HS='nh'
years = np.arange(1982, 2024)
typ = 'SIA'
# months = np.arange(1,13)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
y_comb=[]
y_comb_orig = []
y_comb_OSI450a = []
y_comb_OSI458 = []
y_comb_OSI450a_filt = []
y_comb_OSI450a_filt_corr = []
y_comb_nsidc = []

y_comb_sep=[]
y_comb_orig_sep = []
y_comb_OSI450a_sep = []
y_comb_OSI450a_sep_filt = []
y_comb_OSI450a_sep_filt_corr = []
y_comb_OSI458_sep = []
y_comb_nsidc_sep = []

y_comb_yr=[]
y_comb_orig_yr = []
y_comb_OSI450a_yr = []
y_comb_OSI450a_yr_filt = []
y_comb_OSI450a_yr_filt_corr = []
y_comb_OSI458_yr = []
y_comb_nsidc_yr = []

y_comb_mar=[]
y_comb_orig_mar = []
y_comb_OSI458_mar = []
y_comb_OSI450a_mar = []
y_comb_OSI450a_mar_filt = []
y_comb_OSI450a_mar_filt_corr = []
y_comb_nsidc_mar = []

y_comb_may=[]
y_comb_orig_may = []
y_comb_OSI450a_may = []
y_comb_OSI458_may = []
y_comb_OSI450a_may_filt = []
y_comb_OSI450a_may_filt_corr = []
y_comb_nsidc_may = []

for year in years:
    year = str(year)
    #if int(year)>2002 and int(year)!=2012:
    if HS=='nh':
        Extent = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_CARRA2.npy')/1e6
    else:
        Extent = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_GBL_{HS}.npy')/1e6
    #Extent = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_Removed.npy')/1e6
    #Extent = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed.npy')/1e6
    #else:
    #Extent = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_filt.npy')/1e6
    try:
        #if int(year)>2020:
        #    Extent_OSI450a = np.ones(Extent.shape)*np.nan
        #else:
            #Extent_OSI450a = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_Removed_icechart.npy')/1e6
        Extent_OSI450a = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_extent_OSI450a_{HS}.npy')/1e6
        #Extent_OSI450a =np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_{HS}_Removed_icechart.npy')/1e6
    except:
        Extent_OSI450a = np.ones(Extent.shape)*np.nan
    try:
        #Extent_OSI458 = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_SST_land.npy')/1e6
    #Extent_OSI458 = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed_SST_land.npy')/1e6
        Extent_OSI458 = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_OSI458_{HS}.npy')/1e6
        # if ( (int(year)!=2002) & (int(year)!=2011) & (int(year)!=2012) & (int(year)<2021)):
        #     Extent_OSI458 = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_extent_OSI458.npy')/1e6
        # else:
        #     Extent_OSI458 = np.ones(Extent.shape)*np.nan
    except:
        Extent_OSI458 = np.ones(Extent.shape)*np.nan
    try:
        #Extent_nsidc = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_landspillover.npy')/1e6
        Extent_nsidc = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_nsidc_{HS}.npy')/1e6
        #Extent_nsidc = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed_landspillover.npy')/1e6

    except:
        Extent_nsidc = np.ones(Extent.shape)*np.nan
    try:
        Extent_OSI450a_filt = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_CARRA2_orig.npy')/1e6
        #Extent_OSI450a_filt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_CARRA2_SST.npy')/1e6
        #Extent_OSI450a_filt = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_OSI450a_filt.npy')/1e6
        #Extent_OSI450a_filt = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed_SST.npy')/1e6
    except:
        Extent_OSI450a_filt = np.ones(Extent.shape)*np.nan

    try:
        Extent_OSI450a_filt_corr = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_SIA_values/{year}_daily_SIA_SICCI-HR-SIC_{HS}.npy')/1e6
        # if year<'2004':
        #     Extent_OSI450a_filt_corr = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed_adjust_v2.npy')/1e6
        # else:
        #     Extent_OSI450a_filt_corr = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_SIE_{HS}_Removed_adjust.npy')/1e6
        #     #Extent_OSI450a_filt_corr = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_SIA_OSI450a_filt_corrected.npy')/1e6
    except:
        Extent_OSI450a_filt_corr = np.ones(Extent.shape)*np.nan

    # handle years with 29 days in feb
    if Extent[-1]!=0:
        # zero indexed therefore last day in february (normal year)= 31+28 -1
        Extent[30+28]=np.mean(Extent[30+28:30+29])
        Extent = np.delete(Extent, 30+29)
        
        Extent_OSI450a[30+28]=np.mean(Extent_OSI450a[30+28:30+29])
        Extent_OSI450a = np.delete(Extent_OSI450a, 30+29)

        Extent_nsidc[30+28]=np.mean(Extent_nsidc[30+28:30+29])
        Extent_nsidc = np.delete(Extent_nsidc, 30+29)


        Extent_OSI458[30+28]=np.nanmean(Extent_OSI458[30+28:30+29])
        Extent_OSI458 = np.delete(Extent_OSI458, 30+29)

        Extent_OSI450a_filt[30+28]=np.nanmean(Extent_OSI450a_filt[30+28:30+29])
        Extent_OSI450a_filt = np.delete(Extent_OSI450a_filt, 30+29)

        Extent_OSI450a_filt_corr[30+28]=np.nanmean(Extent_OSI450a_filt_corr[30+28:30+29])
        Extent_OSI450a_filt_corr = np.delete(Extent_OSI450a_filt_corr, 30+29)
    else:
        Extent = Extent[:-1]
        Extent_OSI450a = Extent_OSI450a[:-1]
        Extent_OSI450a_filt = Extent_OSI450a_filt[:-1]
        Extent_OSI450a_filt_corr = Extent_OSI450a_filt_corr[:-1]
        Extent_OSI458 =  Extent_OSI458[:-1]
        Extent_nsidc = Extent_nsidc[:-1]


    #Extent_orig = np.load(f'/dmidata/users/ilo/projects/SST_SIC_PIA/CARRA2_extent_values/{year}_daily_extent_orig.npy')/1e6

    ## MARCH
    y_comb_mar.append(np.mean(Extent[59:90]))
    y_comb_OSI450a_mar.append(np.mean(Extent_OSI450a[59:90]))
    y_comb_OSI450a_mar_filt.append(np.mean(Extent_OSI450a_filt[59:90]))
    y_comb_OSI450a_mar_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[59:90]))
    y_comb_OSI458_mar.append(np.mean(Extent_OSI458[59:90]))
    #if int(year)==2008:
    #y_comb_nsidc_mar.append(np.nan)     
    #else:
    y_comb_nsidc_mar.append(np.mean(Extent_nsidc[59:90]))

    ## MAY
    y_comb_may.append(np.mean(Extent[120:151]))
    # no data avilable for: 1978 October, 1986 April, May, June, 1987 December
    y_comb_OSI450a_may.append(np.mean(Extent_OSI450a[120:151]))
    y_comb_OSI450a_may_filt.append(np.mean(Extent_OSI450a_filt[120:151]))
    y_comb_OSI450a_may_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[120:151]))
    y_comb_OSI458_may.append(np.mean(Extent_OSI458[120:151]))
    y_comb_nsidc_may.append(np.mean(Extent_nsidc[120:151]))

    ### SEPTEMBER
    y_comb_sep.append(np.mean(Extent[243:273]))
    y_comb_OSI450a_sep.append(np.mean(Extent_OSI450a[243:273]))
    y_comb_OSI450a_sep_filt.append(np.mean(Extent_OSI450a_filt[243:273]))
    y_comb_OSI450a_sep_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[243:273]))
    y_comb_OSI458_sep.append(np.nanmean(Extent_OSI458[243:273]))
    y_comb_nsidc_sep.append(np.mean(Extent_nsidc[243:273]))

    ## YEARLY
    y_comb_yr.append(np.nanmean(Extent))
    y_comb_OSI450a_yr.append(np.nanmean(Extent_OSI450a))
    y_comb_OSI450a_yr_filt.append(np.nanmean(Extent_OSI450a_filt))
    y_comb_OSI450a_yr_filt_corr.append(np.nanmean(Extent_OSI450a_filt_corr))
    y_comb_OSI458_yr.append(np.nanmean(Extent_OSI458))
    y_comb_nsidc_yr.append(np.nanmean(Extent_nsidc))    

    y_comb.append(Extent)
    y_comb_OSI450a.append(Extent_OSI450a)
    y_comb_OSI450a_filt.append(Extent_OSI450a_filt)
    y_comb_OSI450a_filt_corr.append(Extent_OSI450a_filt_corr)
    y_comb_OSI458.append(Extent_OSI458)
    y_comb_nsidc.append(Extent_nsidc)

# ##############################################
# # Yearly extend September
# ##############################################
# years_str = [str(y) for y in years]
# y_comb_nsidc_sep = np.array(y_comb_nsidc_sep)
# y_comb_sep = np.array(y_comb_sep)
# y_comb_OSI458_sep = np.array(y_comb_OSI458_sep)
# y_comb_OSI450a_sep = np.array(y_comb_OSI450a_sep)
# y_comb_SICCI_sep = np.array(y_comb_OSI450a_sep_filt_corr)
# y_comb_OSI458_sep[np.array(y_comb_OSI458_sep)<2.5] = np.nan
# y_comb_OSI450a_sep[np.array(y_comb_OSI450a_sep)<2.5] = np.nan
# #y_comb_SICCI_sep[np.array(y_comb_SICCI_sep)<8.5]

# slope1, intercept1, r1, p1, se1 = stats.linregress(years[~np.isnan(y_comb_sep)], y_comb_sep[~np.isnan(y_comb_sep)])
# slope2, intercept2, r2, p2, se2 = stats.linregress(years[~np.isnan(y_comb_OSI450a_sep)], y_comb_OSI450a_sep[~np.isnan(y_comb_OSI450a_sep)])
# slope3, intercept3, r3, p3, se3 = stats.linregress(years[~np.isnan(y_comb_SICCI_sep)], y_comb_SICCI_sep[~np.isnan(y_comb_SICCI_sep)])
# slope4, intercept4, r4, p4, se4 = stats.linregress(years[~np.isnan(y_comb_nsidc_sep)], y_comb_nsidc_sep[~np.isnan(y_comb_nsidc_sep)])

# fig, ax = plt.subplots(figsize=(16,7))
# plt.plot(years, y_comb_sep, '-', color=colors[0], label=f'DMI-MSC-SIC: Trend:{int(np.round(slope1*1e3))}*10³ km²/year') #, label='DMI_MSC NH')
# plt.plot(years, y_comb_SICCI_sep, '-', color=colors[4], label=f'SICCI-HR-SIC: Trend:{int(np.round(slope4*1e3))}*10³ km²/year') #, label='nsidc')
# plt.plot(years, y_comb_OSI450a_sep, '-', color=colors[1], label=f'OSI-450-a: Trend:{int(np.round(slope2*1e3))}*10³ km²/year') #, label='OSI450a')
# plt.plot(years, y_comb_nsidc_sep, '-', color=colors[3], label=f'NOAA/NSIDC: Trend:{int(np.round(slope4*1e3))}*10³ km²/year') #, label='nsidc')
# plt.plot(years, y_comb_OSI458_sep, '-', color=colors[2], label='OSI-458')

# # plt.plot(years, y_comb_sep, '-', label='CARRA2')
# # #plt.plot(years, y_comb_orig_sep, 'o-', label='ORIG')
# # plt.plot(years, y_comb_OSI450a_sep, '-', label='OSI450a')
# # plt.plot(years, y_comb_SICCI_sep, '-', label='SICCI-HR-SIC')
# # plt.plot(years, y_comb_OSI458_sep, '-', label='OSI458')
# # plt.plot(years, y_comb_nsidc_sep, '-', label='NOAA/NSIDC')
# if typ=='removed':
#     plt.ylim(-0.1,0.1)
# else:
#     plt.ylim(2,9)
# plt.xlim(years[0], years[-1])
# plt.ylabel('SIA (Millions of square kilometers)')
# plt.xticks(years, years_str, rotation=45)
# plt.title('September mean sea ice area')
# plt.grid()
# plt.legend()
# plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_Sep_{typ}.png')
# #plt.show()
# plt.close()

# ## SIA removed
# # years_str = [str(y) for y in years]
# # fig, ax = plt.subplots(figsize=(16,7))
# # plt.plot(years, y_comb_yr, 'o-', color=colors[0], label='Total Removed (excluding final correction)')
# # #plt.plot(years, y_comb_orig_yr, 'o-', label='ORIG')
# # plt.plot(years, y_comb_OSI450a_yr, 'o-', color=colors[1], label='Removed by icecharts')
# # plt.plot(years, y_comb_OSI450a_yr_filt, 'o-', color=colors[2], label='Removed by global SST filter')
# # plt.plot(years, y_comb_OSI450a_yr_filt_corr, 'o-', color=colors[3], label='Changed by final correction')
# # plt.plot(years, y_comb_OSI458_yr, 'o-', color=colors[4], label='Removed by SST & land filter')
# # plt.plot(years, y_comb_nsidc_yr, 'o-', color=colors[5], label='Removed by landspillover filter')
# # #if typ=='removed':
# # #plt.ylim(-0.05,0.1)
# # #else:
# # #    plt.ylim(2,7)
# # plt.xlim(years[0], years[-1])
# # plt.ylabel('SIE (Millions of square kilometers)')
# # plt.xticks(years, years_str, rotation=45)
# # plt.title('Yearly mean sea ice extent removed')
# # plt.grid()
# # plt.legend()
# # plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_YR_SIE_{typ}.png')
# # plt.show()
# # plt.close()
# #################################################

# # ##############################################
# # # daily SIE
# # ##############################################
# # x = np.arange(1, len(years)*365+1)
# # plt.figure(figsize=(10,7))

# # #plt.plot(x, np.array(y_comb).flatten(), '-', label='CARRA2')
# # plt.plot(x, np.array(y_comb).flatten(), '-',  linewidth=2, label='CARRA2')
# # plt.plot(x, np.array(y_comb_OSI450a).flatten(), '-',  linewidth=0.9, ='OSI450a')
# # plt.plot(x, np.array(y_comb_OSI450a_filt).flatten(), '-',  linewidth=0.9, label='OSI450a filt')
# # plt.plot(x, np.array(y_comb_orig).flatten(), '-', linewidth=0.9, label='ORIG')
# # #y_comb_OSI458=np.array(y_comb_OSI458).flatten()
# # #y_comb_OSI458[y_comb_OSI458==0]=np.nan
# # #plt.plot(x, np.array(y_comb_OSI458).flatten(), '-',  linewidth=0.9, label='OSI458')
# # #plt.plot(years, y_comb_nsidc_sep, 'o-', label='nsidc')
# # plt.xticks(ticks=x[::365], rotation=45, labels=years.astype(list))
# # #plt.ylim(3,9)
# # plt.xlim(x[0], x[-1])
# # plt.ylabel('Extent (Millions of square kilometers)')
# # #plt.title('September mean sea ice extent')
# # plt.grid()
# # plt.legend()
# # plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_DOY_year_SIC2.png', bbox_inches='tight')
# # #plt.show()
# # plt.close()


# # ##############################################
# # # Yearly extend march
# # ##############################################
# # plt.figure(figsize=(18,6))
# # plt.plot(years, y_comb_mar, 'o-',color=colors[0],  label='Total Removed (excluding final correction)')
# # #plt.plot(years, y_comb_orig_sep, 'o-', label='ORIG')
# # plt.plot(years, y_comb_OSI450a_mar, 'o-', color=colors[1], label='Removed by icecharts')
# # plt.plot(years, y_comb_OSI450a_mar_filt, 'o-', color=colors[2], label='Removed by global SST filter')
# # plt.plot(years, y_comb_OSI450a_mar_filt_corr, 'o-', color=colors[3], label='Changed by final correction')
# # plt.plot(years, y_comb_OSI458_mar, 'o-', color=colors[4], label='Removed by SST & land filter')
# # plt.plot(years, y_comb_nsidc_mar, 'o-', color=colors[5], label='Removed by landspillover filter')

# # #plt.plot(years, y_comb_nsidc_may, 'o-', label='nsidc')
# # plt.xticks(years, years_str, rotation=45)
# # #if typ=='removed':
# # #    plt.ylim(-0.1,0.1)
# # #else:
# # #    plt.ylim(12,16)
# # plt.xlim(years[0], years[-1])
# # plt.ylabel('SIE (Millions of square kilometers)')
# # plt.title('march mean sea ice extent removed')
# # plt.grid()
# # plt.legend()
# # plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_march_SIE_{typ}.png')
# # plt.show()
# # plt.close()


# years_str = [str(y) for y in years]
# y_comb_mar = np.array(y_comb_mar)
# y_comb_nsidc_mar = np.array(y_comb_nsidc_mar)
# y_comb_OSI458_mar = np.array(y_comb_OSI458_mar)
# y_comb_OSI450a_mar = np.array(y_comb_OSI450a_mar)
# y_comb_SICCI_mar = np.array(y_comb_OSI450a_mar_filt_corr)
# y_comb_OSI458_mar[np.array(y_comb_OSI458_mar)<8.5] = np.nan
# y_comb_OSI450a_mar[np.array(y_comb_OSI450a_mar)<8.5] = np.nan
# y_comb_SICCI_mar[np.array(y_comb_SICCI_mar)<8.5]

# slope1, intercept1, r1, p1, se1 = stats.linregress(years[~np.isnan(y_comb_mar)], y_comb_mar[~np.isnan(y_comb_mar)])
# slope2, intercept2, r2, p2, se2 = stats.linregress(years[~np.isnan(y_comb_OSI450a_mar)], y_comb_OSI450a_mar[~np.isnan(y_comb_OSI450a_mar)])
# slope3, intercept3, r3, p3, se3 = stats.linregress(years[~np.isnan(y_comb_SICCI_mar)], y_comb_SICCI_mar[~np.isnan(y_comb_SICCI_mar)])
# slope4, intercept4, r4, p4, se4 = stats.linregress(years[~np.isnan(y_comb_nsidc_mar)], y_comb_nsidc_mar[~np.isnan(y_comb_nsidc_mar)])


# fig, ax = plt.subplots(figsize=(16,7))

# plt.plot(years, y_comb_mar, '-', color=colors[4], label=f'DMI-MSC-SIC: Trend:{int(np.round(slope1*1e3))}*10³ km²/year')
# plt.plot(years, y_comb_SICCI_mar, '-', color=colors[3], label=f'SICCI-HR-SIC: Trend:{int(np.round(slope3*1e3))}*10³ km²/year')
# plt.plot(years, y_comb_OSI450a_mar, '-', color=colors[5], label=f'OSI-450-a: Trend:{int(np.round(slope2*1e3))}*10³ km²/year') #, label='OSI450a')
# plt.plot(years, y_comb_nsidc_mar, '-', color=colors[7], label=f'NOAA/NSIDC: Trend:{int(np.round(slope4*1e3))}*10³ km²/year') #, label='nsidc')
# plt.plot(years, y_comb_OSI458_mar, '-', color=colors[6], label='OSI-458')


# if typ=='removed':
#     plt.ylim(-0.1,0.1)
# else:
#     plt.ylim(12,16)
# plt.xlim(years[0], years[-1])
# plt.ylabel('SIA (Millions of square kilometers)')
# plt.xticks(years, years_str, rotation=45)
# plt.title('March mean sea ice area')
# plt.grid()
# plt.legend()
# plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_Mar_{typ}.png')
# #plt.show()
# plt.close()
# # #################################################



# # years_str = [str(y) for y in years]
# # fig, ax = plt.subplots(figsize=(16,7))
# # plot11, = plt.plot(years, y_comb_sep, '-', color=colors[0], label='Total Removed (excluding final correction)')
# # #plt.plot(years, y_comb_orig_sep, 'o-', label='ORIG')
# # plot12, = plt.plot(years, y_comb_OSI450a_sep, '-', color=colors[1], label='Removed by icecharts')
# # plot13, = plt.plot(years, y_comb_OSI450a_sep_filt, '-', color=colors[2], label='Removed by global SST filter')
# # plot14, = plt.plot(years, y_comb_OSI450a_sep_filt_corr, '-', color=colors[3], label='Changed by final correction')
# # plot15, = plt.plot(years, y_comb_OSI458_sep, '-', color=colors[4], label='Removed by SST & land filter')
# # plot16, = plt.plot(years, y_comb_nsidc_sep, '-', color=colors[5], label='Removed by landspillover filter')

# # plot21, = plt.plot(years, y_comb_mar, '--',color=colors[0],  label='Total Removed (excluding final correction)')
# # #plt.plot(years, y_comb_orig_sep, 'o-', label='ORIG')
# # plot22, = plt.plot(years, y_comb_OSI450a_mar, '--', color=colors[1], label='Removed by icecharts')
# # plot23, = plt.plot(years, y_comb_OSI450a_mar_filt, '--', color=colors[2], label='Removed by global SST filter')
# # plot24, = plt.plot(years, y_comb_OSI450a_mar_filt_corr, '--', color=colors[3], label='Changed by final correction')
# # plot25, = plt.plot(years, y_comb_OSI458_mar, '--', color=colors[4], label='Removed by SST & land filter')
# # plot26, = plt.plot(years, y_comb_nsidc_mar, '--', color=colors[5], label='Removed by landspillover filter')
# # if 'REMOVED' in typ:
# #     plt.ylim(-0.05,0.5)
# # else:
# #     plt.ylim(2,7)
# # plt.rcParams['legend.title_fontsize'] = 'large'
# # plt.xlim(years[0], years[-1])
# # plt.tick_params(axis='both', which='major', labelsize=12)
# # plt.ylabel('SIE (Millions of square kilometers)', fontsize=14)
# # plt.xlabel('Year', fontsize=14)
# # plt.xticks(years, years_str, rotation=45)
# # plt.title(f'{HS}: September and March mean sea ice extend removed', fontsize=16)
# # plt.grid()
# # legend_elements = plt.legend(handles=[plot11, plot13, plot12, plot14, plot15, plot16], loc='upper left', fontsize=11, title=r"$\bf{September}$")


# years_str = [str(y) for y in years]
# y_comb_OSI458_yr = np.array(y_comb_OSI458_yr)
# y_comb_OSI450a_yr = np.array(y_comb_OSI450a_yr)
# y_comb_SICCI_yr = np.array(y_comb_OSI450a_yr_filt_corr)
# y_comb_OSI458_yr[np.array(y_comb_OSI458_yr)<8.5] = np.nan
# y_comb_OSI450a_yr[np.array(y_comb_OSI450a_yr)<8.5] = np.nan
# y_comb_SICCI_yr[np.array(y_comb_SICCI_yr)<8.5]

# fig, ax = plt.subplots(figsize=(16,7))
# plt.plot(years, y_comb_yr, '-', label='CARRA2')
# #plt.plot(years, y_comb_orig_yr, 'o-', label='ORIG')
# plt.plot(years, y_comb_OSI450a_yr, '-', label='OSI450a')
# #plt.plot(years, y_comb_OSI450a_yr_filt, 'o-', label='CARRA2 orig')
# plt.plot(years, y_comb_OSI450a_yr_filt_corr, '-',  linewidth=0.9, label='SICCI-HR-SIC')
# #plt.plot(years, y_comb_OSI450a_sep_filt_corr, 'o-', label='OSI450a filt new')
# plt.plot(years, y_comb_OSI458_yr, '-', label='OSI458')
# # faulty NSIDC years 1984, 1987, 1988
# y_comb_nsidc_yr = np.array(y_comb_nsidc_yr)
# y_comb_nsidc_yr[[2,4,5,6, -1]] = np.nan
# plt.plot(years, y_comb_nsidc_yr, '-', label='NOAA/NSIDC')
# #if typ=='removed':
# #    plt.ylim(-0.1,0.1)
# #else:
# plt.ylim(8,12)
# plt.xlim(years[0], years[-1])
# plt.ylabel('SIA (Millions of square kilometers)')
# plt.xticks(years, years_str, rotation=45)
# plt.title('Yearly mean sea ice area')
# plt.grid()
# plt.legend()
# plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_Yr_{typ}.png')
# #plt.show()
# plt.close()

# # # from matplotlib.lines import Line2D


# # plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_Sep_SIE_{typ}.png', bbox_inches='tight', transparent=True)
# # plt.show()
# # plt.close()


# # # filtered
# # y_std = np.std(y_comb, axis=0)
# # y_mean = np.mean(y_comb, axis=0)

# # # orig 
# # y_std_orig = np.std(y_comb_orig, axis=0)
# # y_mean_orig = np.mean(y_comb_orig, axis=0)

# # # OSI450a
# # y_std_OSI450a = np.std(y_comb_OSI450a, axis=0)
# # y_mean_OSI450a = np.mean(y_comb_OSI450a, axis=0)

# # fig, ax = plt.subplots()
# # DOY = np.arange(1,366)
# # ax.plot(DOY, y_mean, '-', color='orange', label=f'{years[0]}-{years[-1]} mean CARRA2')
# # #ax.fill_between(DOY, (y_mean-y_std), (y_mean+y_std), color='orange', alpha=.15)
# # ax.fill_between(DOY, (y_mean-2*y_std), (y_mean+2*y_std), color='orange', alpha=.1)

# # #ax.plot(DOY, y_mean_orig, '-', color='b', label=f'{years[0]}-{years[-1]} mean ORIG')
# # #ax.fill_between(DOY, (y_mean_orig-y_std_orig), (y_mean_orig+y_std_orig), color='b', alpha=.15)
# # #ax.fill_between(DOY, (y_mean_orig-2*y_std_orig), (y_mean_orig+2*y_std_orig), color='b', alpha=.1)
# # #for i in range(len(years)):
# # #    ax.plot(DOY, np.array(y_comb_OSI450a)[i,:], '-', label=f'{years[i]}')
# # ax.plot(DOY, y_mean_OSI450a, '-', color='g', label=f'{years[0]}-{years[-1]} mean OSI450a')
# # #ax.fill_between(DOY, (y_mean_OSI450a-y_std_OSI450a), (y_mean_OSI450a+y_std_OSI450a), color='g', alpha=.15)
# # ax.fill_between(DOY, (y_mean_OSI450a-2*y_std_OSI450a), (y_mean_OSI450a+2*y_std_OSI450a), color='g', alpha=.1)

# # #ax.plot(months, np.array(y_comb)[min_index], '-', label=f'{years[min_index]} minimum yearly seaice extent')
# # #ax.plot(DOY, np.array(y_comb_orig)[12], '-', label=f'{years[12]}')
# # #ax.plot(months, np.array(y_comb)[max_index], '-', label=f'{years[max_index]} maximum yearly seaice extent')
# # plt.legend()
# # plt.xlabel('DOY')
# # plt.grid()
# # plt.ylabel('Extent (Millions of square kilometers)')
# # plt.suptitle('Arctic Sea Ice Extent')
# # plt.title('(Area of ocean with atleast 15% sea ice)')
# # plt.ylim([0,18])
# # plt.xlim([0,365])
# # plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_DOY_extend.png')
# # plt.close() 


# # ##############################################
# # # daily SIA
# # ##############################################
# x = np.arange(1, len(years)*365+1)
# plt.figure(figsize=(20,10))

# y_comb_OSI458 = np.array(y_comb_OSI458).flatten()
# y_comb_OSI450a = np.array(y_comb_OSI450a).flatten()

# diff_OSI458 = np.insert(np.diff(y_comb_OSI458),0,0)

# y_comb_OSI458[diff_OSI458==0] = np.nan
# y_comb_OSI458[abs(diff_OSI458)>1] = np.nan
# #y_comb_OSI450a_yr[np.array(y_comb_OSI450a_yr)<8.5] = np.nan

# #plt.plot(x, np.array(y_comb).flatten(), '-', label='CARRA2')
# plt.plot(x, np.array(y_comb).flatten(), '-',  linewidth=1, label='CARRA2')
# plt.plot(x, y_comb_OSI450a, '-',  linewidth=0.9, label='OSI450a')
# #plt.plot(x, np.array(y_comb_OSI450a_filt).flatten(), '-',  linewidth=0.9, label='CARRA2 orig')
# plt.plot(x, np.array(y_comb_OSI450a_filt_corr).flatten(), '-',  linewidth=0.9, label='SICCI-HR-SIC')
# #plt.plot(x, np.array(y_comb_orig).flatten(), '-', linewidth=0.9, label='ORIG')
# #y_comb_OSI458=np.array(y_comb_OSI458).flatten()
# #y_comb_OSI458[y_comb_OSI458==0]=np.nan
# #plt.plot(x, y_comb_OSI458, '-',  linewidth=0.9, label='OSI458')
# #plt.plot(years, y_comb_nsidc_sep, 'o-', label='nsidc')
# plt.xticks(ticks=x[::365], rotation=45, labels=years.astype(list))
# plt.ylim(3,16)
# plt.xlim(x[0], x[-1])
# plt.ylabel('Extent (Millions of square kilometers)')
# #plt.title('September mean sea ice extent')
# plt.grid()
# plt.legend()
# plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_DOY_year_SIA_GBL_NH.png', bbox_inches='tight')
# #plt.show()
# plt.close()



y_std = np.std(y_comb, axis=0)
y_mean = np.mean(y_comb, axis=0)

fig, ax = plt.subplots(figsize=(10,8))
DOY = np.arange(1,366)
ax.plot(DOY, y_mean, '-', color="#600202", label=f'{years[0]}-{years[-1]} Avg.')
ax.fill_between(DOY, (y_mean-2*y_std), (y_mean+2*y_std), color="#600202", alpha=.1)

# #ax.plot(DOY, y_mean_orig, '-', color='b', label=f'{years[0]}-{years[-1]} mean ORIG')
# #ax.fill_between(DOY, (y_mean_orig-y_std_orig), (y_mean_orig+y_std_orig), color='b', alpha=.15)
# #ax.fill_between(DOY, (y_mean_orig-2*y_std_orig), (y_mean_orig+2*y_std_orig), color='b', alpha=.1)
# color based on interpolated/original data 1986
DOY_period1_1986 = np.arange(1,88)
DOY_period2_1986 = np.arange(87, 176) # period with missing data (26th of March to 24th of June)
DOY_period3_1986 = np.arange(175,366)

DOY_period1_1987 = np.arange(1,337)
DOY_period2_1987 = np.arange(337, 366) # period with missing data ()

DOY_period2_1988 = np.arange(1,13) # period with missing data ()
DOY_period1_1988 = np.arange(13, 366) 
colors_DOY = ['dimgrey',  # grey
                 '#ffb347',  # orange-yellow instead of bright lemon
                 '#0099ff',  # cyan-blue instead of deep blue
                 '#ff4444',  # strong red instead of orange
                 '#9d4edd',  # deeper purple instead of pastel lavender
                 '#228b22',  # green instead of maroon
                 '#ff1493',  # magenta instead of navy
                 '#808080']  # neutral mid-gray
colors[1] = colors_DOY[1]
colors[0] = colors_DOY[3]
for i in range(len(years[:3])):
    if years[i+4]==1986:
        DOY_period1 = DOY_period1_1986
        DOY_period2 = DOY_period2_1986
    elif years[i+4]==1987:
        DOY_period1 = DOY_period1_1987
        DOY_period2 = DOY_period2_1987
    elif years[i+4]==1988:
        DOY_period1 = DOY_period1_1988
        DOY_period2 = DOY_period2_1988
    
    ax.plot(DOY_period1, np.array(y_comb)[i+4,(DOY_period1-1).astype(int)], '-', linewidth=1,color=colors[i], label=f'{years[i+4]}')
    ax.plot(DOY_period2, np.array(y_comb)[i+4,(DOY_period2-1).astype(int)], '-', linewidth=2, color=colors[i], label=f'{years[i+4]}: interpolated')
    if years[i+4]==1986:
        ax.plot(DOY_period3_1986, np.array(y_comb)[i+4,(DOY_period3_1986-1).astype(int)], '-', linewidth=1,color=colors[i]) # , label=f'{years[i+4]}')

# for i in range(len(years[:3])):
#     ax.plot(DOY, np.array(y_comb)[i+4,:], '-', color=colors[i], label=f'{years[i+4]}')
# ax.plot(DOY, y_mean_OSI450a, '-', color='g', label=f'{years[0]}-{years[-1]} mean OSI450a')
# #ax.fill_between(DOY, (y_mean_OSI450a-y_std_OSI450a), (y_mean_OSI450a+y_std_OSI450a), color='g', alpha=.15)
# ax.fill_between(DOY, (y_mean_OSI450a-2*y_std_OSI450a), (y_mean_OSI450a+2*y_std_OSI450a), color='g', alpha=.1)

# #ax.plot(months, np.array(y_comb)[min_index], '-', label=f'{years[min_index]} minimum yearly seaice extent')
# #ax.plot(DOY, np.array(y_comb_orig)[12], '-', label=f'{years[12]}')
# #ax.plot(months, np.array(y_comb)[max_index], '-', label=f'{years[max_index]} maximum yearly seaice extent')
if HS=='nh':
    plt.legend(fontsize=16, loc='lower left')
else:
    plt.legend(fontsize=16, loc='upper left')
plt.xlabel('DOY', fontsize=18)
plt.grid()
plt.ylabel('Area (Millions of square kilometers)', fontsize=18)
plt.suptitle(f'{HS.upper()} Sea Ice Area', fontsize=20, y=0.955)
plt.title(f'(Area of ice covered ocean)', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
if HS=='nh':
    plt.ylim([0,19])
elif HS=='sh':
    plt.ylim([0,25])
plt.xlim([0,365])
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/figures/SIA/{years[0]}_{years[-1]}_DOY_SIA_{HS}.png', bbox_inches='tight')
plt.close() 