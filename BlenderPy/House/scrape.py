bl_info = {
    "name": "Generate Skyscraper",
    "description": "Generates a stylized skyscraper with cut-out windows",
    "author": "Alexander Wigforss & AI",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Skyscraper",
    "category": "3D View",
}

import bpy
import bmesh
import random as r
from mathutils import Matrix

class SkyscraperProperties(bpy.types.PropertyGroup):
    width_x: bpy.props.FloatProperty(name="Bredd X", default=10.0, min=1.0)
    width_y: bpy.props.FloatProperty(name="Djup Y", default=10.0, min=1.0)
    height_z: bpy.props.FloatProperty(name="Höjd Z", default=30.0, min=1.0)
    
    floors: bpy.props.IntProperty(name="Antal Våningar", default=15, min=1)
    columns: bpy.props.IntProperty(name="Fönsterkolumner", default=8, min=1)
    window_chance: bpy.props.FloatProperty(
        name="Fönsterchans (%)", 
        description="Sannolikhet att ett fönster skapas", 
        default=0.8, min=0.0, max=1.0, subtype='FACTOR'
    )

class MESH_OT_add_skyscraper(bpy.types.Operator):
    """Genererar en stiliserad skyskrapa med fönsterhål"""
    bl_idname = "mesh.add_skyscraper"
    bl_label = "Skapa Skyskrapa"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.skyscraper_tool
        
        # 1. Skapa en ny mesh och ett nytt objekt
        mesh = bpy.data.meshes.new("SkyscraperMesh")
        obj = bpy.data.objects.new("Skyscraper", mesh)
        context.collection.objects.link(obj)
        
        # Gör objektet aktivt
        context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # 2. Starta BMesh för att bygga geometrin
        bm = bmesh.new()
        
        # Skapa bas-kub (skyskrapans kropp)
        # Genom att skala först och flytta sist står huset stabilt på marken (Z=0)
        scale_mat = (Matrix.Scale(props.width_x, 4, (1, 0, 0)) @ 
                     Matrix.Scale(props.width_y, 4, (0, 1, 0)) @ 
                     Matrix.Scale(props.height_z, 4, (0, 0, 1)))
        
        trans_mat = Matrix.Translation((0, 0, props.height_z / 2))
        
        bmesh.ops.create_cube(
            bm, 
            size=1.0, 
            matrix=trans_mat @ scale_mat # Skala först, flytta sen!
        )
        
        # Hitta alla sidoytor (inte tak eller botten)
        side_faces = [f for f in bm.faces if abs(f.normal.z) < 0.1]
        
        # 3. Dela upp sidorna i ett rutnät för fönster (Subdivide)
        # Vi gör detta per sida för att ha kontroll
        for face in side_faces:
            # Subdivide ytan baserat på önskat antal våningar och kolumner
            result = bmesh.ops.subdivide_edges(
                bm, 
                edges=face.edges, 
                cuts=props.floors, # Horisontella snitt (våningar)
                use_grid_fill=True
            )
        '''    
        # Säkerställ att tabellerna är uppdaterade innan loopen
        bm.faces.ensure_lookup_table()
        
        # Räkna ut max tillåten area för att en yta ska räknas som ett fönster
        # Ett fönster kan aldrig vara större än en bråkdel av hela husets fasad
        total_wall_area = (props.width_x * props.height_z)
        max_window_area = total_wall_area / (props.floors * props.columns) * 1.5 # Marginal på 50%
        
        faces_to_remove = []
        for face in bm.faces:
            # 1. Det måste vara en sidoyta (normalen pekar utåt i X eller Y, inte Z)
            if abs(face.normal.z) < 0.1:
                # 2. SÄKRING: Ytan MÅSTE vara liten (ett fönster). 
                # Om arean är för stor är det en hel yttervägg eller en restyta som vi ska ignorera.
                if face.calc_area() < max_window_area:
                    # 3. Slumpa fönsterhål
                    if r.random() < props.window_chance:
                        faces_to_remove.append(face)
                        
        # Ta bort ENDAST de små fönsterytorna
        bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
        '''
        
        # Säkerställ att tabellerna är uppdaterade innan loopen
        bm.faces.ensure_lookup_table()
        
        total_wall_area = (props.width_x * props.height_z)
        max_window_area = total_wall_area / (props.floors * props.columns) * 1.5
        
        # 1. Samla alla giltiga fönsterytor först
        window_faces = []
        for face in bm.faces:
            if abs(face.normal.z) < 0.1:
                if face.calc_area() < max_window_area:
                    window_faces.append(face)
                    
        # 2. Gruppera fönstren baserat på vilken av de 4 väggarna de tillhör
        # Vi använder normalens riktning för att dela upp dem i Norr, Söder, Öster, Väster
        walls = {
            "pos_x": [], "neg_x": [],
            "pos_y": [], "neg_y": []
        }
        
        for face in window_faces:
            n = face.normal
            center = face.calc_center_median()
            if abs(n.x) > 0.5:
                if n.x > 0: walls["pos_x"].append((center.z, center.y, face))
                else:       walls["neg_x"].append((center.z, center.y, face))
            else:
                if n.y > 0: walls["pos_y"].append((center.z, center.x, face))
                else:       walls["neg_y"].append((center.z, center.x, face))

        faces_to_remove = []
        
        # 3. Processa varje vägg för sig med exakt indexering via sortering
        for wall_name, face_data in walls.items():
            if not face_data:
                continue
                
            # Sortera först på höjd (Z), sen på sidled (X eller Y beroende på vägg)
            # Detta ordnar fönstren rad för rad, nedifrån och upp, vänster till höger
            face_data.sort(key=lambda item: (item[0], item[1]))
            
            # Nu när de är sorterade kan vi enkelt återskapa ett perfekt rutnät
            # Eftersom vi delade upp med 'props.columns' snitt, finns det (columns + 2) ytor per rad
            items_per_row = props.columns + 2 
            
            for index, (z, side_coord, face) in enumerate(face_data):
                # Räkna ut exakt rad (våning) och kolumn baserat på listans index
                floor_idx = index // items_per_row
                column_idx = index % items_per_row
                
                # Din logik: varannan rad har fönster, varannan kolumn har fönster
                if floor_idx % 2 == 1 and column_idx % 2 == 1:
                    faces_to_remove.append(face)
                        
        # Ta bort valda faces (slå hål i meshen)
        bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')
        
        # 4. Skriv tillbaka BMesh till Blender-meshen
        bm.to_mesh(mesh)
        bm.free()
        
        mesh.update()
        return {'FINISHED'}

class VIEW3D_PT_skyscraper_panel(bpy.types.Panel):
    bl_label = "Skyskrapa Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Skyscraper"

    def draw(self, context):
        layout = self.layout
        props = context.scene.skyscraper_tool
        
        col = layout.column(align=True)
        col.label(text="Dimensioner:")
        col.prop(props, "width_x")
        col.prop(props, "width_y")
        col.prop(props, "height_z")
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Fönsterinställningar:")
        col.prop(props, "floors")
        col.prop(props, "window_chance")
        
        layout.separator()
        layout.operator("mesh.add_skyscraper", icon="MESH_CUBE")

classes = (
    SkyscraperProperties,
    MESH_OT_add_skyscraper,
    VIEW3D_PT_skyscraper_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.skyscraper_tool = bpy.props.PointerProperty(type=SkyscraperProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.skyscraper_tool

if __name__ == "__main__":
    register()