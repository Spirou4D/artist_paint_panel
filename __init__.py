# -*- coding: utf8 -*-
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {"name": "Paint Artist Panel",
           "author": "CDMJ, Spirou4D",
           "version": (1, 0, 5),
           "blender": (2, 76, 0),
           "location": "Toolbar > Misc Tab > Artist Panel",
           "description": "Art Macros.",
           "warning": "Run only in BI now",
           "category": "Paint"}

import bpy

'''
Modif: 2016-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Modif: 2016-02'01 Patrick optimize the code
'''


#-------------------------------------------------reload image
class ImageReload(bpy.types.Operator):
    """Reload Image Last Saved State"""
    bl_idname = "image.reload_saved_state"
    bl_label = "Reload Image Save Point"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene
        original_type = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        #return image to last saved state
        bpy.ops.image.reload()
        bpy.context.area.type = original_type
        return {'FINISHED'}


#-------------------------------------------------image save
class SaveImage(bpy.types.Operator):
    """Save Image"""
    bl_idname = "image.save_current"
    bl_label = "Save Image Current"
    bl_options = { 'REGISTER', 'UNDO' }


    def execute(self, context):
        scene = context.scene
        original_type = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        #return image to last saved state
        bpy.ops.image.save_dirty()
        bpy.context.area.type = original_type
        return {'FINISHED'}


#--------------------------------------------------Create brush
class BrushMakerScene(bpy.types.Operator):
    """Create Brush Scene"""
    bl_idname = "scene.create_brush_scene"
    bl_label = "Create Scene for Image Brush Maker"
    bl_options = { 'REGISTER', 'UNDO' }

    @classmethod
    def poll(self, context):
        #   A sub-function that controls the use of the class
        notBScene = True
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                notBScene = False
        return context.area.type=='VIEW_3D'and notBScene


    def execute(self, context):
        _name="Brush"
        for sc in bpy.data.scenes:
            if sc.name == "Brush":
                return {'FINISHED'}

        #add new scene and name it 'Brush'
        bpy.ops.scene.new(type='NEW')
        context.scene.name = _name

        #add lamp and move up 4 units in z
        # you can sort elements like this if the code
        # is gettings long
        bpy.ops.object.lamp_add(
                    type = 'POINT',
                    radius = 1,
                    view_align = False,
                    location = (0, 0, 4)
                    )

        #add camera to center and move up 4 units in Z
        bpy.ops.object.camera_add(
                    view_align=False,
                    enter_editmode=False,
                    location=(0, 0, 4),
                    rotation=(0, 0, 0)
                    )

        #rename selected camera
        context.object.name="Tex Camera"

        #change scene size to 1K
        _RenderScene = context.scene.render
        _RenderScene.resolution_x=1024
        _RenderScene.resolution_y=1024
        _RenderScene.resolution_percentage = 100

        #save scene size as preset
        bpy.ops.render.preset_add(name = "1K Texture")

        #change to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after the first ran
        return {'FINISHED'}


#--------------------------------------------------Shaderless
class CanvasShadeless(bpy.types.Operator):
    """Canvas made shadeless Macro"""
    bl_idname = "image.canvas_shadeless"
    bl_label = "Canvas Shadeless"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        #texture draw mode
        context.space_data.viewport_shade = 'TEXTURED'

        #shadeless material
        context.object.active_material.use_shadeless = True

        #change to local view
        bpy.ops.view3d.localview()

        #change to Texture Paint
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cameraview paint
class CameraviewPaint(bpy.types.Operator):
    """Create a front-of camera in painting mode"""
    bl_idname = "image.cameraview_paint"
    bl_label = "Cameraview Paint"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        #toggle on/off textpaint
        obj = context.active_object

        if obj:
            mode = obj.mode
            if mode == 'TEXTURE_PAINT':
                bpy.ops.paint.texture_paint_toggle()

        #save selected plane by rename
        context.object.name = "canvas"

        #variable to get image texture dimensions -
        #thanks to Mutant Bob
        #http://blender.stackexchange.com/users/660/mutant-bob
        select_mat = obj.data.materials[0].texture_slots[0].\
                    texture.image.size[:]

        #add camera
        bpy.ops.object.camera_add(view_align=False,
                    enter_editmode=False,
                    location=(0, 0, 0),
                    rotation=(0, 0, 0),
                    layers=(True, False, False, False, False, False,
                    False, False,False, False, False, False, False,
                    False, False, False, False,False, False, False))

        #ratio full
        bpy.context.scene.render.resolution_percentage = 100

        #name it
        context.object.name = "Canvas View Paint"

        #switch to camera view
        bpy.ops.view3d.object_as_camera()

        #ortho view on current camera
        context.object.data.type = 'ORTHO'

        #move cam up in Z by 1 unit
        bpy.ops.transform.translate(value=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #switch on composition guides for use in cameraview paint
        context.object.data.show_guide = {'CENTER',
                            'CENTER_DIAGONAL', 'THIRDS', 'GOLDEN',
                            'GOLDEN_TRIANGLE_A', 'GOLDEN_TRIANGLE_B',
                            'HARMONY_TRIANGLE_A', 'HARMONY_TRIANGLE_B'
                            }

        #found on net Atom wrote this simple script
        #image_index = 0
        rnd = bpy.data.scenes[0].render
        rnd.resolution_x, rnd.resolution_y = select_mat

        #resolution
        rndx = rnd.resolution_x
        rndy = rnd.resolution_y

        #orthoscale = ((rndx - rndy)/rndy)+1
        if rndx >= rndy:
            orthoscale = ((rndx - rndy)/rndy)+1
        elif rndx < rndy:
            orthoscale = 1
        context.object.data.ortho_scale = orthoscale
        context.selectable_objects

        #deselect camera
        bpy.ops.object.select_all(action='TOGGLE')

        #select plane
        bpy.ops.object.select_all(action='DESELECT')
        ob = bpy.data.objects["canvas"]
        ob.select = True
        context.scene.objects.active = ob

        #selection to texpaint toggle
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip  horiz. macro
class CanvasHoriz(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "image.canvas_horizontal"
    bl_label = "Canvas horiz"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #flip canvas horizontal
        bpy.ops.transform.resize(value=(-1, 1, 1),
                            constraint_axis=(True, False, False),
                            constraint_orientation='GLOBAL',
                            mirror=False, proportional='DISABLED',
                            proportional_edit_falloff='SMOOTH',
                            proportional_size=1 )

        #toggle object to texture
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#--------------------------------------------------flip vertical macro
class CanvasVertical(bpy.types.Operator):
    """Canvas Flip Vertical Macro"""
    bl_idname = "image.canvas_vertical"
    bl_label = "Canvas Vertical"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()

        #flip canvas horizontal
        bpy.ops.transform.resize(value=(1, -1, 1),
                    constraint_axis=(False, True, False),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw15
class RotateCanvasCCW15(bpy.types.Operator):
    """Image Rotate CounterClockwise 15 Macro"""
    bl_idname = "image.rotate_ccw_15"
    bl_label = "Canvas Rotate CounterClockwise 15"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=0.261799,
                        axis=(0, 0, 1),
                        constraint_axis=(False, False, True),
                        constraint_orientation='GLOBAL',
                        mirror=False,
                        proportional='DISABLED',
                        proportional_edit_falloff='SMOOTH',
                        proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw15
class RotateCanvasCW15(bpy.types.Operator):
    """Image Rotate Clockwise 15 Macro"""
    bl_idname = "image.rotate_cw_15"
    bl_label = "Canvas Rotate Clockwise 15"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=-0.261799,
                axis=(0, 0, 1),
                constraint_axis=(False, False, True),
                constraint_orientation='GLOBAL',
                mirror=False,
                proportional='DISABLED',
                proportional_edit_falloff='SMOOTH',
                proportional_size=1)

        #toggle texture mode/object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------ccw 90
class RotateCanvasCCW(bpy.types.Operator):
    """Image Rotate CounterClockwise 90 Macro"""
    bl_idname = "image.rotate_ccw_90"
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=1.5708,
                    axis=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}


#-------------------------------------------------cw 90
class RotateCanvasCW(bpy.types.Operator):
    """Image Rotate Clockwise 90 Macro"""
    bl_idname = "image.rotate_cw_90"
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        scene = context.scene

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=-1.5708,
                    axis=(0, 0, 1),
                    constraint_axis=(False, False, True),
                    constraint_orientation='GLOBAL',
                    mirror=False,
                    proportional='DISABLED',
                    proportional_edit_falloff='SMOOTH',
                    proportional_size=1)

        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}



#-------------------------------------------------image rotation reset
class CanvasResetrot(bpy.types.Operator):
    """Canvas Rotation Reset Macro"""
    bl_idname = "image.canvas_resetrot"
    bl_label = "Canvas Reset Rotation"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        scene = context.scene

        #reset canvas rotation
        bpy.ops.object.rotation_clear()
        return {'FINISHED'}





##############################################################  panel
class ArtistPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Artist Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Artist Macros"

    @classmethod
    def poll(self, cls):
        return bpy.context.scene.render.engine == 'BLENDER_RENDER'

    def draw(self, context):
        layout = self.layout

        row = layout.row()  #INIT
        row.label(text="Image State")
        row = layout.row()
        row.operator("import_image.to_plane",
                    text = "Import Image as plane", icon = 'IMAGE_COL')
        row = layout.row()
        row.operator("image.reload_saved_state",
                    text = "Reload Image", icon = 'LOAD_FACTORY')
        row = layout.row()
        row.operator("image.save_current",
                    text = "Save Image", icon = 'IMAGEFILE')
        row = layout.row()
        row.operator("scene.create_brush_scene",
                text="Create Brush Maker Scene",
                icon='OUTLINER_OB_CAMERA')


        row = layout.row()  #MACRO
        row.label(text="Special Macros")
        row = layout.row()
        row.operator("image.canvas_shadeless",
                    text = "Shadeless Canvas", icon = 'FORCE_TEXTURE')
        row = layout.row()
        row.operator("image.cameraview_paint",
                    text = "Add Painting Camera",
                    icon = 'RENDER_REGION')

        row = layout.row()  #FLIP
        row.label(text="Flip")
        row = layout.row()
        row.operator("image.canvas_horizontal",
                    text="Canvas Flip Horizontal",
                    icon='ARROW_LEFTRIGHT')
        row = layout.row()
        row.operator("image.canvas_vertical",
                    text = "Canvas Flip Vertical",
                    icon = 'FILE_PARENT')

        row = layout.row()  #ROTATION
        row.label(text="Rotation")
        row = layout.row()
        row.operator("image.rotate_ccw_15",
                    text = "Rotate 15 CCW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_cw_15",
                    text = "Rotate 15 CW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_ccw_90",
                    text = "Rotate 90 CCW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.rotate_cw_90",
                    text = "Rotate 90 CW", icon = 'MAN_ROT')
        row = layout.row()
        row.operator("image.canvas_resetrot",
                    text = "Reset Rotation", icon = 'CANCEL')



def register():
    bpy.utils.register_class(ImageReload)
    bpy.utils.register_class(SaveImage)
    bpy.utils.register_class(BrushMakerScene)
    bpy.utils.register_class(CanvasShadeless)
    bpy.utils.register_class(CameraviewPaint)
    bpy.utils.register_class(CanvasHoriz)
    bpy.utils.register_class(CanvasVertical)
    bpy.utils.register_class(RotateCanvasCCW15)
    bpy.utils.register_class(RotateCanvasCW15)
    bpy.utils.register_class(RotateCanvasCCW)
    bpy.utils.register_class(RotateCanvasCW)
    bpy.utils.register_class(CanvasResetrot)
    bpy.utils.register_class(ArtistPanel)

def unregister():
    bpy.utils.unregister_class(ArtistPanel)
    bpy.utils.unregister_class(CanvasResetrot)
    bpy.utils.unregister_class(RotateCanvasCW)
    bpy.utils.unregister_class(RotateCanvasCCW)
    bpy.utils.unregister_class(RotateCanvasCW15)
    bpy.utils.unregister_class(RotateCanvasCCW15)
    bpy.utils.unregister_class(CanvasVertical)
    bpy.utils.unregister_class(CanvasHoriz)
    bpy.utils.unregister_class(CameraviewPaint)
    bpy.utils.unregister_class(CanvasShadeless)
    bpy.utils.unregister_class(BrushMakerScene)
    bpy.utils.unregister_class(SaveImage)
    bpy.utils.unregister_class(ImageReload)

if __name__ == "__main__":
    register()
