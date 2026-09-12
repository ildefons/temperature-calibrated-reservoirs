# Public datasets

The repository does not redistribute the two UCI datasets used by the real-data notebooks.
Place the files below in this directory before running notebooks 06 and 07.

## Appliances Energy Prediction

Expected filename: `energydata_complete.csv`

Official UCI dataset: Appliances Energy Prediction, dataset 374.
The publication notebook uses a six-sample (about one hour) forecasting horizon.

## UCI Air Quality

Expected filename: `AirQualityUCI.csv`

Official UCI dataset: Air Quality, dataset 360.
The publication notebook parses `Date` + `Time`, replaces the `-200` missing-value sentinel,
and uses a one-hour forecasting horizon.

The notebooks print the official UCI archive URLs in their configuration cells.
