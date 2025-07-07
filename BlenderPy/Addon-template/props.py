from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       )

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