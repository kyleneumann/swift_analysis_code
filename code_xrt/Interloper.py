def CalcRateLim(S,t,b = 0.45e-3,A = 0.35, scale=1.1):
    #calculates count rate given...
    # S : desired signal/noise ratio
    # t : exposure time in seconds
    # b : background count rate, counts/s/square arcminute, default of 0.45e-3 from 1SWXRT paper
    # A : area of source region, square arcminutes, default to cirle with radius 20 arcseconds
    # scale : a scaling factor to correct the S/N calculation and match XRT catalogs
    factor1 = S * (4 * A * b * t + S**2)**0.5 / t
    factor2 = S**2 / t
    return 0.5 * (factor1+factor2) * scale

def SourceDensity(cps,slope=-1.2,factor=3e-6):
    #calculates the number density of sources per square arcminute given...
    #cps    : the lower limit of source counts/s, in 
    #slope  : the slope of the luminosity function, from fitting to 1003 GRB fields
    #factor : the multiplicative density factor, from fitting to 1003 GRB fields
    #note - this returns number density of X-ray sources at or above the given flux limit
    return factor*cps**slope

def NumInterloper(area,exposure,SN=4,b = 0.45e-3,A = 0.35, scale=1.1,slope=-1.2,factor=3e-6):
    #calculates the expected number of background "interloper" X-ray sources given
    #area     : the area of a region of space in square arcminutes
    #exposure : the amount of Swift-XRT PC mode observations in seconds
    #SN       : the threshold S/N ratio of a source to be considered a detection, by default = 4
    #other parameters are passed to CalcRateLim and SourceDensity as default parameters
    fluxlim = CalcRateLim(S=SN,t=exposure,b=b,A=A,scale=scale)
    density = SourceDensity(fluxlim,slope=slope,factor=factor)
    return density * area

def CalcArea(a,b):
    # calculates the area of an ellipse
    return 3.141592653589793*a*b
    