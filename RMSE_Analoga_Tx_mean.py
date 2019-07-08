import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.signal import detrend
from eofs.xarray import Eof
import iris
from eofs.multivariate.iris import MultivariateEof
import iris.quickplot as qplt
from tempfile import TemporaryFile
import time
import gc
import os

home_path = '/home/srvx11/lehre/users/a1656041/ipython/Klima1'
variable_mslp = ["PRMSL_GDS0_MSL","mslp"]
variable_rh = ["RH_GDS0_ISBL","rh"]
variable_spfh = ["SPFH_GDS0_ISBL","spfh"]
df_ano = xr.open_mfdataset(home_path+'/Anomalien/*.nc',combine='by_coords')
df_ano = df_ano.rename({variable_mslp[0]:variable_mslp[1],variable_rh[0]:variable_rh[1],variable_spfh[0]:variable_spfh[1]})
df_ano = df_ano.chunk({'time':2000,'lat':29,'lon':29})
print(df_ano)

ds_analoga = xr.open_mfdataset(home_path+'/Analog_Method/Analoga_ranked_pro_TD.nc',combine='by_coords')
ds_analoga = ds_analoga.sel(TD = ds_analoga.TD.dt.year.isin(np.arange(1961,2018,1)))
print(ds_analoga)

First_Analoga_serie = ds_analoga.analoga_dates[:,0]

ds_sparta = xr.open_mfdataset(home_path+'/Analog_Method/Spartacus/Tx/*.nc',combine='by_coords')
ds_sparta = ds_sparta.sel(time=~((ds_sparta.time.dt.month == 2) & (ds_sparta.time.dt.day == 29)))
print(ds_sparta.Tx_area_mean)

forecasts = []
observations = []

i=0
for d in ds_analoga.TD:
    #print(d.values)
    Analoga = ds_analoga.analoga_dates.loc[d.values,:][0]
    #print(Analoga.values)
    forecast = ds_sparta.Tx_area_mean.sel(time = ds_sparta.time.isin(Analoga))
    observation = ds_sparta.Tx_area_mean.sel(time = ds_sparta.time.isin(d))
    
    #print(forecast)
    #print(observation)
    
    forecasts += [forecast.values]
    observations += [observation.values]
    i += 1
    #if i == 5: break

print(forecasts-observations)    

plt.plot(ds_analoga.TD, forecasts)
plt.plot(ds_analoga.TD, observations)
plt.show()