# xspec wrapper

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==5:
    choice1=sys.argv[1]
    choice2=sys.argv[2]
    choice3=sys.argv[3]
    choice4=sys.argv[4]
    specpath=sys.argv[5]

else:
    choice1 = input("Overwrite xspec files? [y/n]: ")
    choice2 = input("Generate figures? [y/n]: ")
    choice3 = input("Run steppar? [y/n]: ")
    choice4 = input("What model to use? [po/bb] (bb will still use a po):")


    os.system("ls")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

if choice1 == "Y" or choice1 == "y":
    choice1 = "y"
else:
    choice1 = "n"

if choice2 == "Y" or choice2 == "y":
    choice2 = "y"
else:
    choice2 = "n"

if choice3 == "Y" or choice3 == "y":
    choice3 = "y"
else:
    choice3 = "n"

if choice4 == "bb":
    pass
else:
    choice4 == "po"

stat = "cstat"

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    fgl = dirpath.split('/')[-1]

    if fgl == "old_ignore":
        continue

    if not os.path.isfile("spec0.pi") or os.path.isfile("skip.txt"):
        print("Empty skipping 4FGL "+fgl)
        continue
    elif choice1 == "n" and os.path.isfile("xspec0.log"):
        print("Overwrite skipping 4FGL "+fgl)
        continue

    print('Running 4FGL '+fgl)

    skip_coef = 0

    openfile = open("nh.log","r")
    openlines = openfile.readlines()
    openfile.close()
    for line in openlines:
        data = line.split()
        try:
            if data[0]=="h1_nh_HI4PI.fits":
                nh = float(data[-1])/1e22
                break
        except:pass

    for i in range(80):
        # xray source i

        outname = "spec"+str(i)+".pi"

        if skip_coef > 3:
            # To stop after enough repeats
            break
        elif not os.path.isfile(outname):
            skip_coef += 1
            continue
        
        xspec_cmd = "xspec <<EOF\n log \n statistic "+stat+" \nquery yes \ndata "+outname+"\n ignore **-0.3 10.-** \n ignore bad \n setplot energy \n setplot ylog \n "
        if choice4 == "po":
            xspec_cmd += "mo tbabs*cflux*po \n "+str(nh)+" -1 \n 0.3 \n 10.0 \n -13 \n 2 \n 1 -1 \n fit 5000 \n" 
        elif choice4 == "bb":
            xspec_cmd += "chatter 0 0 \n mo tbabs*(bb+po) \n "+str(nh)+" -1 \n 1e-1 \n 1 \n 4 -1 \n 1e-4 \n fit 5000 \n thaw 4 \n fit \n thaw 1 \n chatter 10 10 \n fit \n"
        
        if choice3 == "y":
            xspec_cmd += "chatter 0 0 \n parallel steppar 4 \n steppar 4 -14 -12 400 5 -1 4 400 \n y \n \n chatter 10 10 \n fit \n error 4 5 \n" 

        if choice2 == "y":
            xspec_cmd += "\n cpd plot"+str(i)+".ps/cps \n plot ufspec \n cpd none \n quit \n \n \n"
        else:
            xspec_cmd += "quit \n \n \n"
        os.system(xspec_cmd) 

        os.system("mv xspec.log xspec"+str(i)+".log")

        if choice2 == "y":
            os.system("ps2pdf plot"+str(i)+".ps plot"+str(i)+".pdf")

            if os.path.isdir(totpath+"/jpeg_xspec/"):
                os.system("cp plot"+str(i)+".pdf "+totpath+"/jpeg_xspec/"+fgl+"_"+str(i)+".pdf")



        



