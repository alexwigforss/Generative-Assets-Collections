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
from mathutils import Vector, Matrix

# --- Property getter and setter must be global functions ---
def set_z_scale(self, value):
    obj = bpy.context.active_object
    if obj:
        obj.scale.z = value

def get_z_scale(self):
    obj = bpy.context.active_object
    if obj:
        return obj.scale.z
    return 1.0

def set_teeth_depth(self, value):
    obj = bpy.context.active_object
    if not obj or obj.mode != 'EDIT':
        return

    if "tooth_orig_coords" not in obj:
        print("Inga originalkoordinater sparade.")
        return
    
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    selected_verts = {v for f in bm.faces if f.select for v in f.verts}
    if not selected_verts:
        return

    # Återställ till original
    orig_coords = obj["tooth_orig_coords"]
    for v in selected_verts:
        key = str(v.index)
        if key in orig_coords:
            v.co = Vector(orig_coords[key])

    # Skala enligt slidervärde
    center = sum((v.co for v in selected_verts), Vector()) / len(selected_verts)
    pivot = Matrix.Translation(center)
    scale_vec = (value, value, 1.0)
    scale_selected_faces(bm, scale_vec, pivot)

    bmesh.update_edit_mesh(me, loop_triangles=True)
    obj["ResTDepth"] = value


def get_teeth_depth(self):
    obj = bpy.context.active_object
    return obj.get("ResTDepth", 1.0)

# --- Define the custom properties ---
bpy.types.Object.ResThick = bpy.props.FloatProperty(
    name="Responsive Thicknes",
    step=0.1,
    default=1.0,
    min=0.0,
    max=10.0,
    set=set_z_scale,
    get=get_z_scale
)

bpy.types.Object.ResTDepth = bpy.props.FloatProperty(
    name="Responsive Teeth Depth",
    step=0.1,
    default=1.0,
    min=0.0,
    max=2.0,
    set=set_teeth_depth,
    get=get_teeth_depth
)


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
    number_of_teeth: bpy.props.IntProperty(
        name="Teeth",
        description="The gears number of teeth",
        default=6,
        min=3,
        max=100
    ) # type: ignore

class AddGearOperator(bpy.types.Operator):
    """Add a gear into the scene"""
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

    # Spara originalkoordinater för valda vertiklar
    orig_coords = {}
    for v in {v for f in bm.faces if f.select for v in f.verts}:
        orig_coords[str(v.index)] = v.co.copy()[:]

    # Spara på objektet (som dict)
    obj = bpy.context.edit_object
    obj["tooth_orig_coords"] = orig_coords


def scale_selected_faces(bm, scale_vec, pivot):
    """Scale selected vertices in the BMesh."""
    selected_verts = {v for f in bm.faces if f.select for v in f.verts}
    
    if not selected_verts:
        return False

    bmesh.ops.scale(
        bm,
        verts=list(selected_verts),
        vec=scale_vec,
        space=pivot
    )
    return True


class GearPanel(bpy.types.Panel):
    """ Display panel in 3D view"""
    bl_label = "Sample Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = "Gears"

    def draw(self, context):
        layout = self.layout
        gear_props = context.scene.gear_tool
        obj = context.object
        col = layout.column(align=True)
        col.prop(gear_props, "number_of_teeth")
        col.prop(gear_props, "radius")
        col.prop(gear_props, "thicknes")
        col.operator("mesh.add_gear", icon="MESH_CUBE")

        if obj is not None:
            layout.prop(obj, "ResThick", slider=True)
            layout.prop(obj, "ResTDepth", slider=True)
        else:
            layout.label(text="No active object.")


classes = (
    AddGearOperator,
    GearPanel,
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
    del bpy.types.Object.ResThick
    del bpy.types.Object.ResTDepth

if __name__ == "__main__":
    register()
