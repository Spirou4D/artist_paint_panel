# -*- coding: utf8 -*-
# python
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

bl_info = {"name": "Artist Paint Menu",
            "author": "CDMJ, Spirou4D",
            "version": (1, 0),
            "blender": (2, 76, 0),
            "location": "",
            "description": "shortcut menu for Artist Panel addon",
            "warning": "",
            "wiki_url": "",
            "category": "Paint"}

import bpy

class canvasMenu(bpy.types.Menu):
    bl_label = "Artist Paint Menu"
    bl_idname = "view3D.canvas_menu"

    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings
        ipaint = context.tool_settings.image_paint

        layout.prop(ipaint, "use_stencil_layer",
                        text="Use stencil mask")

        col = layout.column(align = True)
        if ipaint.use_stencil_layer==True:
            #col.template_ID(ipaint, "stencil_image")
            #col.operator("image.new", text="New").\
                                #gen_context = 'PAINT_STENCIL'
            col.prop(ipaint, "invert_stencil",
                    text="Invert the mask")

        layout.operator("artist_panel.canvas_horizontal",
                text="Canvas Flip Horizontal",icon='ARROW_LEFTRIGHT')
        layout.operator("artist_panel.canvas_vertical",
                text = "Canvas Flip Vertical", icon = 'FILE_PARENT')
        layout.operator("artist_panel.rotate_ccw_15",
                text = "Rotate 15° CCW", icon = 'TRIA_LEFT')
        layout.operator("artist_panel.rotate_cw_15",
                text = "Rotate 15° CW", icon = 'TRIA_RIGHT')
        layout.operator("artist_panel.rotate_ccw_90",
                text = "Rotate 90° CCW", icon = 'PREV_KEYFRAME')
        layout.operator("artist_panel.rotate_cw_90",
                text = "Rotate 90° CW", icon = 'NEXT_KEYFRAME')
        layout.operator("artist_panel.canvas_resetrot",
                text = "Reset Rotation", icon = 'CANCEL')


def register():
    bpy.utils.register_module(__name__)

    km_list = ['Image Paint']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        kmi = km.keymap_items.new('wm.call_menu', 'C', 'PRESS')
        kmi.properties.name = "view3D.canvas_menu"

def unregister():
    bpy.utils.unregister_module(__name__)

    km_list = ['Image Paint']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        for kmi in (kmi for kmi in km.keymap_items if (kmi.idname == "wm.call_menu" and kmi.properties.name == "view3D.canvas_menu")):
            km.keymap_items.remove(kmi)


if __name__ == "__main__":
    register()
