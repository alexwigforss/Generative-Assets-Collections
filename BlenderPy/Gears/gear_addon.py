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
        default=0.9,
        min=0.1,
        max=10.0
    ) # type: ignore
    number_of_teeth: bpy.props.IntProperty(
        name="Teeth",
        description="The gears number of teeth",
        default=6,
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
        # Select faces (prepare for dynamic scaling)
        bpy.ops.object.mode_set(mode='EDIT')
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        select_every_4th_face(bm)

        return {'FINISHED'}


def select_every_4th_face(bm):
    # Deselect all
    for f in bm.faces:
        f.select = False
    # Select every 4th face
    for i, f in enumerate(bm.faces):
        if i % 4 == 0:
            f.select = True


def scale_selected_faces(bm, scale_vec, pivot):
    """Scale selected vertices in the BMesh."""
    selected_verts = {v for f in bm.faces if f.select for v in f.verts}
    
    if not selected_verts:
        return False  # Nothing to scale

    bmesh.ops.scale(
        bm,
        verts=list(selected_verts),
        vec=scale_vec,
        space=pivot
    )
    return True


class SelectFacesAndScale(bpy.types.Operator):
    """
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

        # Use the helper function
        # select_every_4th_face(bm)
        # Collect all vertices from selected faces
        selected_verts = {v for f in bm.faces if f.select for v in f.verts}
        if not selected_verts:
            self.report({'WARNING'}, "No faces selected")
            return {'CANCELLED'}
        
        # Compute the average center of selected vertices
        center = sum((v.co for v in selected_verts), Vector()) / len(selected_verts)

        # Create a translation matrix to use as the pivot point
        from mathutils import Matrix
        pivot = Matrix.Translation(center)

        # Step Scale
        teeth_depth = context.scene.gear_tool.teeth_depth
        scale_vec = (teeth_depth, teeth_depth, 1.0)
        scaled = scale_selected_faces(bm, scale_vec, pivot)

        if not scaled:
            self.report({'WARNING'}, "Scaling failed — no vertices selected.")
            return {'CANCELLED'}

        self.report({'INFO'}, "Scaling succeded!")

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
