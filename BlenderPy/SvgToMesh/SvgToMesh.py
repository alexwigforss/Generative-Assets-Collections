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

def svg_trans_mesh(self, value):
    obj = bpy.context.active_object
    if obj:
        obj.convert(target='MESH')

class ConvertToMesh(bpy.types.Operator):
    """Converts Svg To Mesh"""
    bl_idname = "mesh.conv_mesh"
    bl_label = "Convert"
    def execute(self, context):
        bpy.ops.object.convert(target='MESH', thickness=5)

        # bpy.ops.object.convert(*, target='MESH', keep_original=False, merge_customdata=True, thickness=5, faces=True, offset=0.01)
        # bpy.ops.convert.bpy.ops.convert(target='MESH', thickness=5)
        # obj = bpy.context.active_object
        # if obj:
        #     obj.convert(target='MESH')
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

class ExtrudeDeth(bpy.types.Operator):
    bl_idname = "my_operator.my_class_name"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        return {"FINISHED"}


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
        col.operator("mesh.conv_mesh", icon="MESH_CUBE")
        col.operator("mesh.add_cube", icon="MESH_CUBE")
        col.operator("mesh.add_material", icon="SHADING_RENDERED")
        col.operator("mesh.reset_z", icon="X")

classes = (
        ConvertToMesh,
        SamplePanel,
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