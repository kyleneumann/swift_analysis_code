# Code to generate region files of the source and background while also making the pictures

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

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
    print(20*"%")
    print("This code will generate source and background regions \n" \
        "around significant sources from the det_overlap table. \n" \
        "If you change the det_overlap file between runs of \n" \
        "region_gen, make sure to turn overwrite on as the order \n" \
        "of sources may have changed.")
    print(20*"%","\n")

    choice1 = input("Overwrite region files? [y/n]: ")

    if choice1 == "Y" or choice1 == "y":
        choice1 = "y"
    else:
        choice1 = "n"

    choice2 = input("Overwrite png files? [y/n]: ")

    if choice2 == "Y" or choice2 == "y":
        choice2 = "y"
    else:
        choice2 = "n"

    os.system("ls -d */")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
print(totpath)
os.chdir(totpath)

overlap_df = pd.read_csv("det_overlap.csv")

if os.path.isfile("input_sources.csv"):
    df = pd.read_csv("input_sources.csv")
elif os.path.isfile(startpath+"input_sources.csv"):
    df = pd.read_csv(startpath+"input_sources.csv")
else:
    df = pd.DataFrame([])

overlap_ls = []

SRC_names = (overlap_df["SRC"].drop_duplicates()).to_numpy()

for src in SRC_names:
    os.chdir(totpath)
    
    if "FGL" in src:
        fgl = True
        name = src[1:].replace("FGL","")
    else:
        fgl = False
        name = src
    
    os.chdir(name)

    if "old_ignore" in os.getcwd() or os.path.isfile("skip.txt"):
        continue

    print(f"Working on {name}")

    targets_df = overlap_df.loc[overlap_df["SRC"]==src].sort_values(by="index",ignore_index=True).set_index("index")
    det_df = pd.read_csv("detinfo.csv")

    ra = (targets_df.RA).to_numpy()
    dec = (targets_df.Dec).to_numpy()
    n_src = len(ra)
    i_ls = []

    if len(ra) != len(dec):
        raise ValueError("Something is wrong with the coordinates. len(RA) != len(Dec)")
    elif len(ra) == 0:
        raise ValueError("Failed to grab coordinates.")
    else: pass

    # if choice1 == "n" and os.path.isfile("src0.reg"):
    #     print("Skipping code for",name)
    #     pass
    # else:
    # print("Running code for",name)
    if choice1 == "y":
        os.system("rm src?.reg")
        os.system("rm back?.reg")
        if n_src > 10:
            os.system("rm src??.reg")
            os.system("rm back??.reg")
    for i in targets_df.index:
        SwXF = targets_df.loc[i,"SwXF"]
        src_name = "src"+str(i)+".reg"
        back_name = "back"+str(i)+".reg"

        i_ls.append(i)

        if os.path.isfile(src_name): continue

        outputfile = open(src_name,"w")

        coordinates = f"{ra[i]},{dec[i]}"
        c0 = SkyCoord(coordinates.replace(","," "),unit=[u.deg,u.deg],frame="fk5")

        outputfile.write("# Region file format: DS9 version 4.1\n")
        outputfile.write('global color=magenta dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
        outputfile.write("fk5\n")
        outputfile.write('annulus('+coordinates+',0",20")\n')
        outputfile.close()

        outputfile = open(back_name,"w")

        outputfile.write("# Region file format: DS9 version 4.1\n")
        outputfile.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
        outputfile.write("fk5\n")
        outputfile.write(f'annulus({coordinates},50",150") # text="{SwXF}"\n')
        outputfile.close()

        for j in det_df.index:
            if SwXF == det_df.loc[j,"SwXF"]: continue
            c1 = SkyCoord(det_df.loc[j,"RA"],det_df.loc[j,"Dec"],unit=[u.deg,u.deg],frame="fk5")

            sep = c1.separation(c0).arcsec

            if sep > 40 and sep < 160: 
                overlap_ls.append(f"{src}/src{i}")
                break

    # max_i = len(ra)

    if choice2 == "n" and os.path.isfile("total.jpeg"):
        pass
    else:
        cmd_str = "/Applications/SAOImageDS9.app/Contents/MacOS/ds9 total.fits -log "
        #cmd_str = "/usr/local/ds9/ds9 total.fits -log "

        for i in i_ls:
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
        try:
            if len(df.loc[df.src==name]) > 0: 
                ra = df.loc[df.src==name].RA.values[0]
                dec = df.loc[df.src==name].Dec.values[0]

                major = df.loc[df.src==name].major.values[0]
                minor = df.loc[df.src==name].minor.values[0]
                ang = df.loc[df.src==name].ang.values[0]
                if os.path.isfile("SRC.reg"): 
                    pass
                else:
                    openfile = open("SRC.reg","w")
                    openfile.write("# Region file format: DS9 version 4.1\n")
                    openfile.write('global color=cyan dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
                    openfile.write("fk5\n")
                    openfile.write(f'ellipse({ra},{dec},{major},{minor},{ang}) # text="{name}"\n')
                    openfile.close()

                if major*3600 < 150:
                    cmd_str += "-zoom 3.6 "
                elif major*3600 < 200:
                    cmd_str += "-zoom 2.2 "
                elif major*3600 < 250:
                    cmd_str += "-zoom 1.5 "
                elif major*3600 > 550:
                    cmd_str += "-zoom 0.8 "

                cmd_str += "-region SRC.reg "

            else: break
            
        except:
            openfile = open("src0.reg")
            openlines = openfile.readlines()
            openfile.close()

            for line in openlines:
                if "annulus" in line:
                    data = line.split(",")
                    ra = str(data[0][8:])
                    dec = str(float(data[1]))

        
        cmd_str += f"-pan to {ra} {dec} wcs fk5 -saveimage total.png 100 -quit"

        # if fgl:
        #     cmd_str += "-region ../../All4FGL.reg -saveimage total.jpeg -quit"
        # else:
        #     cmd_str += "-zoom out -saveimage total.jpeg -quit"
        

        # print(cmd_str)

        os.system(cmd_str)

        if os.path.isdir("../png_dir"):
            pass
        else:
            print("Making directory png_dir")
            os.system("mkdir ../png_dir")
        os.system("cp total.png ../png_dir/"+name+".png")

os.chdir(totpath)
if len(overlap_ls) > 0:
    overlap_out = open("src_overlap.txt","w")
    for item in overlap_ls:
        overlap_out.write(f"{item}\n")
    overlap_out.close()
    # overlap_ls


    


