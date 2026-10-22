# Nebula

This is a project for adjusting the [Nebula](https://github.com/nebula-simulator/nebula) Monte Carlo simulator for precise calculations of low energy losses. 

# How to use
For instructions on how to install and use this software, see the original 
[documentation](https://nebula-simulator.github.io). 
* Instead of using the original cstool, use the version provided [HERE](https://github.com/johannesber407/cstool_Low_Eloss) - this version provides information for the spectra of surface excitations (currently only for gold). 
* This version Nebula saves additional information about the interactions of the particles, like the path length, the inelastic/elastic and surface scattering events, and information about wheather a particle is the primary or secondary electron. To process the output of the simulation accordingly, use [this script](https://github.com/johannesber407/Nebula_Low_Eloss/blob/master/scripts/reels-full_analysis.py).
* This version of Nebula behaves exactly like the original version of Nebula, if the flag for surface excitations, for the output of path length, for the scattering couts and energy losses, and for the primary/secondary are set to false in [physics_config.h](https://github.com/johannesber407/Nebula_Low_Eloss/blob/master/source/physics_config.h). In this case, use [this script](https://github.com/johannesber407/Nebula_Low_Eloss/blob/master/scripts/reels-analysis.py) for the analysis.

# Adjustments
Adjustments of Nebula that have been implemented, to make Nebula more precise for computing the Energy loss spectra especially for low losses:
* Use the correct formula for losses due to recoil - in the original version of Nebula, the recoil losses were implemented incorrectly (see: https://github.com/Nebula-simulator/Nebula/issues/17)
* Implement losses due to surface excitations (see for example https://doi.org/10.1016/j.susc.2007.06.076) 
* Make it possible to access the path lengths, number of scatterings, and information whether a particle is a secondary or a primary. 

# Further Plans for Adjustments

* Implement Doppler broadening at finite temperatures (see for example  https://doi.org/10.1002/sia.1121 )
