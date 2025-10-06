import numpy as np
import os
import re
import datetime as dt
import matplotlib.pyplot as plt
import xarray as xr

from patch_1986_with_NIC_icecharts import missing_1986_data

def Get_data_1986(ID, HS):
    dir_SIC = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/1986/03/'
    files_SIC = sorted(os.listdir(dir_SIC))
    files_SIC = [f for f in files_SIC  if HS in f ]
    identify_dates = [re.findall('\d+', f)[-1][:8] for f in files_SIC]
    dat_num = np.array([int(i) for i in identify_dates])

    y1='1986'
    m1='06'
    # Load files from other month/year
    dir_SIC1 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/{y1}/{m1}/'
    files_SIC1 = sorted(os.listdir(dir_SIC1))
    files_SIC1 = [f for f in files_SIC1  if HS in f ]

    return dat_num, files_SIC, files_SIC1, dir_SIC1, dir_SIC

def missing_SIC_data(d, dat_num, files_SIC, dir_SIC, HS, ID):

    y = d[:4]
    m = d[4:6]

    print(dat_num)
    # criteria for when to use special function for 1986, as there are several months of data missing
    criteria = (int(m)==3 and all(int(d)>dat_num)) or (int(m)==6 and all(int(d)<dat_num)) or ((int(m)>=4) and (int(m)<=5))

    if ((int(y)==1986) and criteria): # several months of data missing (4th, 5th and lots of 3rd and 6th)
        # look for data in march and/or june
        print('getting data for 1986')
        dat_num, files_SIC, files_SIC1, dir_SIC1, dir_SIC = Get_data_1986(ID, HS)
        data_SIC = missing_1986_data(d, dat_num, files_SIC, files_SIC1, dir_SIC1, dir_SIC,HS)
    else:
        y1='' # define as empty string for string comparison later in the script

        # if we are the start or end of the month or in 1986
        if all(int(d)<dat_num) or all(int(d)>dat_num):
            if all(int(d)<dat_num):
                print('looking in previous month')
                # look for data in previous month
                m1 = int(m)-1
            elif all(int(d)>dat_num):
                # look for data in subsequent month
                m1 = int(m)+1

            try: # load data
                m1 = '0' + str(m1) if m1<10 else str(m1)
                if ID=='OSI458_TU' and HS=='sh':
                    dir_SIC1 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/{y}/{m1}/'
                    #dir_SIC1 = f'/dmidata/projects/cmems2/C3S/OSI458/extention_SH/regridded/{y}/{m1}/'
                else:
                    dir_SIC1 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/{y}/{m1}/'
                files_SIC1 = sorted(os.listdir(dir_SIC1))
            except: 
                if int(m)==1: # look in previous year
                    m1 = '12'
                    y1 = str(int(y)-1)
                elif int(m)==12: # look in subsequent year
                    m1 = '01'
                    y1 = str(int(y)+1)                

                # Load files from other month/year
                if y1=='1990': # crossover between SICCI_HR and OSI450a
                    dir_SIC1 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/OSI450a/{y1}/{m1}/'
                    files_SIC1 = sorted(os.listdir(dir_SIC1))
                else:
                    dir_SIC1 = f'/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/regridded_SIC_data/{ID}/{y1}/{m1}/'
                    files_SIC1 = sorted(os.listdir(dir_SIC1))
                
            #else:
            files_SIC1 = [f for f in files_SIC1 if (HS in f) or (HS.upper() in f)]
            # identify files belonging to the relevant date
            if (y1=='1990') or ('SICCI' not in ID):
                identify_dates = [re.findall('\d+', f)[-1][:8] for f in files_SIC1]
                print(files_SIC1)
            else:
                identify_dates = [re.findall('\d+', f)[-3][:8] for f in files_SIC1]
            print(identify_dates)
            
            dat_num1 = np.array([int(i) for i in identify_dates])

            # make combined date and files arrays
            files_SIC = files_SIC + files_SIC1
            dat_num = np.concatenate((dat_num, dat_num1))

        # convert to datetime objects
        
        dates = [dt.datetime.strptime(str(d), '%Y%m%d') for d in dat_num]
        d_rel = dt.datetime.strptime(d, '%Y%m%d')

        # find minimum timewise distance
        index = np.argsort(dates)
        # compute time differences
        delta = [abs(d_rel-d) for d in np.array(dates)[index]]
        # make sure that files are in descending order based on temporal distance
        dates = np.array(dates)[index]
        files_SIC = np.array(files_SIC)[index]

        # find location of minimum difference
        min_index = np.argmin(delta)
        if (d_rel-dates[min_index]).total_seconds()<0:
            print('smallest distance after date')
            min_index2 = min_index-1
            # 1986 ref
            #ind_1986_t0 = min_index-1
        elif (d_rel-dates[min_index]).total_seconds()>0:
            print('smallest distance before date')
            min_index2 = min_index+1
            # 1986 ref
            #ind_1986_t0 = min_index

        # if we have data on both sites of the missing day
        if min_index==delta[min_index2]:
            print('only one day in between')
            weight_closest = 1/2
            weight_furthest = 1/2
        # if the gap is larger
        else:
            # calculate the total tiemwise distance between files
            denom=delta[min_index2]+delta[min_index]
            #print(denom)
            weight_closest = delta[min_index2]/denom
            weight_furthest = delta[min_index]/denom
            #print(f'{weight_closest}, {weight_furthest}')


        fsic = [files_SIC[min_index],files_SIC[min_index2]]
        print(fsic)

        file_SIC = [dir_SIC + f if f'{y}{m}' in f else dir_SIC1 + f for f in fsic]

        print(f'No file available for date {d} using files with smallest temporal distance: {fsic[0]} with weight {weight_closest}, {fsic[1]} with weight {weight_furthest}, ')
        ## take weighted ice_conc if we have a one day whole
        data_SIC = xr.open_dataset(file_SIC[0])
        #print(file_SIC[0])
        data_SIC2 = xr.open_dataset(file_SIC[1])
        #print(file_SIC[1])

        # loop through variables in nc file
        for v1,v2 in zip(data_SIC, data_SIC2):
            
            # time_bnds is 1 dimensional and hence should be ignored
            if 'time_bnds' not in v1:

                #     #SIC=(data_SIC[v1].squeeze().to_numpy()-data_SIC2[v2].squeeze().to_numpy())/2 * (np.sin(2*np.pi*(t-t0)/365)) + (data_SIC[v1].squeeze().to_numpy()+data_SIC2[v2].squeeze().to_numpy())/2
                    
                #     # if v1=='ice_conc':
                #     #     plt.figure()
                #     #     plt.imshow(np.flipud(SIC))
                #     #     plt.colorbar()
                #     #     plt.savefig('/dmidata/projects/cmems2/C3S/CARRA2/figures/test_SIC.png')

                #     #     plt.figure()
                #     #     plt.imshow(np.flipud(data_SIC[v1].squeeze().to_numpy()))
                #     #     plt.colorbar()
                #     #     plt.savefig('/dmidata/projects/cmems2/C3S/CARRA2/figures/test_SIC1.png')

                #     #     plt.figure()
                #     #     plt.imshow(np.flipud(data_SIC2[v2].squeeze().to_numpy()))
                #     #     plt.colorbar()
                #     #     plt.savefig('/dmidata/projects/cmems2/C3S/CARRA2/figures/test_SIC2.png')
                #                     # stack datasets
                #     v = np.vstack((weight_t0*data_SIC[v1],weight_t1*data_SIC2[v2]))
                #     # compute mean and assign to data_SIC
                #     data_SIC[v1] = xr.DataArray(np.expand_dims(np.sum(v, axis=0), axis=0), dims={'time': 1, 'lat': 1800, 'lon': 7200})

                #     #data_SIC[v1] = xr.DataArray(np.expand_dims(SIC, axis=0), dims={'time': 1, 'lat': 1800, 'lon': 7200})
                # else:
                    # stack datasets
                v = np.vstack((weight_closest*data_SIC[v1],weight_furthest*data_SIC2[v2]))
                # compute mean and assign to data_SIC
                data_SIC[v1] = xr.DataArray(np.expand_dims(np.sum(v, axis=0), axis=0), dims={'time': 1, 'lat': 1800, 'lon': 7200})


    return data_SIC
