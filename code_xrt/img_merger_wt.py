import os as os

#os.system("export HEADASNOQUERY= \nexport HEADASPROMPT=/dev/null")
startpath="/Users/kdn5172/Desktop/"
startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==4 or n==6:
    specpath=sys.argv[1]
    choice=sys.argv[2]
    parallel=sys.argv[3]
    
    totpath=startpath+specpath
    os.chdir(totpath)

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"
    if parallel == "Y" or parallel == "y":
        parallel = "y"
    else:
        parallel = "n"

    if parallel == "y":
        n_term=sys.argv[4]
        par_index=sys.argv[5]
        if n_term < 2:
            raise ValueError("input must be greater than 2.")
        if par_index < 1 and par_index > n_term:
            raise ValueError("Integer must be within the range of 1 - "+str(n_term)+".")
    
else:
    os.system("ls")
    specpath=input("Enter data directory: ")
    totpath=startpath+specpath
    os.chdir(totpath)

    choice = input("Overwrite image files? [y/n]: ")

    if choice == "Y" or choice == "y":
        choice = "y"
    else:
        choice = "n"

    parallel = input("Running parallel? [y/n]: ")
    if parallel == "Y" or parallel == "y":
        parallel = "y"
    else:
        parallel = "n"

    if parallel == "y":
        n_term = int(input("How many terminals are in use? [+2]: "))
        if n_term < 2:
            raise ValueError("input must be greater than 2.")
        par_index = int(input("What index is this? [1-"+str(n_term)+"]: "))
        if par_index < 1 and par_index > n_term:
            raise ValueError("Integer must be within the range of 1 - "+str(n_term)+".")
    
j = 0

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    cwd = dirpath.split("/")[-1]
    if cwd == "old_ignore" or os.path.isfile("skip.txt"):
        continue

    print(dirpath)
    
    if parallel == "y":
        if j == n_term: 
            j = 0
        j += 1

        print("j index:",j)
        
        if j != par_index:
            continue

    os.chdir(dirpath)

    prefix_list = []

    if os.path.isfile(dirpath+"/total.img"):
        if choice =="n": continue
        if choice == "y": 
            os.system("rm total.img")
    else:
        overwrite_bool = False
    for filename in [f for f in filenames if f.endswith("po_ex.img")]:
        prefix = filename[:-9]
        if filename[-13:-11] == "wt":
            prefix_list.append(prefix)

    #print("test1")

    if len(prefix_list) == 0:
        continue
    elif len(prefix_list) > 80:
        prefix_list = prefix_list[:80]
    
    mergstr = "ximage <<EOF \n"


    for i,prefix in enumerate(prefix_list):
        name = prefix+"po_ex.img"    
        if i == 0:
            mergstr += "read "+name+" \n"
        else:
            mergstr += "read "+name+" \nsum\nsave\n"
    
    mergstr += "write/fits total_wt.img\nquit\n\n\n\nEOF>>"

    #print(mergstr)
    os.system(mergstr+"\n")

    print("Done ximage")

    os.system("fparkey F total_wt.img+0 VIGNAPP add=yes")

    print("Done fparkey")