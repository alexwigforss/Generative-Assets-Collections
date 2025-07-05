bl_info = {
    "name": "Add Cube",
    "description": "Adds a cube to the 3D View",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "category": "3D View",
}

import bpy

class AddCubeOperator(bpy.types.Operator):
    """Add a cube into the scene"""
    bl_idname = "mesh.add_cube"
    bl_label = "Add Cube"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        return {'FINISHED'}

class AddMaterialOperator(bpy.types.Operator):
    """Add a material into the scene"""
    bl_idname = "mesh.add_material"
    bl_label = "Add Material"
    
    def execute(self,context):
        bpy.ops.object.material_slot_add()
        default_material = bpy.data.materials.new(name='Sample Material')
        default_material.use_nodes = True
        mesh = context.object.data
        mesh.materials.clear()
        mesh.materials.append(default_material)
        return {'FINISHED'}
        n
class SamplePanel(bpy.types.Panel):
    """ Displayy panel in 3D view"""
    bl_label = "Sample Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.add_cube", icon="MESH_CUBE")
        col.operator("mesh.add_material", icon="SHADING_RENDERED")

classes = (
        SamplePanel,
        AddCubeOperator,
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