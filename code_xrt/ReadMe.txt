This directory contains the most recent version of the Swift-XRT analysis code. 

Here is a description of the pipeline:

Directory : dataInit : raw data downloaded from HEASARC observations either in major directory unsorted or within source subdirectories

Program : xrtpipe.py : executes xrtpipeline on dataInit folders, generates dataRef folders
		:[ObsID]ref : dataRef folders will be created along side their original [ObsID] files
	
Directory : dataRef  : refined data processed with xrtpipeline, move all [obsID]ref folders (optional)

Directory : dataUV : folder containing UVOT data (optional)

Directory : data : directory of sources containing refined data : name not relevant

Program : img_merger.py : use Ximage to merge all the ex.img exposure map files in each dataSRC subdirectory
		: total.img : summed exposure maps of a source

Program : evt_merger.py : use Xselect to merge all .evt files in each dataSRC into a .fits and .evt totaled file
		: total.evt : summed event files of observations
		: total.fits : summed fits images of observations for detection and plotting

Program : ximage_detect.py : use Ximage to detect sources

Program : detect_analysis.py : goes through detection files and outputs significant sources within FOV or region of interest
		: TestWithin2.py : python script to verify sources are within roi 

Files : ../input_sources.csv : table of sources and their rois for detect_analysis

Files : det_overlap.csv : .csv of all significant X-ray sources located with detect_analysis
						: if an xrt source is removed from list, make sure to change index of other xrt sources within 4FGL region. Must have incremental order by this step

Program : region_gen.py : generates region files of xrt sources and background regions and generates .jpegs of 4FGL targets overlapped with their .fits and xrt region files
						: if a separate source is within the background region, an output warning file will be generated
	
Program : xsel_step.py : runs xselect on all xrt sources to generate source spectra

File : xsel_table.csv : finalized table of XRT sources to be studied with Xspec

Program : xspec_step.py : runs xspec on all xrt sources to model them with tbabs*cflux*powerlaw

File : xspec_table.csv : last automated .csv table of xrt sources. Can be easily modified for further use.


Misc files and programs:

Program : ../xrt_steps.py : wrapper program to run through all steps of the above xrt analysis steps after all relevant event files and exposure maps are within their source folders 

File : skip.txt : tells the xspec_step.py program to skip this field

File : skip[i].txt : tells analysis programs to skip this individual XRT source 

File : rm_processed_files.py : deletes all processed files other than sw{ObsID}po_cl.evt and sw{ObsID}po_ex.img files and those in old_ignore

Subdirectory : old_ignore : safe folder to archive old or bad data for a given source

For more assistance, contact Kyle Neumann: kdn5172@psu.edu
 