# TopasGraphSim

<p align="center">
<img src="https://user-images.githubusercontent.com/87897942/152699152-d4d39654-4449-4354-b899-4adc81eb25a7.png" width="320" height="160" />
</p>

## An interface to automatically plot and interpret the results of TOPAS simulations

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data read-in is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).


## Features

 - Reproducible graphing and analysis of TOPAS simulation for medical physics
 - Simultaneous plotting and parameter calculation for up to 5 datasets
 - Graph adjustment options
     * Normalization (On/Off)
     * Error bars (On/Off)
     * Difference plot between two datasets
     * Graph order and colors
     * Marker size
     * Line width
     * Zoom-in window
     * Half view of dose profiles
 - Center axis deviation correction
 - Import of EGS simulation results
 - Import of custom measurements (as numpy .txt files)
 - Import of PTW tbaScan (MEPHYSTO mc<sup>2</sup>) measurements
 - Easy to use keyboard shortcuts (see manual below)
 - German and english language support
 - Dark mode

 ## Screenshots
 
 ![dpp](https://user-images.githubusercontent.com/87897942/152709224-aff50e72-bea7-4782-a8c9-54f58a06cef3.png)

![dp](https://user-images.githubusercontent.com/87897942/152709235-7a1cf3d9-5002-4ddc-b144-cb51527693e3.png)

 ## Manual

 Most customization options are available via the menubar, however the workflow can be sped up greatly by using the included keyboard and mouse shortcuts documented below.

 ### Loading and saving data

|Keyboard Shortcut| Associated Function |
|---|---|
| <kbd>Ctrl</kbd> + <kbd>O</kbd> | Open a TOPAS simulation file [*.csv *.bin] |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Open a PTW tbaScan file [*.mcc]            |
| <kbd>Ctrl</kbd> + <kbd>T</kbd> | Open a PDD measurement file [*.txt]        |
| <kbd>Ctrl</kbd> + <kbd>D</kbd> | Open a DP measurement file [*.txt]         |
| <kbd>Ctrl</kbd> + <kbd>S</kbd> | Save the current graph [*.png *.jpg]       |
| <kbd>Ctrl</kbd> + <kbd>Z</kbd> | Remove the last imported dataset           |
| <kbd>Escape</kbd>              | Close the current project           |

### Adjusting the Graph Style

|Mouse/Keyboard Shortcut| Associated Function |
|---|---|
| <kbd>Ctrl</kbd> + <kbd>↑</kbd> <kbd>↓</kbd> | Increase/decrease the marker size|
| <kbd>Ctrl</kbd> + <kbd>←</kbd> <kbd>→</kbd> | Increase/decrease the line width |
| <kbd>Scrollwheel</kbd>                      | Increase/decrease the X-axis limits |
| <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>+</kbd> <kbd>-</kbd> | Increase/decrease the error plot upper limits |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>+</kbd> <kbd>-</kbd> | Increase/decrease the error plot lower limits |
| <kbd>Double Left Click</kbd> on <kbd>Graph</kbd>| Change zoom window location |
| <kbd>Left Click</kbd> on <kbd>Bottom Axis</kbd>| Open axis range selector |
| <kbd>Left Click</kbd> on <kbd>Bottom Axis</kbd>| Rename bottom axis |


### Adjusting the Graph Legend

|Mouse/Keyboard Shortcut| Associated Function |
|---|---|
| <kbd>Hover</kbd> over <kbd>Graph Name</kbd> + <kbd>↑</kbd> <kbd>↓</kbd>  | Change the graph order |
| <kbd>Left Click</kbd> on <kbd>Graph Name</kbd> | Rename the selected graph          |
| <kbd>Right Click</kbd> on <kbd>Graph Name</kbd>| Change color of the selected graph |


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

Built using the beautiful Azure-ttk theme by [@rdbende](https://github.com/rdbende).
Requires python3, numpy, scipy, matplotlib, Pillow, python-opencv, pynput, topas2numpy and tkinter.

<b>Note:</b> Linux users need to have python3-tk installed. If it isnt installed yet, use:

```console
sudo apt-get install python3-tk
```
