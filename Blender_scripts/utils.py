import math
import os
import random
from mathutils import Vector
import argparse
import blendtorch.btb as btb
import bpy
import collections
import json

def capture(publisher, views, image_x, image_y):
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.resolution_x = image_x
    bpy.context.scene.render.resolution_y = image_y
    # iterate over all objects
    print("Making image " + str(views*4) + "\r")
    for ob in bpy.context.scene.objects:
        # make sure object is a camera
        if ob.type == 'CAMERA':
            # capture camera's view
            bpy.context.scene.camera = ob
            btb_cam = btb.Camera(ob)
            osr = btb.OffScreenRenderer(camera=btb_cam, mode='rgba')
            osr.set_render_style(shading="RENDERED", overlays=False)
            publisher.publish(image=osr.render(), )

def newCam(radius, theta, phi, tracking_object, i):
    target_object = bpy.data.objects[tracking_object]

    radius = radius
    t = math.radians(theta)
    p = math.radians(phi)
    x=radius * math.sin(p) * math.cos(t)
    y=radius * math.sin(p) * math.sin(t)
    z=radius * math.cos(p)
    new_camera_pos = Vector((x, y, z))

    bpy.ops.object.camera_add(enter_editmode=False, location=new_camera_pos)
    track_to = bpy.context.object.constraints.new('TRACK_TO')
    track_to.target = target_object
    track_to.up_axis = 'UP_Y'

    bpy.context.scene.camera = bpy.context.object

def setKeyValue(KeyID, value, item):
    # get mesh of object
    # Select all objects in the scene to be deleted:
    for obj in bpy.data.objects:
        if obj.name == item:
            obj.select_set(True)
            # wiremesh = bpy.context.object

            for shape in obj.data.shape_keys.key_blocks:
                if (shape.name == KeyID):
                    shape.value = value
                    obj.data.shape_keys.key_blocks[KeyID].keyframe_insert("value", frame=1)

            break

def Delete_All_Cameras():
    for o in bpy.context.scene.objects:
        if o.type == "CAMERA":
            o.select_set(True)
        else:
            o.select_set(False)
    # Deletes all selected objects in the scene:

    bpy.ops.object.delete()

def set_lighting():
    folder=r'C:\Program Files\Blender Foundation\Blender 3.1\3.1\datafiles\studiolights\world'
    exr_files = [f for f in os.listdir(folder) if f.endswith('.exr')]
    rand_exr = random.choice(exr_files)
    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Environment Texture"].image = bpy.data.images.load(os.path.join(folder, rand_exr))
    world.node_tree.nodes['Value'].outputs[0].default_value = random.uniform(0.0, 2*3.14159)