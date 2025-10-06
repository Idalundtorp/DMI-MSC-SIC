import copernicusmarine
import sys
import os

#copernicusmarine.login()

year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]
print(f"{year}-{month}-{day}T00:00:00")

path1 = sys.argv[4]  # BALTIC_SST_BASEPATH
path2 = sys.argv[5]  # BALTIC_SIC_BASEPATH
path3 = sys.argv[6]  # GLB_SST_BASEPATH

# download sst
os.chdir(path1)
copernicusmarine.subset(
  dataset_id="DMI-BALTIC-SST-L4-NRT-OBS_FULL_TIME_SERIE",
  variables=["analysed_sst", "analysis_error", "mask", "sea_ice_fraction"],
  minimum_longitude=-10,
  maximum_longitude=30,
  minimum_latitude=48,
  maximum_latitude=66,
  start_datetime=f"{year}-{month}-{day}T00:00:00",
  end_datetime=f"{year}-{month}-{day}T23:59:59",
)

# download sic
os.chdir(path2)
copernicusmarine.subset(
  dataset_id="FMI-BAL-SEAICE_CONC-L4-NRT-OBS",
  variables=["concentration_range", "ice_concentration", "product_quality"],
  minimum_longitude=9,
  maximum_longitude=31,
  minimum_latitude=53.20000076293945,
  maximum_latitude=66.19999694824219,
  start_datetime=f"{year}-{month}-{day}T00:00:00",
  end_datetime=f"{year}-{month}-{day}T23:59:59",
)

# download GBL SST
os.chdir(path3)

copernicusmarine.subset(
  dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
  variables=["analysed_sst", "analysis_error", "mask", "sea_ice_fraction"],
  minimum_longitude=-179.97500610351562,
  maximum_longitude=179.97500610351562,
  minimum_latitude=-89.9749984741211,
  maximum_latitude=89.9749984741211,
  start_datetime=f"{year}-{month}-{day}T00:00:00",
  end_datetime=f"{year}-{month}-{day}T23:59:59",
)