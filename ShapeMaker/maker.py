from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal

class ShapeMaker:
    @staticmethod
    def make(shape_type, *args, **kwargs):
        if shape_type == "box":
            return ShapeMaker.make_box(*args, **kwargs)
        elif shape_type == "cylinder":
            return ShapeMaker.make_cylinder(*args, **kwargs)
        elif shape_type == "sphere":
            return ShapeMaker.make_sphere(*args, **kwargs)
        elif shape_type == "cone":
            return ShapeMaker.make_cone(*args, **kwargs)
        elif shape_type == "torus":
            return ShapeMaker.make_torus(*args, **kwargs)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
            
    @staticmethod
    def make_box(length, width, height):
        box = BRepPrimAPI_MakeBox(length, width, height).Shape()
        return box

    @staticmethod
    def make_cylinder(radius, height):
        cylinder = BRepPrimAPI_MakeCylinder(radius, height).Shape()
        return cylinder
    
    @staticmethod
    def make_sphere(radius):
        sphere = BRepPrimAPI_MakeSphere(radius).Shape()
        return sphere

    @staticmethod
    def make_cone(radius, height):
        cone = BRepPrimAPI_MakeCone(radius, 0, height).Shape()
        return cone
    
    @staticmethod
    def make_torus(major_radius, minor_radius):
        torus = BRepPrimAPI_MakeTorus(major_radius, minor_radius).Shape()
        return torus

    @staticmethod
    def save_shape(shape, filepath):
        step_writer = STEPControl_Writer()
        Interface_Static_SetCVal("write.step.schema", "AP203")
        step_writer.Transfer(shape, STEPControl_AsIs)
        status = step_writer.Write(filepath)
        if status != 1:
            print(f"[ERROR] Failed to write shape to {filepath}")
        else:
            print(f"[INFO] Shape saved to {filepath}")
        