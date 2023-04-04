# <p align="center">TopasGraphSim</p>

## <p align="center">A GUI to simplify and streamline the plotting and analysis of medical physics simulations</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/87897942/152699152-d4d39654-4449-4354-b899-4adc81eb25a7.png" width="320" height="160" />
</p>

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data read-in is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).

## Installation

Install using pip:

```console
$ pip install topasgraphsim     
```
     
Then, start the GUI by running:
     
```console
$ python -m topasgraphsim
```

Or, if your Python is added to $PATH, simply run:

```console
$ topasgraphsim
```

Open compatible files from the command line:

```console
$ topasgraphsim "path_to_your_file"
```

Since all my testing in done on Windows 11, I cannot guarantee ToapsGrapSim will work on any other plattform. I'm open to suggestions or PRs making the software work better cross-plattfrom!

## Features

Visit the [wiki](https://github.com/sebasj13/TopasGraphSim/wiki) for detailed information!

Highlights include:

 - Reproducible graphing and analysis of 1D TOPAS simulation for medical physics
 - Simultaneous plotting and parameter calculation for all data sets
 - Calculation of the Gamma Index with adjustable parameters
 - Graph adjustment options
     * Normalization (On/Off)
     * Error bars (On/Off)
     * Graph order and colors
     * Marker size and style
     * Line width
 - Drag and drop of files
 - Center axis deviation correction
 - Import of EGS and RadCalc simulation results *
 - Import of custom measurements (as numpy .txt files) *
 - Import of PTW tbaScan (MEPHYSTO mc<sup>2</sup>) measurements
 - German and english language support
 - Dark mode

 (*) Not yet implemented

 ## Screenshots
 
 ![main](https://user-images.githubusercontent.com/87897942/229850354-928239ef-dba8-49f3-b0bf-b5b7272b2e4c.png)

![tab](https://user-images.githubusercontent.com/87897942/229850628-639411bc-1b1f-4f13-bb67-0866a4d8decb.png)

 ## Parameters

Depending on the imported measurement, the following parameters can be calculated:

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
- FLAT<sub>Krieger</sub> : Flatness of Dose Plateau (Definition by Krieger)
- FLAT<sub>stddev</sub> : Flatness of Dose Plateau (Standard Deviation)
- Penumbra (L&R) : Width of Left and Right Penumbra
- Integral (L&R) : Integral below Left and Right Penumbra

## Dependencies

The UI is based on the [customtkinter](http://github.com/TomSchimansky/CustomTkinter) library.

Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pynput, requests, topas2numpy, and python-tkdnd.
## Contact me!

Thank you for using TopasGraphSim! Please let me know about any issues you encounter, or suggestions/wishes you might have! 
<br></br>
[![Downloads](https://static.pepy.tech/personalized-badge/topasgraphsim?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/topasgraphsim)
