#!/usr/bin/env python
# coding: utf-8

import urllib.request
import zipfile
import os
import argparse
from datetime import datetime, timedelta
import time
import random

def download_usnic_data(date, name, path='/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NIC/shapefiles'):
    year = date.year
    month = date.month
    day = date.day
    url = f'https://usicecenter.gov/File/DownloadArchive?prd={hem}{month:02}{day:02}{year:04}'
    ofile = f'{path}/{name}{str(year)[2:]}{month:02}{day:02}.zip'
    #print(url, ofile)
    
    # Download file
    try:
        urllib.request.urlretrieve(url, ofile)
        print(f'File {ofile} downloaded')
    except:
        #print('Error 404')
        print('No data available at this date')
        time.sleep(random.uniform(0,0.5))
        return
    
    # Create a folder
    directory = f'{name}{str(year)[2:]}{month:02}{day:02}'
    path_file = f'{path}/{directory}'
    os.makedirs(path_file, exist_ok=True)
    print("Directory '% s' created" % path_file)    
    
    # Unzip in this folder
    with zipfile.ZipFile(ofile, 'r') as zip_ref:
        zip_ref.extractall(f'{path}/{directory}')
    #print('File unzip')

    # Remove zip file
    #os.remove(path + 'arctic_zip')

parser = argparse.ArgumentParser()
parser.add_argument("start_date", help="startd date of download yyyy-mm-dd")
parser.add_argument("end_date", help="end date of download yyyy-mm-dd")
parser.add_argument("path", help="path to store data /path/")
parser.add_argument("-hem", type=str, default='NH', help="NH for northern hemisphere or SH for southern hemisphere")
args = parser.parse_args()

start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
date = start_date

if args.hem == 'SH':
    hem = 30
    name = 'antarctic'
else:
    hem = 26
    name = 'arctic'

while date <= end_date:
    download_usnic_data(date, name, args.path)
    date += timedelta(1)
