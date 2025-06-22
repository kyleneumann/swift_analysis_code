import os as os
import subprocess
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)

def ximage_run(ximage_input):
    try:
        process = subprocess.Popen(
            ["ximage"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send commands and capture output
        stdout, stderr = process.communicate(input=ximage_input)
        print("XIMAGE STDOUT:\n", stdout)

        return stdout
    except Exception as e:
        logging.error(f"Error running XIMAGE commands: {e}")
        return ""

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==4:
    choice = sys.argv[1]
    specpath = sys.argv[2]
else:
    print(20*"%")
    print("This code will search for X-ray \n" \
        "sources within the FOV with ximage.")
    print(20*"%","\n")

    choice = input("Overwrite detection files? [y/n]: ")

    os.system("ls -d */")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

if choice == "Y" or choice == "y":
    choice = "y"
else:
    choice = "n"
# if choice2 == "Y" or choice2 == "y":
#     choice2 = "y"
# else:
#     choice2 = "n"
    
# i=0

empty=[]
analyzed=[]

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    
    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath or os.path.isfile("skip.txt"):
        continue
    # print(i)
    
    if choice == 'n':
        if 'total.det' in filenames:
            print("Detect file found, skipping")
            continue
    elif 'total.det' in filenames:
        os.system("rm total.det")

    if 'total.fits' in filenames:
        print(f'     Found total.evt. Conducting XImage search in {dirpath}')
        
        cmd_str = 'log ximage \n read total.fits \n detect/bright/back_box_size=32/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
        stdout = ximage_run(cmd_str)
        if "WARNING:  Background not calculated\n" in stdout or "WARNING:  Background not calculated" in stdout:
            print("Redoing ximage for "+dirpath.split('/')[-1])
            cmd_str = 'log ximage \n read total.fits \n detect/bright/back_box_size=64/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
            stdout = ximage_run(cmd_str)
            if "WARNING:  Background not calculated\n" in stdout or "WARNING:  Background not calculated" in stdout:
                print("Redoing ximage for "+dirpath.split('/')[-1])
                cmd_str = 'log ximage \n read total.fits \n detect/bright/back_box_size=128/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
                stdout = ximage_run(cmd_str)
                if "WARNING:  Background not calculated\n" in stdout or "WARNING:  Background not calculated" in stdout: 
                    empty.append(dirpath.split('/')[-1])
                    print(f"{cwd} failed XIMAGE. Try manually operating it.")
                    continue
        
        analyzed.append(cwd)
        # imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=32/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
        # os.system(imstr)
        # else:
        #     imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=64/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
        #     os.system(imstr)

        #     logfile = open("ximage.log","r")
        #     loglines = [line.rstrip() for line in logfile]
        #     logfile.close()

        #     if "WARNING:  Background not calculated\n" in loglines or "WARNING:  Background not calculated" in loglines:
        #         print("Redoing ximage for "+dirpath.split('/')[-1])
        #         imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=128/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
        #         os.system(imstr)
                
        #imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/back_box_size=64/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'

        
        
    # else:
    #     if cwd == "jpeg_dir" or cwd == "jpeg_xspec":
    #         continue
    #     print("4FGL "+cwd+' has no observations or no summed event file')
    #     empty.append(dirpath.split('/')[-1])
    #     continue


print("Analyzed targets: "+str(len(analyzed)))
print("Failed targets   : "+str(len(empty)))