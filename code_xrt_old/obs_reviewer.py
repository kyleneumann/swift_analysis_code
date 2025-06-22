import os
from astropy.io import fits

startpath=os.getcwd()+"/"#"/Users/kdn5172/Desktop/"
#print("CWD: "+os.getcwd())
os.chdir(startpath)

os.system("ls")
specpath=input("Enter data directory: ")
totpath=startpath+specpath
os.chdir(totpath)
os.system("ls")
targetpath=input("Enter target directory: ")
os.chdir(targetpath)

targpath = os.getcwd()
print(targpath)

filenames = os.listdir()

i=0

choice = input("Print .jpegs? [y/n]")

date_list = []

outfile_arr = []

letters = ["a","b","c","d","e","f","g","h"]

if "total.fits" in filenames:
    for filename in [f for f in filenames if f.endswith("po_cl.evt")]:
        id = str(filename[11:13])

        name = "obs_"+id

        i = 0

        while name+".fits" in outfile_arr:
            i += 1
            if i > len(letters):
                print("Overwriting "+name+".fits")
                break
            if i > 1:
                name = name[:-1]+letters[i]
            else:
                name = name+letters[i]

        fits_name = name+".fits"

        cmd = "xselect <<EOF \n xsel \n read event \n ./ \n"+filename+" \n yes \n extract image \n save image \n "+fits_name+" \n yes \n \n quit \n\n\nEOF>>\n\n\n\n\n"
        os.system(cmd)

        # if int(id) == 2: break

        

        file = fits.open(fits_name)
        date = file[0].header["DATE-OBS"]
        if i == 0:
            ra = file[0].header["ra_nom"]
            dec = file[0].header["dec_nom"]
        if choice == "y":
            os.system("ds9 "+name+".fits -pan to "+str(ra)+" "+str(dec)+" wcs fk5 -log -region ../../All4FGL.reg -saveimage "+name+".jpeg -quit")
        print("Observation "+id+" was observed on "+date)

        date_list.append(date)

        outfile_arr.append(fits_name)

        i = 1

print(date_list)