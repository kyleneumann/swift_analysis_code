import os
import numpy as np

###
print("\n"+"%"*30+"\nThis code removes all processed files other than the original observation files\n"+"%"*30+"\n")
# It's a reset
###


startpath=os.getcwd()+"/"
os.chdir(startpath)

act = input("Are you sure you want to clean all processed files? [y/n]: ")
if act == "y" or act == "Y":
    pass
else:
    raise ValueError("Ending code")

act = input("Including totaled files? [y/n]: ")
if act == "y" or act == "Y":
    act = "y"
else:
    act = "n"

os.system("ls -d */")

specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    if len(filenames) == 0: continue

    if "old_ignore" in dirpath.split('/') or "save.txt" in filenames:
        continue

    if any(file.endswith('.evt') for file in filenames):
        print("Removing processed files from "+dirpath)
    else:
        if "jpeg_dir" in dirpath:
            os.system("rm *")
        elif any(file.endswith('time.csv') for file in filenames):
            for filename in filenames:
                if filename.endswith("time.csv") or filename.endswith("sosta.csv") or filename.endswith("overlap.csv"):
                    os.system("rm "+filename)
        continue

    for filename in filenames:
        if not os.path.isfile(filename):
            print(dirpath+"/"+filename+" is glitched out somehow?")
            continue
        elif filename.endswith("po_cl.evt") or filename.endswith("po_ex.img") or filename.endswith("img.gz") or filename.endswith(".py") or filename == "4FGL_coords.csv":
            continue
        elif act == "n" and (filename == "total.evt" or filename == "total.fits" or filename == "total.img" or filename == "xselect.log"):
            continue
        
        else:
            # print("rm "+dirpath+"/"+filename)
            os.system("rm "+dirpath+"/"+filename)