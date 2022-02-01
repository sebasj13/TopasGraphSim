# topasgraphsim

## Am interface to automatically plot and interpret the results of TOPAS simulations

This GUI can visualize and analyze percentage depth dose (pdd) and dose profiles (dp) simulations from [TOPAS](http://www.topasmc.org/). Depth dose measurements are assumed to be in the z-direction, dose profiles in the x- or y-directions. Data read-in is handled by [topas2numpy](https://github.com/davidchall/topas2numpy).
<br></br>          
![Screenshot 2022-01-24 170455](https://user-images.githubusercontent.com/87897942/150819409-8b761000-df95-442f-a8fd-f599b2981918.png)

## Features

 - Reproducible graphing and analysis of TOPAS simulation for medical physics
 - Simultaneous plotting and parameter calculation for up to 5 datasets
 - Graph adjustment options
     * Normalization (On/Off)
     * Error bars (On/Off)
     * Graph order and colors
     * Marker size
     * Line width
     * Zoom-in window
     * Half view of dose profiles
 - Import of EGS simulation results
 - Import of custom measurements (as numpy .txt files)
 - Import of PTW tbaScan (MEPHYSTO mc<sup>2</sup>) measurements
 - Easy to use keyboard shortcuts (see manual below)
 - German and english language support
 - Dark mode

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
| <kbd>Double Left Click</kbd> on <kbd>Graph</kbd>| Change zoom window location |



### Adjusting the Graph Legend

|Mouse/Keyboard Shortcut| Associated Function |
|---|---|
| <kbd>Hover</kbd> over <kbd>Graph Name</kbd> + <kbd>↑</kbd> <kbd>↓</kbd>  | Change the graph order |
| <kbd>Left Click</kbd> on <kbd>Graph Name</kbd> | Rename the selected graph          |
| <kbd>Right Click</kbd> on <kbd>Graph Name</kbd>| Change color of the selected graph |


## Installation

Install using pip:

```console
pip install topasgraphsim     
```
     
Then, start the GUI by running:
     
```console
python -m topasgraphsim
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
- FLAT<sub>Krieger</sub> : Flatness of Dose Plateau (Definitionby Krieger)
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
