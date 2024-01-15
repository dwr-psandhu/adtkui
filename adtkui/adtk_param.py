import param
from adtk.detector import (
    ThresholdAD,
    PersistAD,
    SeasonalAD,
    AutoregressionAD,
    OutlierDetector,
    print_all_models,
)


# Store the original object in the param class
class ParamWrapper(param.Parameterized):
    _original_object = obj

    def __setattr__(self, key, value):
        # Set attribute both on param class and original object
        super().__setattr__(key, value)
        if key in attributes:
            setattr(self._original_object, key, value)


class ThresholdADParam(ParamWrapper):
    """
    ThresholdAD
    Detector that detects anomaly based on user-given threshold.

        This detector compares time series values with user-given thresholds, and
        identifies time points as anomalous when values are beyond the thresholds.

        Parameters
        ----------
        low: float, optional
            Threshold below which a value is regarded anomaly. Default: None, i.e.
            no threshold on lower side.

        high: float, optional
            Threshold above which a value is regarded anomaly. Default: None, i.e.
            no threshold on upper side.


    """

    low = param.Number(
        default=None,
        bounds=(None, None),
        doc="""
        Threshold below which a value is regarded as an anomaly. Default is None, 
        meaning no threshold on the lower side.""",
    )

    high = param.Number(
        default=None,
        bounds=(None, None),
        doc="""
        Threshold above which a value is regarded as an anomaly. Default is None,
        meaning no threshold on the upper side.""",
    )

    def __init__(self, **params):
        super(self).__init__(_original_object=ThresholdAD(), **params)

    def detect(self, time_series):
        super()._original_object.detect(time_series)
