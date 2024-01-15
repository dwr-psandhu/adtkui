# %%
import pandas as pd
import adtk
from adtk.data import validate_series
from adtk.detector import ThresholdAD

df = pd.read_csv("../carqb_upper_temp.csv", index_col="datetime", parse_dates=True)
df.head()
df = validate_series(df.iloc[:, 0])
# %%
# adtk.detector.print_all_models()
from anomaly_detector import get_all_univariate_detectors

detector_dict = get_all_univariate_detectors()
detector_dict["ThresholdAD"]
# %%
th_ad = ThresholdAD()
getattr(th_ad, "high")

dir(th_ad)
# %%
th_ad = ThresholdAD(high=30, low=12)
adf = th_ad.detect(df)
adf.fillna(False, inplace=True)
# %%
import hvplot.pandas

df.hvplot(label="data") * df[adf].hvplot.scatter(
    color="red", size=20, label="anomalies"
)

# %%
from dms_datastore_ui import param_wrapper

ThresholdADParam = param_wrapper.object_to_param_class(
    th_ad, ["high", "low"], ["detect"]
)
th_ad_p = ThresholdADParam()
# %%
import panel as pn

pn.extension()
pn.Param(th_ad_p)
# %%
df.hvplot(label="data") * df[th_ad_p.detect(df).fillna(False)].hvplot.scatter(
    color="red", size=20, label="anomalies"
)
# %%
