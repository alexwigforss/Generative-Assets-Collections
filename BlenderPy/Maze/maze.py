bl_info = {
    "name": "Generate Maze",
    "description": "Generates a maze in the 3D View",
    "author": "Alexander Wigforss",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Maze",
    "category": "3D View",
}

import random as r
import bpy
import bmesh
#from mathutils import Vector, Matrix

# TODO cell size and rectangular dimensions
# TODO differ pillars from walls
# TODO functionality for punching holes

# Properties
class MazeProperties(bpy.types.PropertyGroup):
    cell_size: bpy.props.FloatProperty(
        name="Cell Size",
        description="Size of one cell",
        default=2.0,
        min=0.1,
        max=10.0
    ) # type: ignore
    dimension_x: bpy.props.IntProperty(
        name="Dimension X",
        description="The dimension of th array holding the maze",
        default=9,
        min=5,
        max=200,
        step=2 # TODO Restrict by any means to put an even number in here.
    )  # type: ignore
    dimension_y: bpy.props.IntProperty(
        name="Dimension_Y",
        description="The dimension of th array holding the maze",
        default=9,
        min=5,
        max=200,
        step=2 # TODO Restrict by any means to put an even number in here.
    )  # type: ignore

#######################################################
# INTERNALS                                           #
#######################################################


def get_random_direction():
    rand = r.randint(0,3)
    if rand == 0:
        return (-1, 0)
    if rand == 1:
        return (0, 1)
    if rand == 2:
        return (1, 0)
    if rand == 3:
        return (0, -1)


def randomize_maze(a, dx, dy):
    for E in range(2,dx - 2):
        if E % 2 == 0:
            for e in range(2,dy - 2):
                if e % 2 == 0:
                    rnd = get_random_direction()
                    a[E+rnd[0]][e+rnd[1]] = 1
                else:
                    pass
    return a


def print_the_maze(lst):
    for E in lst:
        for e in E:
            if e == 1:
                print('🧱', end='')
            else:
                print('  ', end='')
        print()

#######################################################
# OPERATORS                                           #
#######################################################

# class AddCubeOperator(bpy.types.Operator):


class GenerateMazeOperator(bpy.types.Operator):
    """Randomly generate maze array behind the scene"""
    bl_idname = "mesh.gen_maze"
    bl_label = "Generate Maze"


    def execute(self, context):
        # NOTE Dim must be odd number
        dim_x = context.scene.maze_tool.dimension_x
        dim_y = context.scene.maze_tool.dimension_y
        edge =  [1 for x in range(dim_y)]
        GenerateMazeOperator.main_array = []
        GenerateMazeOperator.main_array.append(edge)
        for e in range(1,dim_x-1):
            if e % 2 == 0:
                GenerateMazeOperator.main_array.append([1 if x % 2 == 0 else 0 for x in range(dim_y)])
            else:
                GenerateMazeOperator.main_array.append([1] + [0 for x in range(1, dim_y -1 )] + [1])
        GenerateMazeOperator.main_array.append(edge)

        GenerateMazeOperator.main_array = randomize_maze(GenerateMazeOperator.main_array, dim_x, dim_y)


        # Print the second row of the maze array for debugging
        if len(GenerateMazeOperator.main_array) > 1:
            print("Second row:", GenerateMazeOperator.main_array[1])
        return {'FINISHED'}


class AddMazeOperator(bpy.types.Operator):
    """Add a maze into the scene"""
    bl_idname = "mesh.add_maze"
    bl_label = "Add Maze"

    def execute(self, context):
        lst = GenerateMazeOperator.main_array
        size = context.scene.maze_tool.cell_size


        x_index = 0
        z_index = 0

        for E in lst:
            y_index = 0
            for e in E:
                if e == 1:
                    bpy.ops.mesh.primitive_cube_add(size=size, enter_editmode=False, align='WORLD', location=(x_index * size, y_index * size, size/2))
                y_index += 1
            x_index += 1

        return {'FINISHED'}


#######################################################
# PANEL                                               #
#######################################################
class MazePanel(bpy.types.Panel):
    """ Display panel in 3D view"""
    bl_label = "Maze Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = "Maze"

    def draw(self, context):
        # print('HELLO PANEL')
        layout = self.layout
        maze_props = context.scene.maze_tool
        obj = context.object
        col = layout.column(align=True)
        col.prop(maze_props, "cell_size")
        col.prop(maze_props, "dimension_x")
        col.prop(maze_props, "dimension_y")
        col.operator("mesh.gen_maze", icon="MESH_CUBE")
        col.operator("mesh.add_maze", icon="MESH_CUBE")

        # if obj is not None:
        #     layout.prop(obj, "ResThick", slider=True)
        #     layout.prop(obj, "ResTDepth", slider=True)
        # else:
        layout.label(text="No active object.")


classes = (
    GenerateMazeOperator,
    AddMazeOperator,
    MazePanel,
)


#######################################################
# REGISTER, CLEANUP & STARTPOINT                      #
#######################################################

def register():
    bpy.utils.register_class(MazeProperties)
    bpy.types.Scene.maze_tool = bpy.props.PointerProperty(type=MazeProperties)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.maze_tool
    bpy.utils.unregister_class(MazeProperties)
    # del bpy.types.Object.ResThick
    # del bpy.types.Object.ResTDepth

if __name__ == "__main__":
    register()