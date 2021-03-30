### Telemetry ML Engine Sample Code

#### LSTM prediction machine learning sample code    
    Sample code to predict telemetry data nonlinear trend with tensorflow LSTM RNN

    Class predictor and function predictor_LSTM , input time series source data ,
    result  return evaluated observed and prdicted value and all times ,

    Demo code for predictor deep learning engine with LSTM RNN 
    
#### Telemetry Traffic / Payload Collection and LSTM Prediction sample 

![N|Solid](predict_result.png)


#### Multivariate Gaussian Distribution Abnormal Detection sample code

    Abnormal Detection with multivariate gaussian distribution model, a p(x_input) funtion get the data set x_input's epsilon density value,
    small density means far away from distribution center.

    A training data set with marked abnormal for a best epsilon density value

    compare input data set density value p(x) with training data set density value  best_epsilon(x_training),
    if p(x_input) < best_epsilon(x_training), means data seems far away from gaussian distribution center , and got the abnormal from input data set

##### Training data set
![N|Solid](training_data_set.png)

##### input data set
![N|Solid](input_data_set.png)

##### abnormal data set
![N|Solid](abnormal_data_set.png)

