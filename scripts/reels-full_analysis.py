#script for analyzing the full output of the simulation (use, when the simulation is run with the option to save path lengths, scatterings, and primary/secondary)
import sys
import os
import numpy as np


# Find out which file to open
if len(sys.argv) < 2:
	print("No output file provided")
	sys.exit()
filename = sys.argv[1]
if not os.path.exists(filename):
	print("File {} cannot be found".format(filename))
	sys.exit()


# This is a numpy datatype that corresponds to output files
electron_dtype = np.dtype([
    ('x',  '=f'), ('y',  '=f'), ('z',  '=f'), # Position
    ('dx', '=f'), ('dy', '=f'), ('dz', '=f'), # Direction
    ('E',  '=f'),                             #Energy
    ('path_length', '=f'),                     # path length
    ('n_elastic', '=f'), ('n_inelastic', '=f'), ('n_surface', '=f'),
    ('elastic_loss', '=f'), ('inelastic_loss', '=f'), ('surface_loss', '=f'),
    ('px', '=i'), ('py', '=i'),               # Pixel index
    ('is_secondary', '=i'), # Flag for secondary electrons
    ])                   

output_path="reels_{}.csv"


# Open the output file
data = np.fromfile(filename, dtype=electron_dtype)
print("Number of electrons detected: {}".format(len(data)))

#OPTIONAL: remove secondary electrons
data = data[data['is_secondary'] == 0]
print(len(data), "primary electrons detected")

# Make a histogram of energies
N_bins = 4*int(np.max(data['E']))
spectrum, bin_edges = np.histogram(data['E'], bins=N_bins)
bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2
np.savetxt(output_path.format("primaries"), np.column_stack((bin_centers, spectrum)), delimiter=",", header="omega, intensity", fmt='%f, %f')

#histogram of path lengths
N_bins=4*int(np.max(data['path_length']))
path_length_hist, bin_edges_path_length = np.histogram(data['path_length'], bins=N_bins)
bin_centers_path_length = (bin_edges_path_length[1:] + bin_edges_path_length[:-1]) / 2
np.savetxt(output_path.format("path_length"), np.column_stack((bin_centers_path_length, path_length_hist)), delimiter=",", header="path_length, count", fmt='%f, %d')

#histogram of inelastic, elastic, surface losses
N_bins=4*int(np.max(data['elastic_loss']))
elastic_loss_hist, bin_edges_elastic_loss = np.histogram(data['elastic_loss'], bins=N_bins)
bin_centers_elastic_loss = (bin_edges_elastic_loss[1:] + bin_edges_elastic_loss[:-1]) / 2
np.savetxt(output_path.format("elastic_loss"), np.column_stack((bin_centers_elastic_loss, elastic_loss_hist)), delimiter=",", header="elastic_loss, count", fmt='%f, %d')     

N_bins=4*int(np.max(data['inelastic_loss']))
inelastic_loss_hist, bin_edges_inelastic_loss = np.histogram(data['inelastic_loss'], bins=N_bins)
bin_centers_inelastic_loss = (bin_edges_inelastic_loss[1:] + bin_edges_inelastic_loss[:-1]) / 2
np.savetxt(output_path.format("inelastic_loss"), np.column_stack((bin_centers_inelastic_loss, inelastic_loss_hist)), delimiter=",", header="inelastic_loss, count", fmt='%f, %d')     

N_bins=4*int(np.max(data['surface_loss']))
surface_loss_hist, bin_edges_surface_loss = np.histogram(data['surface_loss'], bins=N_bins)
bin_centers_surface_loss = (bin_edges_surface_loss[1:] + bin_edges_surface_loss[:-1]) / 2
np.savetxt(output_path.format("surface_loss"), np.column_stack((bin_centers_surface_loss, surface_loss_hist)), delimiter=",", header="surface_loss, count", fmt='%f, %d')     

#histogram of number of elastic, inelastic, surface events
bins=np.arange(0, np.max(data['n_elastic'])+2)-0.5
n_elastic_hist, bin_edges_n_elastic = np.histogram(data['n_elastic'], bins=bins)
bin_centers_n_elastic = (bin_edges_n_elastic[1:] + bin_edges_n_elastic[:-1]) / 2
np.savetxt(output_path.format("n_elastic"), np.column_stack((bin_centers_n_elastic, n_elastic_hist)), delimiter=",", header="n_elastic, count", fmt='%f, %d')

bins=np.arange(0, np.max(data['n_inelastic'])+2)-0.5
n_inelastic_hist, bin_edges_n_inelastic = np.histogram(data['n_inelastic'], bins=bins)
bin_centers_n_inelastic = (bin_edges_n_inelastic[1:] + bin_edges_n_inelastic[:-1]) / 2
np.savetxt(output_path.format("n_inelastic"), np.column_stack((bin_centers_n_inelastic, n_inelastic_hist)), delimiter=",", header="n_inelastic, count", fmt='%f, %d')       

bins=np.arange(0, np.max(data['n_surface'])+2)-0.5
n_surface_hist, bin_edges_n_surface = np.histogram(data['n_surface'], bins=bins)
bin_centers_n_surface = (bin_edges_n_surface[1:] + bin_edges_n_surface[:-1]) / 2
np.savetxt(output_path.format("n_surface"), np.column_stack((bin_centers_n_surface, n_surface_hist)), delimiter=",", header="n_surface, count", fmt='%f, %d')


