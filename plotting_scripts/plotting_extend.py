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
colors = ['#000000', '#ffe119', '#4363d8', '#f58231', '#dcbeff', "#800000", '#000075', '#a9a9a9']

years = np.arange(1982, 2025)

# months = np.arange(1,13)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
y_comb=[]
y_comb_orig = []
y_comb_OSI450a = []
y_comb_OSI458 = []
y_comb_OSI450a_filt = []
y_comb_OSI450a_filt_corr = []
y_comb_nsidc = []

#year
y_comb_yr=[]
y_comb_orig_yr = []
y_comb_OSI450a_yr = []
y_comb_OSI450a_yr_filt = []
y_comb_OSI450a_yr_filt_corr = []
y_comb_OSI458_yr = []
y_comb_nsidc_yr = []

#jan
y_comb_jan=[]
y_comb_orig_jan = []
y_comb_OSI458_jan = []
y_comb_OSI450a_jan = []
y_comb_OSI450a_jan_filt = []
y_comb_OSI450a_jan_filt_corr = []
y_comb_nsidc_jan = []

#feb
y_comb_feb=[]
y_comb_orig_feb = []
y_comb_OSI458_feb = []
y_comb_OSI450a_feb = []
y_comb_OSI450a_feb_filt = []
y_comb_OSI450a_feb_filt_corr = []
y_comb_nsidc_feb = []

#mar
y_comb_mar=[]
y_comb_orig_mar = []
y_comb_OSI458_mar = []
y_comb_OSI450a_mar = []
y_comb_OSI450a_mar_filt = []
y_comb_OSI450a_mar_filt_corr = []
y_comb_nsidc_mar = []

#apr
y_comb_apr=[]
y_comb_orig_apr = []
y_comb_OSI458_apr = []
y_comb_OSI450a_apr = []
y_comb_OSI450a_apr_filt = []
y_comb_OSI450a_apr_filt_corr = []
y_comb_nsidc_apr = []

#may
y_comb_may=[]
y_comb_orig_may = []
y_comb_OSI458_may = []
y_comb_OSI450a_may = []
y_comb_OSI450a_may_filt = []
y_comb_OSI450a_may_filt_corr = []
y_comb_nsidc_may = []

#jun
y_comb_jun=[]
y_comb_orig_jun = []
y_comb_OSI458_jun = []
y_comb_OSI450a_jun = []
y_comb_OSI450a_jun_filt = []
y_comb_OSI450a_jun_filt_corr = []
y_comb_nsidc_jun = []

#jul
y_comb_jul=[]
y_comb_orig_jul = []
y_comb_OSI458_jul = []
y_comb_OSI450a_jul = []
y_comb_OSI450a_jul_filt = []
y_comb_OSI450a_jul_filt_corr = []
y_comb_nsidc_jul = []

#aug
y_comb_aug=[]
y_comb_orig_aug = []
y_comb_OSI458_aug = []
y_comb_OSI450a_aug = []
y_comb_OSI450a_aug_filt = []
y_comb_OSI450a_aug_filt_corr = []
y_comb_nsidc_aug = []

#sep
y_comb_sep=[]
y_comb_orig_sep = []
y_comb_OSI450a_sep = []
y_comb_OSI450a_sep_filt = []
y_comb_OSI450a_sep_filt_corr = []
y_comb_OSI458_sep = []
y_comb_nsidc_sep = []

#oct
y_comb_oct=[]
y_comb_orig_oct = []
y_comb_OSI458_oct = []
y_comb_OSI450a_oct = []
y_comb_OSI450a_oct_filt = []
y_comb_OSI450a_oct_filt_corr = []
y_comb_nsidc_oct = []

#nov
y_comb_nov=[]
y_comb_orig_nov = []
y_comb_OSI458_nov = []
y_comb_OSI450a_nov = []
y_comb_OSI450a_nov_filt = []
y_comb_OSI450a_nov_filt_corr = []
y_comb_nsidc_nov = []

#dec
y_comb_dec=[]
y_comb_orig_dec = []
y_comb_OSI458_dec = []
y_comb_OSI450a_dec = []
y_comb_OSI450a_dec_filt = []
y_comb_OSI450a_dec_filt_corr = []
y_comb_nsidc_dec = []

HS = 'nh'
v = 'final'

BASEPATH = '/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values'
for year in years:
    year = str(year)
    # if int(year)>2005 and int(year)!=2012:
    #     Extent = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_extent_filt.npy')/1e6
    # else:
    try:
        print(year)
        if HS=='sh':
            Extent = np.load(f'{BASEPATH}/{year}_daily_extent_GBL_SH_final.npy')/1e6
        else:
            Extent = np.load(f'{BASEPATH}/{year}_daily_extent_CARRA2_corr_final.npy')/1e6
    except:
        if HS=='sh':
            try:
                Extent = np.load(f'{BASEPATH}/{year}_daily_extent_GBL_SH.npy')/1e6
            except:
                Extent = np.load(f'{BASEPATH}/{year}_daily_extent_GBL_sh.npy')/1e6
        else:
            Extent = np.load(f'{BASEPATH}/{year}_daily_extent_filt.npy')/1e6

    try:
        Extent_orig = np.load(f'{BASEPATH}/{year}_daily_extent_orig.npy')/1e6
    except:
        Extent_OSI450a = np.ones(Extent.shape)*np.nan
    try:
        Extent_OSI450a = np.load(f'{BASEPATH}/{year}_daily_extent_OSI450a_{HS}.npy')/1e6
    except:
        Extent_OSI450a = np.ones(Extent.shape)*np.nan
#    try:
    if (int(year)>2002): # & (int(year)!=2011) & (int(year)!=2012)):
        Extent_OSI458 = np.load(f'{BASEPATH}/{year}_daily_extent_OSI458_{HS}.npy')/1e6
    else:
        Extent_OSI458 = np.ones(Extent.shape)*np.nan
    # except:
    #     Extent_OSI458 = np.ones(Extent.shape)*np.nan
    try:
        Extent_nsidc = np.load(f'{BASEPATH}/{year}_daily_extent_nsidc_{HS}.npy')/1e6
    except:
        Extent_nsidc = np.ones(Extent.shape)*np.nan
    try:
        Extent_OSI450a_filt = np.load(f'{BASEPATH}/{year}_daily_extent_OSI450a_filt.npy')/1e6
    except:
        Extent_OSI450a_filt = np.ones(Extent.shape)*np.nan

    try:
        Extent_OSI450a_filt_corr = np.load(f'{BASEPATH}/{year}_daily_extent_OSI450a_filt_corrected.npy')/1e6
    except:
        Extent_OSI450a_filt_corr = np.ones(Extent.shape)*np.nan
    # handle years with 29 days in feb
    # if Extent[-1]!=0:
    #     # zero indexed therefore last day in february (normal year)= 31+28 -1
    #     Extent[30+28]=np.mean(Extent[30+28:30+29])
    #     Extent = np.delete(Extent, 30+29)
        
    #     Extent_orig[30+28]=np.mean(Extent_orig[30+28:30+29])
    #     Extent_orig = np.delete(Extent_orig, 30+29)
        
    #     Extent_OSI450a[30+28]=np.mean(Extent_OSI450a[30+28:30+29])
    #     Extent_OSI450a = np.delete(Extent_OSI450a, 30+29)

    #     Extent_nsidc[30+28]=np.mean(Extent_nsidc[30+28:30+29])
    #     Extent_nsidc = np.delete(Extent_nsidc, 30+29)


    #     Extent_OSI458[30+28]=np.nanmean(Extent_OSI458[30+28:30+29])
    #     Extent_OSI458 = np.delete(Extent_OSI458, 30+29)

    #     Extent_OSI450a_filt[30+28]=np.nanmean(Extent_OSI450a_filt[30+28:30+29])
    #     Extent_OSI450a_filt = np.delete(Extent_OSI450a_filt, 30+29)

    #     Extent_OSI450a_filt_corr[30+28]=np.nanmean(Extent_OSI450a_filt_corr[30+28:30+29])
    #     Extent_OSI450a_filt_corr = np.delete(Extent_OSI450a_filt_corr, 30+29)
    # else:
    Extent = Extent[:-1]
    Extent_orig = Extent_orig[:-1]
    Extent_OSI450a = Extent_OSI450a[:-1]
    Extent_OSI450a_filt = Extent_OSI450a_filt[:-1]
    Extent_OSI450a_filt_corr = Extent_OSI450a_filt_corr[:-1]
    Extent_OSI458 =  Extent_OSI458[:-1]
    Extent_nsidc = Extent_nsidc[:-1]


    #Extent_orig = np.load(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_extent_values/{year}_daily_extent_orig.npy')/1e6
    
    ## YEARLY
    y_comb_yr.append(np.nanmean(Extent))
    y_comb_OSI450a_yr.append(np.nanmean(Extent_OSI450a))
    y_comb_OSI450a_yr_filt.append(np.nanmean(Extent_OSI450a_filt))
    y_comb_OSI450a_yr_filt_corr.append(np.nanmean(Extent_OSI450a_filt_corr))
    y_comb_OSI458_yr.append(np.nanmean(Extent_OSI458))
    y_comb_nsidc_yr.append(np.nanmean(Extent_nsidc))    

    ## JANUARY
    y_comb_jan.append(np.mean(Extent[:31]))
    y_comb_orig_jan.append(np.mean(Extent_orig[:31]))
    y_comb_OSI450a_jan.append(np.mean(Extent_OSI450a[:31]))
    y_comb_OSI450a_jan_filt.append(np.mean(Extent_OSI450a_filt[:31]))
    y_comb_OSI450a_jan_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[:31]))
    y_comb_OSI458_jan.append(np.nanmean(Extent_OSI458[:31]))
    if int(year)==1988:
        y_comb_nsidc_jan.append(np.nan)
    else:
        y_comb_nsidc_jan.append(np.mean(Extent_nsidc[:31]))

    ## FEBRUARY
    y_comb_feb.append(np.mean(Extent[31:59]))
    y_comb_orig_feb.append(np.mean(Extent_orig[31:59]))
    y_comb_OSI450a_feb.append(np.mean(Extent_OSI450a[31:59]))
    y_comb_OSI450a_feb_filt.append(np.mean(Extent_OSI450a_filt[31:59]))
    y_comb_OSI450a_feb_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[31:59]))
    y_comb_OSI458_feb.append(np.nanmean(Extent_OSI458[31:59]))
    y_comb_nsidc_feb.append(np.mean(Extent_nsidc[31:59]))

    ## MARCH
    y_comb_mar.append(np.mean(Extent[59:90]))
    y_comb_orig_mar.append(np.mean(Extent_orig[59:90]))
    y_comb_OSI450a_mar.append(np.mean(Extent_OSI450a[59:90]))
    y_comb_OSI450a_mar_filt.append(np.mean(Extent_OSI450a_filt[59:90]))
    y_comb_OSI450a_mar_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[59:90]))
    y_comb_OSI458_mar.append(np.mean(Extent_OSI458[59:90]))
    if int(year)==2008:
        y_comb_nsidc_mar.append(np.nan)     
    else:
        y_comb_nsidc_mar.append(np.mean(Extent_nsidc[59:90]))

    ## APRIL
    y_comb_apr.append(np.mean(Extent[90:120]))
    y_comb_orig_apr.append(np.mean(Extent_orig[90:120]))
    # no data avilable for: 1978 October, 1986 April, May, June, 1987 December
    if int(year)==1986:
        y_comb_OSI450a_apr.append(np.nan)
        y_comb_OSI450a_apr_filt.append(np.nan)
        y_comb_OSI450a_apr_filt_corr.append(np.nan)
    else:
        y_comb_OSI450a_apr.append(np.mean(Extent_OSI450a[90:120]))
        y_comb_OSI450a_apr_filt.append(np.mean(Extent_OSI450a_filt[90:120]))
        y_comb_OSI450a_apr_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[90:120]))

    y_comb_OSI458_apr.append(np.mean(Extent_OSI458[90:120]))
    y_comb_nsidc_apr.append(np.mean(Extent_nsidc[90:120]))
    
    ## MAY
    y_comb_may.append(np.mean(Extent[120:151]))
    y_comb_orig_may.append(np.mean(Extent_orig[120:151]))
    # no data avilable for: 1978 October, 1986 April, May, June, 1987 December
    if int(year)==1986:
        y_comb_OSI450a_may.append(np.nan)
        y_comb_OSI450a_may_filt.append(np.nan)
        y_comb_OSI450a_may_filt_corr.append(np.nan)
    else:
        y_comb_OSI450a_may.append(np.mean(Extent_OSI450a[120:151]))
        y_comb_OSI450a_may_filt.append(np.mean(Extent_OSI450a_filt[120:151]))
        y_comb_OSI450a_may_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[120:151]))
    y_comb_OSI458_may.append(np.mean(Extent_OSI458[120:151]))
    y_comb_nsidc_may.append(np.mean(Extent_nsidc[120:151]))
    
    ## JUNE
    y_comb_jun.append(np.mean(Extent[151:181]))
    y_comb_orig_jun.append(np.mean(Extent_orig[151:181]))
    # no data avilable for: 1978 October, 1986 April, May, June, 1987 December
    if int(year)==1986:
        y_comb_OSI450a_jun.append(np.nan)
        y_comb_OSI450a_jun_filt.append(np.nan)
        y_comb_OSI450a_jun_filt_corr.append(np.nan)
    else:
        y_comb_OSI450a_jun.append(np.mean(Extent_OSI450a[151:181]))
        y_comb_OSI450a_jun_filt.append(np.mean(Extent_OSI450a_filt[151:181]))
        y_comb_OSI450a_jun_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[151:181]))
    y_comb_OSI458_jun.append(np.mean(Extent_OSI458[151:181]))
    y_comb_nsidc_jun.append(np.mean(Extent_nsidc[151:181]))
    
    ## JULY
    y_comb_jul.append(np.mean(Extent[181:212]))
    y_comb_orig_jul.append(np.mean(Extent_orig[181:212]))
    y_comb_OSI450a_jul.append(np.mean(Extent_OSI450a[181:212]))
    y_comb_OSI450a_jul_filt.append(np.mean(Extent_OSI450a_filt[181:212]))
    y_comb_OSI450a_jul_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[181:212]))
    y_comb_OSI458_jul.append(np.mean(Extent_OSI458[181:212]))
    if int(year)==1984:
        y_comb_nsidc_jul.append(np.nan)
    else:
        y_comb_nsidc_jul.append(np.mean(Extent_nsidc[181:212]))
    
    ## AUGUST
    y_comb_aug.append(np.mean(Extent[212:243]))
    y_comb_orig_aug.append(np.mean(Extent_orig[212:243]))
    y_comb_OSI450a_aug.append(np.mean(Extent_OSI450a[212:243]))
    y_comb_OSI450a_aug_filt.append(np.mean(Extent_OSI450a_filt[212:243]))
    y_comb_OSI450a_aug_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[212:243]))
    y_comb_OSI458_aug.append(np.mean(Extent_OSI458[212:243]))
    if int(year)==1984:
        y_comb_nsidc_aug.append(np.nan)
    else:
        y_comb_nsidc_aug.append(np.mean(Extent_nsidc[212:243]))
    

    ### SEPTEMBER
    y_comb_sep.append(np.mean(Extent[243:273]))
    y_comb_orig_sep.append(np.mean(Extent_orig[243:273]))
    y_comb_OSI450a_sep.append(np.mean(Extent_OSI450a[243:273]))
    y_comb_OSI450a_sep_filt.append(np.mean(Extent_OSI450a_filt[243:273]))
    y_comb_OSI450a_sep_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[243:273]))
    y_comb_OSI458_sep.append(np.nanmean(Extent_OSI458[243:273]))
    y_comb_nsidc_sep.append(np.mean(Extent_nsidc[243:273]))

    ### OCTOBER
    y_comb_oct.append(np.mean(Extent[273:304]))
    y_comb_orig_oct.append(np.mean(Extent_orig[273:304]))
    y_comb_OSI450a_oct.append(np.mean(Extent_OSI450a[273:304]))
    y_comb_OSI450a_oct_filt.append(np.mean(Extent_OSI450a_filt[273:304]))
    y_comb_OSI450a_oct_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[273:304]))
    y_comb_OSI458_oct.append(np.nanmean(Extent_OSI458[273:304]))
    y_comb_nsidc_oct.append(np.mean(Extent_nsidc[273:304]))

    ### NOVEMBER
    y_comb_nov.append(np.mean(Extent[304:334]))
    y_comb_orig_nov.append(np.mean(Extent_orig[304:334]))
    y_comb_OSI450a_nov.append(np.mean(Extent_OSI450a[304:334]))
    y_comb_OSI450a_nov_filt.append(np.mean(Extent_OSI450a_filt[304:334]))
    y_comb_OSI450a_nov_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[304:334]))
    y_comb_OSI458_nov.append(np.nanmean(Extent_OSI458[304:334]))
    y_comb_nsidc_nov.append(np.mean(Extent_nsidc[304:334]))

    ### DECEMBER
    y_comb_dec.append(np.mean(Extent[334:365]))
    y_comb_orig_dec.append(np.mean(Extent_orig[334:365]))
    # no data avilable for: 1978 October, 1986 April, May, June, 1987 December
    if int(year)==1987:
        y_comb_OSI450a_dec.append(np.nan)
        y_comb_OSI450a_dec_filt.append(np.nan)
        y_comb_OSI450a_dec_filt_corr.append(np.nan)
    else:
        y_comb_OSI450a_dec.append(np.mean(Extent_OSI450a[334:365]))
        y_comb_OSI450a_dec_filt.append(np.mean(Extent_OSI450a_filt[334:365]))
        y_comb_OSI450a_dec_filt_corr.append(np.mean(Extent_OSI450a_filt_corr[334:365]))
    y_comb_OSI458_dec.append(np.nanmean(Extent_OSI458[334:365]))
    
    if int(year)==1986 or int(year)==1987 or int(year)==1990:
        y_comb_nsidc_dec.append(np.nan)
    else:
        y_comb_nsidc_dec.append(np.mean(Extent_nsidc[334:365]))

    # COMBINED
    y_comb.append(Extent)
    y_comb_orig.append(Extent_orig)
    y_comb_OSI450a.append(Extent_OSI450a)
    y_comb_OSI450a_filt.append(Extent_OSI450a_filt)
    y_comb_OSI450a_filt_corr.append(Extent_OSI450a_filt_corr)
    y_comb_OSI458.append(Extent_OSI458)
    y_comb_nsidc.append(Extent_nsidc)

##############################################
# Yearly extend JANUARY
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]
y_comb_OSI458_jan = np.where(np.array(y_comb_OSI458_jan) < 1, np.nan, y_comb_OSI458_jan)
y_comb_OSI450a_jan = np.where(np.array(y_comb_OSI450a_jan) < 1, np.nan, y_comb_OSI450a_jan)
y_comb_nsidc_jan = np.where(np.array(y_comb_nsidc_jan) < 1, np.nan, y_comb_nsidc_jan)
y_comb_jan = np.array(y_comb_jan)

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_jan)], y_comb_jan[~np.isnan(y_comb_jan)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_jan)], y_comb_OSI450a_jan[~np.isnan(y_comb_OSI450a_jan)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_jan)], y_comb_nsidc_jan[~np.isnan(y_comb_nsidc_jan)])

print(f'jan: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_jan, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_jan, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_jan, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_jan, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_jan, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_jan))-1,np.round(np.nanmax(y_comb_OSI450a_jan))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('January mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_jan_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend FEBRUARY
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_feb = np.where(np.array(y_comb_OSI458_feb) < 1, np.nan, y_comb_OSI458_feb)
y_comb_OSI450a_feb = np.where(np.array(y_comb_OSI450a_feb) < 1, np.nan, y_comb_OSI450a_feb)
y_comb_nsidc_feb = np.where(np.array(y_comb_nsidc_feb) < 1, np.nan, y_comb_nsidc_feb)
y_comb_feb = np.array(y_comb_feb)

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_feb)], y_comb_feb[~np.isnan(y_comb_feb)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_feb)], y_comb_OSI450a_feb[~np.isnan(y_comb_OSI450a_feb)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_feb)], y_comb_nsidc_feb[~np.isnan(y_comb_nsidc_feb)])

print(f'feb: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_feb, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_feb, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_feb, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_feb, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_feb, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_feb))-1,np.round(np.nanmax(y_comb_OSI450a_feb))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('February mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_feb_SIC_{HS}_{v}.png')
#plt.show()
plt.close()



# ##############################################
# # Yearly extend March
# ##############################################
y_comb_OSI458_mar=np.array(y_comb_OSI458_mar)
y_comb_OSI458_mar[y_comb_OSI458_mar<2]=np.nan
y_comb_OSI450a_mar=np.array(y_comb_OSI450a_mar)
y_comb_OSI450a_mar[y_comb_OSI450a_mar<2]=np.nan
y_comb_nsidc_mar=np.array(y_comb_nsidc_mar)
y_comb_nsidc_mar[y_comb_nsidc_mar<2]=np.nan
y_comb_mar = np.array(y_comb_mar)
#%%%%%%%%%%%%%%%%%%%%%%%%%%
# Linear trends
#%%%%%%%%%%%%%%%%%%%%%%%%%%%

# slope1, intercept1, r1, p1, se1 = stats.linregress(years[~np.isnan(y_comb_mar)], y_comb_mar[~np.isnan(y_comb_mar)])
# slope2, intercept2, r2, p2, se2 = stats.linregress(years[~np.isnan(y_comb_OSI450a_mar)], y_comb_OSI450a_mar[~np.isnan(y_comb_OSI450a_mar)])
# slope3, intercept3, r3, p3, se3 = stats.linregress(years[~np.isnan(y_comb_OSI458_mar)], y_comb_OSI458_mar[~np.isnan(y_comb_OSI458_mar)])
# slope4, intercept4, r4, p4, se4 = stats.linregress(years[~np.isnan(y_comb_nsidc_mar)], y_comb_nsidc_mar[~np.isnan(y_comb_nsidc_mar)])

y_comb_OSI458_mar = np.where(np.array(y_comb_OSI458_mar) < 1, np.nan, y_comb_OSI458_mar)
y_comb_OSI450a_mar = np.where(np.array(y_comb_OSI450a_mar) < 1, np.nan, y_comb_OSI450a_mar)
y_comb_nsidc_mar = np.where(np.array(y_comb_nsidc_mar) < 1, np.nan, y_comb_nsidc_mar)
y_comb_mar = np.array(y_comb_mar)

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_mar)], y_comb_mar[~np.isnan(y_comb_mar)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_mar)], y_comb_OSI450a_mar[~np.isnan(y_comb_OSI450a_mar)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_mar)], y_comb_nsidc_mar[~np.isnan(y_comb_nsidc_mar)])

print(f'mar: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

# plt.figure(figsize=(10,7))
# plt.plot(years, years*slope1+intercept1, '-', linewidth=1, color=colors[0], label=f'DMI_MSC NH: Trend:{int(np.round(slope1*1e3))} thousand km²/year')
# plt.plot(years, years*slope2+intercept2, '-', linewidth=1, color=colors[1], label=f'OSI450a: Trend:{int(np.round(slope2*1e3))} thousand km²/year')
# plt.plot(years, years*slope3+intercept3, '-', linewidth=1, color=colors[2], label=f'OSI458: Trend:{int(np.round(slope3*1e3))} thousand km²/year')
# plt.plot(years, years*slope4+intercept4, '-', linewidth=1, color=colors[3], label=f'nsidc: Trend:{int(np.round(slope4*1e3))} thousand km²/year')
# plt.plot(years, y_comb_mar, 'o-', label='DMI_MSC NH')
#plt.plot(years, y_comb_orig_mar, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_mar, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_mar, 'o-', label='OSI458')
#plt.plot(years, y_comb_nsidc_mar, 'o-', label='nsidc')

plt.xticks(years, years_str, rotation=45)
plt.ylim(np.round(np.nanmin(y_comb_mar))-1,np.round(np.nanmax(y_comb_OSI450a_mar))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.title('March mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_mar_SIC_{HS}_{v}.png')
#plt.show()
plt.close()
# #################################################

##############################################
# Yearly extend APRIL
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_apr = np.where(np.array(y_comb_OSI458_apr) < 1, np.nan, y_comb_OSI458_apr)
y_comb_OSI450a_apr = np.where(np.array(y_comb_OSI450a_apr) < 1, np.nan, y_comb_OSI450a_apr)
y_comb_nsidc_apr = np.where(np.array(y_comb_nsidc_apr) < 1, np.nan, y_comb_nsidc_apr)
y_comb_apr = np.array(y_comb_apr)
y_comb_nsidc_apr[(y_comb_apr+0.01)>y_comb_nsidc_apr] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_apr)], y_comb_apr[~np.isnan(y_comb_apr)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_apr)], y_comb_OSI450a_apr[~np.isnan(y_comb_OSI450a_apr)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_apr)], y_comb_nsidc_apr[~np.isnan(y_comb_nsidc_apr)])

print(f'apr: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_apr, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_apr, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_apr, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_apr, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_apr, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_apr))-1,np.round(np.nanmax(y_comb_OSI450a_apr))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('APRIL mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_apr_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend MAY
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]
y_comb_OSI458_may = np.where(np.array(y_comb_OSI458_may) < 1, np.nan, y_comb_OSI458_may)
y_comb_OSI450a_may = np.where(np.array(y_comb_OSI450a_may) < 1, np.nan, y_comb_OSI450a_may)
y_comb_nsidc_may = np.where(np.array(y_comb_nsidc_may) < 1, np.nan, y_comb_nsidc_may)
y_comb_may = np.array(y_comb_may)
y_comb_nsidc_may[(y_comb_may+0.01)>y_comb_nsidc_may] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_may)], y_comb_may[~np.isnan(y_comb_may)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_may)], y_comb_OSI450a_may[~np.isnan(y_comb_OSI450a_may)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_may)], y_comb_nsidc_may[~np.isnan(y_comb_nsidc_may)])

print(f'may: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_may, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_may, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_may, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_may, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_may, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_may))-1,np.round(np.nanmax(y_comb_OSI450a_may))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('MAY mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_may_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend JUNE
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_jun = np.where(np.array(y_comb_OSI458_jun) < 1, np.nan, y_comb_OSI458_jun)
y_comb_OSI450a_jun = np.where(np.array(y_comb_OSI450a_jun) < 1, np.nan, y_comb_OSI450a_jun)
y_comb_nsidc_jun = np.where(np.array(y_comb_nsidc_jun) < 1, np.nan, y_comb_nsidc_jun)
y_comb_jun = np.array(y_comb_jun)
y_comb_nsidc_jun[(y_comb_jun+0.01)>y_comb_nsidc_jun] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_jun)], y_comb_jun[~np.isnan(y_comb_jun)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_jun)], y_comb_OSI450a_jun[~np.isnan(y_comb_OSI450a_jun)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_jun)], y_comb_nsidc_jun[~np.isnan(y_comb_nsidc_jun)])

print(f'jun: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_jun, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_jun, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_jun, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_jun, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_jun, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_jun))-1,np.round(np.nanmax(y_comb_OSI450a_jun))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('JUNE mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_jun_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend JULY
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_jul = np.where(np.array(y_comb_OSI458_jul) < 1, np.nan, y_comb_OSI458_jul)
y_comb_OSI450a_jul = np.where(np.array(y_comb_OSI450a_jul) < 1, np.nan, y_comb_OSI450a_jul)
y_comb_nsidc_jul = np.where(np.array(y_comb_nsidc_jul) < 1, np.nan, y_comb_nsidc_jul)
y_comb_jul = np.array(y_comb_jul)
y_comb_nsidc_jul[(y_comb_jul+0.01)>y_comb_nsidc_jul] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_jul)], y_comb_jul[~np.isnan(y_comb_jul)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_jul)], y_comb_OSI450a_jul[~np.isnan(y_comb_OSI450a_jul)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_jul)], y_comb_nsidc_jul[~np.isnan(y_comb_nsidc_jul)])

print(f'jul: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_jul, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_jul, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_jul, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_jul, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_jul, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_jul))-1,np.round(np.nanmax(y_comb_OSI450a_jul))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('JULY mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_jul_SIC_{HS}_{v}.png')
#plt.show()
plt.close()


##############################################
# Yearly extend AUGUST
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_aug = np.where(np.array(y_comb_OSI458_aug) < 1, np.nan, y_comb_OSI458_aug)
y_comb_OSI450a_aug = np.where(np.array(y_comb_OSI450a_aug) < 1, np.nan, y_comb_OSI450a_aug)
y_comb_nsidc_aug = np.where(np.array(y_comb_nsidc_aug) < 1, np.nan, y_comb_nsidc_aug)
y_comb_aug = np.array(y_comb_aug)
y_comb_nsidc_aug[(y_comb_aug+0.01)>y_comb_nsidc_aug] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_aug)], y_comb_aug[~np.isnan(y_comb_aug)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_aug)], y_comb_OSI450a_aug[~np.isnan(y_comb_OSI450a_aug)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_aug)], y_comb_nsidc_aug[~np.isnan(y_comb_nsidc_aug)])

print(f'aug: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_aug, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_aug, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_aug, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_aug, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_aug, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_aug))-1,np.round(np.nanmax(y_comb_OSI450a_aug))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('AUGUST mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_aug_SIC_{HS}_{v}.png')
#plt.show()
plt.close()


##############################################
# Yearly extend September
##############################################
# fig, ax = plt.subplots(figsize=(16,7))
# twin1 = ax.twinx()

# years_str = [str(y) for y in years]
# y_comb_OSI458_sep=np.array(y_comb_OSI458_sep)
# y_comb_OSI458_sep[y_comb_OSI458_sep<1]=np.nan
# y_comb_OSI450a_sep=np.array(y_comb_OSI450a_sep)
# y_comb_OSI450a_sep[y_comb_OSI450a_sep<1]=np.nan
# y_comb_nsidc_sep=np.array(y_comb_nsidc_sep)
# y_comb_nsidc_sep[y_comb_nsidc_sep<1]=np.nan

# y_comb_sep = np.array(y_comb_sep)
# #%%%%%%%%%%%%%%%%%%%%%%%%%%
# # Linear trends
# #%%%%%%%%%%%%%%%%%%%%%%%%%%%

# ## MARCH ##
# slope1, intercept1, r1, p1, se1 = stats.linregress(years[~np.isnan(y_comb_mar)], y_comb_mar[~np.isnan(y_comb_mar)])
# slope2, intercept2, r2, p2, se2 = stats.linregress(years[~np.isnan(y_comb_OSI450a_mar)], y_comb_OSI450a_mar[~np.isnan(y_comb_OSI450a_mar)])
# #slope3, intercept3, r3, p3, se3 = stats.linregress(years[~np.isnan(y_comb_OSI458_mar)], y_comb_OSI458_mar[~np.isnan(y_comb_OSI458_mar)])
# slope4, intercept4, r4, p4, se4 = stats.linregress(years[~np.isnan(y_comb_nsidc_mar)], y_comb_nsidc_mar[~np.isnan(y_comb_nsidc_mar)])

# #twin1.plot(years, years*slope1+intercept1, '-', linewidth=1, color=colors[4])
# #twin1.plot(years, years*slope2+intercept2, '-', linewidth=1, color=colors[5])
# #twin1.plot(years, years*slope3+intercept3, '-', linewidth=1, color=colors[6], label=f'OSI458: Trend:{int(np.round(slope3*1e3))}*10³ km²/year')
# #twin1.plot(years, years*slope4+intercept4, '-', linewidth=1, color=colors[7])

# twin1.plot(years, y_comb_mar, '--', color=colors[4], label=f'DMI-MSC-SIC: Trend:{int(np.round(slope1*1e3))}*10³ km²/year')
# #plt.plot(years, y_comb_orig_mar, 'o-', label='ORIG')
# twin1.plot(years, y_comb_OSI450a_mar, '--', color=colors[5], label=f'OSI-450-a: Trend:{int(np.round(slope2*1e3))}*10³ km²/year') #, label='OSI450a')
# twin1.plot(years, y_comb_nsidc_mar, '--', color=colors[7], label=f'NOAA/NSIDC: Trend:{int(np.round(slope4*1e3))}*10³ km²/year') #, label='nsidc')
# twin1.plot(years, y_comb_OSI458_mar, '--', color=colors[6], label='OSI-458')

# ## SEPTEMBER ##
# slope1, intercept1, r1, p1, se1 = stats.linregress(years[~np.isnan(y_comb_sep)], y_comb_sep[~np.isnan(y_comb_sep)])
# slope2, intercept2, r2, p2, se2 = stats.linregress(years[~np.isnan(y_comb_OSI450a_sep)], y_comb_OSI450a_sep[~np.isnan(y_comb_OSI450a_sep)])
# #slope3, intercept3, r3, p3, se3 = stats.linregress(years[~np.isnan(y_comb_OSI458_sep)], y_comb_OSI458_sep[~np.isnan(y_comb_OSI458_sep)])
# slope4, intercept4, r4, p4, se4 = stats.linregress(years[~np.isnan(y_comb_nsidc_sep)], y_comb_nsidc_sep[~np.isnan(y_comb_nsidc_sep)])

# #ax.plot(years, years*slope1+intercept1, '-', linewidth=1, color=colors[0])
# #ax.plot(years, years*slope2+intercept2, '-', linewidth=1, color=colors[1])
# #ax.plot(years, years*slope3+intercept3, '-', linewidth=1, color=colors[2], label=f'OSI458: Trend:{int(np.round(slope3*1e3))}*10³ km²/year')
# #ax.plot(years, years*slope4+intercept4, '-', linewidth=1, color=colors[3])

# ax.plot(years, y_comb_sep, '-', color=colors[0], label=f'DMI-MSC-SIC: Trend:{int(np.round(slope1*1e3))}*10³ km²/year') #, label='DMI_MSC NH')
# #plt.plot(years, y_comb_orig_sep, 'o-', label='ORIG')
# ax.plot(years, y_comb_OSI450a_sep, '-', color=colors[1], label=f'OSI-450-a: Trend:{int(np.round(slope2*1e3))}*10³ km²/year') #, label='OSI450a')
# ax.plot(years, y_comb_nsidc_sep, '-', color=colors[3], label=f'NOAA/NSIDC: Trend:{int(np.round(slope4*1e3))}*10³ km²/year') #, label='nsidc')
# ax.plot(years, y_comb_OSI458_sep, '-', color=colors[2], label='OSI-458')

# ax.set_ylim(np.round(np.nanmin(y_comb_sep))-3,np.round(np.nanmax(y_comb_OSI450a_sep))+2)
# twin1.set_ylim(np.round(np.nanmin(y_comb_mar))-1,np.round(np.nanmax(y_comb_OSI450a_mar))+5)
# plt.xlim(years[0], years[-1])
# ax.set_ylabel('September extent (Millions of square kilometers)', fontsize=14)
# twin1.set_ylabel('March extent (Millions of square kilometers)', fontsize=14)
# ax.set_xticks(years, years_str, rotation=45)
# plt.title(f'{HS.upper()}: September and March mean sea ice extent', fontsize=16)
# ax.grid()

# plt.rcParams['legend.title_fontsize'] = 'large'
# ax.tick_params(axis='both', which='major', labelsize=12)
# twin1.tick_params(axis='both', which='major', labelsize=12)
# ax.set_xlabel('Year', fontsize=14)

# # Combine legends
# ax.legend(loc='upper left', fontsize=12, title=r"$\bf{September}$")
# twin1.legend(loc='upper right', fontsize=12, title=r"$\bf{March}$")
# #ax.legend(lines + lines2, labels + labels2, loc=0, fontsize=12, fancybox=True, framealpha=1) #bbox_to_anchor=(1.08, 0.7))
# plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_sep_SIC_{HS}_{v}.png', bbox_inches='tight', transparent=True)
# plt.show()
# plt.close()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)

years_str = [str(y) for y in years]

# Clean invalid SIC values
y_comb_OSI458_sep = np.where(np.array(y_comb_OSI458_sep) < 1, np.nan, y_comb_OSI458_sep)
y_comb_OSI450a_sep = np.where(np.array(y_comb_OSI450a_sep) < 1, np.nan, y_comb_OSI450a_sep)
y_comb_nsidc_sep = np.where(np.array(y_comb_nsidc_sep) < 1, np.nan, y_comb_nsidc_sep)
y_comb_sep = np.array(y_comb_sep)

# === SEPTEMBER PLOT ===
slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_sep)], y_comb_sep[~np.isnan(y_comb_sep)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_sep)], y_comb_OSI450a_sep[~np.isnan(y_comb_OSI450a_sep)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_sep)], y_comb_nsidc_sep[~np.isnan(y_comb_nsidc_sep)])

# compute decline in %/decade
# computed as (slope/initial_average)*10 (to get it per decade)*100 (to get %)

#start index: 1991-1982=9
# end index: 2020-1982=38
ref_val_sep = np.nanmean(y_comb_sep[:28])
ref_val_sep_OSI450a = np.nanmean(y_comb_OSI450a_sep[:28])
ref_val_sep_NSIDC = np.nanmean(y_comb_nsidc_sep[:28])

decline_perc_dec_1 = (slope1/ref_val_sep)*10*100
decline_perc_dec_2 = (slope2/ref_val_sep_OSI450a)*10*100
decline_perc_dec_4 = (slope4/ref_val_sep_NSIDC)*10*100

ax1.plot(years, y_comb_sep, '-', color=colors[0], label=f'DMI-MSC-SIC: Trend: {int(np.round(slope1*1e3))}×10³ km²/year, {np.round(decline_perc_dec_1,1)} %/dec')
ax1.plot(years, y_comb_OSI450a_sep, '-', color=colors[1], label=f'OSI-450-a: Trend: {int(np.round(slope2*1e3))}×10³ km²/year, {np.round(decline_perc_dec_2,1)} %/dec')
ax1.plot(years, y_comb_nsidc_sep, '-', color=colors[3], label=f'NOAA/NSIDC: Trend: {int(np.round(slope4*1e3))}×10³ km²/year, {np.round(decline_perc_dec_4,1)} %/dec')
ax1.plot(years, y_comb_OSI458_sep, '-', color=colors[2], label='OSI-458')

ax1.set_title(f'{HS.upper()}: Mean Sea Ice Extent', fontsize=18)
ax1.set_ylabel('September extent (millions km²)', fontsize=16)
ax1.set_ylim(np.round(np.nanmin(y_comb_sep)) - 1, np.round(np.nanmax(y_comb_OSI450a_sep)) + 3)
ax1.set_xticks(years)
legend_ax1 = ax1.legend(loc='upper right', fontsize=14, title="September", title_fontsize=14)
legend_ax1.get_title().set_fontweight('bold')
ax1.grid()
ax1.tick_params(axis='both', which='major', labelsize=14)


# === MARCH PLOT ===
slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_mar)], y_comb_mar[~np.isnan(y_comb_mar)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_mar)], y_comb_OSI450a_mar[~np.isnan(y_comb_OSI450a_mar)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_mar)], y_comb_nsidc_mar[~np.isnan(y_comb_nsidc_mar)])

# compute decline in %/decade
# computed as (slope/initial_average)*10 (to get it per decade)*100 (to get %)
# as reference period the monhtly averages for the 1991-2020 reference period and expressed as a percentage of these averages (https://climate.copernicus.eu/climate-indicators/sea-ice)

#start index: 1991-1982=9
# end index: 2024-1982=38
ref_val_mar = np.nanmean(y_comb_mar[:28])
ref_val_mar_OSI450a = np.nanmean(y_comb_OSI450a_mar[:28])
ref_val_mar_NSIDC = np.nanmean(y_comb_nsidc_mar[:28])

decline_perc_dec_1 = (slope1/ref_val_mar)*10*100
decline_perc_dec_2 = (slope2/ref_val_mar_OSI450a)*10*100
decline_perc_dec_4 = (slope4/ref_val_mar_NSIDC)*10*100

ax2.plot(years, y_comb_mar, '--', color=colors[4], label=f'DMI-MSC-SIC: Trend: {int(np.round(slope1*1e3))}×10³ km²/year, {np.round(decline_perc_dec_1,1)} %/dec')
ax2.plot(years, y_comb_OSI450a_mar, '--', color=colors[5], label=f'OSI-450-a: Trend: {int(np.round(slope2*1e3))}×10³ km²/year, {np.round(decline_perc_dec_2,1)} %/dec')
ax2.plot(years, y_comb_nsidc_mar, '--', color=colors[7], label=f'NOAA/NSIDC: Trend: {int(np.round(slope4*1e3))}×10³ km²/year, {np.round(decline_perc_dec_4,1)} %/dec')
ax2.plot(years, y_comb_OSI458_mar, '--', color=colors[6], label='OSI-458')

ax2.set_ylabel('March extent (millions km²)', fontsize=16)
ax2.set_ylim(np.round(np.nanmin(y_comb_mar)) - 1, np.round(np.nanmax(y_comb_OSI450a_mar)) + 4)
ax2.set_xticks(years)
ax2.set_xticklabels(years_str, rotation=45)
ax2.set_xlabel('Year', fontsize=16)
legend_ax2 = ax2.legend(loc='upper right', fontsize=14, title="March", title_fontsize=14)
legend_ax2.get_title().set_fontweight('bold')
ax2.grid()
ax2.tick_params(axis='both', which='major', labelsize=14)

plt.xlim(years[0], years[-1])
plt.tight_layout()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_mar_sep_SIC_{HS}_{v}.png', bbox_inches='tight', transparent=True)
#plt.show()
plt.close()

##############################################
# Yearly extend OCTOBER
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_oct = np.where(np.array(y_comb_OSI458_oct) < 1, np.nan, y_comb_OSI458_oct)
y_comb_OSI450a_oct = np.where(np.array(y_comb_OSI450a_oct) < 1, np.nan, y_comb_OSI450a_oct)
y_comb_nsidc_oct = np.where(np.array(y_comb_nsidc_oct) < 1, np.nan, y_comb_nsidc_oct)
y_comb_oct = np.array(y_comb_oct)
y_comb_nsidc_oct[(y_comb_oct+0.01)>y_comb_nsidc_oct] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_oct)], y_comb_oct[~np.isnan(y_comb_oct)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_oct)], y_comb_OSI450a_oct[~np.isnan(y_comb_OSI450a_oct)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_oct)], y_comb_nsidc_oct[~np.isnan(y_comb_nsidc_oct)])

print(f'oct: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_oct, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_oct, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_oct, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_oct, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_oct, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_oct))-1,np.round(np.nanmax(y_comb_OSI450a_oct))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('OCTOBER mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_oct_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend NOVEMBER
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_nov = np.where(np.array(y_comb_OSI458_nov) < 1, np.nan, y_comb_OSI458_nov)
y_comb_OSI450a_nov = np.where(np.array(y_comb_OSI450a_nov) < 1, np.nan, y_comb_OSI450a_nov)
y_comb_nsidc_nov = np.where(np.array(y_comb_nsidc_nov) < 1, np.nan, y_comb_nsidc_nov)
y_comb_nov = np.array(y_comb_nov)
y_comb_nsidc_nov[(y_comb_nov+0.01)>y_comb_nsidc_nov] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_nov)], y_comb_nov[~np.isnan(y_comb_nov)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_nov)], y_comb_OSI450a_nov[~np.isnan(y_comb_OSI450a_nov)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_nov)], y_comb_nsidc_nov[~np.isnan(y_comb_nsidc_nov)])

print(f'nov: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_nov, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_nov, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_nov, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_nov, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_nov, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_nov))-1,np.round(np.nanmax(y_comb_OSI450a_nov))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('NOVEMBER mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_nov_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend DECEMBER
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_dec = np.where(np.array(y_comb_OSI458_dec) < 1, np.nan, y_comb_OSI458_dec)
y_comb_OSI450a_dec = np.where(np.array(y_comb_OSI450a_dec) < 1, np.nan, y_comb_OSI450a_dec)
y_comb_nsidc_dec = np.where(np.array(y_comb_nsidc_dec) < 1, np.nan, y_comb_nsidc_dec)
y_comb_dec = np.array(y_comb_dec)
y_comb_nsidc_dec[(y_comb_dec+0.01)>y_comb_nsidc_dec] = np.nan

slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_dec)], y_comb_dec[~np.isnan(y_comb_dec)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_dec)], y_comb_OSI450a_dec[~np.isnan(y_comb_OSI450a_dec)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_dec)], y_comb_nsidc_dec[~np.isnan(y_comb_nsidc_dec)])

print(f'dec: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_dec, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_dec, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_dec, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_dec, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_dec, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_dec))-1,np.round(np.nanmax(y_comb_OSI450a_dec))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('DECEMBER mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_dec_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

##############################################
# Yearly extend yearly mean
##############################################
plt.figure(figsize=(10,7))
years_str = [str(y) for y in years]

y_comb_OSI458_yr = np.where(np.array(y_comb_OSI458_yr) < 9, np.nan, y_comb_OSI458_yr)
y_comb_OSI450a_yr = np.where(np.array(y_comb_OSI450a_yr) < 9, np.nan, y_comb_OSI450a_yr)
y_comb_nsidc_yr = np.where(np.array(y_comb_nsidc_yr) < 9, np.nan, y_comb_nsidc_yr)
y_comb_yr = np.array(y_comb_yr)
y_comb_nsidc_yr[(y_comb_yr+0.01)>y_comb_nsidc_yr] = np.nan


slope1, intercept1, *_ = stats.linregress(years[~np.isnan(y_comb_yr)], y_comb_yr[~np.isnan(y_comb_yr)])
slope2, intercept2, *_ = stats.linregress(years[~np.isnan(y_comb_OSI450a_yr)], y_comb_OSI450a_yr[~np.isnan(y_comb_OSI450a_yr)])
slope4, intercept4, *_ = stats.linregress(years[~np.isnan(y_comb_nsidc_yr)], y_comb_nsidc_yr[~np.isnan(y_comb_nsidc_yr)])

print(f'yr: DMI-MSC-SIC trend: {slope1*10**3}, OSI450a trend: {slope2*10**3}, NSIDC trend: {slope4*10**3}, ')

plt.plot(years, y_comb_yr, 'o-', label='CARRA2')
#plt.plot(years, y_comb_orig_yr, 'o-', label='ORIG')
plt.plot(years, y_comb_OSI450a_yr, 'o-', label='OSI450a')
plt.plot(years, y_comb_OSI458_yr, 'o-', label='OSI458')
plt.plot(years, y_comb_nsidc_yr, 'o-', label='nsidc')

plt.ylim(np.round(np.nanmin(y_comb_yr))-1,np.round(np.nanmax(y_comb_OSI450a_yr))+1)
plt.xlim(years[0], years[-1])
plt.ylabel('Extent (Millions of square kilometers)')
plt.xticks(years, years_str, rotation=45)
plt.title('yearly mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_yr_SIC_{HS}_{v}.png')
#plt.show()
plt.close()

#################################################

# ##############################################
# # daily SIE
# ##############################################
x = np.arange(1, len(years)*365+1)
plt.figure(figsize=(20,10))

#plt.plot(x, np.array(y_comb).flatten(), '-', label='CARRA2')
plt.plot(x, np.array(y_comb).flatten(), '-',  linewidth=2, label='CARRA2')
#plt.plot(x, np.array(y_comb_OSI450a).flatten(), '-',  linewidth=0.9, label='OSI450a')
#plt.plot(x, np.array(y_comb_OSI450a_filt).flatten(), '-',  linewidth=0.9, label='OSI450a filt')
#plt.plot(x, np.array(y_comb_orig).flatten(), '-', linewidth=0.9, label='ORIG')
#y_comb_OSI458=np.array(y_comb_OSI458).flatten()
#y_comb_OSI458[y_comb_OSI458==0]=np.nan
#plt.plot(x, np.array(y_comb_OSI458).flatten(), '-',  linewidth=0.9, label='OSI458')
#plt.plot(years, y_comb_nsidc_sep, 'o-', label='nsidc')
plt.xticks(ticks=x[::365], rotation=45, labels=years.astype(list))
#plt.ylim(3,9)
plt.xlim(x[0], x[-1])
plt.ylabel('Extent (Millions of square kilometers)')
#plt.title('September mean sea ice extent')
plt.grid()
plt.legend()
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_DOY_year_SIC_GBL_NH.png', bbox_inches='tight')
#plt.show()
plt.close()

# # filtered
y_std = np.std(y_comb, axis=0)
y_mean = np.mean(y_comb, axis=0)

# # orig 
# y_std_orig = np.std(y_comb_orig, axis=0)
# y_mean_orig = np.mean(y_comb_orig, axis=0)

# # OSI450a
# y_std_OSI450a = np.std(y_comb_OSI450a, axis=0)
# y_mean_OSI450a = np.mean(y_comb_OSI450a, axis=0)

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
    
    ax.plot(DOY_period1, np.array(y_comb)[i+4,(DOY_period1-1).astype(int)], '-', linewidth=1, color=colors[i], label=f'{years[i+4]}')
    ax.plot(DOY_period2, np.array(y_comb)[i+4,(DOY_period2-1).astype(int)], '-', linewidth=2, color=colors[i], label=f'{years[i+4]}: interpolated')
    if years[i+4]==1986:
        ax.plot(DOY_period3_1986, np.array(y_comb)[i+4,(DOY_period3_1986-1).astype(int)], '-', linewidth=1, color=colors[i]) # , label=f'{years[i+4]}')
    #ax.plot(DOY, np.array(y_comb)[i+4,:], '-', color=colors[i], label=f'{years[i+4]}')
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
plt.ylabel('Extent (Millions of square kilometers)', fontsize=18)
plt.suptitle(f'{HS.upper()} Sea Ice Extent', fontsize=20, y=0.955)
plt.title('(Area of ocean with atleast 15% sea ice)', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
if HS=='nh':
    plt.ylim([0,19])
elif HS=='sh':
    plt.ylim([0,25])
plt.xlim([0,365])
plt.savefig(f'/dmidata/projects/cmems2/C3S/CARRA2/CARRA2_dokumentation/figures/{years[0]}_{years[-1]}_DOY_extend_{HS}.png', bbox_inches='tight')
plt.close() 
