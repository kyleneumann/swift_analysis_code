import os as os
from astropy.io import fits
import numpy as np

# detect_analysis non FGL

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

# choiceFGL = input("Use 4FGL? [y/n]: ")

# if choiceFGL == "y" or choiceFGL == "Y":
#     choiceFGL = "y"
#     print(os.getcwd())
#     try:
#         from TestWithin2 import TestWithin
#     except:
#         raise ValueError("Couldn't find testwithin")

#     FGL = fits.open('4FGL_DR4.fit')
#     FGLnames = FGL[1].data['Source_Name']
#     FGLRA = FGL[1].data['RAJ2000 ']
#     FGLDec = FGL[1].data['DEJ2000 ']
#     FGLsma = FGL[1].data['Conf_95_SemiMajor']
#     FGLsmi = FGL[1].data['Conf_95_SemiMinor']
#     FGLang = FGL[1].data['Conf_95_PosAng']
# else:
#     choiceFGL = "n"

if n==3:
    print("Received 3 variables")
    choiceFGL = "n"
    choice = sys.argv[1]
    specpath = sys.argv[2]
elif n==4:
    print("Received 4 variables")
    choiceFGL = sys.argv[1]
    choice = sys.argv[2]
    specpath = sys.argv[3]
else:
    choiceFGL = input("Use 4FGL? [y/n]: ")
    choice = input("Overwrite detection files? [y/n]: ")

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"

    os.system("ls -d */")
    specpath=input("Enter data directory: ")

if choiceFGL == "y" or choiceFGL == "Y":
    choiceFGL = "y"
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
            print("Couldn't find TestWithin2. Ignoring FGL.")
            choiceFGL = "n"
        
    os.chdir(startpath)
    if choiceFGL == "y":
        print("Make sure the directory names are labeled as their 4FGL source!\n")
        FGL = fits.open('4FGL_DR4.fit')
        FGLnames = FGL[1].data['Source_Name']
        FGLRA = FGL[1].data['RAJ2000 ']
        FGLDec = FGL[1].data['DEJ2000 ']
        FGLsma = FGL[1].data['Conf_95_SemiMajor']
        FGLsmi = FGL[1].data['Conf_95_SemiMinor']
        FGLang = FGL[1].data['Conf_95_PosAng']
else:
    choiceFGL = "n"

    
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
    fgl = dirpath.split('/')[-1]

    if "old_ignore" in dirpath:
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
        print('Have found an XImage detection file for '+fgl)
        
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
            problem.append(dirpath[-12:])
            continue
        else:
            analyzed.append(dirpath[-12:])
        
        #outfile.write('hh mm ss DD DM DS SNdetect SNsosta\n')
        # for i in range(0,len(dets)):
        #     outfile.write(dets[i][50:77]+''+dets[0][98:]+' '+SN[i])
        #     outfile.write('\n')
                
# % now reading in the created file

        MyRAs = []
        MyDecs = []
        MySN = np.array(SNsosta)

        MyFGL=dirpath.split('/')[-1]

        # print(dirpath)
                
        for det in dets:
            MyRAs.append(15*(float(det[50:52])+float(det[53:55])/60+float(det[56:62])/3600))
            if float(det[63:66]) == 0.0:
                MySign = float(det[63]+"1")
            else:
                MySign = np.abs(float(det[63:66]))/float(det[63:66])
            MyDecs.append(float(det[63:66])+MySign*(float(det[67:69])/60+float(det[70:76])/3600))

        if choiceFGL == "y":
            MyName='4FGL '+dirpath.split('/')[-1]

            # print(MyName)
            # print(FGLnames)
            
            # try:
            find = np.where(FGLnames == MyName)[0][0]
            thisRA,thisDec,thissma,thissmi,thisang = FGLRA[find],FGLDec[find],FGLsma[find],FGLsmi[find],FGLang[find]
            try:
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
            except:
                print(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
                In95 = TestWithin(MyRAs,MyDecs,MySN,thisRA,thisDec,thissma,thissmi,thisang,MyName,True)
            # print("Test within")
            # except:
            
            #     pass
            detfile.close()
            logfile.close()
            outfile.write('4FGL,RA,Dec,SNdetect,SNsosta,In95\n')        
            for i in range(0,len(dets)):            
                # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
                outfile.write(MyName+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+','+str(In95[i])+'\n')
            
            
        else:
            MyName=dirpath.split('/')[-1]
            # In95 = False
            detfile.close()
            logfile.close()
            outfile.write('4FGL,RA,Dec,SNdetect,SNsosta\n')        
            for i in range(0,len(dets)):            
                # outfile.write(MyFGL+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
                outfile.write(MyName+','+str(MyRAs[i])+','+str(MyDecs[i])+','+str(SNdetect[i])+','+str(SNsosta[i])+'\n')
            

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
            print(dirpath.split('/')[-1]+" is broken, rerun ximage with different settings.")
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

# raise ValueError("STOP")