'''
https://docs.blender.org/api/blender_python_api_2_63_7/
https://docs.blender.org/api/blender_python_api_2_63_7/bpy.ops.mesh.html#module-bpy.ops.mesh
'''

'''
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
Construct a cylinder mesh

Parameters:	
vertices (int in [3, inf], (optional)) – Vertices
radius (float in [0, inf], (optional)) – Radius
depth (float in [0, inf], (optional)) – Depth
end_fill_type (enum in [‘NOTHING’, ‘NGON’, ‘TRIFAN’], (optional)) –
Cap Fill Type

NOTHING Nothing, Don’t fill at all.
NGON Ngon, Use ngons.
TRIFAN Triangle Fan, Use triangle fans.
view_align (boolean, (optional)) – Align to View, Align the new object to the view
enter_editmode (boolean, (optional)) – Enter Editmode, Enter editmode when adding this object
location (float array of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object
rotation (float array of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object
layers (boolean array of 20 items, (optional)) – Layer
'''

import bpy
import bmesh
from mathutils import Vector

bpy.ops.mesh.primitive_cylinder_add(
    vertices=20,
    radius=2.0,
    depth=0.5,
    end_fill_type='NOTHING',  # 👈 This skips the caps
    location=(0.0, 0.0, 0.0),
    rotation=(0.0, 0.0, 0.0)
)

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