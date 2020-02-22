import pygmsh
import math
import meshio

lc = 0.005 # Mesh/Characteristic length
front3d = 0 # Set to 1 if Frontal 3D mesh algorithm is used
turns = 5 # Geometry/Number of coil turns
r = 0.11 # Geometry/Coil radius
rc = 0.01 #Geometry/Coil wire radius
hc = 0.2 # Geometry/Coil height
legsLength = 0.4 # Geometry/Legs length
ht = 0.3 # Geometry/Tube height
rt1 = 0.081 # Geometry/Tube internal radius
rt2 = 0.092 # Geometry/Tube external radius
lb = 1 # Geometry/Infinite box width
left = 1 # Geometry/Terminals on the left?

geom = pygmsh.built_in.Geometry()
# inductor
p0 = geom.add_point([-legsLength, -r, -hc/2], lc)
p1 = geom.add_point([-legsLength, -r+rc, -hc/2], lc)
p2 = geom.add_point([-legsLength, -r, -hc/2+rc], lc)
p3 = geom.add_point([-legsLength, -r-rc, -hc/2], lc)
p4 = geom.add_point([-legsLength, -r, -hc/2-rc], lc)

c0 = geom.add_circle_arc(p1,p0,p2)
c1 = geom.add_circle_arc(p2,p0,p3)
c2 = geom.add_circle_arc(p3,p0,p4)
c3 = geom.add_circle_arc(p4,p0,p1)

ll = geom.add_line_loop([c0, c1, c2,c3])

s = geom.add_plane_surface(ll)
last_extruded = s
vol_coil = list()
in_leg, b, _ = geom.extrude(s, translation_axis=[legsLength, 0, 0], recombine=True)
last_extruded = in_leg
vol_coil.append(b)

samedirection = True
iterations = 4 * turns + 2 if samedirection else 0
for i in range(0, iterations): 
    a, b, _ = geom.extrude(
            last_extruded, 
            translation_axis=[0, 0, hc/turns/4], 
            rotation_axis=[0,0,1],
            point_on_axis=[0,0,0], 
            angle=math.pi/2
            )
    last_extruded = a
    vol_coil.append(b)


out_leg, b, _ = geom.extrude(last_extruded, translation_axis=[legsLength * -1 if samedirection else 1, 0, 0], recombine=True)
vol_coil.append(b)

mesh = pygmsh.generate_mesh(geom)
points = mesh.points
cells = mesh.cells
cells_tetra = cells["tetra"]
cells_triangle = cells["triangle"]
cells_vertex = cells["vertex"]
meshio.write_points_cells('coil.obj', points, cells)

