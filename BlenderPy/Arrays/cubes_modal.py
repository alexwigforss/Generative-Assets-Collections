bl_info = {
    "name": "Add Cubes",
    "description": "Adds a cube to the 3D View",
    "author": "Alexander Wigforss",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Cubes",
    "category": "3D View",
}

import bpy

fields = [[[True,True,True],
          [True,True,True],
          [True,True,True]
          ],
         [[True,True,True],
          [True,False,True],
          [True,True,True]
          ],
         [[True,True,True],
          [True,True,True],
          [True,True,True]
          ],]

class AddCubesOperator(bpy.types.Operator):
    """Add a cube into the scene"""
    bl_idname = "mesh.add_cubes"
    bl_label = "Add Cubes"

    def execute(self, context):
        global fields
        for f in enumerate(fields):
            for row in enumerate(f[1]):
                for slot in enumerate(row[1]):
                    if slot[1] == True:
                        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(slot[0], row[0], f[0]))
                        
        #z_index += 2
        return {'FINISHED'}

# Modal operator to add cubes with a delay
import time

class AddCubesModalOperator(bpy.types.Operator):
    """Add cubes one by one with a delay"""
    bl_idname = "mesh.add_cubes_modal"
    bl_label = "Add Cubes (Modal)"

    _timer = None
    _positions = None
    _index = 0

    def invoke(self, context, event):
        global fields
        # Gather all positions where True
        self._positions = []
        for z, field in enumerate(fields):
            for y, row in enumerate(field):
                for x, val in enumerate(row):
                    if val:
                        self._positions.append((x, y, z))
        self._index = 0
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)  # 0.3 seconds delay
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._index < len(self._positions):
                pos = self._positions[self._index]
                bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=pos)
                self._index += 1
                return {'RUNNING_MODAL'}
            else:
                # Done, remove timer
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}
        return {'PASS_THROUGH'}

class AddMaterialOperator(bpy.types.Operator):
    """Add a material into the scene"""
    bl_idname = "mesh.add_material"
    bl_label = "Add Material"
    
    def execute(self,context):
        obj = context.object

        # Create a new material with nodes
        material = bpy.data.materials.new(name="Node Material")
        material.use_nodes = True

        # Set base color of Principled BSDF
        principled = material.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = (0.2, 0.6, 1.0, 1.0)  # Light blue

        # Assign to mesh
        if obj.type == 'MESH':
            mesh = obj.data
            mesh.materials.clear()
            mesh.materials.append(material)
        
        return {'FINISHED'}
        
class SamplePanel(bpy.types.Panel):
    """ Displayy panel in 3D view"""
    bl_label = "Sample Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        # MORE Icons
        # https://docs.blender.org/api/current/bpy_types_enum_items/icon_items.html#rna-enum-icon-items
        col.operator("mesh.add_cubes_modal", icon="MESH_CUBE")
        col.operator("mesh.add_material", icon="SHADING_RENDERED")

classes = (
    SamplePanel,
    AddCubesModalOperator,
    AddMaterialOperator,
)
    

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()