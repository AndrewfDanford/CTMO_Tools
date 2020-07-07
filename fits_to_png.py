from astropy.io import fits
import png
import aplpy
import glob

for file in glob.glob('data/2019-07-09/vr_boo/*.fit'):

	image_file = file
	fits.info(image_file)
	image_data = fits.getdata(image_file, ext=0)

	fig = aplpy.FITSFigure(image_data)
	fig.show_grayscale()
	fig.add_colorbar()

	fig.savefig('images/'+file.split('/')[-1]+'.png')
	fig.close()
	print('image saved')
