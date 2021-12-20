# topas-create-graphs

## A script to automatically plot the results of a topas simulation

Works for percentage depth dose (pdd) and dose profiles (dp). Depth dose measurements are assumed to  
be in the z-direction, dose profiles in the x- or y-directions.  

## Automatically calculates relevant parameters

| Measurement type | Parameters |         |              |             |                |                 |
|------------------|:----------:|:-------:|:------------:|:-----------:|:--------------:|:---------------:|
|                  |            |         |              |             |                |                 |
| Depth dose       |  Q-Factor  |  z<sub>max</sub>  |              |             |                |                 |
|                  |            |         |              |             |                |                 |
| Dose profile     |    FWHM    | CAX<sub>dev</sub>  | FLAT<sub>Krieger</sub>  | FLAT<sub>stddev</sub>  | Penumbra (L&R) | Integral (L&R)  |

- Q-Factor : Radiation Quality Factor
- z<sub>max</sub> : Depth at Maximum

- FWHM : Full-Width at Half-Maximum
- CAX<sub>dev</sub> : Centre Axis Deviation
- FLAT<sub>Krieger</sub> : Flatness of Dose Plateau (Definitionby Krieger)
- FLAT<sub>stddev</sub> : Flatness of Dose Plateau (Standard Deviation)
- Penumbra (L&R) : Width of Left and Right Penumbra
- Integral (L&R) : Integral below Left and Right Penumbra

## Includes an optional GUI

The script is intended as a command line tool, where the first argument is the path to the file,
and the second is the number of histories. However, the GUI can also be used. It comes with basic
file selection and preview of the graph, as well as the option to save the graph.

### Assumes a ".csv" input file format from a TOPAS Scorer with the following header format:

\# TOPAS Version: {...}  
\# Parameter File: {...}.txt  
\# Results for scorer {...}  
\# Scored in component: {...}  
\# X in {...} bin of {...} cm  
\# Y in 1 {...} of {...} cm  
\# Z in {...} bins of {...} cm  
\# DoseToMedium ( Gy ) : {Sum/Mean}   Standard_Deviation     
Voxel Coordinate X, Voxel Coordinate Y, Voxel Coordinate Z, {Sum/Mean} Value, Standard_Deviation Value   
                 .   
                 .   
                 .   
## Dependencies

Uses the beautiful Azure-ttk dark theme by @rdbende.
Requires python3, numpy, scipy, matplotlib, PIL, cv2, and tkinter.
