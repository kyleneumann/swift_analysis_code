# observation time finder

import os as os
import matplotlib.pyplot as plt

from astropy.io import fits

import pandas as pd
import numpy as np

from Interloper import NumInterloper 

if os.path.isfile("4FGL_DR4.fit"):
    FGL = fits.open('4FGL_DR4.fit')
    FGLnames = FGL[1].data['Source_Name']
    FGLsma = FGL[1].data['Conf_95_SemiMajor']
    FGLsmi = FGL[1].data['Conf_95_SemiMinor']
else:
    print("4FGL_DR4.fit")
    FGL = 0

startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)
if n == 2:
    specpath=sys.argv[1]
else:
    os.system("ls -d */")
    specpath=input("Enter data directory: ")
    
if specpath == ".":
    specpath=""
totpath=startpath+specpath
os.chdir(totpath)

count=0
iteration=0

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)

    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath:
        continue

    if os.path.isfile("xselect.log"):
        count+=1
        
print('total of '+str(count)+' found')
        
        
src_arr = []
obs_time = np.zeros(count)
n_int3 = np.zeros(count)
n_int4 = np.zeros(count)
area_arr = np.zeros(count)

os.chdir(totpath)

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    src_name = dirpath.split('/')[-1]

    if src_name == "old_ignore":
        continue
    

    if os.path.isfile("xselect.log"):
        logfile = open("xselect.log","r")
        loglines = [line.rstrip() for line in logfile]
        logfile.close()
        if FGL != 0:
            find = np.where(FGLnames == "4FGL "+src_name)[0]
            if len(find) == 0:
                print("Failed to find "+src_name+". Try changing directory name to "+src_name+"c.")
                continue
                
            find = find[0]
            area = np.pi*FGLsma[find]*FGLsmi[find]*3600
            #print(area)

            for line in loglines:
                Contents =  line.split()
                try:
                    if Contents[0] == "in":
                        #print(src_name,data[1])
                        break
                except: pass
            try:
                src_arr.append(src_name)
                obs_time[iteration]=float(Contents[1])
                area_arr[iteration]=area
                n_int3[iteration]=NumInterloper(area,float(Contents[1]),SN=3)
                n_int4[iteration]=NumInterloper(area,float(Contents[1]),SN=4)
            except:
                raise ValueError("Something broke with "+src_name)
        else:
            for line in loglines:
                Contents =  line.split()
                try:
                    if Contents[0] == "in":
                        #print(src_name,data[1])
                        break
                except: pass
            src_arr.append(src_name)
            obs_time[iteration]=float(Contents[1])
        iteration+=1
        
        
# print(len(src_arr))
# print(len(area_arr))
# print(len(obs_time))
# print(len(n_int3))
# print(len(n_int4))

df = pd.DataFrame({"4FGL":src_arr,"area":area_arr, "obs_time":obs_time,"exp_int_3":n_int3,"exp_int_4":n_int4})

os.chdir(totpath)
df.to_csv("obs_time.csv",index=False)

fig=plt.figure(figsize=(8,8))
ax = plt.gca()    

ax.set_xscale("log")
ax.set_xlabel("Observation Time (s)")

logbins = np.logspace(np.log10(min(obs_time)),np.log10(max(obs_time)),int(15*(len(obs_time)/95)**0.5))

# ax.hist(np.log10(obs_time),bins=15)
ax.hist(obs_time,bins=logbins)

fig.savefig('observation_time.pdf',format='pdf',bbox_inches='tight')

ax.grid()
# plt.show()

#%%

fig=plt.figure(figsize=(6,6))
ax=fig.add_subplot(111)

ax.loglog(area_arr*obs_time,n_int3,'bo',ms=1,label='S/N > 3')
ax.loglog(area_arr*obs_time,n_int4,'rx',ms=1,label='S/N > 4')

ax.grid()
ax.legend()

ax.set_xlabel(r"Exposure $\times$ Area ($s \times \rm{arcmin}^2 $)")
ax.set_ylabel('Expected # Interlopers')


