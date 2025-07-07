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
    radius: bpy.props.IntProperty(
        name="Radius",
        description="Radius of the gear",
        default=2,
        min=0,
        max=10
    )
'''
bpy.props.IntProperty(
    name='myprop',
    description='f_u',
    translation_context='*',
    default=0,
    min=-0,
    max=100,
    step=1,
    options={'ANIMATABLE'},
    override=set(),
    tags=set(),
    subtype='NONE',
    update=None,
    get=None,
    set=None)
'''

class AddGearOperator(bpy.types.Operator):
    """Add a cube into the scene"""
    bl_idname = "mesh.add_gear"
    bl_label = "Add Gear"

    def execute(self, context):
        # Using a fixed Z index to avoid undefined variable
        # bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.ops.mesh.primitive_cylinder_add(
        vertices=20,
        radius=2.0,
        depth=0.5,
        end_fill_type='NOTHING',  # 👈 This skips the caps
        location=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0)
        )
        return {'FINISHED'}


class SelectFacesAndScale(bpy.types.Operator):
    """Add a cube into the scene"""
    bl_idname = "mesh.scale_faces"
    bl_label = "Scale Faces"

    def execute(self, context):
        # Ensure you're in Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.edit_object
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

        # Apply scaling on X and Y axes only (Z remains unchanged)
        bmesh.ops.scale(
            bm,
            verts=list(selected_verts),
            vec=(0.5, 0.5, 1.0),  # Scale X and Y inward, leave Z unchanged
            space=pivot
        )

        # Update the mesh
        bmesh.update_edit_mesh(me, loop_triangles=True)
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
        col.operator("mesh.add_gear", icon="MESH_CUBE")
        col.prop(gear_props, "radius")
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
