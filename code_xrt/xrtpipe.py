import os as os

print(20*"%")
print("This code process XRT level one data into processed data. \n" \
      "Code has the capabilities to save all output data or delete \n" \
      "everythiong except for event files and exposure maps. Will \n" \
      "output data in [ObsID]ref subdirectories and will skip an \n" \
      "observation if a reference subdirectory already exists.")
print(20*"%","\n")

# os.system("export HEADASNOQUERY= \nexport HEADASPROMPT=/dev/null")
keep_all = input("Keep all output files? [y/n]: ")
if keep_all == "n" or keep_all == "N":
    keep_all = "n"
else:
    keep_all = "y"

mode = input("Which mode do you want to process? [pc/wt/both]: ")
if mode != "pc" and mode != "wt":
    mode = "both"

print(mode)
# raise ValueError("STOP")

startpath=os.getcwd()+"/"
# startpath="/Users/kdn5172/Desktop/"
os.chdir(startpath)
os.system("ls -d */")
specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

os.system("ls -d */")
outpath = input("Enter output directory [NONE]: ")
outpath = totpath+outpath
if outpath[-1] != "/": outpath+="/"

if not os.path.isdir(outpath): os.system(f"mkdir {outpath}")

#Getting event designation for steminputs
for dirpath, dirnames, filenames in os.walk(totpath):
    for filename in [f for f in filenames if f.endswith("cl.evt.gz")]:
        if filename[-16:-14] != mode and mode != "both":
            continue
        stemp=(filename[0:13])
        os.chdir(dirpath)
        os.chdir('../..')
        thisdir = os.path.abspath(".")
        print(thisdir)
        
        if not os.path.exists(f'{outpath}{thisdir}ref'):
            print("Will create a new directory for Xrtpipeline output")
            os.system(f"mkdir {outpath}{thisdir}ref")
        else:
            print("Xrtpiptline output already exists. Skipping iteration")
            continue
        
        pipel=f'xrtpipeline indir={thisdir} outdir={outpath}{thisdir}ref steminputs={stemp} chatter=2 cleanup=yes'
        pipel=pipel+' srcra=OBJECT srcdec=OBJECT createexpomap=yes exprpcgrade="0-12" exprwtgrade="0-2" clobber=yes'
        pipel=pipel+' gtiexpr="Vod1.ge.29.82.and.Vod1.le.30.25.and.Vod2.ge.29.3.and.Vod2.le.29.80.and.Vrd1.ge.16.40.and.Vrd1.le.16.80.and.Vrd2.ge.16.45.and.Vrd2.le.16.90.and.CCDTemp.ge.-102.and.CCDTemp.le.-50.0.and.ANG_DIST.le.0.3"'
        os.system(pipel)

if keep_all == "n":
    print("Deleting unnecessary files")
    for dirpath, dirnames, filenames in os.walk(outpath):
        os.chdir(dirpath)
        
        thisdir = dirpath.split("/")[-1]
        # print(thisdir)
        if thisdir.endswith("ref"):
            print("Deleting items from "+thisdir)
            # print("Test 2")
            for filename in [f for f in filenames if not f.endswith("po_cl.evt") and not f.endswith("po_ex.img")]:
                # print("rm "+dirpath+"/"+filename)
                os.system("rm "+dirpath+"/"+filename)
