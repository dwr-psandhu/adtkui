# Anomaly Detection of Timeseries Data

Create a UI that allows users to 
* Choose and load the timeseries. Use hvplot to plot the timeseries
* Choose the anomaly detection algorithm and its parameters

The UI should display the results of the anomaly detection algorithm.

## Design

The UI should have the following components:
* A file upload widget to upload the timeseries data
* A dropdown to choose the anomaly detection algorithm
  * The algorithms parameters will be displayed using Parameterized class generation using the default values
* A button to run the anomaly detection algorithm
* A plot of the timeseries data and the anomalies detected

