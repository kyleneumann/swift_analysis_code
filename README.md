### swift_analysis_code
### Author: Kyle Neumann - kdn5172@psu.edu

# Swift Analysis Tools/Pipeline

The directory contains code to run XRT and UVOT processing and analysis. Included is an example data directory that will work with the code as an example. XRT Tutorial Map is an overall tutorial for XRT utilizing the Leicester Swift pages in the order utilized by this code. 

## Data Downloading
Swift_TOO.ipynb is a notebook that will allow you to download XRT, UVOT, and/or BAT data of a source over a given date range. This data will come either from the UK Science Data Center (uksdc=True) or HEASARC (uksdc=False).

HEASARCFinder.py is a Python script that will utilize HEASARC to locate and write wget scripts for observations of a source. DataDownloader.ipynb will utilize the output text to download the observations.

## XRT Analysis
Starting from the initial observation folders, utilize xrtpipe.py to process all data from raw data into processed data in the {ObsID}ref directory. Can remove all except the cleaned event files and exposure maps from the {ObsID}ref directory. xrt_steps.py is a Python script wrapper that runs all the steps given several inputs. Will search for sources and run the powerlaw spectral fitting on everyone.

## UVOT Analysis
Currently only contains the light curve analysis code. Move every UVOT sky image to the same directory, and the code will generate a total light curve per filter given an extraction source region and background region.

## data folder
Example folder of sources to display how xrt_steps.py and others will work, along with file organization options. TXS 1516+064 will produce a spectrum with a very well-done powerlaw fit, while V1405 Cas will fail to properly fit to a powerlaw. Both will be included within the final processed tables. input_sources.csv contains example positioning of the two example sources with accurate coordinates. Semimajor axes, semiminor axes, and position angle (in degrees) are exaggerated to show region generation.

## Commenting and Utilizing Repo
If you experience an error or issue, consider opening an issue in the repository, and I will check it out. If you wish to use this code in your analysis, please include a citation in the acknowledgements. Citations are available under "Cite this repository".
