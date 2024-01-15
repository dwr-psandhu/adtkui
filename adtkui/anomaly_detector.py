import param
import panel as pn

pn.extension()
import hvplot.pandas
import holoviews as hv
from holoviews import opts, dim
import pandas as pd
from adtk.data import validate_series
from adtk.detector import (
    _TrainableUnivariateDetector,
    _NonTrainableUnivariateDetector,
    ThresholdAD,
    PersistAD,
    SeasonalAD,
    AutoregressionAD,
    OutlierDetector,
)
from .param_wrapper import object_to_param_class, get_attributes, get_methods

from typing import Dict, Optional, Type


def get_all_subclasses_from_superclass(superclass: Type) -> Dict[str, Optional[str]]:
    result = dict()
    for sb in superclass.__subclasses__():
        if sb.__name__[0] != "_":
            result.update({sb.__name__: sb})
        else:
            result.update(_get_all_subclasses_from_superclass(sb))
    return result


def get_all_univariate_detectors():
    from adtk.detector import (
        _NonTrainableUnivariateDetector,
        _TrainableUnivariateDetector,
    )

    models = get_all_subclasses_from_superclass(_NonTrainableUnivariateDetector)
    models.update(get_all_subclasses_from_superclass(_TrainableUnivariateDetector))
    return models


# load all univariate detectors from a config yaml file
name_to_class = get_all_univariate_detectors()
del name_to_class["CustomizedDetector1D"]
del name_to_class["LevelShiftAD"]
del name_to_class["VolatilityShiftAD"]


def load_detectors(config_file):
    import yaml

    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    detectors = {}
    for detector_name, detector_config in config.items():
        detector_class = getattr(adtk.detector, detector_name)
        detector = detector_class(**detector_config)
        detectors[detector_name] = detector
    return detectors


def save_detectors(config_file, detectors):
    import yaml

    config = {}
    for detector_name, detector in detectors.items():
        config[detector_name] = detector.__dict__
    with open(config_file, "w") as f:
        yaml.dump(config, f)


def test_load_save():
    detectors = load_detectors("detectors.yaml")
    save_detectors("detectors.yaml", detectors)


def create_detector_param_class(name, **kwargs):
    obj = name_to_class[name](**kwargs)
    return object_to_param_class(
        obj,
        name_to_class[name],
        get_attributes(obj),
        get_methods(obj),
    )


class AnomalyDetectorUI(param.Parameterized):
    file = param.FileSelector()
    detector = param.ObjectSelector(
        default="ThresholdAD",
        objects=name_to_class.keys(),
    )
    dummy = param.Parameter(default=0)

    def __init__(self, **params):
        super().__init__(**params)
        self._df = pd.DataFrame()
        self._adf = pd.DataFrame()
        self._detector_param_class = {
            objname: create_detector_param_class(objname)
            for objname in self.param.detector.objects
        }
        self._detectors = {}

    @param.depends("file", watch=True)
    def load_data(self):
        if self.file:
            self._df = validate_series(
                pd.read_csv(self.file, index_col="datetime", parse_dates=True).iloc[
                    :, 0
                ]
            )
        self.dummy += 1

    @param.depends("dummy")
    def plot(self):
        if not self._df.empty:
            detector = self._detectors[self.detector]
            try:
                self._adf = detector.fit_detect(self._df)
            except:
                self._adf = detector.detect(self._df)
            self._adf.fillna(False, inplace=True)
            return self._df.hvplot(label="data") * self._df[self._adf].hvplot.scatter(
                color="red", size=20, label="anomalies"
            )
        else:
            return hv.Div("No file selected")

    @param.depends("detector")
    def detector_widget(self):
        if not self.detector in self._detectors:
            param_obj = self._detector_param_class[self.detector]()
            self._detectors[self.detector] = param_obj
        self.dummy += 1
        return pn.Param(self._detectors[self.detector])

    def detect(self, event):
        self.dummy += 1

    def view(self):
        self.run_button = pn.widgets.Button(name="Detect")
        self.run_button.on_click(self.detect)
        return pn.Column(
            pn.Param(self, parameters=["file", "detector"]),
            self.detector_widget,
            self.run_button,
            self.plot,
        ).servable()


if __name__ == "__main__":
    adui = AnomalyDetectorUI()
    adui.view().show()
