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
    seal_deform = round(random.uniform(0, 1), 4)
    tab_deform = round(random.uniform(0, seal_deform), 4)
    utils.setKeyValue("Seal", seal_deform, "Can")
    utils.setKeyValue("Tab", tab_deform, "Can")
    displace_1= random.uniform(0, 1)
    displace_2= random.uniform(0, 1)
    displace_3= random.uniform(0, 1)
    normal_scale=displace_1+displace_2+displace_3
    displace_1=displace_1/normal_scale
    displace_2=displace_2/normal_scale
    displace_3=displace_3/normal_scale
    random_normal_scale=random.uniform(0.6, 1)
    displace_1=displace_1*random_normal_scale
    displace_2=displace_2*random_normal_scale
    displace_3=displace_3*random_normal_scale
    utils.setKeyValue("Displace_1", displace_1, "Can")
    utils.setKeyValue("Displace_2", displace_2, "Can")
    utils.setKeyValue("Displace_3", displace_3, "Can")
    #shrink=["Shrink_1", "Shrink_2", "Shrink_3"]
    #twist=["Twist_1"]
    #fold=["Fold_1", "Fold_2", "Fold_3"]
    #pinch=["Pinch_1", "Pinch_2"]
    #crinkle=["Crinkle_1", "Crinkle_2", "Crinkle_3"]
    deformations=["shrink", "fold", "pinch", "crinkle"] #["shrink", "twist", "fold", "pinch", "crinkle"]
    num_elements = min(2, len(deformations))
    selections=random.sample(deformations, num_elements)
    shrinkval=0; twistval=0; foldval=0; pinchval=0; crinkleval=0
    for select in selections:
        if select=="shrink":
            shrinkval=random.uniform(0.3,1)
        if select=="twist":
            twistval=random.uniform(0.3,1)
        if select=="fold":
            foldval=random.uniform(0.3,1)
        if select=="pinch":
            pinchval=random.uniform(0.3,1)
        if select=="crinkle":
            crinkleval=random.uniform(0.3,1)

    norm=shrinkval+twistval+foldval+pinchval+crinkleval
    shrinkval=shrinkval/norm
    twistval=twistval/norm
    foldval=foldval/norm
    pinchval=pinchval/norm
    crinkleval=crinkleval/norm
    extent=random.uniform(0.7, 1.5)

    shrinkval=shrinkval*extent
    twistval=twistval*extent
    foldval=foldval*extent
    pinchval=pinchval*extent
    crinkleval=crinkleval*extent

    if "shrink" in selections:
        shrink_1=random.uniform(0,1)
        shrink_2=random.uniform(0,1)
        shrink_3=random.uniform(0,1)
        norm=shrink_1+shrink_2+shrink_3
        shrink_1 = shrink_1/norm
        shrink_2 = shrink_2/norm
        shrink_3 = shrink_3/norm
        shrink_1 = shrink_1*shrinkval
        shrink_2 = shrink_2*shrinkval
        shrink_3 = shrink_3*shrinkval
        utils.setKeyValue("Shrink_1", shrink_1, "Lattice")
        utils.setKeyValue("Shrink_2", shrink_2, "Lattice")
        utils.setKeyValue("Shrink_3", shrink_3, "Lattice")

    if "twist" in selections:
        twist_1=random.uniform(0,1)
        twist_1=twist_1*twistval
        utils.setKeyValue("Twist_1", twist_1, "Lattice")

    if "fold" in selections:
        fold_1=random.uniform(0,1)
        fold_2=random.uniform(0,1)
        fold_3=random.uniform(0,1)
        norm=fold_1+fold_2+fold_3
        fold_1=fold_1/norm
        fold_2=fold_2/norm
        fold_3=fold_3/norm
        fold_1=fold_1*foldval
        fold_2=fold_2*foldval
        fold_3=fold_3*foldval
        utils.setKeyValue("Fold_1", fold_1, "Lattice")
        utils.setKeyValue("Fold_2", fold_2, "Lattice")
        utils.setKeyValue("Fold_3", fold_3, "Lattice")

    if "pinch" in selections:
        choice=random.uniform(0, 1)
        if choice>0.5:
            pinch_1=random.uniform(0,1)
            pinch_2=0
            pinch_1=pinch_1*pinchval
        else:
            pinch_1=0
            pinch_2=random.uniform(0,1)
            pinch_2=pinch_2*pinchval
        utils.setKeyValue("Pinch_1", pinch_1, "Lattice")
        utils.setKeyValue("Pinch_2", pinch_2, "Lattice")

    if "crinkle" in selections:
        crinkle_1=random.uniform(0,1)
        crinkle_2=random.uniform(0,1)
        crinkle_3=random.uniform(0,1)
        norm=crinkle_1+crinkle_2+crinkle_3
        crinkle_1=crinkle_1/norm
        crinkle_2=crinkle_2/norm
        crinkle_3=crinkle_3/norm
        crinkle_1=crinkle_1*crinkleval
        crinkle_2=crinkle_2*crinkleval
        crinkle_3=crinkle_3*crinkleval
        utils.setKeyValue("Crinkle_1", crinkle_1, "Lattice")
        utils.setKeyValue("Crinkle_2", crinkle_2, "Lattice")
        utils.setKeyValue("Crinkle_3", crinkle_3, "Lattice")

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
    bpy.context.scene.render.film_transparent = True
    utils.capture(pub, i, image_x, image_y)
    # Delete Cameras
    utils.Delete_All_Cameras()
    utils.setKeyValue("Seal", 0, "Can")
    utils.setKeyValue("Tab", 0, "Can")
    utils.setKeyValue("Displace_1", 0, "Can")
    utils.setKeyValue("Displace_2", 0, "Can")
    utils.setKeyValue("Displace_3", 0, "Can")
    utils.setKeyValue("Shrink_1", 0, "Lattice")
    utils.setKeyValue("Shrink_2", 0, "Lattice")
    utils.setKeyValue("Shrink_3", 0, "Lattice")
    utils.setKeyValue("Twist_1", 0, "Lattice")
    utils.setKeyValue("Fold_1", 0, "Lattice")
    utils.setKeyValue("Fold_2", 0, "Lattice")
    utils.setKeyValue("Fold_3", 0, "Lattice")
    utils.setKeyValue("Pinch_1", 0, "Lattice")
    utils.setKeyValue("Pinch_2", 0, "Lattice")
    utils.setKeyValue("Crinkle_1", 0, "Lattice")
    utils.setKeyValue("Crinkle_2", 0, "Lattice")
    utils.setKeyValue("Crinkle_3", 0, "Lattice")


def main():
    bt_args, remainder = btb.parse_blendtorch_args()
    pub = btb.DataPublisher(bt_args.btsockets["DATA"], bt_args.btid)
    number_of_views = 3000
    rad_min = 0.3  # meters
    rad_max = 0.45
    theta_range = 50  # degrees
    phi_max = 70  # degrees
    phi_min = 50

    print("Creating Cams")
    for i in range(int(number_of_views+4 / 4)):
        CreateScenario(rad_min, rad_max, theta_range, phi_min, phi_max, i, pub, image_x=512, image_y=512)
main()
