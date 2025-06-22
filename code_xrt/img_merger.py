import os as os
import subprocess
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

#os.system("export HEADASNOQUERY= \nexport HEADASPROMPT=/dev/null")
startpath="/Users/kdn5172/Desktop/"
startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

import sys
n = len(sys.argv)

if n == 1:
    print("\n",20*"%")
    print("This code will merge all exposure maps within a directory. \n" \
        "WARNING: exposure map summing time increases nonlinearly \n" \
        "with more observations. Code allows for parallelization using \n" \
        "the 'in_progress.txt'. If code crashes or stops, please remove \n" \
        "progress.txt before attempting again.")
    print(20*"%","\n")

    os.system("ls -d */")
    specpath=input("Enter data directory: ")
    totpath=startpath+specpath
    os.chdir(totpath)

    choice = input("Overwrite image files? [y/n]: ")

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"

    mode = input("Which mode do you want to process? [pc/wt/both]: ")
else:
    specpath=sys.argv[1]
    choice=sys.argv[2]
    mode=sys.argv[3]

    totpath=startpath+specpath
    os.chdir(totpath)

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"

if choice == "y":
    if mode != "wt":
        # os.system('find . -type f -name "total.img" -exec rm {} +')
        os.system("find . -type d -name '*old_ignore*' -prune -o -type f -name 'total.img' -exec rm -v {} +")
    if mode != "pc":
        os.system("find . -type d -name '*old_ignore*' -prune -o -type f -name 'total_wt.img' -exec rm -v {} +")

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    if "old_ignore" in dirpath or os.path.isfile("skip.txt") or "dataInit" in dirpath: continue
    
    if os.path.isfile("progress.txt"): continue
    else:
        subprocess.run(["touch","in_progress.txt"])

    print(dirpath)

    os.chdir(dirpath)

    prefix_list = []
    prefix_list_wt = []

    if os.path.isfile(dirpath+"/total.img") and mode != "wt":
        os.system("rm in_progress.txt")
        continue
    
    for filename in [f for f in filenames if f.endswith("po_ex.img")]:
        prefix = filename[:-9]
        if filename[-13:-11] == "pc" and mode != "wt":
            prefix_list.append(prefix)
        elif filename[-13:-11] == "wt" and mode != "pc":
            prefix_list_wt.append(prefix)

    #print("test1")

    if len(prefix_list) == 0:
        os.system("rm in_progress.txt")
        continue
    elif len(prefix_list) > 80:
        prefix_list = prefix_list[:80]
    
    # mergstr = "ximage <<EOF \n"
    mergstr = ""

    for i,prefix in enumerate(prefix_list):
        name = prefix+"po_ex.img"    
        if i == 0:
            mergstr += "read "+name+" \n"
        else:
            mergstr += "read "+name+" \nsum\nsave\n"
    
    mergstr += "write/fits total.img\nquit\n\n\n\nEOF>>"

    #print(mergstr)
    # os.system(mergstr+"\n")
    stdout = ximage_run(mergstr)

    print("Done ximage")

    os.system("fparkey F total.img+0 VIGNAPP add=yes")

    print("Done fparkey")

    if len(prefix_list_wt) == 0:
        os.system("rm in_progress.txt")
        continue
    elif len(prefix_list_wt) > 80:
        prefix_list_wt = prefix_list_wt[:80]
    
    # mergstr = "ximage <<EOF \n"
    mergstr = ""

    for i,prefix in enumerate(prefix_list_wt):
        name = prefix+"po_ex.img"    
        if i == 0:
            mergstr += "read "+name+" \n"
        else:
            mergstr += "read "+name+" \nsum\nsave\n"
    
    mergstr += "write/fits total_wt.img\nquit\n\n\n\nEOF>>"

    #print(mergstr)
    # os.system(mergstr+"\n")
    stdout = ximage_run(mergstr)

    print("Done ximage")

    os.system("fparkey F total_wt.img+0 VIGNAPP add=yes")

    print("Done fparkey")

    os.system("rm in_progress.txt")
