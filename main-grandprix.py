########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../library")
import racecar_core
import racecar_utils as rc_utils

from enum import IntEnum, Enum

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Add any global variables here
speed = 0
angle = 0

FRONT_WINDOW = (-10, 10)
FRONT_RIGHT_WINDOW = (30, 40)
FRONT_LEFT_WINDOW = (320, 330)
RIGHT_WINDOW = (65, 70)
LEFT_WINDOW = (285, 290)

class State(IntEnum):
    see_marker = 0
    follow_marker = 1
    search = 2

cur_state = State.see_marker


MIN_CONTOUR_AREA = 200


########################################################################################
# Functions
########################################################################################

def start():
    """
    This function is run once every time the start button is pressed
    """

    global speed
    global angle
    global cur_state

    # Have the car begin at a stop
    rc.drive.stop()
    speed = 0
    angle = 0
    cur_state = State.see_marker


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """

    global speed
    global angle
    global cur_state

    scan = rc.lidar.get_samples()
    _, fr_dist = rc_utils.get_lidar_closest_point(scan, FRONT_RIGHT_WINDOW)
    _, fl_dist = rc_utils.get_lidar_closest_point(scan, FRONT_LEFT_WINDOW)


    color_image = rc.camera.get_color_image()
    markers = rc_utils.get_ar_markers(color_image)

    depth_image = rc.camera.get_depth_image()
    depth_image = (depth_image - 0.01) % 5000

    speed = 1

    if cur_state == State.see_marker:
        if len(markers) > 0 and rc_utils.get_pixel_average_distance(depth_image, markers[0].get_corners()[0], 11) < 120 and markers[0].get_orientation().value != 0:
            cur_state = State.follow_marker
        else:
            if fr_dist > 150:
                angle = 0.4
            elif fl_dist > 150:
                angle = -0.4
            else:
                angle = 0

    elif cur_state == State.follow_marker:
        if len(markers) > 0:
            if markers[0].get_orientation().value == 1:
                angle = -0.75
            elif markers[0].get_orientation().value == 3:
                angle = 0.75
        else:
            cur_state = State.search

    elif cur_state == State.search:
        if len(markers) > 0:
            cur_state = State.see_marker
        else:
            if fr_dist > 120 or fl_dist < 45:
                angle = 0.7
            elif fl_dist > 120 or fr_dist < 45:
                angle = -0.7
            else:
                angle = 0

    



    rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
