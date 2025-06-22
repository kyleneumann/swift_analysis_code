import os as os
import subprocess
import logging
logging.basicConfig(level=logging.INFO)

def xselect_run(xselect_input):
    try:
        process = subprocess.Popen(
            ["xselect"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send commands and capture output

        stdout, stderr = process.communicate(input=xselect_input)

        print("XSelect STDOUT:\n", stdout)

        return stdout

    except Exception as e:
        logging.error(f"Error running XSelect commands: {e}")
        return ""


startpath=os.getcwd()+"/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

import sys
n = len(sys.argv)

if n == 1:
    print(20*"%")
    print("This code will merge all event files within a \n" \
        "directory into a totalled event file and fits \n" \
        "image. Will output wt events with a '_wt' flag.")
    print(20*"%","\n")

    os.system("ls -d */")
    specpath=input("Enter data directory: ")

    choice = input("Overwrite event files? [y/n]: ")

    mode = input("Which mode do you want to process? [pc/wt/both]: ")

else:
    specpath=sys.argv[1]
    choice=sys.argv[2]
    mode=sys.argv[3]

if choice == "y":
    if mode != "wt":
        # os.system('find . -type f -name "total.img" -exec rm {} +')
        os.system("find . -type d -name '*old_ignore*' -prune -o -type f -name 'total.evt' -exec rm -v {} +")
    if mode != "pc":
        os.system("find . -type d -name '*old_ignore*' -prune -o -type f -name 'total_wt.evt' -exec rm -v {} +")


totpath=startpath+specpath
os.chdir(totpath)

if choice == "Y" or choice == "y":
    choice = "y"
else:
    choice = "n"

if mode != "pc" and mode != "wt":
    mode = "both"

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    prefix_list = []
    prefix_list_wt = []

    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath or os.path.isfile("skip.txt") or "dataInit" in dirpath: continue
    

    print(dirpath)

    if os.path.isfile(dirpath+"/total.evt"):
        if choice =="n": continue
        if choice == "y": 
            overwrite_bool = True
    else:
        overwrite_bool = False
    for filename in [f for f in filenames if f.endswith("po_cl.evt")]:
        prefix = filename[:-9]
        if mode != "wt":
            if filename[-13:-11] == "pc":
                prefix_list.append(prefix)
        if mode != "pc":
            if filename[-13:-11] == "wt":
                prefix_list.append(prefix_list_wt)

    if len(prefix_list) == 0 and len(prefix_list_wt) == 0:
        continue
    elif len(prefix_list) > 80:
        print("Over 80 observations detected, keeping first 80.")
        prefix_list = prefix_list[:80]
    
    # mergstr = "xselect <<EOF \n xsel \n "

    mergstr = "xsel \n"

    for i,prefix in enumerate(prefix_list):
        name = prefix+"po_cl.evt"    
        if i == 0:
            mergstr += "read event "+name+" \n ./ \n yes \n"
        else:
            mergstr += "read event "+name+" \n \n \n \n "
    
    if overwrite_bool:
        mergstr += "extract event copyall=yes\nsave events total.evt\nyes\nyes\nextract image\nsave image total.fits\nyes\n\nexit\nno\n\nEOF>>"
    else:
        mergstr += "extract event copyall=yes\nsave events total.evt\nyes\nextract image\nsave image total.fits\nno\n\nexit\nno\n\nEOF>>"

    #print(mergstr)
    # os.system(mergstr)
    stout = xselect_run(mergstr)
    
    overwrite_bool = False

    if os.path.isfile(dirpath+"/total_wt.evt"):
        if choice =="n": continue
        if choice == "y": 
            overwrite_bool = True

    if len(prefix_list_wt) == 0: continue
    elif len(prefix_list_wt) > 80:
        print("Over 80 observations detected, keeping first 80.")
        prefix_list_wt = prefix_list_wt[:80]
    
    mergstr = "xselect <<EOF \n xsel \n "

    for i,prefix in enumerate(prefix_list_wt):
        name = prefix+"po_cl.evt"    
        if i == 0:
            mergstr += "read event "+name+" \n ./ \n yes \n"
        else:
            mergstr += "read event "+name+" \n \n \n \n "
    
    if overwrite_bool:
        mergstr += "extract event copyall=yes\nsave events total_wt.evt\nyes\nyes\nextract image\nsave image total_wt.fits\nyes\n\nexit\nno\n\nEOF>>"
    else:
        mergstr += "extract event copyall=yes\nsave events total_wt.evt\nyes\nextract image\nsave image total_wt.fits\nno\n\nexit\nno\n\nEOF>>"

    # os.system(mergstr)
    stout_wt = xselect_run(mergstr)
