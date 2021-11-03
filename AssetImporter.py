import bpy, os, json,sys, time
from blenderkit import append_link
from blender_customs import *
import pathlib
from bpy.types import WindowManager
from bpy.props import (
            StringProperty,
            EnumProperty,
            BoolProperty,
            )
import bpy.utils.previews
#os.system('cls')
bl_info = {
	"name": "Asset Importer",
	"author": "banan039",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"category": "Import",
	"location": "View layer properties > Import assets",
	"wiki_url": "github_link",
	"description": "Importer for blender assets, supported formats: *.blend, *.fbx, *.glb, *.dae. Check Readme file on github for more information"
}


def getListOfFiles(dirName=os.getcwd()):
    """get list of all files in directory dirName with full paths, searches recursively"""
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

assets_dict = {
    "armatures": "Armature",
    "objects": "Object",
    "meshes": "Mesh",
    "images": "Image",
    "materials": "Material",
    "objects": "Object"

}

def mesh_names_to_ob_names():
    """Renames meshes to its"""
    for ob in [ob for ob in bpy.data.objects if ob.type == 'MESH']:
        ob.data.name = ob.name

def import_asset(file_path, inner_path, ob_name):
    """Importing {ob_name} from class {inner_path} from file {os.path.basename(file_path)}"""
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, ob_name),
        directory=os.path.join(file_path, inner_path),
        filename=ob_name
    )
def import_assets_by_category(file_path,asset_type):
    """imports only specific asset type from filepath"""
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        data_from_objects = getattr(data_from, asset_type)
        data_to_objects = getattr(data_to, asset_type)
        for ob in data_from_objects:
            data_to_objects.append(ob)

def import_all_assets_no_linked(file_path,excluded=[]):
    """Append ALL assets from *.blend filepath, except types defined in `excluded` list"""
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        for asset_type in dir(data_to): 
            if not asset_type in excluded:
                data_from_objects = getattr(data_from, asset_type)
                data_to_objects = getattr(data_to, asset_type)
                for ob in data_from_objects:
                    data_to_objects.append(ob)

def link_the_unlinked_objects(objects=[]):
    """Links all unlinked objects to current scene if `objects` array is empty, 
    otherwise links all objects from this array, accepts str or objects types"""
    scene = bpy.context.scene
    if objects:
        for ob in objects:
            if isinstance(ob, str):
                print(ob)
                scene.collection.objects.link(bpy.data.objects[ob])
            else:
                print(ob.name)
                scene.collection.objects.link(ob)
    else:
        scene_objs = [ob.name for ob in scene.collection.objects ]
        unlinked = [ob.name for ob in bpy.data.objects if not ob.name in scene_objs]
        for ob in unlinked:
            print(ob)
            scene.collection.objects.link(bpy.data.objects[ob])

        
def import_scene(file_path):
    """Imports just scenes from blend filepath"""
    import_assets_by_category(file_path,'scenes')
            

def import_by_message(m,file_path,**args):
    """Performs various import depending on the message"""
    me = m.lower()
    if me == 'scene': import_scene(file_path)
    elif me == 'object': import_asset(file_path, 'Object', args['ob_name'])
    elif me == 'objects_all': append_link.append_objects(file_name=file_path)
    elif me == 'brush': append_link.append_brush(file_name=file_path)
    elif me == 'material': append_link.append_material(file_name=file_path)
    elif me == 'particle': append_link.append_particle_system(file_name=file_path, target_object=args['ob_name'])
    elif me == 'armature': import_asset(file_path, 'Armature', args['ob_name'])

def append_whole_blend_file(PATH):
    """Appending all objects from specified PATH to *.blend file"""
    #root_scene = [scene for scene in bpy.data.scenes][0]
    root_scene = bpy.context.scene
    print(root_scene.name)
    print(str(dir(root_scene)))
    import_scene(PATH)
    for scene in [scene for scene in bpy.data.scenes if scene.name != root_scene.name]:
        for ob in scene.objects:
            root_scene.collection.objects.link(ob)
    for scene in [scene for scene in bpy.data.scenes if scene.name != root_scene.name]:
        bpy.data.scenes.remove(scene)
#append_whole_blend_file(PATH)

"""Addon Part"""


class BlenderResources():
    """Deprecated, not used"""
    def __init__(self, main_path=os.path.expandvars('%USERPROFILE%\\Documents\\BlenderResources'),res_path='blends',im_path='previews'):
        #self.settings = os.path.join(main_path, 'settings.json')
        #self.settings = os.path.expandvars('%USERPROFILE%\\BlenderResourcesSettings.json')
        #if not os.path.exists(self.settings):
        data = {}
        data["main_path"] = main_path
        data["res_path"] = res_path
        data["im_path"] = im_path
            #json_to_file(self.settings,data)
        #else:
        #    data = file_to_json(self.settings)
        self.main_path = data['main_path']
        self.res_path = os.path.join(self.main_path, data['res_path'])
        self.im_path = os.path.join(self.main_path, data['im_path'])
        #print(self.res_path, self.im_path)
        print(str(data))


def remove_ext(file):
    """Removes extension from file"""
    size = (-1) * (len(file.split('.')[-1]) + 1)
    return file[:size]

def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.my_previews_dir
    main_path = os.path.dirname(directory[:-1])
    res_path = os.path.join(main_path, 'blends')
    fil = wm.filter_field
    #if not wm.Paths.im_path.split('\\')[-1] in directory: 
        #directory = os.path.join(directory, wm.Paths.im_path.split('\\')[-1])
    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]

    if directory == pcoll.my_previews_dir:
        return pcoll.Preview

    print("Scanning directory: %s" % directory)
    print(main_path,res_path)

    if directory and os.path.exists(directory):
        #imgs = getListOfFiles(directory)
        for i, file in enumerate([file for file in os.listdir(directory) if file.lower().endswith('.png')]):
            name = remove_ext(file)
            if fil:
                if not fil in name: continue
            for ext in wm.exts:
                blend_file = os.path.join(res_path, name + ext)
                
                if os.path.exists(blend_file):
                    filepath = os.path.join(directory, file)
                    thumb = pcoll.load(filepath, filepath, 'IMAGE')
                    enum_items.append((name, name, "", thumb.icon_id, i))
                    #print(blend_file, file)
                    break
                
    #bpy.data.window_managers["WinMan"].Preview = name

    pcoll.Preview = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.Preview


#def get_

def import_by_extension(filepath):
    """Imports a file from filepath to blender depending on its extension"""
    e = ''
    if filepath.lower().endswith('.blend'):
        import_all_assets_no_linked(filepath, excluded=['scenes'])
        link_the_unlinked_objects()
    elif filepath.lower().endswith('.fbx'): bpy.ops.import_scene.fbx(filepath=filepath)
    elif filepath.lower().endswith('.glb'): bpy.ops.import_scene.gltf(filepath=filepath)
    elif filepath.lower().endswith('.dae'): bpy.ops.wm.collada_import(filepath=filepath)
    print(f'Attempted import {os.path.basename(filepath)} [{filepath}]')

from bpy.types import (Panel, Operator)


class ImportButton(Operator):
    """Import assets from preview"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    
    def execute(self, context):
        wm = context.window_manager
        directory = wm.my_previews_dir
        main_path = os.path.dirname(directory[:-1])
        res_path = os.path.join(main_path, 'blends')
        if wm.Preview:
            res_file = os.path.join(res_path, wm.Preview)
            for ext in wm.exts:
                file = res_file + ext
                if os.path.exists(file):
                    import_by_extension(file)
                    break
        return {'FINISHED'}

class FilterButton(Operator):
    """Filter assets. If filter text field is empty then the previews collection is reloaded"""
    bl_idname = "object.filter_operator"
    bl_label = "Filter Button"
    
    def execute(self, context):
        wm = context.window_manager
        #pcoll = preview_collections["main"]
        bpy.utils.previews.remove(preview_collections["main"])
        pcoll = bpy.utils.previews.new()
        pcoll.my_previews_dir = ""
        pcoll.Preview = ()

        preview_collections["main"] = pcoll
        return {'FINISHED'}


class PreviewsExamplePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Import assets"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "view_layer"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.prop(wm, "my_previews_dir")

        row = layout.row()
        row.template_icon_view(wm, "Preview")

        row = layout.row()
        row.prop(wm, "Preview")
        
        row = layout.row()
        row.prop(wm, "filter_field")
        
        row = layout.row()
        row.operator(FilterButton.bl_idname,text="Filter", icon="FILTER")
        #props.fun_name = 'Filter'
        
        row = layout.row()
        row.operator(ImportButton.bl_idname,text="Import assets", icon="IMPORT")

    def execute(self, context):
        print('Executed')
# We can store multiple preview collections here,
# however in this example we only store "main"
preview_collections = {}


def register():
    """Register addon"""
    WindowManager.exts = ['.blend','.fbx','.glb','.dae']
    WindowManager.my_previews_dir = StringProperty(
            name="Path",
            subtype='DIR_PATH',
            default=os.path.expandvars('%USERPROFILE%\\Documents')
            )
    
    WindowManager.Preview = EnumProperty(
            items=enum_previews_from_directory_items,
            )
    WindowManager.filter_field = StringProperty(
            name="",
            subtype='FILE_NAME',
            default=''
            )
    WindowManager.my_bool = BoolProperty(name='My special bul'
            )
    # Note that preview collections returned by bpy.utils.previews
    # are regular Python objects - you can use them to store custom data.
    #
    # This is especially useful here, since:
    # - It avoids us regenerating the whole enum over and over.
    # - It can store enum_items' strings
    #   (remember you have to keep those strings somewhere in py,
    #   else they get freed and Blender references invalid memory!).
    
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.Preview = ()

    preview_collections["main"] = pcoll
    bpy.utils.register_class(FilterButton)
    bpy.utils.register_class(ImportButton)
    bpy.utils.register_class(PreviewsExamplePanel)


def unregister():
    """Unregister addon"""
    from bpy.types import WindowManager

    #del WindowManager.Preview

    #for pcoll in preview_collections.values():
    for pcoll in preview_collections.values():
        print(pcoll)
        bpy.utils.previews.remove(pcoll)
    #preview_collections.clear()
    bpy.utils.unregister_class(PreviewsExamplePanel)
    bpy.utils.unregister_class(ImportButton)
    bpy.utils.unregister_class(FilterButton)
    


if __name__ == "__main__":
    register()
    #for e in  dir(bpy.props):
        #print(e)
    #print('\n\nutils')
    #for e in  dir(bpy.utils):
        #print(e)