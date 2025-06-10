import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Ellipse
mpl.rcParams['font.family']='serif'
mpl.rcParams['font.size']=16
plt.style.use('dark_background')

import astropy.units as u
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy.wcs import WCS
from regions import PixCoord
from regions import EllipseSkyRegion, EllipsePixelRegion
from regions import make_example_dataset

#%%

def TestWithin(pointRA,pointDec,SN,cenRA,cenDec,SMA,SMI,angi,Title='You should give a title for this',Plot=True):
    #pointRA, pointDec : RA and Dec, in decimal degrees, of test point
    #cenRA, decDec     : RA and Dec center of ellipse
    #SMA, SMI          : semi-major and semi-minor axis in degrees
    #angi              : angle from north towards east
    
    #angi is degrees towards east from celestial north of SMA. Needs to be converted, though
    
    #make WCS for our purposes
    w = WCS(naxis=2)
    w.wcs.crpix = [0, 0]
    w.wcs.cdelt = np.array([-1/3600, 1/3600])
    w.wcs.crval = [cenRA, cenDec]
    w.wcs.ctype = ["RA---AIT", "DEC--AIT"]
    w.wcs.set_pv([(0, 0, 0)])
    
    #define target point
    point_sky = SkyCoord(pointRA, pointDec, unit='deg' ,frame='fk5')
    
    #check to make sure SMA > SMI : reverse them if they are not
    if SMA < SMI:
        holder = SMA
        SMA = SMI
        SMI = holder
    
    #convert angle "from north" to angle "from east" for calculatio purposes
    ang = angi+90
    
    #defining the ellipse
    
    center_sky = SkyCoord(cenRA*u.deg, cenDec*u.deg, frame='fk5') 
    region_sky = EllipseSkyRegion(center=center_sky,width=2*SMA*u.deg, height=2*SMI*u.deg,angle=ang*u.deg)
    
    if Plot:
        center_pixel = center_sky.to_pixel(w)
                
        region_pixel = region_sky.to_pixel(w)
        region_artist = region_pixel.as_artist(fc='white',color='red',lw=2,ls='--')
        
        fig=plt.figure(figsize=(8,8))
        
        ax = plt.gca()        
        ax.add_artist(region_artist)
        
        ax.plot(center_pixel[0],center_pixel[1],'c+')
        
        for i in range(0,len(point_sky)):
            point_pixel = point_sky[i].to_pixel(w)
            if SN[i]<3:
                ax.plot(point_pixel[0],point_pixel[1],marker='x',color='lime')
            if SN[i]>=3:
                ax.plot(point_pixel[0],point_pixel[1],marker='o',color='lime')
        
        ax.set_xlim(-1000,1000)
        ax.set_ylim(-1000,1000)
        ax.set_aspect('equal')
        ax.set_xlabel('East <    RA(arcsec)-cen     > West')
        ax.set_ylabel('South <    Dec(arcsec)-cen     > North')
        ax.set_title(Title)
        ax.grid()
        plt.savefig(Title[5:]+'.pdf',format='pdf',bbox_inches='tight')
        
        #plt.show()
    
    return region_sky.contains(point_sky, w)
 
    
#%% making venn diagram : loading stuff in

# ExcessSum = pd.read_csv('ExcessSummary.txt')
# ExcessSum['Inside95actual'] = ExcessSum['Inside95?'].values
# ExcessSum['Flag'] = ExcessSum['Inside95?'].values

# ExcessRA = ExcessSum['RA'].values
# ExcessDec = ExcessSum['Dec'].values

# ExcessCoord = SkyCoord(ra=ExcessRA, dec=ExcessDec, frame='fk5',unit=(u.hourangle, u.deg))

# FGL = fits.open('4FGL_DR4.fit')

# FGLname = FGL[1].data['Source_Name']
# FGLRA = FGL[1].data['RAJ2000 ']
# FGLDec = FGL[1].data['DEJ2000 ']
# FGLsma = FGL[1].data['Conf_95_SemiMajor']
# FGLsmi = FGL[1].data['Conf_95_SemiMinor']
# FGLang = FGL[1].data['Conf_95_PosAng']

#%% comparing

# for i in range(0,len(ExcessSum)):
#     FindIt = np.where((FGLname == ExcessSum['Name'][i]+'c') + (FGLname == ExcessSum['Name'][i]+'e') + (FGLname == ExcessSum['Name'][i]))[0]
#     if len(FindIt) == 0:
#         ExcessSum['Flag'][i] = False
#         continue
#     else:
#         ExcessSum['Flag'][i] = True
#     FindIt = FindIt[0]
    
#     myRA = ExcessCoord[i].ra.deg
#     myDec = ExcessCoord[i].dec.deg
    
#     toPlot=False
#     if i%251 == 0:
#         toPlot=True
    
#     MyOutput = TestWithin(myRA,myDec,FGLRA[FindIt],FGLDec[FindIt],FGLsma[FindIt],FGLsmi[FindIt],FGLang[FindIt],Title=ExcessSum['Name'][i],Plot=toPlot)
    
#     if i%251 == 0:
#         print(MyOutput)
    
#     ExcessSum['Inside95actual'][i] = MyOutput
    
    
#%% Output

# Right = ExcessSum['Inside95actual'].values
# Wrong = ExcessSum['Inside95?'].values

# FalsePositive = sum((Right == False) * (Wrong == True))
# FalseNegative = sum((Right == True) * (Wrong == False))

# AllPositive = sum((Right == True) * (Wrong == True))
# AllNegative = sum((Right == False) * (Wrong == False))

# print(" done! ")
# print("All Postive: "+str(AllPositive))     
# print("False Postive: "+str(FalsePositive)+" (in wrong ellipses, but not right ellipses)")     
# print("False Negative: "+str(FalseNegative)+" (in right ellipses, but not wrong ellipses)")     
# print("All Negative: "+str(AllNegative))     
    
    