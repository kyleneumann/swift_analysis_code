
import os as os
from astropy.io import fits
import numpy as np
import pandas as pd

startpath=os.getcwd()+"/"
os.chdir(startpath)

filename = "xrt_table_master.csv"

df = pd.read_csv(filename)

dir_list = df["Directory"].to_list()
target_list = df["4FGL"].to_list()
swxf_list = df["SwXF4-DR4"].to_list()
ra_arr = df["RA"].to_numpy()
dec_arr = df["Dec"].to_numpy()
ind_arr = df["index"].to_numpy(dtype=int)

outfile = open(startpath+"err_rad.csv","w")
outfile.write("SwXF,err_rad\n")

for i,target in enumerate(target_list):
    dirpath = startpath+dir_list[i]
    ra = ra_arr[i]
    dec = dec_arr[i]
    index = ind_arr[i]
    name = swxf_list[i]
    
    os.chdir(dirpath+"/"+target)

    print("Calculating centroid for "+name)

    cmd = "xrtcentroid infile=total.fits outfile=centroid"+str(index)+".txt outdir=./ "
    cmd += "calcpos=yes interactive=no boxra="+str(ra)+" boxdec="+str(dec)+" boxradius=0.333 clobber=yes chatter=0"

    os.system(cmd)

    openfile = open("centroid"+str(index)+".txt","r")
    openlines = openfile.readlines()
    openfile.close()

    for line in openlines:
        data = line.split()
        # print(data)

        errad = -1
        if len(data) > 1:
            if data[0] == "Error" and data[1] == "radius":
                errad = str(data[-1])
                break
        
    outfile.write(name+","+errad+"\n")

outfile.close()
