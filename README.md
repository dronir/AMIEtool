
# Requirements


## Python

Python 2.7 is required. The scripts may work with 2.6 but I haven't tested. They do not work with Python 3.

A resonably new version of Matplotlib is required (the scripts were written in early 2011 but may work with older versions). Matplotlib requires NumPy to work.

## Required files

All these files need to be placed in the working directory.

### Lunar map

The area selection script uses a lunar map from Clementine data, which is available on [Wikimedia Commons](http://commons.wikimedia.org/wiki/File:Moonmap_from_clementine_data.png).

### AMIE summary files

To find the images in the given regions, the script requires the files `GEO_MOON_LP.TAB` and `GEO_MOON_EP.TAB` which are found in the AMIE data archive.

# Basic procedure

## Picking areas

First pick out the areas you want. Run the area picker tool with the following command:

`python pickareas.py areas.txt`

Here we save the selected areas into the file `areas.txt`. When you run the script, a plot window with a lunar map will appear. You can resize the window if you want it bigger. Click on the map twice to define two opposite corner points of a rectangular area (in latitude and longitude). Repeat to select more areas. When you close the plot window, the areas will be written into the file you specify.

Note: because the longitude coordinate wraps from 0° to 360°, you cannot make areas which extend over the zero meridian. This line is drawn in red in the plot window.

If the output file already exists, it will be overwritten without asking. You can also run the script with the option `-a`, in which case new areas will be appended to an existing file.

## Plotting the areas

You can draw the areas listed in a file by running `python plotareas.py areas.txt`.

## Listing the images

The `listImages.py` program takes areas from the previous script and prints all the ftp paths to relevant AMIE images to standard output. The command 

`python listImages.py areas.txt > imagepaths.txt` 

will print the full ftp paths to every AMIE image which are within any of the areas defined in `areas.txt`, and direct the output to `imagepaths.txt`.

In the archive, a single AMIE exposure is divided into separate files for each of the seven filter regions. By default the script prints the path to all these individual frames. To limit the search to certain filters, you can specify them on the command line like this:

`python listImages.py --filters=234 areas.txt > imagepaths.txt` 

This would show only the images for filters 2, 3 and 4. The numbers must be given as one string with no spaces.

## Downloading images

The `wget` tool can be used to download all images using the paths in a file. To download all the images into the current working directory, simply run 

`wget --input-file=imagepaths.txt --user=username --password=password` 

with the proper username and password for the ftp server.