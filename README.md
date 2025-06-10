### swift_analysis_code
### Author: Kyle Neumann - kdn5172@psu.edu

# Swift Analysis Tools/Pipeline

Directory contains code to run XRT and UVOT processing and analysis. Included is an example data directory that will work with the code as an example. XRT Tutorial Map is an overall tutorial for XRT utilizing the Leicester Swift pages in the order utilized by this code. 

## Data Downloading
Swift_TOO.ipynb is a notebook that will allow you to download XRT, UVOT, and/or BAT data of a source over a given date range. This data will come either from the UK Science Data Center (uksdc=True) or HEASARC (uksdc=False).

HEASARCFinder.py is a python script that will utilize HEASARC to locate and write wget scripts to observations of a source. DataDownloader.ipynb will utilize the output text to download the observations.

## XRT Analysis
Starting from the initial observation folders, utilize xrtpipe.py to process all data from raw data into processed data in the {ObsID}ref directory. Can remove all except the cleaned event files and exposure maps from the {ObsID}ref directory. xrt_steps.py is a python script wrapper that runs all the steps following this given several inputs. Will search for sources and run the powerlaw spectral fitting on everyone.

## UVOT Analysis
Currently only contains the light curve analysis code. Move every UVOT sky image to the same directory and the code will generate a totaled light curve per filter given an extraction source region and background region.
