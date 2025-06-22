import os
import numpy as np

print(20*"%")
print("This code will delete all (or most) processed files. \n" \
      "Careful how and where you activate this code. Meant \n"
      "for heavy fast clean up of data files.")
print(20*"%","\n")


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

    if "old_ignore" in dirpath.split('/') or "save.txt" in filenames or "Init" in dirpath or "UV" in dirpath or "skip.txt" in filenames:
        continue

    if any(file.endswith('.evt') for file in filenames):
        print("Removing processed files from "+dirpath)
    else:
        if "png_dir" in dirpath:
            os.system("rm *")
        elif any(file.endswith('time.csv') for file in filenames):
            for filename in filenames:
                if filename.endswith("time.csv") or filename.endswith("table.csv") or filename.endswith("overlap.csv"):
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