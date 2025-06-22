# xspec wrapper

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd

from math import log10, floor
def round_to_n(x,n=1):
    return round(x, n-1-int(floor(log10(abs(x)))))

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==3:
    choice1=sys.argv[1]
    specpath=sys.argv[2]
else:
    choice1 = input("Overwrite xspec table? [y/n]: ")

    os.system("ls")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

if choice1 == "Y" or choice1 == "y":
    choice1 = "y"
else:
    choice1 = "n"

if os.path.isfile("xspec_table.csv") and choice1 == "n":
    exit

try:
    df_sosta = pd.read_csv("det_overlap_sosta.csv")
except:
    raise ValueError("Need tp run find_sig_det.py for this directory")

print(df_sosta)

# cflux_list = []
# dcflux_list = []
# pi_list = []
# dpi_list = []
# cstat_list = []
# bins_list = []

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    fgl = dirpath.split('/')[-1]
    FGLn = fgl

    if fgl == "old_ignore":
        continue

    if not os.path.isfile("xspec0.log"):
        continue

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

    skip_coef=0

    for i in range(80):
        # xray source i

        outname = "xspec"+str(i)+".log"

        if skip_coef > 3:
            # To stop after enough repeats
            break
        elif not os.path.isfile(outname):
            skip_coef += 1
            continue
        elif os.path.isfile("skip"+str(i)+".txt"):
            continue

        openfile = open(outname,"r")
        openlines = openfile.readlines()
        openfile.close()

        loc_bool = False

        cflux = -99
        dcflux = -99
        pi = -99
        dpi = -99
        cstat = -99
        bins = -99
        steppar_bool = '!XSPEC12>  chatter 10 10 \n' in openlines
        #print(steppar_bool)
        steppar_work = False

        for line in openlines:
            data = line.split()
            if steppar_bool:
                try:
                    if data[1] == "fit" and len(data) == 2:
                        loc_bool = True
                        #print("test0")
                except:
                    continue
            else:
                try:
                    if data[1] == "fit" and data[2] == "5000":
                        loc_bool = True
                        #print("test0")
                except:
                    continue

            #print(data)

            # try:
            if loc_bool and bins == -99:
                # print("test1")
                if len(data) < 8: continue
                # print("test2")
                if data[0] == "#" and data[4] == "lg10Flux":
                    cflux = float(data[6])
                    dcflux = float(data[8])
                elif data[0] == "#" and data[4] == "PhoIndex":
                    pi = float(data[5])
                    dpi = float(data[7])
                elif data[0] == "#Fit" and data[3] == "C-Statistic":
                    cstat = float(data[4])
                    bins = float(data[6])
                    if steppar_bool:
                        # print("test0")
                        pass
                    else:
                        break
            if bins != -99:
                try:
                    # print("test1")
                    # if data[0] == "#" or data[1] == "error":
                    #     print(data)
                    # try:
                    if data[0] == "#" and data[1] == "4":
                        # print("test2")
                        error_str = data[4]
                        error_str = error_str[1:-1]
                        error_ls = error_str.split(",")
                        lower = round_to_n(abs(float(error_ls[0])),2)
                        upper = round_to_n(abs(float(error_ls[1])),2)

                        dcflux = round_to_n(np.mean([lower,upper]),2)
                    elif data[0] == "#" and data[1] == "5":
                        # print("test3")
                        error_str = data[4]
                        error_str = error_str[1:-1]
                        error_ls = error_str.split(",")
                        lower = round_to_n(abs(float(error_ls[0])),2)
                        upper = round_to_n(abs(float(error_ls[1])),2)

                        dpi = round_to_n(np.mean([lower,upper]),2)
                        steppar_work = True
                        break
                    # except:
                    #     pass
                except:
                    pass
                    

            # except:
            #     print("Source "+str(i)+" of "+fgl+" has a broken log file.")
        # print(df_sosta.loc[df_sosta["4FGL"]==FGLn])

        # print(df_sosta.loc[df_sosta.index == i])

        df = df_sosta.loc[df_sosta["4FGL"]==FGLn].loc[df_sosta["index"] == i]

        # print("test")
        df["nH"] = [nh]
        df["lg10Flux"] = [cflux]
        df["dlg10Flux"] = [dcflux]
        df["PhoIndex"] = [pi]
        df["dPhoIndex"] = [dpi]
        df["cstat"] = [cstat]
        df["bins"] = [bins]
        df["Steppar"] = [steppar_work]

        # print("test")
        # cflux_list.append(cflux)
        # dcflux_list.append(dcflux)
        # pi_list.append(pi)
        # dpi_list.append(dpi)
        # cstat_list.append(cstat)
        # bins_list.append(bins)
        try:
            df_total = pd.concat([df_total,df])
            # print("test")
        except:
            df_total = df


# FGL_names = df_sosta["4FGL"].to_numpy()
# SwXF_names = df_sosta["SwXF"].to_numpy()

# print(len(cflux_list))
# print(len(pi_list))
# print(len(FGL_names))

os.chdir(totpath)

# d = {"4FGL": FGL_names, "SwXF":SwXF_names, "lg10Flux":cflux_list, "dlg10Flux":dcflux_list, "PhoIndex":pi_list, "dPhoIndex":dpi_list,"cstat":cstat_list,"bins":bins_list}
# df = pd.DataFrame(data=d)

df_total.to_csv("xspec_table.csv",index=False)



        