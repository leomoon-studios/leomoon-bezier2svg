import bpy
from bpy.props import *
from mathutils import Vector, Matrix
from bpy_extras.io_utils import ExportHelper

elmul = lambda x,y:Vector([a*b for a,b in zip(x,y)])

class SVGFile:
    svg_template = '''
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
 <!-- Created with LeoMoon Bezier2SVG -->

{layers}
</svg>
'''

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []

    def to_string(self):
        return SVGFile.svg_template.format(width=self.width, height=self.height, layers=''.join([str(l) for l in self.layers]))

    def new_layer(self, title, path):
        layer = SVGFile.Layer(title, path)
        self.layers.append(layer)
        return layer

    class Layer:
        svg_layer_template = '''
 <g>
 <title>{title}</title>
 <path fill="#fff" stroke="#000" stroke-width="1.5" opacity="0.5" d="{path}" id="svg_{title}"/>
 </g>
'''
        def __init__(self, title, path):
            self.title = title
            self.path=path
        
        def __str__(self):
            return SVGFile.Layer.svg_layer_template.format(title=self.title, path=self.path)

class BEZIER2SVG_OT_export(bpy.types.Operator, ExportHelper):
    """Export Bezier curve as SVG"""
    bl_idname = "bezier2svg.export"
    bl_label = "Bezier2SVG (.svg)"

    # ExportHelper mixin class uses this
    filename_ext = ".svg"
    filter_glob: StringProperty(
        default="*.svg",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    # ###

    selection_only : BoolProperty(name="Selection only", description="Export selected objects only", default=True)
    
    projection_axis : EnumProperty(
        items=[
            ('Z', 'Z', '', 0),
            ('-Z', '-Z', '', 1),
            ('X', 'X', '', 2),
            ('-X', '-X', '', 3),
            ('Y', 'Y', '', 4),
            ('-Y', '-Y', '', 5),
            ('Viewport', 'Viewport', '', 6),
        ],
        name="Projection Axis",
        description="Projection along global axis",
        default="Viewport"
    )

    scale : FloatProperty(name="Scale (px / Blender Unit) ", description="Scale of exported image", default=100)
    
    def execute(self, context):
        def projectPoint(object, point: Vector):
            if(self.projection_axis == '-X'):
                m = Matrix((
                    (0.0, -1.0, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (-1.0, 0.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == 'X'):
                m = Matrix((
                    (0.0, 1.0, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (1.0, 0.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == '-Y'):
                m = Matrix((
                    (1.0, 0.0, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, -1.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == 'Y'):
                m = Matrix((
                    (-1.0, 0.0, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == '-Z'):
                m = Matrix((
                    (1.0, -0.0, 0.0, 0.0),
                    (0.0, -1.0, 0.0, 0.0),
                    (-0.0, 0.0, -1.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == 'Z'):
                m = Matrix((
                    (1.0, 0.0, 0.0, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)))
            elif(self.projection_axis == 'Viewport'):
                a = [a for a in context.window.screen.areas if a.type == 'VIEW_3D'].pop()
                m = a.spaces.active.region_3d.view_matrix

            return m @ (object.matrix_world @ point)

        def canvas_bounding_box(objects):
            bounding_points = [projectPoint(ob, Vector(bp)) for ob in objects for bp in ob.bound_box]
            min_x = min(bounding_points, key=lambda a: a[0])[0]
            max_x = max(bounding_points, key=lambda a: a[0])[0]
            min_y = min(bounding_points, key=lambda a: a[1])[1]
            max_y = max(bounding_points, key=lambda a: a[1])[1]

            origin = Vector((
                min_x,
                max_y,
                0
            ))

            size = Vector((max_x-min_x, max_y-min_y))
            return origin, size

        def parse_point(object, point: Vector) -> tuple:
            # move to svg coords

            p = (projectPoint(object, point) - origin)*self.scale
            p.y *= -1
            return p[:2]
        
        def parse_segment(object, start_point: bpy.types.BezierSplinePoint, end_point: bpy.types.BezierSplinePoint):
            return "C {:5.11f} {:5.11f}, {:5.11f} {:5.11f}, {:5.11f} {:5.11f} \n".format(
                *(
                    parse_point(object, start_point.handle_right)+
                    parse_point(object, end_point.handle_left)+
                    parse_point(object, end_point.co)
                )
            )
            

        if self.selection_only:
            objects = [ob for ob in context.visible_objects if ob.type=='CURVE' and ob.select_get() == True]
        else:
            objects = [ob for ob in context.visible_objects if ob.type=='CURVE']
        
        origin, canvas_size = canvas_bounding_box(objects)
        svg_file = SVGFile(*(canvas_size*self.scale))
        for object in objects:
            splines = object.data.splines
            path = ''
            for spline in splines:
                if len(spline.bezier_points):
                    first_point = spline.bezier_points[0]
                    last_point = spline.bezier_points[-1]

                    path += "M {:5.11f} {:5.11f} \n".format(*parse_point(object, first_point.co))
                    for prev_idx, b_point in enumerate(spline.bezier_points[1:]):
                        prev_point = spline.bezier_points[prev_idx]
                        path += parse_segment(object, prev_point, b_point)
                    
                    if spline.use_cyclic_u:
                        path += parse_segment(object, last_point, first_point)
                else:
                    print('Non-bezier curve not exported in object: %s' % object.name)
                    self.report({'WARNING'}, 'Non-bezier curve not exported in object: %s' % object.name)
            if path:
                svg_file.new_layer(object.name, path)

        with open(self.filepath, 'w') as f:
            f.write(svg_file.to_string())

        return {'FINISHED'}

export_menu = lambda self, context: self.layout.operator("bezier2svg.export")
def register():
    bpy.types.TOPBAR_MT_file_export.append(export_menu)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(export_menu)