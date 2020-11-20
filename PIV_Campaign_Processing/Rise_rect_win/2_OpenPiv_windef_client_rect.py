# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:42:13 2019

@author: Manuel
"""

import os
import numpy as np
from windef_rect_rise import piv

class Settings(object):
    pass  
settings = Settings()

'Data related settings'
settings.save_folder_suffix = 'R_h2_f1200_1_p13'
# Folder with the images to process
settings.filepath_images = 'C:\PIV_Processed\Images_Preprocessed' + os.sep + settings.save_folder_suffix + os.sep
# Folder for the outputs
settings.save_path = 'C:\PIV_Processed\Images_Processed' + os.sep
# Root name of the output Folder for Result Files

# Format and Image Sequence
settings.frame_pattern_a = settings.save_folder_suffix + '.*.tif'
settings.frame_pattern_b = None    

'Region of interest'
# (50,300,50,300) #Region of interest: (xmin,xmax,ymin,ymax) or 'full' for full image
# settings.ROI = (0,1269,0,500) # The first number is the position of the interface measured from the bottom of the image
# settings.ROI = 'full'
settings.ROI = np.asarray([0,1280,0,500]) 


'Image preprocessing'
settings.dynamic_masking_method = 'None'
settings.dynamic_masking_threshold = 0.005
settings.dynamic_masking_filter_size = 7 

# windows and displacement calculation
settings.interpolation_order = 3
settings.subpixel_method = 'gaussian'
settings.correlation_method = 'linear'  # 'circular' or 'linear'
settings.iterations = 3 # select the number of PIV passes

"""
Here we set the window sizes. This code uses rectangular windows, if this is 
not desired, simply put the same values for window_height and window_width as
well as overlap_height and overlap_width
"""
# base 2
settings.window_height = (256, 128, 64)
settings.overlap_height = (128, 64, 32)
settings.window_width = (64, 32, 16)
settings.overlap_width = (32, 16, 8) 
# # base 3
# settings.window_height = (192, 96, 48, 24, 12)
# settings.overlap_height = (96, 48, 24, 12, 6) # 50%
# settings.window_width = (48, 24, 12, 6)
# settings.overlap_width = (24, 12, 6, 3) # 50%

# sig2noise
settings.extract_sig2noise = True  # 'True' or 'False' (only for the last pass)
settings.sig2noise_method = 'peak2peak'
settings.sig2noise_mask = 3
settings.do_sig2noise_validation = True # This is time consuming
settings.sig2noise_threshold = 1.3

# validation
settings.validation_first_pass = True
settings.MinMax_U_disp = (-3, 3)
settings.MinMax_V_disp = (-20, 20)
settings.std_threshold = 70 # threshold of the std validation
settings.median_threshold = 50  # threshold of the median validation
settings.median_size = 1 
settings.replace_vectors = True # Enable the replacment. Chosse: True or False
settings.filter_method = 'localmean' # select a method to replace the outliers: 'localmean', 'disk', 'distance'
settings.max_filter_iteration = 4
settings.filter_kernel_size = 1  # kernel size for the localmean method

# smoothing
settings.smoothn=False #Enables smoothing of the displacemenet field
settings.smoothn_p=0.01 # This is a smoothing parameter

# cosmetics
settings.scaling_factor = 1  # scaling factor pixel/meter
settings.dt = 1  # time between to frames (in seconds)
settings.save_plot = False
settings.show_plot = False
settings.scale_plot = 200 # select a value to scale the quiver plot of the vectorfield
settings.plot_ROI = True
settings.beginning_index = 391

# run the script with these settings

height = np.array([[256,128,96],[256,128,64],[128, 64, 48],[256,128,64],[128,64,32],[256,128,64,32]])
overlap_height = np.array([[128,64,48],[128,64,32],[64, 32, 24],[128,64,32],[64,32,16],[128,64,32,16]])
width = np.array([[64,32,24],[64,32,16],[32, 16, 12],[16,16,16],[64,32,32],[64,32,32,32]])
overlap_width= np.array([[32,16,12],[32,16,8],[16, 8, 6],[8,8,8],[32,16,16],[32,16,16,16]])
iterations=np.array([3,3,3,3,3,4])
settings.run = 2
piv(settings)
# import time
# for i in range(2,3):
#     start = time.time()
#     settings.window_height = height[i]
#     settings.overlap_height = overlap_height[i]
#     settings.window_width = width[i]
#     settings.overlap_width = overlap_width[i]
#     settings.run=7
#     settings.iterations=iterations[i]
#     piv(settings)
#     print(time.time()-start)















