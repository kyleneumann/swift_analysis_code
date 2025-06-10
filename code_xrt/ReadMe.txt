This directory contains the most recent version of the 4FGL unassociated source - Swift-XRT followup project. 

Here is a description of the pipeline:

Program : HEASARCFinder.py : generates WGET queries given a list of targets

File : HEASqueries.txt : a list of generated WGET queries for downloading raw data from HEASARC

File : 4FGLmatch.txt : a list of correspondences between Swift ObsIDs and (4FGL) targets

Program : WGETscripts.py : executes list of WGET commands to download data

Here is the start of the more general pipeline:

Directory : dataInit : raw, unsorted data downloaded from HEASARC

Program : xrtpipe.py : executes xrtpipeline on dataInit folders, generates dataRef folders
	
Directory : dataRef  : refined data processed with xrtpipeline, move all [obsID]ref folders

Program : cp_observations.py : copies .evt and .img files from dataRef directories into appropriate dataSRC directories

(Alternative) Program : 4FGLmatcher.py : copies .evt and .img files to appropriate dataSRC directories given 4FGLmatch.txt

Program : img_merger.py : use Ximage to merge all the ex.img exposure map files in each dataSRC subdirecto

Program : evt_merger.py : use Xselect to merge all .evt files in each dataSRC into a .fits and .evt totaled file
	
Directory : dataSRC  : the refined data, sorted by 4FGL source for analysis in-place
		: J####.#+#### : a directory holding all .evt, .img, for a source
			: total.evt : totaled event file
			: total.img : totaled exposure map
			: total.fits : totaled fits file for detection and plotting

Directory : old_ignore : directory inside 4FGL target directory which contains files to be ignored by programs

Program : obs_time.py : use .fit file and dataSRC to generate a .csv and .pdf of X-ray observation time per 4FGL target

Program : ximage_detect.py : use Ximage to detect sources
		: use alt code if some .det files weren't generated

Program : detect_analysis.py or det_analysis : goes through previous codes and outputs a .pdf of the X-ray field with sources overlaid with the 4FGL region
		: in 4FGL mode, it will attempt to only locate sources within the 4FGL ellipse. Directories must be named similar to their 4FGL counterpart for this to work

Program : find_sig_dets.py : generates a .csv with all xrt sources within 4FGL region with or without SN limitation. Run if moved sources

Files : det_overlap_sosta.csv : .csv of all xrt sources within a 4FGL region with SN >= 3
		: if an xrt source is removed from list, make sure to change index of other xrt sources within 4FGL region. Must have incremental order by this step

Program : region_gen.py : generates region files of xrt sources and generates .jpegs of 4FGL targets overlapped with their .fits and xrt region files

Program : source_checker.py : verify all region files match their det_overlap_sosta.csv counterparts 

Program : xsel_step.py : runs xselect on all xrt sources to generate necessary files for xspec

Program : xspec_step.py : runs xspec on all xrt sources to model them with tbabs*cflux*powerlaw

Program : xspec_reader.py : goes through all xspeci.log files grab relevant data for the xspec_table.csv

File : xspec_table.csv : last automated .csv table of xrt sources. Can be easily modified for further use.

File : TYCHO2xmatch.csv : .csv example of matching TYC2 to our xrt sources. A match implies it should be removed from xspec_table.csv

File : xrt_table_master.csv : manually editted final file with all significant X-ray sources 
		: all SN < 4.00 and Tycho2 matches have been removed. Additional columns of information have been added using Gamma-ray data and other programs

Program : error_rad.py : Generates the positional error radius of each X-ray source in arcseconds and outputs to err_rad.csv


Misc files and programs:

Program : check_detection.py : verify the .det files were properly generated

Program : obs_reviewer.py : creates a .jpeg of every .evt inside of a directory to look for patterns

Program : TestWithin2.py : tests whether a source is within the 2-sigma uncertainty ellipse of a related 4FGL source

File : region_notes.csv : notes for which XRT fields and sources need editing or need a skip.log file

File : skip.txt : tells the xspec_step.py program to skip this field for being bad/unfixable

File : skip[i].txt : tells the xspec_reader.py program to skip this individual XRT source 

File : rm_processed_files.py : deletes all processed files other than sw{ObsID}po_cl.evt and sw{ObsID}po_ex.img files and those in old_ignore

Subdirectory : old_ignore : safe folder to archive old or bad data for a 4FGL target

For more assistance, contact Kyle Neumann: kdn5172@psu.edu
 