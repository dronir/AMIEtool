#!/usr/bin/python
# coding: UTF-8

from sys import exit

def getAreas(filename):
	"""Get list of areas from file as list of tuples of floats (lon_min, lon_max, lat_min, lat_max)."""
	areas = []
	try: 
		f = file(filename)
	except IOError:
		print "Error opening file %s!" % (filename)
		exit()
	for line in f:
		areas.append(tuple(map(float, line.split())))
	return areas

def checkCoordinates(lon, lat, area):
	"""Check whether given lon and lat are within limits given in tuple."""
	if lon >= area[0] and lon <= area[1] and lat >= area[2] and lat <= area[3]:
		return True
	else:
		return False

def checkAreas(lon, lat, areas=None):
	"""Given list of areas, return True if point is in any of them."""
	if areas == None:
		return False
	else:
		return reduce(lambda x,y: x or y, [checkCoordinates(lon, lat, area) for area in areas])

def printList(filters=[], areas=None):
	"""Given list of filter numbers and list of areas, print paths to all AMIE images in those areas.
	
	'areas' must be a list of tuples (lon_min, lon_max, lat_min, lat_max).
	'filters' must be a list containing numbers between 1 and 8, corresponding to the different AMIE filters.
	
	Both parameters, 'filters' and 'areas' are optional. 
	1. If filters is given and areas is not, the code prints all AMIE images from those filters 
	(anywhere on the surface). 
	2. If areas is given and filters not, print images from all filters in those regions.
	3. If neither is given, print list of all AMIE images."""

	ftp_path_base = "ftp://anonymous@psa.esac.esa.int/pub/mirror/SMALL-MISSIONS-FOR-ADVANCED-RESEARCH-AND-TECHNOLOGY/AMIE/S1-L-X-AMIE-3-RDR-%s-V1.0/DATA"
	filename_base = "GEO_MOON_%s.TAB"

	for phase in ["LP", "EP"]:
		filename = filename_base % phase
		ftp_path = ftp_path_base % phase
		try:
			f = file(filename)
		except IOError:
			print "Error reading file %s!" % (filename)
			exit()
		for line in f:
			line = line.split(",")
			filter_no = int(line[4])
			if filters and not filter_no in filters: # No need to go on
				continue
			# Get filename, centre latitude and longitude, then
			# print file path if lat/lon in given areas.
			filename = line[0].strip('".')
			cent_lon = float(line[10])
			cent_lat = float(line[15])
			timestamp = line[1]
			orbit = line[2]
			image = line[3]
			if checkAreas(cent_lon, cent_lat, areas):
				print ftp_path + filename
				


if __name__=="__main__":
	from optparse import OptionParser
	from sys import argv
	import os
	
	descr_msg = "Return list of AMIE images from desired filters with coordinates in areas given in a file."
	usage_msg = "%prog [options] filename"
	
	commandline = OptionParser(usage=usage_msg, description=descr_msg)
	commandline.add_option("-f", "--filters", type="string", dest="filterstring",
	                       action="store", metavar="STRING", 
	                       help="Limit to given string of filters (see README).")

	options, args = commandline.parse_args()
	
	if len(args) != 1:
		print "Usage:", "%s [options] filename" % (os.path.basename(argv[0]))
 		print "Use option -h or --help for help message."
		exit()
	
	filename = args[0]
	
	if options.filterstring:
		filters = map(int, list(options.filterstring))
	else:
		filters = []

	areas = getAreas(filename)
	printList(filters, areas)