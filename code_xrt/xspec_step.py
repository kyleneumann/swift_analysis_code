# xspec wrapper
#%%

import os as os
from astropy.io import fits
import numpy as np
import pandas as pd

import subprocess
import logging
logging.basicConfig(level=logging.INFO)

def terminal_run(program = "xselect",cmd = "quit\n\n",print_out = False):
    try:
        process = subprocess.Popen(
            [program],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send commands and capture output
        stdout, stderr = process.communicate(input=cmd)
        if print_out:
            print("XSELECT STDOUT:\n", stdout)
        return stdout
    
    except Exception as e:
        logging.error(f"Error running XIMAGE commands: {e}")
        return ""

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==5:
    specpath=sys.argv[1]
    choice1=sys.argv[2]
    choice2=sys.argv[3]
    choice3=sys.argv[4]

else:
    print("\n",20*"%")
    print("This code will analyze the spectrum of sources using\n" \
    " XSPEC. This iteration of the code uses the tbabs, cflux, \n"
    "and powerlaw models. If you wish to use something different, \n" \
    "please modify the code or run xspec manually, then run the \n" \
    "xspec_reader.")
    print(20*"%","\n")

    choice1 = input("Overwrite xspec files? [y/n]: ")
    choice2 = input("Generate figures? [y/n]: ")
    choice3 = input("Run steppar? [y/n]: ")

    os.system("ls -d */")

    specpath=input("Enter data directory: ")
os.chdir(specpath)

totpath=os.getcwd()+"/"

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

try:
    df_main = pd.read_csv("xsel_table.csv")
except:
    raise ValueError("Need tp run det_analysis.py for "+totpath)

if "4FGL" in df_main.columns: src_col = "4FGL"
else: src_col = "SRC"

stat = "cstat"

cols = [f for f in df_main.columns if f != "In95"]

addcols = ["exposure","counts","nh","logFX","dlogFX","PhoIndex","dPhoIndex","cstat","bins","Steppar"]

cols += addcols

df_out = pd.DataFrame([],columns=cols)

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    src = dirpath.split('/')[-1]

    df_src = df_main.loc[df_main["SRC"] == src].set_index("index",drop=False)

    if "old_ignore" in dirpath or os.path.isfile("skip.txt"):
        continue

    # if not os.path.isfile("spec0.pi") or os.path.isfile("skip.txt"):
    #     print("Empty skipping 4FGL "+fgl)
    #     continue

    # print('Running 4FGL '+fgl)

    if not os.path.isfile("nh.log"): continue

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

    for filename in [f for f in filenames if (f.endswith(".pi") and f.startswith("spec"))]:
        index = int(filename.replace(".pi","").replace("spec",""))

        if index not in df_src.index: continue

        df = df_src.loc[index].copy()
        # df["nH"] = nh

        if choice1 == "n" and os.path.isfile(f"xspec{index}.log"):
            # print("Not overwriting, skipping 4FGL "+fgl+"/"+str(i))
            pass
        else:
            # if len(df) == 0:
            #     continue
            # elif len(df) != 1:
            #     df
            #     raise ValueError(f"Something broke for {src}/{index}")
            
            # nh = df.nh
            xspec_cmd = (f"log xspec{index}.log \nstatistic {stat} \nquery yes \ndata {filename} \n \
                        ignore **-0.3 10.-** \n ignore bad \n setplot energy \n setplot ylog \n \
                        mo tbabs*cflux*po \n{nh} -1 \n 0.3 \n 10.0 \n -13 \n 2 \n 1 -1 \n fit 5000 \n")


            if choice3 == "y":
                xspec_cmd2 = f"\n cpd plot{index}.ps/cps \n plot ufspec \n cpd none \n quit \n \n \n"

                stout = terminal_run(program="xspec",cmd=xspec_cmd+xspec_cmd2,print_out=False)

                with open(f"xspec{index}.log") as xlog:
                    for line in xlog:
                        if "cflux" in line and "lg10Flux" in line:
                            data = line.split()
                            Fx = float(data[6])
                        elif "powerlaw" in line and "PhoIndex" in line:
                            data = line.split()
                            pI = float(data[5])

                xspec_cmd += f"chatter 0 0 \n parallel steppar 4 \n steppar 4 {Fx-1} {Fx+1} 200 5 {pI-1} {pI+1} 200 \n y \n \n chatter 10 10 \n fit \n error 4 5 \n" 

            if choice2 == "y":
                xspec_cmd += f"\n cpd plot{index}.ps/cps \n plot ufspec \n cpd none \n quit \n \n \n"
            else:
                xspec_cmd += "quit \n \n \n"

            stout = terminal_run(program="xspec",cmd=xspec_cmd,print_out=True)
            
            if choice2 == "y":
                os.system(f"ps2pdf plot{index}.ps plot{index}.pdf")

                if os.path.isdir(totpath+"/jpeg_xspec/"):
                    os.system(f"cp plot{index}.pdf {totpath}/jpeg_xspec/{src}_{index}.pdf")


        if choice3 == "y":
            steppar = True
        else:
            steppar = False
        steps = False

        exposure = 0

        # with open(f"xspec{index}.log") as xlog:
        #     for line in xlog:
        #         if "Net" in line and "count" in line:
        #             data = line.split()
        #             cps = float(data[6])
        #         elif "Exposure" in line and "Time:" in line and "Background" not in line:
        #             data = line.split()
        #             # print(data)
        #             exposure = float(data[3])
        #             df["exposure"] = exposure
        #             df["counts"] = round(cps*exposure,0)
        #             df["nh"] = nh
        #         elif steps and "cflux" in line and "lg10Flux" in line:
        #             data = line.split()
        #             df["logFX"] = float(data[6])
        #             df["dlogFX"] = float(data[8])
        #         elif steps and "powerlaw" in line and "PhoIndex" in line:
        #             data = line.split()
        #             df["PhoIndex"] = float(data[5])
        #             df["dPhoIndex"] = float(data[7])
        #         elif steps and "C-Statistic" in line and "bins" in line:
        #             data = line.split()
        #             df["cstat"] = float(data[4])
        #             df["bins"] = int(data[6])
        #         elif "parallel" in line and "steppar" in line: 
        #             steps = True
        with open(f"xspec{index}.log") as xlog:
            for line in xlog:
                if "Net" in line and "count" in line:
                    data = line.split()
                    cps = float(data[6])
                elif "Exposure" in line and "Time:" in line and "Background" not in line:
                    data = line.split()
                    # print(data)
                    exposure = float(data[3])
                    df["exposure"] = exposure
                    df["counts"] = round(cps*exposure,0)
                    df["nh"] = nh
                elif "cflux" in line and "lg10Flux" in line:
                    data = line.split()
                    df["logFX"] = float(data[6])
                    df["dlogFX"] = float(data[8])
                elif "powerlaw" in line and "PhoIndex" in line:
                    data = line.split()
                    df["PhoIndex"] = float(data[5])
                    df["dPhoIndex"] = float(data[7])
                elif "C-Statistic" in line and "bins" in line:
                    data = line.split()
                    df["cstat"] = float(data[4])
                    df["bins"] = int(data[6])
                elif "error 4 5" in line and steppar:
                    steps = True
                    df["dlogFX"] = -1
                    df["dPhoIndex"] = -1
                elif steps and "4" in line and "#" in line and df["dlogFX"] == -1:
                    data = line.split()
                    error = data[4]
                    print(data)
                    print(error)
                    error = np.mean(abs(np.array(eval(error))))
                    df["dlogFX"] = error
                elif steps and "5" in line and "#" in line and df["dPhoIndex"] == -1:
                    data = line.split()
                    error = data[4]
                    error = np.mean(abs(np.array(eval(error))))
                    df["dPhoIndex"] = error

        df["Steppar"] = steppar
        for col in cols:
            if col not in df.keys():
                df[col] = np.nan
        
        df_out = pd.concat([df_out,df.to_frame().T],ignore_index=True)

os.chdir(totpath)
df_out.to_csv("xspec_table.csv",index=False,na_rep="nan")

print(df_out)