import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import Dataset
from wrf import getvar

import metpy
import metpy.calc as mpcalc
from metpy.plots import Hodograph, SkewT
from metpy.units import units

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import inset_axes

#===============function==================
def sel_nearest_loc(lat, lon, data_lat, data_lon, data):
    '''
    * lat, lon (float) - required lat/lon

    * data_lat, data_lon (xarray) - data lat/lon

    * data (xarray) - data which is nearest at required lat/lon
    '''

    abslat = np.sqrt(np.square(data_lat - lat))
    abslon = np.sqrt(np.square(data_lon - lon))
    c = np.maximum(abslat, abslon)
    
    ([xloc],[yloc]) = np.where(c == np.min(c))
    
    nearest = data.sel(south_north = yloc, west_east = xloc)
    return nearest

#=================Data=====================
dire = '/home/ubuntu/Build_WRF/WRF/run/{}'
file = dire.format('wrfout_d02_2020-12-25_00:00:00')
data = Dataset(file)

tt = -1

data_lat = getvar(data, 'lat')
data_lon = getvar(data, 'lon')

lat = 37.67713 #37.80456 #choose lat
lon = 128.71834 #128.85535 #choose lon

p = getvar(data, 'pressure', timeidx = tt)
temp = getvar(data, 'tc', timeidx = tt)
dewp = getvar(data, 'td', timeidx = tt)
u = getvar(data, 'ua', timeidx = tt)
v = getvar(data, 'va', timeidx = tt)

p = sel_nearest_loc(lat, lon, data_lat, data_lon, p)
t = sel_nearest_loc(lat, lon, data_lat, data_lon, temp)
td = sel_nearest_loc(lat, lon, data_lat, data_lon, dewp)
u = sel_nearest_loc(lat, lon, data_lat, data_lon, u)
v = sel_nearest_loc(lat, lon, data_lat, data_lon, v)

values = [p, t, td, u, v]
u = units.Quantity(u.values, 'm/s')
v = units.Quantity(v.values, 'm/s')
p = units.Quantity(p.values, 'hPa')
t = units.Quantity(t.values, 'degC')
td= units.Quantity(td.values, 'degC')

fig = plt.figure(figsize = (15, 15))
skew = SkewT(fig)

skew.plot(p, t, 'r', linewidth = 2)
skew.plot(p, td, 'g', linewidth = 2)
skew.plot_barbs(p, u, v, xloc = 1)

skew.ax.set_xlim(-60, 40)
skew.ax.set_ylim(1000, 100)

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

skew.ax.tick_params(axis = 'both', which = 'major', labelsize = 15)
skew.ax.set_xlabel('')
skew.ax.set_ylabel('')
#cape_cin
#prof = mpcalc.parcel_profile(p, t[0], td[0]).to('degC')
#skew.plot(p, prof, 'k', linewidth = 2)
#skew.shade_cape(p, t, prof)


lat = values[0].XLAT.values
lon = values[0].XLONG.values
utc = str(values[0].Time.values)[:-10]
skew.ax.set_title('LAT : {:.5} | LON : {:.5}\n{}'.format(lat, lon, utc), fontsize = 20)


#hodograph
ax_hod = inset_axes(skew.ax, '40%','40%', loc = 1)
h = Hodograph(ax_hod, component_range=80.)
h.add_grid(increment=20)
h.plot_colormapped(u, v, metpy.calc.wind_speed(u, v))

plt.show()
plt.savefig(f'./SkewT_{utc}', bbox_inches = 'tight')
