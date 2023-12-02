import bpy
from bpy import context

import inspect
from pprint import pprint

def write_obj(mesh : bpy.types.Object, path : str, store_normals : bool = False):
    """Write mesh to .obj file

    Args:
        mesh (mesh): The blender mesh object
        path (str): The path to write the obj file
    """
    mesh_w_matrix = mesh.matrix_world
    mesh_obj = mesh.to_mesh()
    mesh_uv_layer = mesh_obj.uv_layers.active
    
    # https://blender.stackexchange.com/questions/32468/how-to-write-a-simple-wavefront-obj-exporter-in-python
    with open(path, 'w') as f:
        f.write("# OBJ file\n")
        for v in mesh_obj.vertices:
            v_w = mesh_w_matrix @ v.co
            f.write("v %.4f %.4f %.4f\n" % (v_w[0], v_w[1], v_w[2]))

        if mesh_uv_layer is not None:
            for i in range(len(mesh_uv_layer.data)):
                f.write("vt %.6f %.6f\n" % (mesh_uv_layer.data[i].uv[0], mesh_uv_layer.data[i].uv[1]))
            f.write("\n")

        # TODO: this is very inefficient because of the way that blender stores the UVs.
        # exploit point position to reduce the amount of vertex coordinates
        uv_idx = 1
        for p in mesh_obj.polygons:
            f.write("f")
            for i in p.vertices:
                f.write(" %d/%d" % (i + 1, uv_idx))
                uv_idx += 1
            f.write("\n")


        #for n in mesh_obj.vertex_normals:
        #    f.write("vn %.4f %.4f %.4f\n" % (n[0], n[1], n[2]))