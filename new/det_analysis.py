import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

import os as os
# import subprocess
import logging
logging.basicConfig(level=logging.INFO)

def get_j2000_name(ra_deg, dec_deg):
    coord = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame='fk5')
    ra_str = coord.ra.to_string(unit=u.hourangle, sep='', precision=1, pad=True)
    dec_str = coord.dec.to_string(sep='', alwayssign=True, precision=0, pad=True)
    return f'J{ra_str}{dec_str}'

# detect_analysis non FGL

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n == 1:
    print(20*"%")
    print("This code will search for significant X-ray sources \n" \
        "found in ximage_detect. To utilize only specific \n" \
        "sources, please utilize TestWithin2 and the \n" \
        "appropriate docs.")
    print(20*"%","\n")

    os.system("ls -d */")
    specpath=input("Enter data directory: ")

    choiceFGL = (input("Use 4FGL? [y/n]: ")).lower()
    if choiceFGL == "y" or choiceFGL == "Y": 
        choice2 = "y"
    else:
        choice2 = (input("Use TestWithin to find only relevant sources [y/n]: ")).lower()

    choice = input("Overwrite detection files? [y/n]: ")

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"

    sn = float(input("Enter SN lower limit: "))

elif n > 1:
    specpath = sys.argv[1]
    if n > 2:
        choiceFGL = sys.argv[2].lower()
        if n > 3:
            choice2 = sys.argv[3].lower()
            if n > 4:
                choice = sys.argv[4]
                if n == 6:
                    sn = float(sys.argv[5])
                else:
                    sn = 3
            else:
                choice = input("Overwrite detection files? [y/n]: ")

                if choice == "Y" or choice == "y":
                    choice = "y"
                else:
                    choice = "n"

                sn = float(input("Enter SN lower limit: "))
        else:
            if choiceFGL == "y" or choiceFGL == "Y": 
                choiceFGL = choiceFGL.lower()
                choice2 = "y"
            else:
                choice2 = (input("Use TestWithin to find only relevant sources [y/n]: ")).lower()

            choice = input("Overwrite detection files? [y/n]: ")

            if choice == "Y" or choice == "y":
                choice = "y"
            else:
                choice = "n"

            sn = float(input("Enter SN lower limit: "))
    else:
        choiceFGL = input("Use 4FGL? [y/n]: ")
        if choiceFGL == "y" or choiceFGL == "Y": 
            choice2 = "y"
        else:
            choice2 = input("Use TestWithin to find only relevant sources [y/n]: ")

        choice = input("Overwrite detection files? [y/n]: ")

        if choice == "Y" or choice == "y":
            choice = "y"
        else:
            choice = "n"

        sn = float(input("Enter SN lower limit: "))
        

if choiceFGL.lower() == "y" or choice2.lower() == "y":

    # print(os.getcwd())
    if os.path.isfile("TestWithin2.py"):
        print("Found TestWitin2")
        from TestWithin2 import TestWithin
    else:
        os.chdir("../../")
        tempath = os.getcwd()
        found = False
        for dirpath, dirnames, filenames in os.walk(tempath):
            os.chdir(dirpath)
            if os.path.isfile("TestWithin2.py"):
                print("Found TestWitin2")
                from TestWithin2 import TestWithin
                found = True
                break
        if not found:
            print("Couldn't find TestWithin2.")
            choiceFGL = "n"
        
    os.chdir(startpath)

    # Major and minor axes in degrees and positional angle in degrees
    cols = ['src',"RA","Dec","major","minor","ang"]

    if choiceFGL.lower() == "y":
        print("Make sure the directory names are labeled as their 4FGL source!\n")
        FGL = fits.open('4FGL_DR4.fit')
        FGLnames = FGL[1].data['Source_Name']
        FGLRA = FGL[1].data['RAJ2000 ']
        FGLDec = FGL[1].data['DEJ2000 ']
        FGLsma = FGL[1].data['Conf_95_SemiMajor']
        FGLsmi = FGL[1].data['Conf_95_SemiMinor']
        FGLang = FGL[1].data['Conf_95_PosAng']

        df = pd.DataFrame([FGLnames,FGLRA,FGLDec,FGLsma,FGLsmi,FGLang],columns=cols)

    elif choice2.lower() == "y":
        input_file = "input_sources.csv"
        print("Make sure the directory names are labeled as their source!\n")
        print(f"Default file is listed as '{input_file}'.")
        if os.path.isfile(input_file):
            df = pd.read_csv(input_file)
        else:
            os.system("ls")
            input_file = input(f"Couldn't find {input_file}, what file would you prefer to use instead?")
            if os.path.isfile(input_file):
                df = pd.read_csv(input_file)
            else:
                print(f"Couldn't find {input_file}. Code ignoring TestWithin request.")
                choice2 = "n"
        if choice2 == "y":
            for col in cols:
                if col not in df.columns:
                    raise ValueError(f"{input_file} needs to at least have these columns: {cols}")
else:   
    choiceFGL = "n"
    choice2 = "n"
    
totpath=startpath+specpath
os.chdir(totpath)

# print("Test")

i=0

empty=[]
analyzed=[]
problem=[]
bad_ximage = []

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    # print('4FGL '+dirpath.split('/')[-1])
    src = dirpath.split('/')[-1]

    if "old_ignore" in dirpath or os.path.isfile("skip.txt"):
        continue

    if os.path.isfile("detinfo.csv") and choice == "n":
        print("Skipping "+dirpath.split('/')[-1])
        continue
    
    # does the directory have a ximage .det file?
    if 'total.det' in filenames:
        
        i+=1
        
        detfile = open('total.det','r')
        logfile = open('ximage.log','r')
        outfile = open('detinfo.csv','w')
        
        dets = []
        Xpixels = []
        Ypixels = []
        SNsosta = []
        SNdetect = []
        print('Have found an XImage detection file for '+src)
        
        #read lines from .det and .log files
        lines = [line.rstrip() for line in detfile]
        loglines = [line.rstrip() for line in logfile]
        
        # the lines in the .det file that we want do not start with '!'
        for line in lines:
            if line.split()[0] != '!':
                dets.append(line)
                SNdetect.append(float(line.split()[-1]))
        
        # the lines in the .log file that we want start with 'X'
        for i in range(0,len(loglines)):
            if len(loglines[i].split())>0:
                if loglines[i].split()[0] == 'X':
                    Xpixels.append(loglines[i].split()[2])
                    Ypixels.append(loglines[i].split()[5])
                if loglines[i].split()[0] == 'Signal':
                    SNsosta.append(float(loglines[i].split()[-1]))
        # check to make sure that the same number of .det and .leg files have been found        
        if len(dets) != len(SNsosta):
            print('Problem! The .det and .log files may be malformed.')
            problem.append(dirpath.split("/")[-1])
            continue
        else:
            analyzed.append(dirpath.split("/")[-1])
    
                
# % now reading in the created file

        MyRAs = []
        MyDecs = []
        SwXFs = []
        MySN = np.array(SNsosta)

        MySRC=src

        # print(dirpath)
                
        for det in dets:
            dat = det.split()
            ra = f"{dat[5]}h{dat[6]}m{dat[7]}s"
            dec = f"{dat[8]}d{dat[9]}m{dat[10]}s"
            coord = SkyCoord(ra,dec,frame="fk5")
            SwXFs.append(get_j2000_name(coord.ra.deg,coord.dec.deg))
            MyRAs.append(coord.ra.deg)
            MyDecs.append(coord.dec.deg)

        if choiceFGL == "y":
            MyName=src

            # print(MyName)
            # print(FGLnames)
            
            # try:
            find = np.where(df.src == MyName)[0][0]
            thisRA,thisDec,thissma,thissmi,thisang = df.loc[find].RA,df.loc[find].Dec,df.loc[find].major,df.loc[find].minor,df.loc[find].ang

            try:
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
            except:
                print(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
            # print("Test within")
            # except:
            
            #     pass
            outfile.write('SRC,SwXF,RA,Dec,SNdetect,SNsosta,In95\n')        
            for i in range(0,len(dets)):            
                # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
                outfile.write(MyName+","+SwXFs[i]+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+','+str(In95[i])+'\n')
            
        elif choice2 == "y": 
            MyName = src   

            find = np.where(df.src == MyName)[0][0]
            thisRA,thisDec,thissma,thissmi,thisang = df.loc[find].RA,df.loc[find].Dec,df.loc[find].major,df.loc[find].minor,df.loc[find].ang
            try:
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
            except:
                print(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)

            outfile.write('SRC,SwXF,RA,Dec,SNdetect,SNsosta,In95\n')        
            for i in range(0,len(dets)):            
                # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
                outfile.write(MyName+","+SwXFs[i]+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+','+str(In95[i])+'\n')
        else:
            MyName=src
            # In95 = False
            outfile.write('SRC,SwXF,RA,Dec,SNdetect,SNsosta\n')        
            for i in range(0,len(dets)):            
                # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
                outfile.write(MyName+","+SwXFs[i]+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
            

        # outfile.write('4FGL,RA,Dec,SNdetect,SNsosta,In95\n')        
        # for i in range(0,len(dets)):            
        #     # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
        #     outfile.write(MyName+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+','+str(In95[i])+'\n')
            
            
        detfile.close()
        logfile.close()
        outfile.close()
        

    elif 'ximage.log' in filenames:
        logfile = open('ximage.log','r')

        loglines = [line.rstrip() for line in logfile]
        logfile.close()

        broken_bool = False

        for line in loglines:
            if line.find("WARNING:  Background not calculated") != -1:
                broken_bool = True
                break
        
        if broken_bool:
            print(src+" is broken, rerun ximage with different settings.")
            bad_ximage.append(dirpath.split('/')[-1])
        else:
            print('Found no XImage detection file. Empty or no detections.')

if len(bad_ximage) > 0:
    os.chdir(totpath)

    outfile = open("bad_ximage.txt","w")
    outfile.write("4FGL\n")
    for src in bad_ximage:
        outfile.write(src+"\n")
    outfile.close()
os.chdir(totpath)
print("\nDetection reader, complete. Analyzing significant sources now.\n")

df_total = 0
count_arr = []
src_arr = []
id_list = []

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath or "skip.txt" in filenames:
        continue

    if not os.path.isfile("detinfo.csv"): continue
        #print(dirpath)
    srcname = cwd

    df = pd.read_csv("detinfo.csv")
    try:
        df = df.loc[df["In95"] == True]
    except:
        pass
    #df["index_col"] = df.index
    df = df.loc[df.SNsosta >= sn]

    if "4FGL" in df.columns: src_col = "4FGL"
    else: src_col = "SRC"

    try:
        df[src_col].to_numpy()[0]
        count = len(df)
    except:
        count = 0
        print("Skipping "+srcname)
        continue

    if count == 0: continue

    df = df.sort_values(by="SNsosta")

    if In95 in df.columns:
        df = df.drop(columns=["In95"])

    df["index"] = df.reset_index(drop=True).index
    count_arr.append(count)

    if type(df_total) == int:
        df_total = df.copy()
    else:
        df_total = pd.concat([df_total,df])
    
os.chdir(totpath)
df_total.to_csv("det_overlap.csv",index=False,na_rep="nan")

# raise ValueError("STOP")