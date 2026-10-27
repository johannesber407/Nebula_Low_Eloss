#script for gernerating a .tri file for a rough surface with a given RMS roughness. The .tri file can be used as input for the simulation.
import math
import open3d as o3d
import numpy as np


# ============================================================
# Geometry parameters
# ============================================================

#define geometry variables:

sample_half=1000
sample_depth=2000
sample_roughness=50 #~ RMS (stimmt nur ungefähr)

n_grid=100
n_vertices=n_grid**2
detector_distance=100
filename = "rough_surface_rms_50.tri"




# ============================================================
# Helpers
# ============================================================

triangles = []


def add_triangle(mat_in, mat_out, p1, p2, p3):
    """Add one triangle to the geometry."""
    triangles.append((mat_in, mat_out, p1, p2, p3))


def add_quad(mat_in, mat_out, p1, p2, p3, p4):
    """Split a quadrilateral into two triangles."""
    add_triangle(mat_in, mat_out, p1, p2, p3)
    add_triangle(mat_in, mat_out, p1, p3, p4)


def fmt_point(p):
    return " ".join(f"{x:.6f}" for x in p)


# ============================================================
# Sample surface
# ============================================================

if sample_roughness <= 0:
    #flat surface
    s1 = (-sample_half, -sample_half, 0)
    s2 = ( sample_half, -sample_half, 0)
    s3 = ( sample_half,  sample_half, 0)
    s4 = (-sample_half,  sample_half, 0)

    add_quad(0, -123, s1, s2, s3, s4)

else:
    #generate rough surface
    #generate random points in 3d resembling rough surface on even mesh
    z=np.random.normal(0,sample_roughness,n_vertices)
    x,y=np.meshgrid(np.linspace(-sample_half,sample_half,n_grid),np.linspace(-sample_half,sample_half,n_grid))

    #make data fit each other
    z=z.reshape(n_grid,n_grid)

    #make the perimeter of the mesh flat
    z[0,:]=0
    z[-1,:]=0
    z[:,0]=0
    z[:,-1]=0



    #generate a random point cloud
    pcd=o3d.geometry.PointCloud()
    pcd.points=o3d.utility.Vector3dVector(np.column_stack((x.ravel(), y.ravel(), z.ravel())))

    #generate mesh from point cloud
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(k=100)

    poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=11, scale=1)

    # Find connected triangle components
    triangle_clusters, cluster_n_triangles, cluster_area = (
        poisson_mesh.cluster_connected_triangles()
    )

    triangle_clusters = np.asarray(triangle_clusters)
    cluster_n_triangles = np.asarray(cluster_n_triangles)
    cluster_area = np.asarray(cluster_area)

    # Keep only components with enough triangles
    min_triangles = 50

    remove_triangles = (
        cluster_n_triangles[triangle_clusters] < min_triangles
    )
    poisson_mesh.remove_triangles_by_mask(remove_triangles)

    #remove vertices wothout tringle
    poisson_mesh.remove_unreferenced_vertices()


    for triangle in poisson_mesh.triangles:
        p1 = poisson_mesh.vertices[triangle[0]]
        p2 = poisson_mesh.vertices[triangle[1]]
        p3 = poisson_mesh.vertices[triangle[2]]
        add_triangle(-123, 0, p1, p2, p3)


# ============================================================
# Sample block
# ============================================================
s10=(-sample_half, -sample_half, 0)
s20=( sample_half, -sample_half, 0)
s30=( sample_half,  sample_half, 0)
s40=(-sample_half,  sample_half, 0)

s11=(-sample_half, -sample_half, -sample_depth)
s21=( sample_half, -sample_half, -sample_depth)
s31=( sample_half,  sample_half, -sample_depth)
s41=(-sample_half,  sample_half, -sample_depth)

add_quad(-122, -122, s10, s20, s21, s11)
add_quad(-122, -122, s20, s30, s31, s21)
add_quad(-122, -122, s30, s40, s41, s31)
add_quad(-122, -122, s40, s10, s11, s41)
add_quad(-127, -127, s11, s21, s31, s41)


# ============================================================
# Detector
# ============================================================

# Detector material is -126.
#
# The normal must point toward the sample.
# Since this is a boundary between the same material,
# orientation does not affect the detector material assignment.

d1 = (-sample_half, -sample_half, detector_distance)
d2 = ( sample_half, -sample_half, detector_distance)
d3 = ( sample_half,  sample_half, detector_distance)
d4 = (-sample_half,  sample_half, detector_distance)

add_quad(-126, -126, d1, d2, d3, d4)


# ============================================================
# Mirror tube
# ============================================================
#
# The tube follows the detector viewing direction.
#
# Its cross-section is the same 1000 x 1000 nm square as
# the sample. The tube extends from the sample to the
# detector region.
#
add_quad(-122, -122, s10, s20, d2, d1)
add_quad(-122, -122, s20, s30, d3, d2)
add_quad(-122, -122, s30, s40, d4, d3)
add_quad(-122, -122, s40, s10, d1, d4)




# ============================================================
# Write .tri file
# ============================================================

#create .tri file


with open(filename, "w") as f:
    for mat_in, mat_out, p1, p2, p3 in triangles:
        f.write(
            f"{mat_in:4d} {mat_out:4d}  "
            f"{fmt_point(p1)}   "
            f"{fmt_point(p2)}   "
            f"{fmt_point(p3)}\n"
        )

print(f"Wrote {filename}")
if sample_roughness > 0:
    #calculate rms
    rms = np.sqrt(np.mean(z**2))
    print(f"RMS: {rms:.2f}")
else:
    print("RMS: 0.00")
