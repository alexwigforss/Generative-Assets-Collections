import bpy

    
class CameraMatchingPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View for Adjusting the Focal Length and Location of the Camera"""
    bl_label = "Z Scale"
    bl_idname = "Dyn_Scale_Z"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Z Scale"
    bl_label = "Scale"


    def setVal(self, val):
        obj = bpy.context.active_object
        if obj is not None:
            obj.scale = (1.0, 1.0, val)
        else:
            print("No active object selected.")
        

    def getVal(self):
        obj = bpy.context.active_object
        if obj is not None:
            return obj.scale.z
        else:
            return 1.0

    bpy.types.Object.ZScale = bpy.props.FloatProperty(
        step = 0.1,
        default = 1.0,
        min = 0.0,
        max = 10.0, 
        set = setVal,
        get = getVal
        )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Focal Length (mm):")
        
        row = layout.row()
        row.prop(context.object, "FocalLength", text = "")


def register():
    bpy.utils.register_class(CameraMatchingPanel)


def unregister():
    bpy.utils.unregister_class(CameraMatchingPanel)


if __name__ == "__main__":
    register()
