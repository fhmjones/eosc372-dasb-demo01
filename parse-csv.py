# To generate the location list from data files
# The result will be hand-edited so that the map has only one dataset at each location

import glob 

# open a text file to overwrite any previous version
# add headers to this file.
writefile = open("data/latlong-list.csv", "w")
writefile.write("filename,date,locn,drop,lat,long\n")

# parse all data files to build a text file listing filenames and locations. 
for csvfile in glob.glob('data/*.csv'):
    with open (csvfile, 'rt') as myfile:  # Open for reading
        for myline in myfile:             # For each line, read to a string, find lat/long
            if myline.find("LATITUDE = ") == 0: 
                lat = float(myline[10:])
            if myline.find("LONGITUDE = ") == 0: 
                lon = float(myline[11:])
                # write out the file name, date, location #, drop # from the file name
                # add latitude and longitude to the string.
                # assumes latitude is before longitude in all files (true for these data)                
                str2 = myfile.name[5:]+","+csvfile[9:17]+","+csvfile[18:23]+","+csvfile[24:29]+","+str(lat)+","+str(lon)+'\n'
                writefile.write(str2)
writefile.close()

# After building this file of locations, drops, and corresponding data files,
# the list was edited by hand to reduce to one sounding only at each location. 
# The reason for this is to ensure students are not confused by multiple data
# sets at each location on the map. 