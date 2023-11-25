import bpy
from bpy import context

import inspect,pprint

def write_obj(mesh : bpy.types.Object, path : str, store_normals : bool = False):
    """Write mesh to .obj file

    Args:
        mesh (mesh): The blender mesh object
        path (str): The path to write the obj file
    """
    mesh_w_matrix = mesh.matrix_world
    mesh_obj = mesh.to_mesh()

    
    # https://blender.stackexchange.com/questions/32468/how-to-write-a-simple-wavefront-obj-exporter-in-python
    with open(path, 'w') as f:
        f.write("# OBJ file\n")
        for v in mesh_obj.vertices:
            v_w = mesh_w_matrix @ v.co
            print(v_w)
            f.write("v %.4f %.4f %.4f\n" % (v_w[0], v_w[1], v_w[2]))
        for p in mesh_obj.polygons:
            f.write("f")
            for i in p.vertices:
                f.write(" %d" % (i + 1))
            f.write("\n")
