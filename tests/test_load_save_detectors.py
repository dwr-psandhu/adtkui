# write tests for load and save detectors


def test_load_save():
    detectors = load_detectors("detectors.yaml")
    save_detectors("detectors.yaml", detectors)


# Path: tests/test_load_save_detectors.py
# Compare this snippet from dms_datastore_ui/anomaly_detector.py:
#
# from typing import Dict, Optional, Type
#
#
# %%
from dms_datastore_ui import anomaly_detector

# %%
detector_param_class = {
    objname: anomaly_detector.create_detector_param_class(objname)
    for objname in anomaly_detector.name_to_class.keys()
}
detectors = {
    detector_name: detector_class()
    for detector_name, detector_class in detector_param_class.items()
}
# %%
detectors
# %%
anomaly_detector.save_detectors("detectors.yaml", detectors)
# %%
detectors_loaded = anomaly_detector.load_detectors("detectors.yaml")
# %%
