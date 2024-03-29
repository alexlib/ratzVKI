# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 07:37:07 2021

@author: Manuel Ratz
"""

import sys
sys.path.append('C:\\Users\manue\Documents\GitHub\\ratzVKI\PIV_Campaign_Processing')

import numpy as np # for array calculations
import cv2 # for image processing
from matplotlib import pyplot as plt # for plotting
import os # for filepaths
import image_processing_functions as imp # for interface detection
import post_processing_functions as ppf
import imageio

ppf.set_plot_parameters(20, 15, 10)

plus = 0 # offset in case we went to look at a certain image
"""General settings"""
# amount of images to process
Img_Amount = 2000
# size of the output files lower for large image amounts to save time
if Img_Amount < 20:
    dpi = 400
else:
    dpi = 80
# width of the channel
Width = 5
# acquisition frequency of the camera
Fps = 500

"""Interface Detection"""
# threshold for the gradient 
Threshold_Gradient = 5
# threshold for outliers
Threshold_Outlier_out = 60 # 0.075
Threshold_Outlier_in = 20 # 0.02
# threshold for the kernel filtering
Threshold_Kernel_out = 2 #0.01
Threshold_Kernel_in = 2 #0.001
# pixels to cut near the wall
Wall_Cut = 3

# whether to mirror the right side onto the left
Do_Mirror = True
# whether to do light nonlocal means denoising
Denoise = True

"""locate the images"""
# letter of the current run
Test_Case = 'P1500_C30_A'
Case = 'Rise'
Fluid = 'Water'

Fol_Data, Pressure, Run, H_Final, Frame0, Crop_Index, Speed =\
    imp.get_parameters(Test_Case, Case, Fluid)
N_T = Frame0+Img_Amount-1+plus
Pix2mm = Width/(Crop_Index[1]-Crop_Index[0]) 
# name of the output folder
# Fol_Out = ppf.create_folder('Crop_Check')
Fol_Images_Detected = ppf.create_folder(Fol_Data + os.sep + 'Images_Detected')

"""initialize arrays"""
h_mm_avg = np.zeros([N_T+1])*np.nan  
h_cl_left = np.zeros([N_T+1])*np.nan  
h_cl_right = np.zeros([N_T+1])*np.nan  
angle_gauss = np.zeros([N_T+1])*np.nan  
angle_cosh = np.zeros([N_T+1])*np.nan 
curvature_gauss = np.zeros(([N_T+1]))
curvature_cosh = np.zeros(([N_T+1]))

def func(x_func,a,b):
    return (np.cosh(np.abs(x_func)**a/b)-1)

"""gif setup"""
images = [] # empty list to append into
GIFNAME = 'Detected_interface_hyperbolic_cosine.gif' # name of the gif

# loop over all the images
for i in range(0+plus,Img_Amount+plus):
    # get the index starting from N_T
    Idx = i
    # get the index starting from 0
    Load_Idx = Frame0+Idx
    MEX= 'Exporting Im '+ str(i+1)+' of ' + str(Img_Amount) # update on progress
    print(MEX) 
    # load the image and highpass filter it
    img_hp, img = imp.load_image(Fol_Data, Crop_Index, Idx, Load_Idx,\
                                  Pressure, Run, Speed, Denoise, Fluid)
    # calculate the detected interface position
    grad_img, y_index, x_index = imp.edge_detection_grad(img_hp,\
        Threshold_Gradient, Wall_Cut, Threshold_Outlier_in, Threshold_Outlier_out
        , Threshold_Kernel_out, Threshold_Kernel_in,\
            do_mirror = Do_Mirror, fluid = Fluid, idx = Idx)
    # fit a gaussian to the detected interface
    mu_s,i_x,i_y,i_x_mm,i_y_mm,X,img_width_mm = imp.fitting_advanced(\
        grad_img, Pix2mm, l=5, sigma_f=1e-4, sigma_y=1e-9)
    
    # this is the part with the hyperbolic cosine fit
    i_x_fit = i_x_mm - 2.5
    X_plot = (np.linspace(-2.5,2.5,1000))
    
    # calculate the fitting parameters
    fit_val, shift, inverted = imp.fitting_cosh(i_x_fit, i_y)
    # calculate the fitted hyperbolic cosine
    y_cosh_fine = (func(X_plot, fit_val[0], fit_val[1]))
    # invert if needed
    if inverted == True:
        y_cosh_fine *= (-1)
    # convert to mm
    y_cosh_fine += shift
    y_cosh_fine *= Pix2mm
    # save the values into the arrays
    h_mm_avg[Load_Idx] = imp.vol_average(mu_s,X,img_width_mm)
    h_cl_left[Load_Idx] = mu_s[0]
    h_cl_right[Load_Idx] = mu_s[-1]
    angle_gauss[Load_Idx]= imp.contact_angle(mu_s,X,-1, Pix2mm)
    angle_cosh[Load_Idx]= imp.contact_angle(y_cosh_fine,X,-1, Pix2mm)
    curvature_gauss[Load_Idx] = imp.integrate_curvature(mu_s)
    curvature_cosh[Load_Idx] = imp.integrate_curvature(y_cosh_fine)
    
    # plot the result
    fig, ax = plt.subplots() 
    # convert back to pixels
    mu_s = mu_s/Pix2mm 
    y_cosh_fine = y_cosh_fine/Pix2mm
    # show the image in greyscale
    ax.imshow(np.flip(img, axis = 0), cmap=plt.cm.gray) 
    # plot the detected gradient onto the image
    ax.scatter(i_x, i_y, marker='x', s=(70./fig.dpi)**2, color = 'lime') 
    # plot the Gaussian Process
    ax.plot((X)/(Pix2mm), mu_s, 'r-', linewidth=0.5) 
    # plot the hyperbolic cosine fit
    ax.plot((X_plot+2.5)/Pix2mm-0.5, y_cosh_fine, lw=0.5, color = 'yellow')
    # flip the y axis to show the image correctly
    ax.invert_yaxis()
    # crop the image around the interface
    ax.set_ylim(mu_s[500]-20, mu_s[500]+65)
    # cosmetics
    ax.set_aspect('equal')
    ax.axis('off')
    # save the image
    NAME_OUT = Fol_Images_Detected + os.sep + 'Stp_%05d.png' %(Idx+Frame0)
    fig.tight_layout()
    fig.savefig(NAME_OUT, dpi= dpi)
    plt.close(fig)
    
    # append the image into the gif list (every second to save time)
    if (i%2) == 0:
        images.append(imageio.imread(NAME_OUT))
# imageio.mimsave(GIFNAME, images, duration = 0.10)

# get the pressure and f0_exp
pressure, f0_exp = imp.load_labview_files(Fol_Data, Test_Case)

# calculate the height offset
h_offset = np.mean(h_mm_avg[-50:])

# shift the data accordingly
h_mm_avg = h_mm_avg[Frame0+plus:]+H_Final-h_offset
h_cl_left = h_cl_left[Frame0+plus:]+H_Final-h_offset
h_cl_right = h_cl_right[Frame0+plus:]+H_Final-h_offset
angle_gauss = angle_gauss[Frame0+plus:]
angle_cosh = angle_cosh[Frame0+plus:]
curvature_gauss = curvature_gauss[Frame0+plus:]
curvature_cosh = curvature_cosh[Frame0+plus:]
pressure = pressure[Frame0-f0_exp:Frame0-f0_exp+Img_Amount]
# set up the time scale
t = np.linspace(0,len(h_mm_avg)/Fps,len(h_mm_avg)+1)[Frame0-f0_exp:]

# save the data
imp.saveTxt(Fol_Data, h_mm_avg, h_cl_left, h_cl_right, angle_gauss,\
            angle_cosh, pressure, curvature_gauss, curvature_cosh,\
                Test_Case)
