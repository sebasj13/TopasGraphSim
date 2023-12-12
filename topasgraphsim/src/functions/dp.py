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

    D0 = (
        interpolated_dose[int(len(interpolated_dose) / 2)]
        + interpolated_dose[int(len(interpolated_dose) / 2) - 1]
    ) / 2
    XL20 = interpolated_axis[: int(len(interpolated_axis) / 2)][
        (
            np.abs(
                interpolated_dose[: int(len(interpolated_axis) / 2)] - 0.2 * max(dose)
            )
        ).argmin()
    ]
    XL50 = interpolated_axis[: int(len(interpolated_axis) / 2)][
        (
            np.abs(
                interpolated_dose[: int(len(interpolated_axis) / 2)] - 0.5 * max(dose)
            )
        ).argmin()
    ]
    XL80 = interpolated_axis[: int(len(interpolated_axis) / 2)][
        (
            np.abs(
                interpolated_dose[: int(len(interpolated_axis) / 2)] - 0.8 * max(dose)
            )
        ).argmin()
    ]
    XR20 = interpolated_axis[int(len(interpolated_axis) / 2) :][
        (
            np.abs(
                interpolated_dose[
                    int(len(interpolated_axis) / 2) : len(interpolated_axis)
                ]
                - 0.2 * max(dose)
            )
        ).argmin()
    ]
    XR50 = interpolated_axis[int(len(interpolated_axis) / 2) :][
        (
            np.abs(
                interpolated_dose[
                    int(len(interpolated_axis) / 2) : len(interpolated_axis)
                ]
                - 0.5 * max(dose)
            )
        ).argmin()
    ]
    XR80 = interpolated_axis[int(len(interpolated_axis) / 2) :][
        (
            np.abs(
                interpolated_dose[
                    int(len(interpolated_axis) / 2) : len(interpolated_axis)
                ]
                - 0.8 * max(dose)
            )
        ).argmin()
    ]

    HWB = round(abs(XR50 - XL50), 3)
    CAXdev = round(XL50 + 0.5 * HWB, 3)

    Dose80 = [value for value in dose if value >= 0.8 * max(dose)]

    if cax == True:
        return CAXdev

    flat_krieger = round(
        max([value for value in dose if value >= 0.95 * max(dose)])
        - min([value for value in dose if value >= 0.95 * max(dose)]) / D0,
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
        HWB,
        CAXdev,
        flat_krieger,
        flat_stddev,
        S,
        Lpenumbra,
        Rpenumbra,
        Lintegral,
        Rintegral,
    ]
