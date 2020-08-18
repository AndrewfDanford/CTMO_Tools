import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from astropy.visualization import make_lupton_rgb

##############################################################################
# Save fits file names

g_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/M16/M16_300_g.fit'
r_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/M16/M16_300_r.fit'
i_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/M16/M16_300_i.fit'
'''
g_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/GRB_200711A/60/GRB200711-001_g.fit'
r_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/GRB_200711A/60/GRB200711-001_r.fit'
i_name = '/Users/mrd/Documents/CTMO/data/2020-08-06/lights/GRB_200711A/60/GRB200711-001_i.fit'
'''

##############################################################################
# get data from fits file
g = fits.open(g_name)[0].data
r = fits.open(r_name)[0].data
i = fits.open(i_name)[0].data

print(fits.open(g_name))


##############################################################################
# stack filters 
# must use dstack
# need array as MxNx3 not 3xMxN

rgb = np.dstack((		r.astype(np.uint8),	
						g.astype(np.uint8),
						i.astype(np.uint8)
						))		


##############################################################################					
# plot the stacked array
plt.imshow(rgb, origin='lower')
plt.title('M16 \n 300s exposure \n Aug 6 2020')
plt.savefig('M16_false_color.jpeg',dpi=800)
plt.show()



##############################################################################
# make lupton rgb
rgb_default = make_lupton_rgb(	i.astype(np.float), 
								r.astype(np.float), 
								g.astype(np.float),
								Q=0.01,
								stretch=5000, 
								filename="M16_true_color.jpeg")


##############################################################################
# plot lupton rgb
plt.imshow(rgb_default, origin='lower')
plt.show()

#[1400:2100,2000:2800] for pillars
#[900:3000,1250:3200] for whole nebula







