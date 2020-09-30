# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:42:13 2019

@author: Theo
"""

# add two directories that include the new files
# note that we need to import openpiv in a separate, original namespace
# so we can use everything from openpiv as openpiv.filters and whatever is 
# going to replace it will be just filteers (for example)


from OpenPIV_windef_func import PIV_windef
#import time

class Settings(object):
    pass  
#start_time = time.time()
settings = Settings()

'Data related settings'
# Folder with the images to process
settings.filepath_images = './Pre_Pro_PIV_IMAGES/'
# Folder for the outputs
settings.save_path = './Results_PIV/'
# Root name of the output Folder for Result Files
settings.save_folder_suffix = 'Test_1'
# Format and Image Sequence
settings.frame_pattern_a = 'A010a.tif'
settings.frame_pattern_b = 'A010b.tif'    

'Region of interest'
# (50,300,50,300) #Region of interest: (xmin,xmax,ymin,ymax) or 'full' for full image
settings.ROI = 'full'

'Image preprocessing'
# 'None' for no masking, 'edges' for edges masking, 'intensity' for intensity masking
# WARNING: This part is under development so better not to use MASKS
settings.dynamic_masking_method = 'None'
settings.dynamic_masking_threshold = 0.005
settings.dynamic_masking_filter_size = 7 

'Processing Parameters'
settings.correlation_method = 'linear'  # 'circular' or 'linear'
settings.iterations = 2  # select the number of PIV passes
# add the interroagtion window size for each pass. 
# For the moment, it should be a power of 2 
settings.windowsizes = (64, 32, 16, 8) # if longer than n iteration the rest is ignored
# The overlap of the interroagtion window for each pass.
settings.overlap = (32, 16, 8, 4) # This is 50% overlap
# Has to be a value with base two. In general window size/2 is a good choice.
# methode used for subpixel interpolation: 'gaussian','centroid','parabolic'
settings.subpixel_method = 'gaussian'
# order of the image interpolation for the window deformation
settings.interpolation_order = 5
settings.scaling_factor = 22222.2222  # scaling factor pixel/meter
settings.dt = 24e-6  # time between to frames (in seconds)
'Signal to noise ratio options (only for the last pass)'
# It is possible to decide if the S/N should be computed (for the last pass) or not
settings.extract_sig2noise = True  # 'True' or 'False' (only for the last pass)
# method used to calculate the signal to noise ratio 'peak2peak' or 'peak2mean'
settings.sig2noise_method = 'peak2peak'
# select the width of the masked to masked out pixels next to the main peak
settings.sig2noise_mask = 2
# If extract_sig2noise==False the values in the signal to noise ratio
# output column are set to NaN
'vector validation options'
# choose if you want to do validation of the first pass: True or False
settings.validation_first_pass = True
# only effecting the first pass of the interrogation the following passes
# in the multipass will be validated
'Validation Parameters'
# The validation is done at each iteration based on three filters.
# The first filter is based on the min/max ranges. Observe that these values are defined in
# terms of minimum and maximum displacement in pixel/frames.
settings.MinMax_U_disp = (-30, 30)
settings.MinMax_V_disp = (-30, 30)
# The second filter is based on the global STD threshold
settings.std_threshold = 5  # threshold of the std validation
# The third filter is the median test (not normalized at the moment)
settings.median_threshold = 1  # threshold of the median validation
# On the last iteration, an additional validation can be done based on the S/N.
settings.median_size = 1 #defines the size of the local median
'Validation based on the signal to noise ratio'
# Note: only available when extract_sig2noise==True and only for the last
# pass of the interrogation
# Enable the signal to noise ratio validation. Options: True or False
settings.do_sig2noise_validation = True # This is time consuming
# minmum signal to noise ratio that is need for a valid vector
settings.sig2noise_threshold = 1.1
'Outlier replacement or Smoothing options'
# Replacment options for vectors which are masked as invalid by the validation
settings.replace_vectors = True # Enable the replacment. Chosse: True or False
settings.smoothn=True #Enables smoothing of the displacemenet field
settings.smoothn_p=0.5 # This is a smoothing parameter
# select a method to replace the outliers: 'localmean', 'disk', 'distance'
settings.filter_method = 'localmean'
# maximum iterations performed to replace the outliers
settings.max_filter_iteration = 4
settings.filter_kernel_size = 2  # kernel size for the localmean method
'Output options'
# Select if you want to save the plotted vectorfield: True or False
settings.save_plot = True
# Choose wether you want to see the vectorfield or not :True or False
settings.show_plot = False
settings.scale_plot = 200 # select a value to scale the quiver plot of the vectorfield
# run the script with the given settings
settings.counter = 0

i = 1
for i in range(1, 11):
    settings.frame_pattern_a = 'A%03da.tif' % i
    settings.frame_pattern_b = 'A%03db.tif' % i 
    settings.counter = i
    PIV_windef(settings)

#end_time = time.time()
#print('Calculationtime: %.3f' % (end_time-start_time))