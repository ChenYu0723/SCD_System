# ITS with Markov method.

This project's data is metroData_ODflow_15.csv

It is inflow and outflow of every station with 15 min.
## Code structure
```
.
├── README.md
├── __pycache__
├── _trial_temp
│   ├── _trial_marker
│   └── test.log
├── code
│   ├── DistanceCalculation.py
│   ├── SCD_Old.py
│   ├── SCD_Prediction.py
│   ├── SCD_Prediction10.1.py
│   ├── SCD_Prediction11.0.py
│   ├── SCD_Prediction12.0.py
│   ├── SCD_Prediction12.1.py
│   ├── SCD_Prediction13.0(SingleStepPrediction).py
│   ├── SCD_Prediction14.2(MultiStepPrediction).py
│   ├── SCD_Prediction15.5(SingleStepPrediction).py
│   ├── SCD_Prediction16.3(MultiStepPrediction).py
│   ├── SCD_Statistics.py
│   ├── SCD_Statistics2.0.py
│   ├── SCD_Statistics3.0.py
│   ├── SCD_Statistics4.0.py
│   ├── SCD_Visualization.py
│   ├── __pycache__
│   ├── errorUser.py
│   ├── findCoordinate.py
│   ├── find_demo.py
│   ├── station_dataframe.py
│   └── station_list.py
├── data
│   ├── prediction_data
│   ├── raw_data
│   └── true_data
├── model
│   ├── 1d_markov.py
│   ├── 1d_markov_2.py
│   ├── 2d_markov(SingleStepPrediction).py
│   ├── __pycache__
│   ├── arima.py
│   ├── arima_2.py
│   ├── gbm.py
│   ├── output
│   ├── rdf.py
│   ├── rdf_2.py
│   ├── svc.py
│   ├── svr.py
│   └── svr_2.py
├── plot_cn_paper
│   ├── SCD_Statistics.py
│   ├── SCD_Statistics_fast.py
│   ├── SCD_Statistics_fast2.py
│   ├── res_plot_data.txt
│   └── result
├── plot_en_paper
│   ├── SCD_Plot.py
│   ├── SCD_Plot10.1(PlotDistance).py
│   ├── SCD_Plot11.0(OtherHeatmap).py
│   ├── SCD_Plot12.2(PlotDaily).py
│   ├── SCD_Plot13.0(AllUserTrips).py
│   ├── SCD_Plot14.1(MetroMap).py
│   ├── SCD_Plot15.2(UserLabelTrips).py
│   ├── SCD_Plot2.0.py
│   ├── SCD_Plot2.1.py
│   ├── SCD_Plot3.4(TripsCount).py
│   ├── SCD_Plot4.2(StationFlowCount).py
│   ├── SCD_Plot5.1(TripHourCount).py
│   ├── SCD_Plot6.3(TransHeatmap).py
│   ├── SCD_Plot7.1(StateAccuracy).py
│   ├── SCD_Plot8.2(EveryTSAccuracy).py
│   └── SCD_Plot9.3(OneWeekFlow).py
└── result
    ├── fig
    └── txt

```
