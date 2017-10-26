import matplotlib
matplotlib.use('Agg')
print(matplotlib.__version__)

import cartopy
from cartopy.feature import GSHHSFeature, NaturalEarthFeature
import matplotlib.colors
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
import os
import pandas as pd
import pyproj
import seaborn as sns
import sys
import xarray as xr
EPSG3857 = pyproj.Proj(init='EPSG:3857')

# TODO: use xarray instead
# with xr.open_dataset('/home/dalton/habs_ESPG3857/ci-latest-wgs84.nc') as nc:

ds = xr.open_dataset("/home/dalton/habs_ESPG3857/ci-latest-wgs84.nc")
print(ds)

lon = ds.lon
lat = ds.lat
lon,lat = np.meshgrid(lon, lat)
lo,la = EPSG3857(lon, lat)

#band1 = np.ma.masked_invalid(ds.Band1) # shifting everything up to valid scale
band1 = ds.Band1.values.astype('B')
print("band1 min: ", band1.min(), "band1 max: ", band1.max())
band1 = np.ma.masked_invalid(band1)
print("band1 min: ", band1.min(), "band1 max: ", band1.max())
print("")
#print("Printing band1...")
print("")
print(band1)
print("")
print("band1 min: ", band1.min(), "band1 max: ", band1.max())

# wtf = pd.DataFrame(band1).fillna(value=0)
# for col in wtf.columns:
#     print("Col {} min: ".format(col), wtf[col].min(), "Col {} max: ".format(col), wtf[col].max())
#     sns.kdeplot(wtf[col])


# wtf = np.ndarray.flatten(band1)
# #wtf = np.nan_to_num(wtf)
# print("Min value: ", wtf.min(), "Max value: ", wtf.max())
# sns.distplot(wtf)
# plt.show()
# 
# print(np.histogram(wtf, bins=range(0, 256)))
# #print(np.histogram(wtf, bins=range(-128, 127)))


v = plt.get_cmap("YlGn")  
n = matplotlib.colors.Normalize(vmin=0, vmax=251)

c = [v(n(d)) for d in range(0, 252)]
print(c)

#output

colors = c + [(0., 1., 0., 0.)] + [(.8, .8, .8, 1.)] + [(.8, .8, .8, 1.)] + [(0., 1., 0., 0.)] 

#colors = [(1., 0., 0., 1.)]*252 + [(0., 1., 0., 0.)] + [(.8, .8, .8, 1.)] + [(.8, .8, .8, 1.)] + [(0., 1., 0., 0.)]

h = [matplotlib.colors.to_hex(c, True) for c in colors]
print(h)
print("")
to_pal =  [x.upper() for x in [colr[0]+colr[-2:]+colr[1:7] for colr in h]]
for _ in to_pal:
    print(_)

for i in range(len(to_pal)):
    print("<se:Value>{}</se:Value>".format(to_pal[i]))
    print("<se:Threshold>{}</se:Threshold>".format(i + 1))

my_cmap = matplotlib.colors.ListedColormap(colors)  

# image size/resolution
height = 1024
width = 1024
dpi = 256

fig = plt.figure(dpi=dpi, facecolor='none', edgecolor='none')
fig.set_alpha(0)
fig.set_figheight(height/dpi)
fig.set_figwidth(width/dpi)
ax = fig.add_axes([0., 0., 1., 1.], xticks=[], yticks=[], projection=cartopy.crs.GOOGLE_MERCATOR)
ax.outline_patch.set_visible(False)

# coastline/states
coastline = NaturalEarthFeature(category='physical', name='coastline', scale='10m', facecolor='none', edgecolor='silver',  linewidth=0.6)
states = NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines', scale='10m', facecolor='none', edgecolor='dimgrey', linewidth=0.4)
lakes = NaturalEarthFeature(category='physical', name='lakes', scale='10m', facecolor='none', edgecolor='silver',  linewidth=0.6)
ax.add_feature(coastline)
ax.add_feature(states)
ax.add_feature(lakes)

ax.set_axis_off()
ax.set_frame_on(False)
ax.set_clip_on(False)
ax.set_position([0, 0, 1, 1])

# color scale
cmin = 0.0
cmax = 255.0
nlvls = 255
lvls = np.linspace(cmin, cmax, nlvls)

# -- plot speed - pcolor
# when using this call signature, pcolor(X, Y, C, **kwargs), ideally the dims of X and Y should be one greater than C, otherwise the last row/col of C is ignored
pcolor = ax.pcolormesh(lo, la, band1, cmap=my_cmap)

# remove some plot stuff
ax.set_frame_on(False)
ax.set_clip_on(False)
ax.set_position([0, 0, 1, 1])

ax.set_xlim(lo.min(), lo.max())
ax.set_ylim(la.min(), la.max())
filename = 'band1_test.png'
fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.0, transparent=True)

plt.close(fig)
