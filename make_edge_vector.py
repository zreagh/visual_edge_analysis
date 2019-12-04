#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script reads in video information frame-by-frame, and then calculates
visual edge information for each frame, storing the information in a vector.
This can be averaged within TRs in an fMRI analysis to 'regress out'
high-frequency visual information in the video.

@author: zreagh
"""

import cv2
import numpy as np

# Can uncomment this pyplot import for frame plotting - see below
#from matplotlib import pyplot as plt

# Define the paths to your video file and eventual JPEG image files
vidpath = '/Users/zreagh/Desktop/edge_vector_analysis/test.mov'
imgpath = '/Users/zreagh/Desktop/edge_vector_analysis/'

edge_outfile = open('edge_outfile.csv','w')
edge_outfile.write('frame,prop_edge_pix\n')
  
# Function to extract video info including frames
def AnalyzeFrames(vidpath): 
    
    print("\nGetting video info & writing out image files for each frame...\n")
      
    # Path to video file 
    vidObj = cv2.VideoCapture(vidpath) 
    
    # Get FPS
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    print("Frames per second: {0}\n".format(fps))
    
    # Used as counter variable 
    count = 0
    
    # Create an empty list to be filled with image names for calculations below
    jpeglist = []
  
    # Checks whether frames were extracted 
    success = 1
  
    # Make sure vidObj call is read
    while success: 
        
        # Function extract frames 
        success, frame = vidObj.read()
  
        # Saves the frames indexed with frame number as jpeg frames
        cv2.imwrite("frame{0}.jpg".format(count), frame)
        
        # Iteratively fill our list to be called in frame analyses below
        jpeglist.append("frame{0}.jpg".format(count))
  
        # Tick up our counter with each frame
        count += 1
    
    # Drop the video from the buffer
    vidObj.release()

    # Print some useful info to the console
    print('Total number of frames: {0}\n'.format(count))
    print('Video duration in seconds: {0}\n'.format(round(count/fps)))
    
    # Loop through the images and do edge calculations
    # NOTE: I am constraining to range 0:193 here because my 193rd image is
    # empty for some reason. You can probably delete this for your purposes
    # so that it reads "for jpeg in jpeglist:" instead!
    print("Analyzing visual edges and writing output file...\n")
    
    for jpeg in jpeglist[0:193]:
        
        img = cv2.imread(imgpath + jpeg,0)
        edges = cv2.Canny(img,100,200)
        
        # Get the total number of pixels for each image
        n_pix = np.sum(edges > -1)
        
        # Get the proportion of white (edge) pixels for each image
        n_white_pix = np.sum(edges == 255)
        
        # Calculate the proportion of edge pixels (white/total) for each image
        prop_edge_pix = float(n_white_pix/n_pix)
        
        edge_outfile.write('{0},{1}\n'.format(jpeg,prop_edge_pix))

        # Prints out relevant calculations above for each image - uncomment to
        # debug or peek under the hood
#        print('\nFrame image:', jpeg)
#        print('Total number of pixels:', n_pix)
#        print('Number of white pixels:', n_white_pix)
#        print('Proportion of edge pixels:', prop_edge_pix)
        
        # Plot each raw frame and edge frame side-by-side - uncomment to
        # peek under the hood (will slow things down a bunch FYI)
#        plt.subplot(121),plt.imshow(img,cmap = 'gray')
#        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#        plt.show()

    print("Done! Check your output file: edge_outfile.csv")
    
# Do the damn thing
if __name__ == '__main__': 
  
    # Calling the function 
    AnalyzeFrames(vidpath)    