import math
import os
import random
from mathutils import Vector
import argparse
import blendtorch.btb as btb
import bpy
import collections
import json
import utils

def CreateScenario(rad_min, rad_max, theta_range, phi_min, phi_max, i, pub, image_x, image_y):
    utils.set_lighting()
    tab_deform= round(random.uniform(0, 0.6))
    seal_deform = round(random.uniform(tab_deform, 1), 4)
    utils.setKeyValue("Tab", tab_deform, "Can")
    utils.setKeyValue("Seal", seal_deform, "Can")

    radius = random.uniform(rad_min, rad_max)
    theta = random.uniform(45 - theta_range / 2, 45 + theta_range / 2)
    phi = random.uniform(phi_min, phi_max)
    tracked_object = "Can"
    utils.newCam(radius, theta, phi, tracked_object, i)

    radius = random.uniform(rad_min, rad_max)
    theta = random.uniform(135 - theta_range / 2, 135 + theta_range / 2)
    phi = random.uniform(phi_min, phi_max)
    tracked_object = "Can"
    utils.newCam(radius, theta, phi, tracked_object, i)

    radius = random.uniform(rad_min, rad_max)
    theta = random.uniform(225 - theta_range / 2, 225 + theta_range / 2)
    phi = random.uniform(phi_min, phi_max)
    tracked_object = "Can"
    utils.newCam(radius, theta, phi, tracked_object, i)

    radius = random.uniform(rad_min, rad_max)
    theta = random.uniform(315 - theta_range / 2, 315 + theta_range / 2)
    phi = random.uniform(phi_min, phi_max)
    tracked_object = "Can"
    utils.newCam(radius, theta, phi, tracked_object, i)

    utils.capture(pub, i, image_x, image_y)
    # Delete Cameras
    utils.Delete_All_Cameras()
    utils.setKeyValue("Tab", 0, "Can")
    utils.setKeyValue("Seal", 0, "Can")

def main():
    bt_args, remainder = btb.parse_blendtorch_args()

    pub = btb.DataPublisher(bt_args.btsockets["DATA"], bt_args.btid)
    number_of_views = 3000
    rad_min=0.3     #meters
    rad_max=0.45
    theta_range=50  #degrees
    phi_max=70     #degrees
    phi_min=50

    print("Creating Cams")
    for i in range(int(number_of_views+4/4)):
        CreateScenario(rad_min,rad_max,theta_range,phi_min,phi_max,i,pub, image_x=512, image_y=512)

main()

#No response within timeout interval can be caused by new cameras taking too long to generate. Change constants.py in blendtorch package