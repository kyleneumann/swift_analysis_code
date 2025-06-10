import os as os


startpath=os.getcwd()+"/"
os.chdir(startpath)

import sys
n = len(sys.argv)

if n==4:
    choice = sys.argv[1]
    choice2 = sys.argv[2]
    specpath = sys.argv[3]
else:
    choice = input("Overwrite detection files? [y/n]: ")

    choice2 = input("Alt ximage code? [y/n]: ")

    os.system("ls")
    specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)

if choice == "Y" or choice == "y":
    choice = "y"
else:
    choice = "n"
if choice2 == "Y" or choice2 == "y":
    choice2 = "y"
else:
    choice2 = "n"
    
i=0

empty=[]
analyzed=[]

for dirpath, dirnames, filenames in os.walk(totpath):
    os.chdir(dirpath)
    
    cwd = dirpath.split("/")[-1]
    if "old_ignore" in dirpath:
        continue

    print(dirpath)
    print(i)
    
    if choice == 'n':
        if 'total.det' in filenames:
            print("You told me not to overwrite, skipping this one.")
            continue
    elif 'total.det' in filenames:
        os.system("rm total.det")

    if 'total.fits' in filenames:
        print('     Found total.evt. Conducting XImage search')
        analyzed.append(dirpath.split('/')[-1])
        if choice2 == "n":
            imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=32/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
            os.system(imstr)
        else:
            imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=64/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
            os.system(imstr)

            logfile = open("ximage.log","r")
            loglines = [line.rstrip() for line in logfile]
            logfile.close()

            if "WARNING:  Background not calculated\n" in loglines or "WARNING:  Background not calculated" in loglines:
                print("Redoing ximage for "+dirpath.split('/')[-1])
                imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/bright/back_box_size=128/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'
                os.system(imstr)
                
        #imstr = 'ximage <<EOF \n log ximage \n read total.fits \n detect/back_box_size=64/prob_limit=4e-4/snr=2.0/source_box_size=4. \n sosta/detect_sources \n quit \n \n \n'

        
        
    else:
        if cwd == "jpeg_dir" or cwd == "jpeg_xspec":
            continue
        print("4FGL "+cwd+' has no observations or no summed event file')
        empty.append(dirpath.split('/')[-1])
        continue


print("Analyzed targets: "+str(len(analyzed)))
print("Empty targets   : "+str(len(empty)-1))