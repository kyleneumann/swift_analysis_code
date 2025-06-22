# Code to conduct xselect analysis of sources, producing clean region files up to GRPPHA step

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==3:
    choice1=sys.argv[1]
    specpath=sys.argv[2]
else:
    choice1 = input("Overwrite spectrum files? [y/n]: ")

    os.system("ls -d */")
    specpath=input("Enter data directory: ")
    
totpath=startpath+specpath
os.chdir(totpath)
if choice1 == "Y" or choice1 == "y":
    choice1 = "y"
else:
    choice1 = "n"

overlap_df = pd.read_csv("det_overlap_sosta.csv")

FGL_names = (overlap_df["4FGL"].drop_duplicates()).to_numpy()

for FGL_name in FGL_names:
    os.chdir(totpath)
    if FGL_name[:4] == "4FGL" or FGL_name[1:4] == "FGL":
        name = FGL_name[5:]
    else:
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

    if (choice1 == "n" and os.path.isfile("spec0.pi")) or not os.path.isfile("src0.reg"):
        print("Skipping xselect for" ,name," either not saving or no region files")
        continue
    else:
        print("Running xselect for",name)
        # for i,r in enumerate(ra):
        j_end = 0 

        for i in range(100):
            src_name = "src"+str(i)+".reg"
            back_name = "back"+str(i)+".reg"

            if not os.path.isfile(src_name):
                if j_end > 3:
                    break
                else:
                    j_end += 1
                    continue
            
            src_spec_name = "src"+str(i)+".pi"
            back_spec_name = "back"+str(i)+".pi"
            
            arf_name = "arf"+str(i)+".arf"
            rmf_name = "rmf"+str(i)+".rmf"
            
            total_name = "spec"+str(i)+".pi"
            
            openreg = open(src_name,"r")
            openlines = openreg.readlines()
            openreg.close()

            for line in openlines:
                if "annulus" in line:
                    data = line.split(",")
                    thisRA = float(data[0][8:])
                    thisDec = float(data[1])
                        
            #First, make sure the source region does not have too much X-ray flux to cause overlap.
            XselTest="xselect <<EOF\nxsel\n read event\n./\n total.evt \nyes\nfilter region "+src_name+"\nextract spectrum\nexit\nno\nEOF\n"
            os.system(XselTest)
            
            inneran=0
            #Doing the pile-up check
            # with open("xselect.log","r") as xlog:
            #     for line in xlog:
            #         if line.startswith(" Spectrum         has"):
            #             cps=float((line.strip().split()[5]))
            #             if (1.0 >= cps > 0.5):
            #                 inneran=2
            #             elif (3.0 >= cps > 1.0):
            #                 inneran=4
            #             elif (4.0 >= cps > 3.0):
            #                 inneran=5
            #             elif (6.0 >= cps > 4.0):
            #                 inneran=6
            #             elif (8.0 >= cps > 6.0):
            #                 inneran=7
            #             elif (10.0 >= cps > 8.0):
            #                 inneran=9
            #             elif (cps > 10.0):
            #                 inneran=12
            #             if (cps <= 0.5):
            #                 inneran=0
            # xlog.close()
            cps = 1
            inneran=0

            while cps > 0.5 and inneran<19:
                with open("xselect.log","r") as xlog:
                    for line in xlog:
                        if line.startswith(" Spectrum         has"):
                            cps=float((line.strip().split()[5]))
                            break
                if cps > 0.5:
                    if inneran == 0:
                        os.system("cp "+src_name+" src"+str(i)+"_old.reg")
                        print("%"*30+"\nSource "+str(i)+" of name is too bright\n"+"%"*30)
                    inneran += 1

                    openreg = open(src_name,"r")
                    openlines = openreg.readlines()
                    openreg.close()
                    for i,line in enumerate(openlines):
                        if line[:7] == "annulus":
                            data = line.split(",")
                            data[2] = str(int(inneran))+'"'
                            openlines[i] = ",".join(data)
                            break

                    outreg = open(src_name,"w")
                    for line in openlines:
                        outreg.write(line)
                    outreg.close()
                    os.system(XselTest)
                    with open("xselect.log","r") as xlog:
                        for line in xlog:
                            if line.startswith(" Spectrum         has"):
                                cps=float((line.strip().split()[5]))
                                break
            
            #Writing new src file using the inner annulus generated with the pile-up check.
            # file=open("src"+str(i)+".reg","w")
            # Removing srci.reg (might break)
            # file=open("srci.reg","w")

            # file.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1'+"\n")
            # file.write("fk5"+"\n")
            # file.write('annulus('+str(thisRA)+','+str(thisDec)+','+str(inneran)+'",20")')
            # file.close()
            
            #Doing the Spectrum extraction and ARF operation
            XselMaina="xselect <<EOF\nxsel\n read event \n./\n total.evt \nyes\nfilter region "+back_name+"\nextract spectrum\nsave spectrum "+back_spec_name+"\n\n\n\nclear region \n \n \n \n"
            XselMainb="filter region "+src_name+"\nextract spectrum\nsave spectrum "+src_spec_name+"\n\n\n\nexit\nno\nEOF\n"
            os.system(XselMaina+XselMainb)
            
            #Makign ARF file with xrtmkarf
            XARF="xrtmkarf outfile="+arf_name+" expofile=total.img phafile="+src_spec_name+" srcx=-1 srcy=-1 psfflag=yes clobber=yes > arf.log"
            os.system(XARF)
            print("\n\n(\,--------'()'--o\n (_    ___    /~' arf arf \n  (_)_)  (_)_)\n\n")
            #Looking in the ARF log file to get fluence, RMF to use
            for line in open("arf.log","r"):
                fluence=100
                if "ON AVERAGE" in line:
                    try:
                        fluence=float(line[35:45])
                    except:
                        fluence=float(line[34:44])
                    print("The fluence in the source region is (%) "+str(fluence))
                if "xrt/cpf/rmf/" in line:
                    print("I have found the rmf file to use!")
                    #The rmf location is in single quotes, so I find those quotes and get the characters within them.
                    rmfbounds=([pos for pos, char in enumerate(line) if char=="'"])
                    rmfstring=str(line[rmfbounds[0]+1:rmfbounds[1]])
                    #Copying and renaming the rmf file
                    os.system("cp "+rmfstring+" .")
                    os.system("mv sw*.rmf "+rmf_name)
                    
            #Using the ARF, RMF, spectrums to do grppha (binding things all together now)
            GRPPHA="grppha <<EOF\n"+src_spec_name+"\n!"+total_name+"\nchkey BACKFILE "+back_spec_name+"\nchkey RESPFILE "+rmf_name+"\nchkey ANCRFILE "+arf_name+"\ngroup min 1\nexit\nEOF\n"
            os.system(GRPPHA)
            print('Compressed spectrum file created.')
            
            #calculating catalogued nh at this position
            
            findNH="nh equinox=2000 ra="+str(thisRA)+" dec="+str(thisDec)+" disio=2.5 tchat=0 lchat=10"
            os.system(findNH)
            for line in open("nh.log","r"):
                if "Average nH (cm**-2)" in line:
                    for j in line.split():
                        try:
                            foundNH=float(j)
                            break
                        except:
                            continue
            takeNH=foundNH/1e22
            
            
            

    


