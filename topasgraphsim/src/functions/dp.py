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

    # Find the index of the maximum dose
    max_dose_index = np.argmax(interpolated_dose)

    # Use this index to split the axis and dose arrays
    left_interpolated_axis = interpolated_axis[:max_dose_index]
    right_interpolated_axis = interpolated_axis[max_dose_index:]
    left_interpolated_dose = interpolated_dose[:max_dose_index]
    right_interpolated_dose = interpolated_dose[max_dose_index:]

    # Now use these new arrays to calculate your parameters
    XL20 = left_interpolated_axis[(np.abs(left_interpolated_dose - 0.2 * max(dose))).argmin()]
    XL50 = left_interpolated_axis[XL50index:=((np.abs(left_interpolated_dose - 0.5 * max(dose))).argmin())]
    XL80 = left_interpolated_axis[(np.abs(left_interpolated_dose - 0.8 * max(dose))).argmin()]
    XR20 = right_interpolated_axis[(np.abs(right_interpolated_dose - 0.2 * max(dose))).argmin()]
    XR50 = right_interpolated_axis[XR50index:=((np.abs(right_interpolated_dose - 0.5 * max(dose))).argmin())]
    XR80 = right_interpolated_axis[(np.abs(right_interpolated_dose - 0.8 * max(dose))).argmin()]

    HWB = round(abs(XR50 - XL50), 3)
    CAXdev = round(XL50 + 0.5 * HWB, 3)
    PlateauCenter = int(np.average([XL50index, XR50index]))
    PlateauDose = np.average([interpolated_dose[PlateauCenter - 2:PlateauCenter+3]])
    PlateauRatio = round(PlateauDose / max(dose), 3)
    Dose80 = [value for value in dose if value >= 0.8 * max(dose)]

    if cax == True:
        return CAXdev

    flat_krieger = round(
        max([value for value in dose if value >= 0.95 * max(dose)])
        - min([value for value in dose if value >= 0.95 * max(dose)]) / np.max(interpolated_dose),
        5,
    )
    flat_stddev = round(np.std(Dose80), 3)

    if len(Dose80) % 2 != 0:
        Dose80 = (
            Dose80[0 : int(len(Dose80) / 2)]
            + Dose80[int(len(Dose80) / 2) + 1 : len(Dose80)]
        )

    S = round(
        max(
            [Dose80[i - 1] / Dose80[len(Dose80) - i] for i in range(1, len(Dose80) + 1)]
        ),
        3,
    )

    Lpenumbra = round(abs(XL80 - XL20 + CAXdev), 3)
    Rpenumbra = round(abs(XR80 - XR20 + CAXdev), 3)

    XL20index = np.where(interpolated_axis == XL20)[0][0]
    XL80index = np.where(interpolated_axis == XL80)[0][0]
    XR20index = np.where(interpolated_axis == XR20)[0][0]
    XR80index = np.where(interpolated_axis == XR80)[0][0]
    try:
        Lintegral = round(
            abs(
                integrate.simps(
                    interpolated_dose[XL20index:XL80index],
                    interpolated_axis[XL20index:XL80index],
                )
            ),
            3,
        )
        Rintegral = round(
            abs(
                integrate.simps(
                    interpolated_dose[XR80index:XR20index],
                    interpolated_axis[XR80index:XR20index],
                )
            ),
            3,
        )
    except Exception:
        Lintegral = 0
        Rintegral = 0

    if CAXdev > 150:
        raise Exception

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
