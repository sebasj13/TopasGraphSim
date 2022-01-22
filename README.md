# topasgraphsim

## Am interface to automatically plot and interpret the results of TOPAS simulations

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data readin is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).
<br></br>          
![image](https://user-images.githubusercontent.com/87897942/150624839-cd4fa333-b52e-43a9-98ca-6f3a2e41340a.png)

## Features

 - Simultaneous plotting and parameter calculation for up to 5 datasets
 - Graph adjustment options (marker size and line width)
 - Reproducible graphing of simulation results
 - Import of measurement results
 - Easy to use keyboard shortcuts
 - Toggle for data normalization
 - German and english language support
 - Dark mode

## Installation

Install using pip:

```console
pip install topasgraphsim     
```
     
Then, start the GUI by running:
     
```console
python -m topasgraphsim
```
     
## Calculated parameters

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
     
## Dependencies

Built using the beautiful Azure-ttk theme by @rdbende.
Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pywin32, topas2numpy and tkinter.
