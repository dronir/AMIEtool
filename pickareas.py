#!/usr/bin/python
# coding: UTF-8

# Program for choosing areas on the lunar surface to use in
# selecting SMART-1/AMIE images with listImages.py

# The script requires the following image in the same directory:
# http://commons.wikimedia.org/wiki/File:Moonmap_from_clementine_data.png

from matplotlib import pyplot as plot
from math import floor

global start_x, start_y, hold, areas
hold = False
areas = []

def AMIEcoord(x, y):
	"""Transform image coordinates to AMIE coordinates.
	This means longitude ranges between [0, 360] instead of [-180, 180]."""
	lat = y
	lon = (x + 360) % 360
	return (lon, lat)

def click(event):
	"""On mouse click either start or end area selection.
	
	If global variable 'hold' is False, start a new area, mark it with a point.
	If 'hold' is True, end area, save the area to global list 'areas',
	and draw the selection box on the map. """
	
	global start_x, start_y, hold, areas
	if event.inaxes:
		x = event.xdata
		y = event.ydata
		if hold:
			# End selection, save coordinates and draw
			plot.title("Click for new starting point or close window to write file.")
			print "End area at (%.2f, %.2f)." % (x, y)
			hold = False
			plot.plot([start_x, x, x, start_x, start_x], [start_y, start_y, y, y, start_y], c="red")
			plot.plot(x,y, ".", c="red")
			x1, y1 = AMIEcoord(start_x, start_y)
			x2, y2 = AMIEcoord(x, y)
			x1, x2 = sorted([x1, x2])
			y1, y2 = sorted([y1, y2])
			areas.append((x1, x2, y1, y2))
		else:
			# Start making a selection
			print "Start area at (%.2f, %.2f)." % (x, y)
			plot.title("Click for new end point.")
			plot.plot(x,y, ".", c="red")
			hold = True
			start_x = x
			start_y = y
		
if __name__=="__main__":
	# Handle command line arguments:
	from sys import argv, exit
	if len(argv) == 2:
		# For one argument, use it as output filename, overwriting
		outfile = argv[1]
		mode = 'w'
	elif len(argv) == 3 and argv[1] == "-a":
		# For two arguments, if the first is '-a', use second as
		# filename and append.
		outfile = argv[2]
		mode = "a"
	else:
		# With bad command line, print usage message and exit.
		print "Usage: %s [-a] outputfile" % (argv[0])
		exit()
	
	# Set up plot window and connect 'click' function to mouse click event.
	moonmap = plot.imread("Moonmap_from_clementine_data.png")
	plot.connect("button_press_event", click)
	plot.title("Click for new area starting point. Note: do not make areas that span across the red line.")
	plot.subplots_adjust(left=0.04, right=0.98, bottom=0.04, top=0.98)
	plot.axis([-180, 180, -90, 90])
	plot.grid()
	plot.yticks(range(-90, 90, 10))
	plot.xticks(range(-180, 180, 10), range(180,359,10)+range(0,180,10), rotation="90")
	plot.imshow(moonmap, interpolation=None, extent=[-180, 180, -90, 90])
	plot.plot([0, 0], [-90, 90], c='red')
	plot.show()
	# Program waits at this point until plot window is closed.
	# Then write areas:
	if areas:
		action = {"a":"Added", "w":"Wrote"}
		try:
			f = open(outfile, mode)
		except IOError:
			print "Error writing file %s!" % (outfile)
			exit()
		for area in areas:
			f.write("%.2f\t%.2f\t%.2f\t%.2f\n" % area)
		print "%s %d areas to %s." % (action[mode], len(areas), outfile)
	else:
		action = {"a":"changed", "w":"created"}
		print "No areas were selected. Output file not %s." % (action[mode])