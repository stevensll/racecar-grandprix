### BWSI 2021 Grandprix Team CocaCola
import sys
from typing import Tuple
import cv2 as cv
import numpy as np
from numpy.testing._private.utils import jiffies

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
from enum import IntEnum
import custom_funcs as rc_cf


rc = racecar_core.create_racecar()
class State(IntEnum) :
    challenge1 = 1
    challenge2 = 2

#VARIABLES GO HERE


########################################################################################
# CONSTANTS
########################################################################################


# Color HSV
CROP_FLOOR = ((300, 0), (rc.camera.get_height(), rc.camera.get_width()))
CROP_FLOOR_2 = (300, rc.camera.get_width()//2), (rc.camera.get_height(), rc.camera.get_width())
BLUE = ((90, 200, 200), (120, 255, 255), "blue")  
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")
ORANGE = ((15,230,230), (35,255,255,),"orange")
PURPLE = ((125,200,200),(140,255,255), "purple")


RIGHT_WINDOW = (32,38)
LEFT_WINDOW = (322,328)
timer = 0.0

MIN_CONTOUR_AREA = 30

speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels

right_center = [0,0]
left_center = [0,0]
counter = 0
center = [0,0]

def start():
    rc.drive.stop()
    print("Team Cocacola Grand Prix Challenge!")

def challenge9():
    global counter
    global speed
    global angle
    global center
    CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()//3))
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

    contours=rc_cf.get_n_contour_info(1, image, BLUE[0], BLUE[1], CROP_FLOOR)
    if contours:
        center = [contours[0][1][0], contours[0][1][1]-150]
    

    angle = rc_utils.remap_range(center[1],0, rc.camera.get_width(),-1,1, True)
    rc_utils.draw_circle(cropped_image, center)

    speed = 1
    rc.display.show_color_image(cropped_image)



def challenge2(path_color):
    global speed
    global angle
    global right_center
    global left_center
    global PURPLE
    global ORANGE

    global counter

    CROP_FLOOR = ((300, rc.camera.get_width()//2 ), (rc.camera.get_height(),rc.camera.get_width()))
    MULTIPLIER = 4
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])


    purple_center = rc_cf.get_contour_info(image, PURPLE[0], PURPLE[1], CROP_FLOOR)
    orange_center = rc_cf.get_contour_info(image, ORANGE[0], ORANGE[1], CROP_FLOOR)

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
    
    center,_,_ = rc_cf.get_contour_info(image,color[0],color[1], CROP_FLOOR)
    if path_color != color: 
        MULTIPLIER = 20

    if center is not None:
        angle = (center[1] - rc.camera.get_width() * 3/8 )  / rc.camera.get_width()  * MULTIPLIER
        print(angle)
        angle = rc_utils.clamp(angle, -1, 1) 
        rc_utils.draw_circle(cropped_image, center)

    speed = 0.45
    rc.display.show_color_image(cropped_image)


def update():
    global speed
    global angle
    global right_center
    global left_center
    global ORANGE
    global PURPLE
    global counter

    lt = rc.controller.Trigger.LEFT
    rt = rc.controller.Trigger.RIGHT
    speed = rc.controller.get_trigger(rt)-rc.controller.get_trigger(lt)
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    
    # challenge2(PURPLE)
    challenge2(PURPLE)
    rc.drive.set_max_speed(0.5)
    rc.drive.set_speed_angle(speed, angle)

    if rc.controller.is_down(rc.controller.Button.B):
        print(f"Speed: {speed} Angle: {angle} Counter: {counter}")
        # if green_center is None:
        #     print("No green contour found")
        # else:
        #     print(green_center, speed)
    
if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
