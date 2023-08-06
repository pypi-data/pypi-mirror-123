import argparse
import lsdnumbatools as lsdnb
import numpy as np


def flip_raster():
	parser = argparse.ArgumentParser()
	parser.add_argument("fname", help="path + file name", type = str)
	parser.add_argument("-d", "--direction", help="Direction of the flipping", type = str, default = 'x')
	parser.add_argument("-o", "--output", help="name of the output", type = str, default = 'flipped_raster.tif')
	args = parser.parse_args()

	dem = lsdnb.DEM()

	dem.load_main_raster(fname = args.fname, nodata_method = "closed")

	dem.ds["topography"].values = np.flip(dem.ds["topography"].values, axis = 0) if args.direction == 'x' else np.flip(dem.ds["topography"].values, axis = 1)

	dem.save_raster("topography", dem.ds["crs"].item(0), args.output, fmt = 'GTIFF')