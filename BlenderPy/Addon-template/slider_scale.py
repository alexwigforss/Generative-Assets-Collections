import bpy

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

# --- Define the custom property globally ---
bpy.types.Object.ZScale = bpy.props.FloatProperty(
    name="Z Scale",
    step=0.1,
    default=1.0,
    min=0.0,
    max=10.0,
    set=set_z_scale,
    get=get_z_scale
)


# --- Panel class ---
class CameraMatchingPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View for Adjusting the Z Scale of the Active Object"""
    bl_label = "Z Scale"
    bl_idname = "VIEW3D_PT_zscale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z Scale"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is not None:
            layout.prop(obj, "ZScale", slider=True)
        else:
            layout.label(text="No active object.")


# --- Register ---
def register():
    bpy.utils.register_class(CameraMatchingPanel)

def unregister():
    bpy.utils.unregister_class(CameraMatchingPanel)
    del bpy.types.Object.ZScale  # Clean up


if __name__ == "__main__":
    register()