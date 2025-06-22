import numpy as np
import os as os
import pandas as pd

queries=np.genfromtxt("HEASqueries.txt",dtype='str',delimiter='\n')
qlen = len(queries)

# startpath="/Users/kdn5172/Desktop/"
startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

os.system("ls")
specpath=input("Output data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

print("Running wget for "+str(qlen)+" now:")
for i in range(0,qlen):
    try:
        if i%int(qlen/10) == 0:
            percent = round(i/qlen,2)*100
            print(str(int(percent))+" completed")
    except: pass
    os.system(queries[i])