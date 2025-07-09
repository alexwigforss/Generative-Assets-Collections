bl_info = {
    "name": "Add Gear",
    "description": "Adds a gear to the 3D View",
    "author": "Alexander Wigforss",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh",
    "category": "3D View",
}

import bpy
import bmesh
from mathutils import Vector

class GearProperties(bpy.types.PropertyGroup):
    '''Propertys for the panel'''
    radius: bpy.props.FloatProperty(
        name="Radius",
        description="Radius of the gear",
        default=2.0,
        min=0.1,
        max=10.0
    ) # type: ignore
    thicknes: bpy.props.FloatProperty(
        name="Thicknes",
        description="Thicknes of the gear",
        default=0.2,
        min=0.1,
        max=10.0
    ) # type: ignore
    teeth_depth: bpy.props.FloatProperty(
        name="Teeth Depth",
        description="Thicknes of the gear",
        default=0.2,
        min=0.1,
        max=10.0
    ) # type: ignore
    number_of_teeth: bpy.props.IntProperty(
        name="Teeth",
        description="The gears number of teeth",
        default=5,
        min=3,
        max=100
    ) # type: ignore

class AddGearOperator(bpy.types.Operator):
    """Add a cylinder into the scene"""
    bl_idname = "mesh.add_gear"
    bl_label = "Add Gear"

    def execute(self, context):
        radius = context.scene.gear_tool.radius
        thicknes = context.scene.gear_tool.thicknes
        nr_of_teeth = context.scene.gear_tool.number_of_teeth
        bpy.ops.mesh.primitive_cylinder_add(
        vertices= nr_of_teeth * 4,
        radius=radius,
        depth=thicknes,
        end_fill_type='NOTHING',  # 👈 This skips the caps
        location=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0)
        )
        return {'FINISHED'}


class SelectFacesAndScale(bpy.types.Operator):
    """Get mesh of selected cylinder
    chose each 4th face and
    scalle it on x,y based on teeth_depth 
    """
    bl_idname = "mesh.scale_faces"
    bl_label = "Scale Faces"

    def execute(self, context):
        # Ensure you're in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        # Deselect everything first
        for f in bm.faces:
            f.select = False

        # Select every other face
        for i, f in enumerate(bm.faces):
            if i % 4 == 0:
                f.select = True

        # Collect all vertices from selected faces
        selected_verts = {v for f in bm.faces if f.select for v in f.verts}

        # Compute the average center of selected vertices
        center = sum((v.co for v in selected_verts), Vector()) / len(selected_verts)

        # Create a translation matrix to use as the pivot point
        from mathutils import Matrix
        pivot = Matrix.Translation(center)

        teeth_depth = context.scene.gear_tool.teeth_depth

        # Apply scaling on X and Y axes only (Z remains unchanged)
        bmesh.ops.scale(
            bm,
            verts=list(selected_verts),
            vec=(teeth_depth, teeth_depth, 1.0),  # Scale X and Y inward, leave Z unchanged
            space=pivot
        )

        # Update the mesh
        bmesh.update_edit_mesh(me, loop_triangles=True)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)        
        return {'FINISHED'}


class GearPanel(bpy.types.Panel):
    """ Display panel in 3D view"""
    bl_label = "Sample Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        layout = self.layout
        gear_props = context.scene.gear_tool
        col = layout.column(align=True)
        col.prop(gear_props, "number_of_teeth")
        col.prop(gear_props, "radius") # TODO Link to setter scale x,y 
        col.prop(gear_props, "thicknes")  # TODO Link to setter scale z
        col.operator("mesh.add_gear", icon="MESH_CUBE")

        col.prop(gear_props, "teeth_depth") # TODO Link to setter
        col.operator("mesh.scale_faces", icon="MESH_CUBE")


classes = (
    AddGearOperator,
    GearPanel,
    SelectFacesAndScale,
)

def register():
    bpy.utils.register_class(GearProperties)
    bpy.types.Scene.gear_tool = bpy.props.PointerProperty(type=GearProperties)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.gear_tool
    bpy.utils.unregister_class(GearProperties)

if __name__ == "__main__":
    register()
