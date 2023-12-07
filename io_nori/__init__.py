bl_info = {
    "name": "Export Nori scenes format",
    "author": "Adrien Gruson, Philipp Lindenberger, Darío Marcos",
    "version": (0, 3),
    "blender": (2, 80, 0),
    "location": "File > Export > Nori exporter (.xml)",
    "description": "Export Nori scenes format (.xml)",
    "warning": "",
    "wiki_url": "",
    "category": "Export"}

import bpy, os, math, shutil
from mathutils import Matrix, Vector, Color
from xml.dom.minidom import Document

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import *
from bpy.types import Operator

from bpy_extras import io_utils, node_shader_utils
import bmesh
from bpy_extras.wm_utils.progress_report import (
    ProgressReport,
    ProgressReportSubstep,
)

from .nori_writer import *
from .menu import *

######################
# blender code
######################
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper

class NoriExporter(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    # add to menu
    bl_idname = "export.nori"
    bl_label = "Export Nori scene"

    # filtering file names
    filename_ext = ".xml"
    filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})

    ###################
    # other options
    ###################

    export_light : BoolProperty(
                    name="Export Lights",
                    description="Export lights to Nori",
                    default=True)

    export_material_colors : BoolProperty(
                    name="Export BSDF properties",
                    description="Export material colors instead of viewport colors",
                    default=True)
    
    export_textures : BoolProperty(
                    name="Export Textures",
                    description="Export texture connected to color socket of the material. Only effective \
                     when 'Export BSDF properties' is selected.",
                    default=True)

    export_meshes_in_world : BoolProperty(
                    name="Export OBJ in world coords",
                    description="Export meshes in world coordinate frame.",
                    default=True)
    
    export_meshes_triangular : BoolProperty(
                    name="Triangular Mesh",
                    description="Convert faces to triangles.",
                    default=True)

    nb_samples : IntProperty(name="Numbers of camera rays",
                    description="Number of camera ray",
                    default=32)

    env_map_scale : FloatProperty(name="Environment map scale",
                    description="Factor that scales the environment map's radiance (if it exists)",
                    default=100)

    export_thin_lens : BoolProperty(name="Use thin-lens camera model",
                    description="Export thin-lens camera model parameters (1/f, focal distance) ",
                    default=False)

    def execute(self, context):
        nori = NoriWriter(context, self.filepath)
        nori.setExportMeshesWorld(self.export_meshes_in_world)
        nori.export_triangular = self.export_meshes_triangular
        nori.export_textures = self.export_textures
        nori.export_thin_lens = self.export_thin_lens
        nori.write(self.export_light, self.export_material_colors, bpy.context.scene.cycles.samples)
        return {'FINISHED'}

    def invoke(self, context, event):
        #self.frame_start = context.scene.frame_start
        #self.frame_end = context.scene.frame_end

        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_export(self, context):
    import os
    default_path = os.path.splitext(bpy.data.filepath)[0] + ".xml"
    self.layout.operator(NoriExporter.bl_idname, text="Export Nori scenes...").filepath = default_path


# Register Nori exporter inside blender
def register():
    bpy.utils.register_class(NoriExporter)
    bpy.utils.register_class(NoriExporterPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_export)

def unregister():
    bpy.utils.unregister_class(NoriExporter)
    bpy.utils.unregister_class(NoriExporterPanel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export)

if __name__ == "__main__":
    register()
