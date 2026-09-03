# Nebula

This is a project for adjusting the [Nebula](https://github.com/nebula-simulator/nebula) Monte Carlo simulator for precise calculations of low Energy losses. For
instructions on how to install and use this software, see the original 
[documentation](https://nebula-simulator.github.io).

# Adjustments
Adjustments of Nebula I plan to work on, to make Nebula more precise for computing the Energy loss spectra especially for low losses:
* Use the correct formula for losses due to recoil (done)
* Implement losses due to surface excitations (see for example https://doi.org/10.1016/j.susc.2007.06.076) (done)
* Make it possible to choose between datasets for the optical data (e.g. use data from https://doi.org/10.1063/1.3243762)
* Make it possible to export the trajectories of the particles 
