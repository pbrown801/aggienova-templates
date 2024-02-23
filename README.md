# Aggienova
This is the github repository for the Texas A&M AGGIENOVA research team to create spectrophotometric time-series templates for supernovae.

repo structure:

actively used (2024):

filters/  contains filter response curves

spectra/  contains spectra 

output/  output figures and plots and templates
  
input/    contains csv files from the open supernova catalog and dat files from SOUSA

python/   all the active python code for the project.   The main file run_pipeline.py resides here


not currently used:


old/ contains python code written by a previous team we can use/modify
idlcode/ contains the idl code Peter Brown used to create a version of the templates

images/ contains code and images for animating the spectra and images along the changing light curve.  Mahir worked on this.  It would require a set of 3 color images which correspond exactly to the 6 filter epochs from Swift.  To avoid the interpolated light curves, all epochs in the photometry file would need to have all 6 filters.
uvot/  not sure, maybe associated with the images folder for the animation


others/     contains snflux_1a.dat which is the Hsiao template of similar format to what we are creating
