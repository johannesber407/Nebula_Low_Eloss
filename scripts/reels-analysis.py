#script to analyze the output of the simulation (use, when the simulation is run with the option to save only energies and pixel indices)
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
    ('px', '=i'), ('py', '=i'),               # Pixel index
    ])                   

output_path="reels_energy.csv"


# Open the output file
data = np.fromfile(filename, dtype=electron_dtype)
print("Number of electrons detected: {}".format(len(data)))



# Make a histogram of energies
N_bins = 4*int(np.max(data['E']))
spectrum, bin_edges = np.histogram(data['E'], bins=N_bins)
bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2
np.savetxt(output_path, np.column_stack((bin_centers, spectrum)), delimiter=",", header="energy (eV), intensity", fmt='%f, %f')

