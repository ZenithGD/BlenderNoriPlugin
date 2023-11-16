import bpy
from bpy import context

def write_obj(mesh, path : str, store_normals : bool = False):
    """Write mesh to .obj file

    Args:
        mesh (mesh): The blender mesh object
        path (str): The path to write the obj file
    """
    mesh_obj = mesh.to_mesh()
    # https://blender.stackexchange.com/questions/32468/how-to-write-a-simple-wavefront-obj-exporter-in-python
    with open(path, 'w') as f:
        f.write("# OBJ file\n")
        for v in mesh_obj.vertices:
            f.write("v %.4f %.4f %.4f\n" % v.co[:])
        for p in mesh_obj.polygons:
            f.write("f")
            for i in p.vertices:
                f.write(" %d" % (i + 1))
            f.write("\n")
