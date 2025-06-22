import os
from astropy.io import fits

startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

for dirpath, dirnames, filenames in os.walk(startpath):
    os.chdir(dirpath)

    for filename in [f for f in filenames if f.endswith("po_cl.evt") or f.endswith("po_ex.img")]:
        os.system("cp "+filename+" "+startpath)