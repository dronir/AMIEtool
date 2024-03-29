#!/usr/bin/python
# coding: UTF-8

# Tool for plotting lunar areas from a file generated by pickpoints.py

from matplotlib import pyplot as plot

if __name__=="__main__":
	from sys import argv, exit
	moonmap = plot.imread("Moonmap_from_clementine_data.png")
	plot.subplots_adjust(left=0.04, right=0.96, bottom=0.04, top=0.96)
	plot.axis([-180, 180, -90, 90])
	plot.grid()
	plot.yticks(range(-90, 90, 10))
	plot.xticks(range(-180, 180, 10), rotation="90")
	plot.imshow(moonmap, interpolation=None, extent=[-180, 180, -90, 90])
#	plot.plot([0, 0], [-90, 90], c='red')

	if len(argv) != 2:
		exit()
	try: 
		f = file(argv[1])
	except IOError:
		print "Error opening file %s!" % (filename)
		exit()	
	
	N = 0
	for line in f:
		N += 1
		x1, x2, y1, y2 = map(float, line.split())
		# Correct for AMIE coordinates
		x1 = (x1 - 360)
		x2 = (x2 - 360)
		if x1 < -180: x1 += 360
		if x2 < -180: x2 += 360

		#plot.fill_between([x1, x2], [y1, y1], [y2, y2], color="red", alpha=0.2)
		plot.plot([x1,x1,x2,x2,x1], [y1,y2,y2,y1,y1], color="red")
	plot.title("Plotting %d areas from %s" % (N, argv[1]))
	plot.show()
	
	