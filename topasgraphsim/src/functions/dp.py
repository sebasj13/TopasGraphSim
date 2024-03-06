import numpy as np
import scipy.integrate as integrate
import scipy.interpolate as interpolate


def calculate_parameters(axis, dose, cax=False):

    """
    A function to calculate the relevant
    descriptive parameters of dose profiles.
    """
    
    interpolated_axis = np.linspace(axis[0], axis[-1], len(axis) * 100)
    akima_dose_interpolator = interpolate.Akima1DInterpolator(axis, dose)
    interpolated_dose = np.flip(akima_dose_interpolator.__call__(interpolated_axis))
    max_dose = np.max(interpolated_dose)

    XL20index = []
    XL50index = []
    XL80index = []

    for i, d in enumerate(interpolated_dose):
        if XL20index == [] and d > 0.2*max_dose:
            XL20index += [d]
            XL20index += [interpolated_dose[i-1]]
        elif XL50index == [] and d > 0.5*max_dose:
            XL50index += [d]
            XL50index += [interpolated_dose[i-1]]
        elif XL80index == [] and d > 0.8*max_dose:
            XL80index += [d]
            XL80index += [interpolated_dose[i-1]]
            break

    XL20 = (np.abs(np.array(XL20index) - 0.2 * max_dose)).argmin()
    XL20 = XL20index[XL20]
    XL50 = (np.abs(np.array(XL50index) - 0.5 * max_dose)).argmin()
    XL50 = XL50index[XL50]
    XL80 = (np.abs(np.array(XL80index) - 0.8 * max_dose)).argmin()
    XL80 = XL80index[XL80]

    XL20index = min(np.where(interpolated_dose==XL20)[0])
    XL50index = min(np.where(interpolated_dose==XL50)[0])
    XL80index = min(np.where(interpolated_dose==XL80)[0])
    XL20 = interpolated_axis[XL20index]
    XL50 = interpolated_axis[XL50index]
    XL80 = interpolated_axis[XL80index]

    XR20index = []
    XR50index = []
    XR80index = []

    for i, d in enumerate(np.flip(interpolated_dose)):
        if XR20index == [] and d > 0.2*max_dose:
            XR20index += [d]
            XR20index += [np.flip(interpolated_dose)[i-1]]
        elif XR50index == [] and d > 0.5*max_dose:
            XR50index += [d]
            XR50index += [np.flip(interpolated_dose)[i-1]]
        elif XR80index == [] and d > 0.8*max_dose:
            XR80index += [d]
            XR80index += [np.flip(interpolated_dose)[i-1]]
            break

    XR20 = (np.abs(np.array(XR20index) - 0.2 * max_dose)).argmin()
    XR20 = XR20index[XR20]
    XR50 = (np.abs(np.array(XR50index) - 0.5 * max_dose)).argmin()
    XR50 = XR50index[XR50]
    XR80 = (np.abs(np.array(XR80index) - 0.8 * max_dose)).argmin()
    XR80 = XR80index[XR80]

    XR20index = max(np.where(interpolated_dose==XR20)[0])
    XR50index = max(np.where(interpolated_dose==XR50)[0])
    XR80index = max(np.where(interpolated_dose==XR80)[0])
    XR20 = interpolated_axis[XR20index]
    XR50 = interpolated_axis[XR50index]
    XR80 = interpolated_axis[XR80index]

    HWB = round(abs(XR50 - XL50), 3)
    CAXdev = (round(XL50 + 0.5 * HWB, 3) + round(XR50 - 0.5 * HWB, 3) )/ 2
    #find the index of the axis af the cax_dev value
    CAXdevindex = np.abs(interpolated_axis - CAXdev).argmin()
    CAXdevpoints = int(abs(CAXdevindex - XL50index)//10)
    PlateauDose = np.mean(interpolated_dose[CAXdevindex - CAXdevpoints : CAXdevindex + CAXdevpoints+1])
    PlateauRatio = round(PlateauDose/max_dose, 3)

    Width80 = HWB*0.8
    FieldL80 = CAXdev - Width80/2
    FieldR80 = CAXdev + Width80/2
    Dose80 = interpolated_dose[(np.abs(interpolated_axis - FieldL80)).argmin():(np.abs(interpolated_axis - FieldR80)).argmin()]

    if cax == True:
        return CAXdev

    flat_krieger = round(   abs(min(Dose80)-max(Dose80))/max(Dose80),3)
    flat_stddev = round(np.std(Dose80/max(Dose80)), 3)

    S = interpolated_dose[CAXdevindex-len(Dose80)//2:CAXdevindex+len(Dose80)//2]
    S = max(np.divide(S, S[::-1]))
    S = round(S-1,3)

    Rpenumbra = round(abs(XL80 - XL20), 3)
    Lpenumbra = round(abs(XR80 - XR20), 3)

    try:
        Rintegral = round(
            abs(
                integrate.simpson(
                    y=interpolated_dose[XL20index:XL80index]/max_dose,
                    x=interpolated_axis[XL20index:XL80index],
                )
            ),
            3,
        )
        Lintegral = round(
            abs(
                integrate.simpson(
                    y=interpolated_dose[XR80index:XR20index]/max_dose,
                    x=interpolated_axis[XR80index:XR20index],
                )
            ),
            3,
        )
    except Exception:
        Lintegral = 0
        Rintegral = 0

    return [
        f"{HWB} ({round(XL50,2)}/{round(XR50,2)})",
        CAXdev,
        flat_krieger,
        flat_stddev,
        S,
        Lpenumbra,
        Rpenumbra,
        Lintegral,
        Rintegral,
        PlateauRatio,
    ]
