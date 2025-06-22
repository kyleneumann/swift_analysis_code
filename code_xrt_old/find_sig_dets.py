import os as os
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

startpath=os.getcwd()+"/"
os.chdir(startpath)

# simbad = pd.read_csv("SIMBADxmatch.csv")
# simbad_names = simbad.main_id.to_numpy()

# choice = input("Overwrite overlap file? [y/n]: ")

# if choice == "Y" or choice == "y":
#     choice = "y"
# else:
#     choice = "n"

import sys
n = len(sys.argv)

if n==3:
    specpath=sys.argv[1]
    sn = float(sys.argv[2])
else:
    os.system("ls -d */")
    specpath=input("Enter data directory: ")

    sn = float(input("Enter SN lower limit: "))
    
totpath=startpath+specpath
os.chdir(totpath)

if os.path.isfile("obs_time.csv"):
    obs_df = pd.read_csv("obs_time.csv")


# outfile = open("det_overlap.csv","w")
# outfile.write("4FGL,RA,Dec,SNdetect,SNsosta\n")

count_arr = []
src_arr = []
id_list = []
# sn=4

try:
    float(sn)
except:
    raise TypeError("Input must be number.")

df_total = 0

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath:
        continue

    if os.path.isfile("detinfo.csv"):
        #print(dirpath)
        srcname = dirpath.split('/')[-1]

        df = pd.read_csv("detinfo.csv")
        try:
            df = df.loc[df["In95"] == True]
        except:
            pass
        #df["index_col"] = df.index
        try:
            df["4FGL"].to_numpy()[0]
            count = len(df.loc[df.SNsosta >= sn].RA.to_numpy())
        except:
            count = 0
            print("Skipping "+srcname)
            continue

        id = (((df.loc[df["SNsosta"] >= sn]).reset_index(drop=True)).index).to_numpy()
        for i in range(len(id)):
            id_list.append(id[i])
        
        count_arr.append(count)

        if srcname not in src_arr:
            src_arr.append(srcname)

        if type(df_total) != int:
            df_total = pd.concat([df_total,df])
        else:
            df_total = df

os.chdir(totpath)

try:
    try:
        obs_df = obs_df.drop(columns = "count")
    except:
        pass

    count2 = []
    obs_src = obs_df["4FGL"].to_numpy()
    for i in range(len(obs_src)):
        if obs_src[i] in src_arr:
            for j in range(len(src_arr)):
                if obs_src[i] == src_arr[j]:
                    count2.append(count_arr[j])
                    break
        else:
            count2.append(0)

    obs_df.insert(5,"count",count2)

    #print(obs_df)

    obs_df.to_csv("obs_time.csv",index=False)
except:
    print("Either missing obs_time.csv or something is broken. obs_time.csv is not updated.")

try:
    df_total = df_total.drop(columns="In95")
except:
    pass

df_total.to_csv("det_overlap.csv",index=False)
#print(df_total)

df_total = df_total.loc[df_total["SNsosta"] >= sn]
#df_total["index"] = df_total.index

ra = np.round(df_total["RA"].to_numpy(),4)
dec = np.round(df_total["Dec"].to_numpy(),4)

coords = SkyCoord(ra*u.deg,dec*u.deg,frame="fk5")
hms = coords

swiftname=[]
matchname=np.full(len(ra),"NA")

for i in range(len(ra)):
    swiftname.append(f'SwXF J{coords.ra[i].to_string(unit=u.hourangle, sep="", precision=1, pad=True)}{coords.dec[i].to_string(sep="", precision=0, alwayssign=True, pad=True)}')
    # names = simbad.loc[simbad.RA == ra[i]].loc[simbad.Dec == dec[i]].main_id.to_numpy()
    
    # n = len(names)

    # if n == 0:
    #     pass
    # else:
    #     for j,name in enumerate(names):
    #         if i == 0:
    #             n_str = str(name)
    #         else:
    #             n_str += ", "+name
    #     matchname[i] = n_str
# print(id_list)
df_total.insert(1, "SwXF", swiftname,allow_duplicates=True)
df_total["index"] = id_list
# df_total.insert(2, "Match", matchname,allow_duplicates=True)

df_total.to_csv("det_overlap_sosta.csv",index=False)

# outfile.close()

