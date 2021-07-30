### BWSI 2021 Grandprix Team CocaCola
#newtest
### BWSI 2021 Grandprix Team CocaCola
import sys
from typing import Tuple
import cv2 as cv
import numpy as np
from numpy.lib.utils import _set_function_name
from numpy.testing._private.utils import jiffies

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
import custom_funcs as rc_cf
from enum import IntEnum
import math

rc = racecar_core.create_racecar()

class State(IntEnum) :
    green_line_follow = 0
    challenge1 = 1
    challenge2 = 2
    challenge3 = 3
    challenge4 = 4
    challenge5 = 5
    challenge6 = 6
    challenge7 = 7
    challenge8 = 8

robotState = State.green_line_follow


#VARIABLES GO HERE

#Variables for green line follow
timer = 0.0
MIN_CONTOUR_AREA = 30
# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))

BLUE = ((90, 200, 200), (120, 255, 255), "blue")  # The HSV range for the color blue
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")
ORANGE = ((15,230,230), (35,255,255,),"orange")
PURPLE = ((125,200,200),(140,255,255), "purple")

AR_ORANGE = ((10,20,20), (40,255,255),"orange")
AR_PURPLE = ((110,20,20),(140,255,255), "purple")


contour_center = None  # The (pixel row, pixel column) of contour
green_contours = None
image = None
depth_image = None
scan = None
color_image = None
marker = None

#Challenge 2
CROP_FLOOR_2 = ((300, 0), (rc.camera.get_height(), rc.camera.get_width()))
right_center = [0,0]
left_center = [0,0]
counter = 0
center = [0,0]
#Challenge 3
FRONT_WINDOW = (-10, 10)
FRONT_RIGHT_WINDOW = (30, 40)
FRONT_LEFT_WINDOW = (320, 330)
RIGHT_WINDOW = (65, 70)
LEFT_WINDOW = (285, 290)

class Challenge3State(IntEnum):
        see_marker = 0
        follow_marker = 1
        search = 2

cur_state = Challenge3State.search

#Challenge 4
ar_color = None

#Challenge 6
FRONT_WINDOW_6 = (-20, 20)
detected_obstacle_time = 0.0
detected_obstacle = False
forward_dist = None

#Drive Function
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels

def start():
    global robotState
    rc.drive.set_max_speed(0.5)
    rc.drive.stop()
    robotState = State.green_line_follow

    print("Team Cocacola Grand Prix Challenge!")

def update():
    global speed, angle, robotState, scan, color_image, timer, depth_image, marker, contour_center, ar_color
    timer += rc.get_delta_time()
    color_image = rc.camera.get_color_image()
    depth_image = rc.camera.get_depth_image()
    depth_image = (depth_image - 0.01) % 10000
    scan = rc.lidar.get_samples()
    markers = rc_utils.get_ar_markers(color_image)

    #DO NOT TOUCH#######################################################
    # if color_image is None:
    #     contour_center = None
    #     contour_area = 0

    # else:
    #     image = rc_utils.crop(color_image, CROP_FLOOR[0], CROP_FLOOR[1])
    #     green_contours = rc_utils.find_contours(image, GREEN[0], GREEN[1])
    #     contour = rc_utils.get_largest_contour(green_contours, MIN_CONTOUR_AREA)
    #     if contour is not None:
    #         contour_center = rc_utils.get_contour_center(contour)
    #         contour_area = rc_utils.get_contour_area(contour)
    #         rc_utils.draw_contour(image, contour)
    #         rc_utils.draw_circle(image, contour_center)
    #     else:
    #         contour_center = None
    #         contour_area = 0
    image = rc_utils.crop(color_image, CROP_FLOOR[0], CROP_FLOOR[1])
    contour_center = rc_cf.get_contour_info(color_image,GREEN[0], GREEN[1],CROP_FLOOR)[0]
    rc.display.show_color_image(image)
    
    #DO NOT TOUCH#######################################################

    

    if robotState == State.green_line_follow:
        green_line_follow()
    if robotState == State.challenge1:
        challenge1() 
    elif robotState ==State.challenge2:
        if ar_color == "orange": challenge2(ORANGE)
        elif ar_color == "purple": challenge2(PURPLE)
    elif robotState == State.challenge3:
        challenge3()
    elif robotState == State.challenge4:
        challenge4(ar_color)
    elif robotState == State.challenge6:
        challenge6()

    for marker in markers:
        id = marker.get_id()
        marker.detect_colors(color_image, [BLUE, RED, GREEN,AR_ORANGE,AR_PURPLE])
        color = marker.get_color()
        orientation = marker.get_orientation()
        marker_top, marker_left = marker.get_corners()[marker.get_orientation().value]
        marker_bottom, marker_right = marker.get_corners()[(marker.get_orientation().value + 2) % 4]
        ar_center = ( marker_top + (marker_bottom-marker_top)//2, marker_left + (marker_right-marker_left)//2)
        ar_dis = depth_image[ar_center]
        if id is not None:
            # print(id)
            #print(ar_center)
            # print(ar_dis)
            #print(color)
            #print(orientation)
            if id == 0 and ar_dis < 60:
                robotState = State.challenge1
                timer = 0
            elif id == 1 and ar_dis < 100:
                robotState = State.challenge2
                ar_color = color
            elif id == 3 and ar_dis < 300:
                robotState = State.challenge4
                ar_color = color
                timer = 0
            elif id == 199 and ar_dis < 200:
                robotState = State.challenge3
                timer = 0
            elif id == 5 and ar_dis < 60:
                robotState = State.challenge6
                timer = 0
    # print(forward_dist)
    rc.drive.set_speed_angle(speed, angle)


def green_line_follow():
    global contour_center,angle,speed, color_image, image, green_contours
    
    if contour_center is not None:
        #error = contour_center[1] - rc.camera.get_width() / 2
        #angle = 2 * error/rc.camera.get_width()

        angle = rc_utils.remap_range(contour_center[1], 0, rc.camera.get_width(), -1, 1)

        max_speed = 0.6
        min_speed = 0.3
        speed = math.cos(0.5 * math.pi * angle) * max_speed + min_speed

        speed = rc_utils.clamp(speed, -0.5, 0.6)

def challenge1():
    global scan, green_contours, image, robotState, marker, speed, angle, timer, contour_center
    RIGHT_WINDOW = (32,38)
    LEFT_WINDOW = (322,328)

    _, right_dis = rc_utils.get_lidar_closest_point(scan, RIGHT_WINDOW)
    _, left_dis = rc_utils.get_lidar_closest_point(scan, LEFT_WINDOW)
    

    kP = 0.01
    error = right_dis - left_dis
    angle = kP * error

    angle = rc_utils.clamp(angle, -1, 1)

    max_speed = 0.6
    min_speed = 0.4
    speed = math.cos(0.5 * math.pi * angle) * max_speed + min_speed

    speed = rc_utils.clamp(speed, -0.5, 0.6)

    if contour_center is not None and timer > 5.0:
        robotState = State.green_line_follow

def challenge2(path_color):
    global speed, angle
    global right_center, left_center
    global PURPLE, ORANGE, CROP_FLOOR
    global counter, robotState

    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, CROP_FLOOR_2[0], CROP_FLOOR_2[1])

    purple_contours = rc_utils.find_contours(cropped_image, PURPLE[0], PURPLE[1])
    orange_contours = rc_utils.find_contours(cropped_image, ORANGE[0], ORANGE[1])
    
    color = [[],[]]

    if path_color == PURPLE:
        if orange_contours:
            color = ORANGE
        else: 
            color = PURPLE

    elif path_color == ORANGE:
        if purple_contours:
            color = PURPLE
        else:
            color = ORANGE
    
    contours = rc_cf.get_n_contour_info(2,image,color[0],color[1], CROP_FLOOR)
    if contours:
        if len(contours) >= 1:
            if contours[0] and contours[0][1]:
                right_center = contours[0][1]

        if len(contours) == 2:
            if contours [1] and contours[1][1]:
                left_center = contours[1][1]

    center = [(right_center[0] + left_center[0]) // 2, (right_center[1] + left_center[1])//2]

    speed = 0.5
    angle = rc_utils.remap_range(center[1],0,rc.camera.get_width(),-1,1,True)

    if color is not path_color:
        angle = 1
        speed = 0.5
        counter+=rc.get_delta_time()
        if counter > 1.55:
            angle = 1
        if counter > 2.5:
            angle = 0
        if counter > 3:
            angle = -1
        if counter > 3.75:
            angle = 0
        if counter > 4:
            robotState = State.green_line_follow
    print(angle,counter)
    
def challenge3():
    global speed, angle
    global cur_state, FRONT_LEFT_WINDOW, FRONT_RIGHT_WINDOW, depth_image, color_image,robotState, timer, contour_center

    scan = rc.lidar.get_samples()
    _, fr_dist = rc_utils.get_lidar_closest_point(scan, FRONT_RIGHT_WINDOW)
    _, fl_dist = rc_utils.get_lidar_closest_point(scan, FRONT_LEFT_WINDOW)

    markers = rc_utils.get_ar_markers(color_image)


    if cur_state == Challenge3State.see_marker:
        if len(markers) > 0 and rc_utils.get_pixel_average_distance(depth_image, markers[0].get_corners()[0], 11) < 120 and markers[0].get_orientation().value != 0:
            cur_state = Challenge3State.follow_marker
        else:
            if fr_dist > 150:
                angle = 0.4
            elif fl_dist > 150:
                angle = -0.4
            else:
                angle = 0

    elif cur_state == Challenge3State.follow_marker:
        if len(markers) > 0:
            if markers[0].get_orientation().value == 1:
                angle = -0.75
            elif markers[0].get_orientation().value == 3:
                angle = 0.75
        else:
            cur_state = Challenge3State.search

    elif cur_state == Challenge3State.search:
        if len(markers) > 0:
            cur_state = Challenge3State.see_marker
        else:
            if fr_dist > 120 or fl_dist < 45:
                angle = 0.7
            elif fl_dist > 120 or fr_dist < 45:
                angle = -0.7
            else:
                angle = 0
    
    if contour_center is not None and timer > 5.0:
        robotState = State.green_line_follow

def challenge4(ar_color):
    global speed, angle, timer, scan, contour_center, robotState
    _, front_dis = rc_utils.get_lidar_closest_point(scan, (-10, 10))
    speed = 0.5
    angle = 0
    print(front_dis)
    print(ar_color)

    if ar_color == "red" and front_dis < 300:
        speed = 0
        angle = 0
    elif ar_color == "blue" and front_dis > 40:
        speed = 0.5
        angle = 0
    elif ar_color == "blue" and front_dis < 40:
        speed = 0
        angle = 0
    
    if contour_center is not None and timer > 5.0:
        robotState = State.green_line_follow

def challenge6():
    global speed, angle, timer, detected_obstacle, detected_obstacle_time, scan, FRONT_WINDOW, forward_dist
    forward_dist = rc_utils.get_lidar_average_distance(scan, 0.0, 30.0)
    print(forward_dist)
    angle = 0
    speed = 1

    if speed > 0 and forward_dist < 160:
        if not detected_obstacle:
            detected_obstacle = True
            detected_obstacle_time = timer
        if timer - detected_obstacle_time < 0.5:
            speed = -1
        else:
            speed = 0
    elif forward_dist > 160:
        speed = 1
        detected_obstacle = False
        detected_obstacle_time = 0.0

def update_slow():
    global robotState
    print(robotState)    


if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
