import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy import time as t
from astroquery.heasarc import Heasarc
import pandas as pd
import os

#Read a file in. The file should have object names, RAs, and DECs

filename = 'SwXFcoords.csv'

startpath = os.getcwd()+"/"

if os.path.isfile(filename):
    totpath = startpath
    filename = totpath+filename
else:
    os.system("ls -d */")

    specpath=input("Which directory is "+filename+" in?: ")
    totpath=startpath+specpath
    os.chdir(totpath)

    for dirpath, dirnames, filenames in os.walk(totpath):
        os.chdir(dirpath)
        if os.path.isfile(filename):
            totpath = dirpath+"/"
            filename = totpath+filename
            break

database=pd.read_csv(filename,delimiter=',',header=0)

#Setting up HEASARC query interface.
heasarc = Heasarc()
mission = 'swiftxrlog'

telescope = input("Which telescope? [XRT/UVOT/both] ")

radius = input("What search radius in arcmin? ")
try:
    radius = float(radius)
    if radius == 0:
        radius = 10
except:
    print(radius,"was not accepted as a float. Defaulting to 10'.")
    radius = 10
if telescope.upper() == "XRT":
    telescope = "xrt"
elif telescope.upper() == "UVOT":
    telescope = 'uvot'
else:
    telescope = "both"
#Counters
Empty=0
Full=0
duration=[]

#Opening a txt file to write WGET queries
querylist=open("HEASqueries.txt",'w')
matchlist=open('4FGLmatch.txt','w')

print("Running query now:")

obs_list = []

for i in range(0,len(database)):
    
    #Read in the RA and DEC of each object. Should be in format understandable to astropy.Skycoords
    RA=(database['RA'].values)[i]
    DEC=(database['Dec'].values)[i]
    name=(database['Name'].values)[i]
    print((database['Name'].values)[i],RA,DEC)

    coords = SkyCoord(RA,DEC, equinox = 'J2000', frame='fk5', unit=(u.deg,u.deg))
    #astroquery.heasarc returns an error if no data is found for the query, so test to see if there's
    #   an error after sending the query. If there is no error, take the results into a table.
    
    #Be sure to change the "radius" parameter to the search radius you want!
    try:
        table = heasarc.query_region(coords, catalog=mission, radius=radius*u.arcminute)
        # table = heasarc.query_region(coords, mission=mission, radius=10*u.arcminute)

        Full += 1
    except (ValueError,TypeError):
        print("ValueError or TypeError!")
        Empty += 1
        continue
    
    try:
        obsinfo=np.asarray(table)
    except (ValueError,TypeError,AttributeError):
        print("something awful happened")
        continue
    
    #Write the WGET query to download the results
    batchquery=[]
    obsdur=0
    # print(obsinfo)
    for j in range(0,len(obsinfo)):
        try:
            float(obsinfo[j][1])
            obsID=str((obsinfo[j][1]))
        except:
            obsID=str((obsinfo[j][1]))[2:13]
        
        #writing obsID into match file
        matchlist.write(name+','+obsID+'\n')

        #The table has time of observation in MJD, need to convert to YYYY-MM for query
        time=t.Time(obsinfo[j][4],format='mjd')
        time.format='fits'
        year=(time.value[0:4])
        month=(time.value[5:7])
        #We only want PC mode. Remove this if you want WT mode as well
        if (obsinfo[j][7]==b'PHOTON        '):
            obsdur+=obsinfo[j][5]
        #Need to get observation ID number, stripped of all the useless stuff that piles up.
        try:
            obsID=str((obsinfo[j][1]))
            float(obsID)
        except:
            obsID=str((obsinfo[j][1]))[2:13]
            
        obs_list.append(obsID)
        finstring=year+"_"+month+"/"+obsID    
        firststring="wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/"
        #Create queries for auxil and xrt datasets.
        for i in range(2):
            if i == 0 and (telescope=="xrt" or telescope=="both"):
                query = firststring+finstring+"/auxil/"
                batchquery=np.append(batchquery,query)

                query = firststring+finstring+"/xrt/"
                batchquery=np.append(batchquery,query)
                # batchquery=np.append(batchquery,query)
            elif i == 1 and (telescope=="uvot" or telescope=="both"):
                query = firststring+finstring+"/uvot/"
                batchquery=np.append(batchquery,query)
            elif i > 1:
                break

            
        # query0=firststring+finstring+"/auxil/"
        # query1=firststring+finstring+"/xrt/"
        # query2=firststring+finstring+"/uvot/"

        # # batchquery=np.append(batchquery,query0)
        # # batchquery=np.append(batchquery,query1)
        # batchquery=np.append(batchquery,query2)
    duration=np.append(duration,obsdur)
    #Make sure no queries are repeated.
    uniquer=np.unique(batchquery)
    #Write queries to .txt file. The queries can be run however you like.
    for k in range(0,len(uniquer)):
        querylist.write(uniquer[k]+'\n')
    
# uniqueID=np.unique(obs_list)
outfile = open("obsID.csv","w")
for ID in obs_list:
    outfile.write(str(ID)+"\n")
outfile.close()

querylist.close()
matchlist.close()