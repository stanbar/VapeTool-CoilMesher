import pygmsh
import math
import meshio

def legs_go_same_direction(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def normalcoil(wraps, innerDiameter, wireDiameter, legsLength):
    normalization_factor = 0.4/legsLength
    legsLength *= normalization_factor
    innerDiameter *= normalization_factor
    wireDiameter *= normalization_factor
    samedirection = legs_go_same_direction(wraps)
    wraps = math.floor(wraps)
    coilHeight = wraps * wireDiameter / 1.8

    lc = 0.005 # Mesh/Characteristic length
    front3d = 0 # Set to 1 if Frontal 3D mesh algorithm is used

    print("legsLength: {} innerDiameter: {} coilHeight: {} wireDiameter: {}".format(legsLength, innerDiameter, coilHeight, wireDiameter))

    geom = pygmsh.built_in.Geometry()
    # inductor
    p0 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2], lc)
    p1 = geom.add_point([-legsLength, -innerDiameter+wireDiameter, -coilHeight/2], lc)
    p2 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2+wireDiameter], lc)
    p3 = geom.add_point([-legsLength, -innerDiameter-wireDiameter, -coilHeight/2], lc)
    p4 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2-wireDiameter], lc)

    c0 = geom.add_circle_arc(p1,p0,p2)
    c1 = geom.add_circle_arc(p2,p0,p3)
    c2 = geom.add_circle_arc(p3,p0,p4)
    c3 = geom.add_circle_arc(p4,p0,p1)

    ll = geom.add_line_loop([c0, c1, c2,c3])

    s = geom.add_plane_surface(ll)
    last_extruded = s
    vol_coil = list()
    in_leg, b, _ = geom.extrude(s, translation_axis=[legsLength, 0, 0])
    last_extruded = in_leg
    vol_coil.append(b)

    iterations = 4 * wraps + (2 if samedirection else 0)
    for i in range(0, iterations): 
        a, b, _ = geom.extrude(
                last_extruded, 
                translation_axis=[0, 0, coilHeight/wraps], 
                rotation_axis=[0,0,1],
                point_on_axis=[0,0,0], 
                angle=math.pi/2
                )
        last_extruded = a
        vol_coil.append(b)


    out_leg, b, _ = geom.extrude(last_extruded, translation_axis=[legsLength * (-1 if samedirection else 1), 0, 0])
    vol_coil.append(b)
    return geom

def parallelcoil(wraps, innerDiameter, wireDiameter, legsLength, parallelWires = 2):
    normalization_factor = 0.4/legsLength
    legsLength *= normalization_factor
    innerDiameter *= normalization_factor
    wireDiameter *= normalization_factor
    samedirection = legs_go_same_direction(wraps)
    wraps = math.floor(wraps)
    coilHeight = wraps * wireDiameter / 1.8 * parallelWires

    lc = 0.005 # Mesh/Characteristic length
    front3d = 0 # Set to 1 if Frontal 3D mesh algorithm is used

    print("legsLength: {} innerDiameter: {} coilHeight: {} wireDiameter: {}".format(legsLength, innerDiameter, coilHeight, wireDiameter))

    geom = pygmsh.built_in.Geometry()

    for wireNumber in range(0,parallelWires):
        p0 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2 + (wireNumber * 2 * wireDiameter) ], lc)
        p1 = geom.add_point([-legsLength, -innerDiameter+wireDiameter, - coilHeight/2 + (wireNumber * 2 * wireDiameter) ], lc)
        p2 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2 + wireDiameter + (wireNumber * 2 * wireDiameter) ], lc)
        p3 = geom.add_point([-legsLength, -innerDiameter-wireDiameter, - coilHeight/2 + (wireNumber * 2 * wireDiameter) ], lc)
        p4 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2 - wireDiameter + (wireNumber * 2 * wireDiameter) ], lc)

        c0 = geom.add_circle_arc(p1,p0,p2)
        c1 = geom.add_circle_arc(p2,p0,p3)
        c2 = geom.add_circle_arc(p3,p0,p4)
        c3 = geom.add_circle_arc(p4,p0,p1)

        ll = geom.add_line_loop([c0, c1, c2,c3])

        s = geom.add_plane_surface(ll)
        last_extruded = s
        vol_coil = list()
        in_leg, b, _ = geom.extrude(s, translation_axis=[legsLength, 0, 0])
        last_extruded = in_leg
        vol_coil.append(b)

        iterations = 4 * wraps + (2 if samedirection else 0)
        for i in range(0, iterations): 
            a, b, _ = geom.extrude(
                    last_extruded, 
                    translation_axis=[0, 0, coilHeight/wraps], 
                    rotation_axis=[0,0,1],
                    point_on_axis=[0,0,0], 
                    angle=math.pi/2
                    )
            last_extruded = a
            vol_coil.append(b)


        out_leg, b, _ = geom.extrude(last_extruded, translation_axis=[legsLength * (-1 if samedirection else 1), 0, 0])
        vol_coil.append(b)
    return geom

def claptoncoil(wraps, innerDiameter, wireDiameter, outerDiameter, legsLength):
    normalization_factor = 0.4/legsLength
    legsLength *= normalization_factor
    innerDiameter *= normalization_factor
    outerDiameter *= normalization_factor
    wireDiameter *= normalization_factor
    samedirection = legs_go_same_direction(wraps)
    wraps = math.floor(wraps)
    coilHeight = wraps * wireDiameter / 1.8 * 2

    lc = 0.010 # Mesh/Characteristic length
    front3d = 0 # Set to 1 if Frontal 3D mesh algorithm is used

    print("legsLength: {} innerDiameter: {} coilHeight: {} wireDiameter: {}".format(legsLength, innerDiameter, coilHeight, wireDiameter))

    geom = pygmsh.built_in.Geometry()
    # inductor
    p0 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2], lc)
    p1 = geom.add_point([-legsLength, -innerDiameter+wireDiameter, -coilHeight/2], lc)
    p2 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2+wireDiameter], lc)
    p3 = geom.add_point([-legsLength, -innerDiameter-wireDiameter, -coilHeight/2], lc)
    p4 = geom.add_point([-legsLength, -innerDiameter, -coilHeight/2-wireDiameter], lc)

    c0 = geom.add_circle_arc(p1,p0,p2)
    c1 = geom.add_circle_arc(p2,p0,p3)
    c2 = geom.add_circle_arc(p3,p0,p4)
    c3 = geom.add_circle_arc(p4,p0,p1)

    ll = geom.add_line_loop([c0, c1, c2,c3])

    s = geom.add_plane_surface(ll)
    last_extruded = s
    vol_coil = list()
    in_leg, b, _ = geom.extrude(s, translation_axis=[legsLength, 0, 0])
    last_extruded = in_leg
    vol_coil.append(b)

    iterations = 4 * wraps + (2 if samedirection else 0)
    for i in range(0, iterations): 
        a, b, _ = geom.extrude(
                last_extruded, 
                translation_axis=[0, 0, coilHeight/wraps], 
                rotation_axis=[0,0,1],
                point_on_axis=[0,0,0], 
                angle=math.pi/2
                )
        last_extruded = a
        vol_coil.append(b)

    out_leg, b, _ = geom.extrude(last_extruded, translation_axis=[legsLength * (-1 if samedirection else 1), 0, 0])
    vol_coil.append(b)
        
    # outer
    p0 = geom.add_point([-legsLength,                 -innerDiameter, -coilHeight/2 + 2*wireDiameter], lc)
    p1 = geom.add_point([-legsLength + outerDiameter, -innerDiameter, -coilHeight/2 + 2*wireDiameter], lc)
    p2 = geom.add_point([-legsLength,                 -innerDiameter, -coilHeight/2 + 2*wireDiameter + outerDiameter ], lc)
    p3 = geom.add_point([-legsLength - outerDiameter, -innerDiameter, -coilHeight/2 + 2*wireDiameter], lc)
    p4 = geom.add_point([-legsLength,                 -innerDiameter, -coilHeight/2 + 2*wireDiameter - outerDiameter ], lc)

    c0 = geom.add_circle_arc(p1,p0,p2)
    c1 = geom.add_circle_arc(p2,p0,p3)
    c2 = geom.add_circle_arc(p3,p0,p4)
    c3 = geom.add_circle_arc(p4,p0,p1)

    ll = geom.add_line_loop([c0, c1, c2,c3])


    s = geom.add_plane_surface(ll)
    last_extruded = s

    
    iterations = 4 * math.floor(legsLength/outerDiameter/2)
    for i in range(0, iterations): 
        a, b, _ = geom.extrude(
                last_extruded, 
                translation_axis=[outerDiameter/2, 0, 0], 
                rotation_axis=[1, 0, 0],
                point_on_axis=[-legsLength, -innerDiameter, -coilHeight/2], 
                angle=math.pi/2
                )
        last_extruded = a
        vol_coil.append(b)
    
    effectiveDiameter = innerDiameter - outerDiameter/2
    radius = (effectiveDiameter/2)
    circumference = math.pi*2*radius
    noWraps = circumference // outerDiameter
    arc = math.pi / 2 / noWraps


    return geom



def generate_mesh(geom):
    mesh = pygmsh.generate_mesh(geom)
    points = mesh.points
    cells = mesh.cells
    cells_tetra = cells["tetra"]
    cells_triangle = cells["triangle"]
    cells_vertex = cells["vertex"]
    meshio.write_points_cells('coil.obj', points, cells)


if __name__ == "__main__":
    legsLength = 15
    innerDiameter = 3.2
    wireDiameter = 0.322
    outerDiameter = 0.322
    wraps = 5
    # geom = claptoncoil(wraps, innerDiameter, wireDiameter, outerDiameter, legsLength)
    geom = parallelcoil(wraps, innerDiameter, wireDiameter, legsLength)
    geom = normalcoil(wraps, innerDiameter, wireDiameter, legsLength)
    generate_mesh(geom)