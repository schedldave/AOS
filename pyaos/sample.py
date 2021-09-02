import json
import numpy as np
import os
import cv2
import time
from LFR_utils import read_poses_and_images, pose_to_virtualcamera, init_aos, init_window
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import pyaos.lfr as LFR

def imshow(image, *args, **kwargs):
    """A replacement for cv2.imshow() for use in Jupyter notebooks using matplotlib.

        Args:
          image : np.ndarray. shape (N, M) or (N, M, 1) is an NxM grayscale image. shape
            (N, M, 3) is an NxM BGR color image. 
    """
    if len(image.shape) == 3:
      # Height, width, channels
      # Assume BGR, do a conversion  
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Draw the image
    plt.imshow(image, *args, **kwargs)
    # We'll also disable drawing the axes and tick marks in the plot, since it's actually an image
    plt.axis('off')
    # Make sure it outputs
    # plt.show()


def divide_by_alpha(rimg2):
  a = np.stack((rimg2[:,:,3],rimg2[:,:,3],rimg2[:,:,3]),axis=-1)
  return rimg2[:,:,:3]/a

if __name__ == '__main__':
    
    if 'window' not in locals() or window == None: 
        window = init_window() # only init the window once (causes problems if closed and loaded again!)
    fov = 32.3443 # 50.815436217896945
    # init the light-field renderer
    aos = init_aos(1024,1024,fov=fov)
    basedatapath = Path(__file__).resolve().parent
    # load a digital terrain
    aos.loadDEM( os.path.join(basedatapath, '..', 'data', 'zero_plane.obj') )
    aos.setDEMTransform([0,0,51])

    # load multiple images and corresponding poses
    
    pose_file = os.path.join( basedatapath, '..', 'data', '20210810_conifer_ex2_set2', 'colmap', 'poses', 'RGB.json' )
    images_dir = os.path.join( basedatapath, '..', 'data', '20210810_conifer_ex2_set2', 'colmap', 'images', 'cr1024' )
    single_images, site_poses = read_poses_and_images( aos,pose_file, images_dir, adjust_mean=False )
    center_index = int(round(len(single_images) / 2))

    plt.subplot(121)
    imshow(np.asarray(single_images[center_index],dtype=np.uint8)), plt.title(f'center image (id={center_index})')
    #plt.show()

    # compute an integral 
    integral = aos.render(pose_to_virtualcamera(aos.getPose(center_index)), fov)
    tmp = divide_by_alpha(integral) # integrals are 4 channel images, where the last channel (alpha) contains the number of overlapping images

    xyz = aos.getXYZ()
    #print(xyz)
    
    

    plt.subplot(122)
    imshow(np.asarray(tmp,dtype=np.uint8)), plt.title('integral image (N={})'.format(aos.getViews()))

    plt.show()


    # cleanup
    del aos
    del window


