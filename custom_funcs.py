import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
from typing import *
from enum import IntEnum

def get_contour_info(image, colorStart: Tuple[int,int], colorEnd:Tuple[int,int], CROP_FLOOR, MIN_CONTOUR_AREA = 150):
    """
    Takes in an image, HSV range, and finds the color with the biggest contour area

    Returns:
        1) The center of the detected contour 
        2) The area of the detected contour
        3) The modified image with a draw function appied
    """
    contour_center = None
    contour_area = 0
    contour = None

    #only look at colors around the floor region
    cropped_image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])
    #get all possible contours of this color
    contours = rc_utils.find_contours(cropped_image, colorStart, colorEnd)
    #set the largest contour of that color, if found
    contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)

    if contour is not None:
        #Calculate
        contour_center = list(rc_utils.get_contour_center(contour))
        contour_area = rc_utils.get_contour_area(contour)
    
    return contour_center,contour_area,cropped_image

