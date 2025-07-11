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

z_index = 1

class ResetZIndex(bpy.types.Operator):
    """Reset Z Position to 1"""
    bl_idname = "mesh.reset_z"
    bl_label = "Reset"
    def execute(self, context):
        global z_index
        z_index = 1
        return {'FINISHED'}

class AddCubeOperator(bpy.types.Operator):
    """Add a cube into the scene"""
    bl_idname = "mesh.add_cube"
    bl_label = "Add Cube"

    def execute(self, context):
        global z_index
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, z_index))
        z_index += 2
        return {'FINISHED'}

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
        col.operator("mesh.add_cube", icon="MESH_CUBE")
        col.operator("mesh.add_material", icon="SHADING_RENDERED")
        col.operator("mesh.reset_z", icon="X")

classes = (
        ResetZIndex,
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