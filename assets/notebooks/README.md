Notebooks organization
------------

The project was initially developed and models trained at Kaggle platform to leverage the free GPU resources. 

This folder has the core slightly refactored notebooks with code needed to recreate the results. The links below lead to original notebooks stored at Kaggle (requires permissions).

**[1.0-iv-make_dataset-build_constants.ipynb](https://github.com/kcostya/call-for-code-fires/blob/master/assets/notebooks/1.0-iv-make_dataset-build_constants.ipynb)**
    
    ├── Inputs
    │   ├── ../merra1/full_dataset3.csv'       <- Your comments go here!
    │   ├── ../201015-ca-population-density/2015_population_density_CA.csv'
    │   ├── ../land-cover/ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-USER_REGION-v2.0.7.nc'
    |
    ├── Outputs
    │   ├── ../constants_basegrid_divider_1.csv
 
 [merra1]()
 
 [land-cover]()
 
 [201015-ca-population-density]()

 **[1.1-iv-make_dataset-dataset_builder.ipynb](https://github.com/kcostya/call-for-code-fires/blob/master/assets/notebooks/1.1-iv-make_dataset-dataset_builder.ipynb)**
 
    ├── Inputs
    │   ├── ../constants_basegrid_divider_1.csv       <- output from 1.0-iv-make_dataset-build_constants.ipynb
    │   ├── ../temporal/fire_merra_VI_embs_3h_basegrid_divider_1.csv
    |
    ├── Outputs
    │   ├── ../basegrid_12h.csv
    │   ├── ../basegrid_24h.csv
    │   ├── ../basegrid_6h.csv
 
 [temporal]()
    
 **[2.0-iv-prediction-non_fire_prediction.ipynb](https://github.com/kcostya/call-for-code-fires/blob/master/assets/notebooks/2.0-iv-prediction-non_fire_prediction.ipynb)**
 
    ├── Inputs
    │   ├── ../basegrid_12h.csv     <- output from 1.1-iv-make_dataset-dataset_builder.ipynb
    |
    ├── Outputs
    │   ├── ../start_2010-02-01_00h_step_12h.pickle_commit5
    
 **[3.0-iv-make_dataset-convert_to_pandas.ipynb](https://github.com/kcostya/call-for-code-fires/blob/master/assets/notebooks/3.0-iv-make_dataset-convert_to_pandas.ipynb)**
 
    ├── Inputs
    │   ├── ../basegrid_12h.csv     <- output from 1.1-iv-make_dataset-dataset_builder.ipynb
    │   ├── ../start_2010-02-01_00h_step_12h.pickle_commit5     <- output from 2.0-iv-prediction-non_fire_prediction.ipynb
    |
    ├── Outputs
    │   ├── ../start_2010-02-01_00h_step_12h_pred_noinputfire_shifted_to_zero_scaled_up_to_8.csv
    │   ├── ../start_2010-02-01_00h_step_12h_pred_noinputfire_th_min08853_colormax_min06308.csv
    
 **[3.1-kk-prediction-semitemporal_generator.ipynb](https://github.com/kcostya/call-for-code-fires/blob/master/assets/notebooks/3.0-kk-prediction-semitemporal_generator.ipynb)**
 
    ├── Inputs
    │   ├── ../basegrid_12h.csv     <- output from 1.1-iv-make_dataset-dataset_builder.ipynb
    │   ├── ../start_2010-02-01_00h_step_12h_pred_noinputfire_shifted_to_zero_scaled_up_to_8.csv     <- output from 3.0-iv-make_dataset-convert_to_pandas.ipynb
    |
    ├── Outputs
    │   ├── ../valid_prediction_2017-11-13.csv    <- sample prediction for just 8 steps
    │   ├── ../fire_pred_exist.pickle      <- pickle with numpy array of all predictions for the valid set
    │   ├── ../history_dict.pickle      <- pickle with keras model history dictionary
    
