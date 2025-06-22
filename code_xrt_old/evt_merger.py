import os as os


#os.system("export HEADASNOQUERY= \nexport HEADASPROMPT=/dev/null")
startpath="/Users/kdn5172/Desktop/"
startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

import sys
n = len(sys.argv)

if n == 1:
    os.system("ls")
    specpath=input("Enter data directory: ")

    choice = input("Overwrite event files? [y/n]: ")
else:
    specpath=sys.argv[1]
    choice=sys.argv[2]

totpath=startpath+specpath
os.chdir(totpath)

if choice == "Y" or choice == "y":
    choice = "y"
else:
    choice = "n"

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    prefix_list = []

    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath or os.path.isfile("skip.txt"):
        continue

    print(dirpath)

    if os.path.isfile(dirpath+"/total.evt"):
        if choice =="n": continue
        if choice == "y": 
            overwrite_bool = True
    else:
        overwrite_bool = False
    for filename in [f for f in filenames if f.endswith("po_cl.evt")]:
        prefix = filename[:-9]
        if filename[-13:-11] == "pc":
            prefix_list.append(prefix)

    if len(prefix_list) == 0:
        continue
    elif len(prefix_list) > 80:
        prefix_list = prefix_list[:80]
    
    mergstr = "xselect <<EOF \n xsel \n "

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
    os.system(mergstr)