#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xarray as xr
from datetime import timedelta
import datetime

#from cmocean import cm as cmo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from netCDF4 import Dataset
from scipy.interpolate import RegularGridInterpolator
from scipy.stats import pearsonr
from pyproj import Transformer
import re
import glob
import sys
import os

import numpy as np
from osgeo import gdal, osr, ogr
import sklearn.metrics as skm
import pandas as pd
import xarray as xr
import rioxarray
import datetime as dt

##for debuggin gdal ERROR open .... failed


#print("GDAL Version:", gdal.__version__)
#print("GDAL Data Path:", gdal.GetConfigOption("GDAL_DATA"))
#os.environ["GDAL_DATA"] = "/home/nimo/miniforge3/envs/valsit/share/gdal"
#os.environ["PROJ_LIB"] = "/home/nimo/miniforge3/envs/valsit/share/proj"

# READ INPUTS
if len(sys.argv) != 4:
    print("Usage: python Read_NIC_shapefiles.py START_DATE END_DATE DATAPATH")
    sys.exit(1)

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]
path = sys.argv[3]
# Convert strings to datetime objects
start_date = dt.datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = dt.datetime.strptime(end_date_str, "%Y-%m-%d")

def rasterize_shape_file_nh(shp_name,out_tiff, width=432, height=432, bands=7, dtype=gdal.GDT_Int16,epsg=6931,gtr = (-5400000.,25000,0.0, 5400000., 0.0, -25000)):
    "data soruce"
    dsour = ogr.Open(shp_name)
    layer = dsour.GetLayer() 
    
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(out_tiff, width, height, bands, dtype)
    arr = np.ones((height,width),dtype=np.int16)*(-99)
    spr = osr.SpatialReference()
    spr.ImportFromEPSG(epsg)
    prj =spr.ExportToWkt()
    dataset.SetProjection(prj)
    dataset.SetGeoTransform(gtr)
    #att_list = ["ATTRIBUTE=SA","ATTRIBUTE=SB","ATTRIBUTE=SC","ATTRIBUTE=CT","ATTRIBUTE=CA","ATTRIBUTE=CB","ATTRIBUTE=CC"]
    att_list = [
    #"ATTRIBUTE=ICECODE",
    "ATTRIBUTE=CT",
    "ATTRIBUTE=CA",
    "ATTRIBUTE=CB",
    "ATTRIBUTE=CC",
    "ATTRIBUTE=SA",
    "ATTRIBUTE=SB",
    "ATTRIBUTE=SC",
    "ATTRIBUTE=SO",
    "ATTRIBUTE=SD",
    "ATTRIBUTE=FA",
    "ATTRIBUTE=FB",
    "ATTRIBUTE=FC",
    "ATTRIBUTE=FP",
    "ATTRIBUTE=FS"]
    for i in range(7):
        dataset.GetRasterBand(i+1).WriteArray(arr)
        out = gdal.RasterizeLayer(dataset,[i+1],layer, options=[att_list[i]])
    return out


def list_fields(shapefile_path):
    ds = ogr.Open(shapefile_path)
    layer = ds.GetLayer()
    layer_defn = layer.GetLayerDefn()
    print("Fields in shapefile:")
    for i in range(layer_defn.GetFieldCount()):
        field_name = layer_defn.GetFieldDefn(i).GetName()
        print(f"- {field_name}")

#path = 'NIC_charts/vectors/compressed/arctic100412/ARCTIC100412.shp'
#path = '/net/isilon/ifs/arch/home/sstdev/Projects/CARRA2/original_SIC_data/NIC/shapefiles/ARCTIC250103.shp'
#list_fields(path)
#rasterize_shape_file(path,str(path[-10:-4]+'.tiff'))
#rasterize_shape_file_nh(path,'test.tiff')

def rasterize_to_ease2_12km(
    shp_name, out_tiff, width=864, height=864, bands=7,
    dtype=gdal.GDT_Int16, epsg=6931,
    gtr=(-5400000., 12500, 0.0, 5400000., 0.0, -12500)
):
    dsour = ogr.Open(shp_name)
    layer = dsour.GetLayer()

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(out_tiff, width, height, bands, dtype)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    dataset.SetProjection(srs.ExportToWkt())
    dataset.SetGeoTransform(gtr)

    arr = np.ones((height, width), dtype=np.int16) * -99
    for i in range(bands):
        dataset.GetRasterBand(i+1).WriteArray(arr)

    att_list = [
        #"ICECODE",
        "CT",
        "CA",
        "CB",
        "CC",
        "SA",
        "SB",
        "SC"
    ]

    for i in range(bands):
        layer.ResetReading()
        gdal.RasterizeLayer(dataset, [i+1], layer, options=[f"ATTRIBUTE={att_list[i]}"])

    return out_tiff


def reproject_coords(x_coords, y_coords, src_epsg=6931, dst_epsg=4326):
    transformer = Transformer.from_crs(f"EPSG:{src_epsg}", f"EPSG:{dst_epsg}", always_xy=True)
    lon, lat = transformer.transform(x_coords, y_coords)
    return lon, lat

def geotiff_to_netcdf(tiff_path, netcdf_path):
    ds = gdal.Open(tiff_path)
    #bands_data = [ds.GetRasterBand(i).ReadAsArray() for i in range(1, ds.RasterCount+1)]

    bands_data = [np.flipud(ds.GetRasterBand(i).ReadAsArray()) for i in range(1, ds.RasterCount+1)]  # Flip bands
    gt = ds.GetGeoTransform()
    width = ds.RasterXSize
    height = ds.RasterYSize

    x = np.arange(width) * gt[1] + gt[0] + gt[1]/2
    y = np.arange(height) * gt[5] + gt[3] + gt[5]/2
    xv, yv = np.meshgrid(x, y)
    lon, lat = reproject_coords(xv, yv)
    # Flip lat and lon arrays vertically to match flipped data
    lat = np.flipud(lat)
    lon = np.flipud(lon)

     # Rename dimensions to xc/yc for CDO compatibility
    dims = ("yc", "xc")

    # Build dataset
    ds_xr = xr.Dataset(
        {
            "total_concentration": (dims, bands_data[0]),
            "primary_conc": (dims, bands_data[1]),
            "secondary_conc":   (dims, bands_data[2]),
            "tertiary_conc": (dims, bands_data[3]),
            "primary_stage_of_development_SA":   (dims, bands_data[4]),
            "secondary_stage_of_development_SB":   (dims, bands_data[5]),
            "tertiary_stage_of_development_SC":   (dims, bands_data[6]),
        },
        coords={
            "lat": (dims, lat),
            "lon": (dims, lon),
            "xc": ("xc", x),
            "yc": ("yc", y)
        }
    )

    # Add attributes for lat/lon and xc/yc
    ds_xr['lat'].attrs.update({
        'standard_name': 'latitude',
        'long_name': 'latitude',
        'units': 'degrees_north',
        '_FillValue': np.nan
    })
    ds_xr['lon'].attrs.update({
        'standard_name': 'longitude',
        'long_name': 'longitude',
        'units': 'degrees_east',
        '_FillValue': np.nan
    })
    ds_xr['xc'].attrs.update({
        'standard_name': 'projection_x_coordinate',
        'long_name': 'x coordinate in Cartesian system',
        'units': 'km',
        '_FillValue': np.nan
    })
    ds_xr['yc'].attrs.update({
        'standard_name': 'projection_y_coordinate',
        'long_name': 'y coordinate in Cartesian system',
        'units': 'km',
        '_FillValue': np.nan
    })

    # Add 'coordinates' attribute to all data variables
    for var in ds_xr.data_vars:
        ds_xr[var].attrs['coordinates'] = 'lat lon'
        ds_xr[var] = ds_xr[var].where(ds_xr[var] != -99)  # Mask no-data values

    # Add global attributes
    ds_xr.attrs.update({
        'source': 'National Ice Center Shape',
        'reference': '',
        'hemisphere': 'nh',
        'title': 'Gridded Ice Chart',
        'grid_mapping_name': (
            '+proj=laea +lat_0=90 +lon_0=0 +x_0=0 +y_0=0 '
            '+a=6378137 +rf=298.252840776245 +units=m +no_defs +type=crs'
        ),
        'institution': 'Danish Meteorological Institute',
        'comment': "This gridded ice chart was created by rasterising the ice chart given in the 'source' attribute",
    })

    # Save the NetCDF file
    ds_xr.to_netcdf(netcdf_path, format="NETCDF4")
    return netcdf_path


def extract_date_from_filename(filename):
    base = filename.split('.')[0]
    date_str = base[-6:]  # YYmmdd
    year = "20" + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:6]
    return f"{year}{month}{day}"


shapefiles = [f for f in os.listdir(f'{path}/shapefiles') if f.endswith('shp')]
# Define dates of interest (YYYY-MM-DD) and pick files between start and enddate
filtered_files = [f for f in shapefiles if start_date <= dt.datetime.strptime(f[6:-4], "%y%m%d") <= end_date]

for file in filtered_files:
    date = extract_date_from_filename(file)
    shp_path = f"{path}/shapefiles/arctic{date[2:]}/ARCTIC{date[2:]}.shp"
    tiff_path = "TMP.tiff"
    netcdf_path = f"{path}/{date}_NH_NIC-SHP.nc"
    if os.path.exists(netcdf_path):
        continue
    # # 2. Rasterize using SIG3_CODE
    rasterize_to_ease2_12km(shp_path, tiff_path)

    # # 3. Convert raster to NetCDF
    geotiff_to_netcdf(tiff_path, netcdf_path)


