# topasgraphsim

## A interface to automatically plot the results of topas simulations and measurements

Works for percentage depth dose (pdd) and dose profiles (dp). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions.
Available languages: english and german.
<br></br>          
![image](https://user-images.githubusercontent.com/87897942/150243578-4dc4f73c-0f0b-4852-9553-0f31ba0f18d3.png)
<br></br>
## Installation

Install using pip:

```console
pip install topasgraphmc     
```
     
Then, start the GUI by running:
     
```console
python -m topasgraphsim
```
     
## Automatically calculates relevant parameters

| Measurement type | Parameters |                   |                        |                       |                |                |
| ---------------- | :--------: | :---------------: | :--------------------: | :-------------------: | :------------: | :------------: |
|                  |            |                   |                        |                       |                |                |
| Depth dose       |  Q-Factor  |  z<sub>max</sub>  |                        |                       |                |                |
|                  |            |                   |                        |                       |                |                |
| Dose profile     |    FWHM    | CAX<sub>dev</sub> | FLAT<sub>Krieger</sub> | FLAT<sub>stddev</sub> | Penumbra (L&R) | Integral (L&R) |

- Q-Factor : Radiation Quality Factor
- z<sub>max</sub> : Depth at Maximum

- FWHM : Full-Width at Half-Maximum
- CAX<sub>dev</sub> : Centre Axis Deviation
- FLAT<sub>Krieger</sub> : Flatness of Dose Plateau (Definitionby Krieger)
- FLAT<sub>stddev</sub> : Flatness of Dose Plateau (Standard Deviation)
- Penumbra (L&R) : Width of Left and Right Penumbra
- Integral (L&R) : Integral below Left and Right Penumbra

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
Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pywin32, and tkinter.
