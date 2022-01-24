# topasgraphsim

## Am interface to automatically plot and interpret the results of TOPAS simulations

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data read-in is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).
<br></br>          
![Screenshot 2022-01-24 170455](https://user-images.githubusercontent.com/87897942/150819409-8b761000-df95-442f-a8fd-f599b2981918.png)

## Features

 - Simultaneous plotting and parameter calculation for up to 5 datasets
 - Graph adjustment options (marker size and line width)
 - Reproducible graphing of simulation results
 - Import of measurement results (including PTW tbaScan data)
 - Optional zoom-in window
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

Built using the beautiful Azure-ttk theme by [@rdbende](https://github.com/rdbende).
Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pywin32, topas2numpy and tkinter.
