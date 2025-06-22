# Code to generate region files of the source and background while also making the pictures

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd



startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==4:
    choice1=sys.argv[1]
    choice2=sys.argv[2]

    if choice1 == "Y" or choice1 == "y":
        choice1 = "y"
    else:
        choice1 = "n"
    if choice2 == "Y" or choice2 == "y":
        choice2 = "y"
    else:
        choice2 = "n"

    specpath=sys.argv[3]
else:
    choice1 = input("Overwrite region files? [y/n]: ")

    if choice1 == "Y" or choice1 == "y":
        choice1 = "y"
    else:
        choice1 = "n"

    choice2 = input("Overwrite jpeg files? [y/n]: ")

    if choice2 == "Y" or choice2 == "y":
        choice2 = "y"
    else:
        choice2 = "n"

    os.system("ls -d */")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
print(totpath)
os.chdir(totpath)

overlap_df = pd.read_csv("det_overlap_sosta.csv")

FGL_names = (overlap_df["4FGL"].drop_duplicates()).to_numpy()

for FGL_name in FGL_names:
    os.chdir(totpath)
    if FGL_name[:4] == "4FGL" or FGL_name[1:4] == "FGL":
        fgl = True
        name = FGL_name[5:]
    else:
        fgl = False
        name = FGL_name
    
    os.chdir(name)

    targets_df = overlap_df.loc[overlap_df["4FGL"]==FGL_name]

    ra = (targets_df.RA).to_numpy()
    dec = (targets_df.Dec).to_numpy()

    if len(ra) != len(dec):
        raise ValueError("Something is wrong with the coordinates. len(RA) != len(Dec)")
    elif len(ra) == 0:
        raise ValueError("Failed to grab coordinates.")
    else: pass

    if choice1 == "n" and os.path.isfile("src0.reg"):
        print("Skipping code for",name)
        pass
    else:
        print("Running code for",name)
        for i,r in enumerate(ra):
            src_name = "src"+str(i)+".reg"
            back_name = "back"+str(i)+".reg"


            outputfile = open(src_name,"w")

            coordinates = str(r)+","+str(dec[i])

            outputfile.write("# Region file format: DS9 version 4.1\n")
            outputfile.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
            outputfile.write("fk5\n")
            outputfile.write('annulus('+coordinates+',0",20")\n')
            outputfile.close()

            outputfile = open(back_name,"w")

            outputfile.write("# Region file format: DS9 version 4.1\n")
            outputfile.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
            outputfile.write("fk5\n")
            outputfile.write('annulus('+coordinates+',50",150") # text={'+str(i)+'}\n')
            outputfile.close()
    max_i = len(ra)

    if choice2 == "n" and os.path.isfile("total.jpeg"):
        pass
    else:
        cmd_str = "/Applications/SAOImageDS9.app/Contents/MacOS/ds9 total.fits -log "
        #cmd_str = "/usr/local/ds9/ds9 total.fits -log "

        for i in range(max_i):
            cmd_str += "-region src"+str(i)+".reg -region back"+str(i)+".reg "
        # if os.path.isfile("../../All4FGL.reg"):
        #     cmd_str += "-region ../../All4FGL.reg -zoom out -saveimage total.jpeg -quit"
        # else:
        if os.path.isfile("4FGL_coords.csv"):
            openfile = open("4FGL_coords.csv")
            openlines = openfile.readlines()
            openfile.close()

            for line in openlines:
                data = line.split(",")
                ra = str(data[0])
                dec = str(float(data[1]))
            
        else:
            openfile = open("src0.reg")
            openlines = openfile.readlines()
            openfile.close()

            for line in openlines:
                if "annulus" in line:
                    data = line.split(",")
                    ra = str(data[0][8:])
                    dec = str(float(data[1]))
        
        cmd_str += "-pan to "+ra+" "+dec+" wcs fk5 "

        if fgl:
            cmd_str += "-region ../../All4FGL.reg -saveimage total.jpeg -quit"
        else:
            cmd_str += "-zoom out -saveimage total.jpeg -quit"
        

        # print(cmd_str)

        os.system(cmd_str)

        if os.path.isdir("../jpeg_dir"):
            pass
        else:
            print("Making directory jpeg_dir")
            os.system("mkdir ../jpeg_dir")
        os.system("cp total.jpeg ../jpeg_dir/"+name+".jpeg")


    


