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

def set_depth_scale(self, value):
    obj = bpy.context.active_object
    if obj:
        obj.scale.z = value

def get_depth_scale(self):
    obj = bpy.context.active_object
    if obj:
        return obj.scale.z
    return 1.0

# --- Define the custom property globally ---
bpy.types.Object.DepthScale = bpy.props.FloatProperty(
    name="Z Scale",
    step=0.1,
    default=1.0,
    min=0.0,
    max=10.0,
    set=set_depth_scale,
    get=get_depth_scale
)
def svg_trans_mesh(self, value):
    obj = bpy.context.active_object
    if obj:
        obj.convert(target='MESH')

class ConvertToMesh(bpy.types.Operator):
    """Converts Svg To Mesh"""
    bl_idname = "mesh.conv_mesh"
    bl_label = "Convert"
    bl_description = "Converts (selected?) curve to mesh."
    def execute(self, context):
        bpy.ops.object.convert(target='MESH', thickness=5)
        return {'FINISHED'}

class ExtrudeDepth(bpy.types.Operator):
    bl_idname = "mesh.extrude_mesh"
    bl_label = "Extrude"
    bl_description = "Extrude from plane to 3d object"
    # bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #obj = context.object
        obj = bpy.context.active_object
        if not obj:
            print("Noooo no object")
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.extrude_context_move(MESH_OT_extrude_context={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.00810834), "orient_type":'NORMAL', "orient_matrix":((0.0876781, 0.996149, -0), (-0.996149, 0.0876781, 0), (0, 0, 1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False, "translate_origin":False})

        return {"FINISHED"}


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
        obj = context.object
        col = layout.column(align=True)
        # MORE Icons
        # https://docs.blender.org/api/current/bpy_types_enum_items/icon_items.html#rna-enum-icon-items
        col.operator("mesh.conv_mesh", icon="MESH_CUBE")
        col.operator("mesh.add_cube", icon="MESH_CUBE")
        col.operator("mesh.add_material", icon="SHADING_RENDERED")
        col.operator("mesh.extrude_mesh", icon="MESH_CUBE")

        # Slider with setter / getter
        if obj is not None:
            layout.prop(obj, "DepthScale", slider=True)
        else:
            layout.label(text="No active object.")

class CameraMatchingPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View for Adjusting the Z Scale of the Active Object"""
    bl_label = "Depth Scale"
    bl_idname = "VIEW3D_PT_zscale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Depth Scale"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is not None:
            layout.prop(obj, "DepthScale", slider=True)
        else:
            layout.label(text="No active object.")

classes = (
        ConvertToMesh,
        ExtrudeDepth,
        SamplePanel,
        AddMaterialOperator,
        CameraMatchingPanel
        )
    

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.DepthScale

if __name__ == "__main__":
    register()