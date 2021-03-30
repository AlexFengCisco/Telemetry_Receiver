### Telemetry ML Engine Sample Code

#### LSTM prediction machine learning sample code    
    Sample code to predict telemetry data nonlinear trend with tensorflow LSTM RNN

    Class predictor and function predictor_LSTM , input time series source data ,
    result  return evaluated observed and prdicted value and all times ,

    Demo code for predictor deep learning engine with LSTM RNN 
    
#### Telemetry Traffic / Payload Collection and LSTM Prediction sample 

![N|Solid](predict_result.png)


#### Multivariate Gaussian Distribution Abnormal Detection sample code

    Abnormal Detection with multivariate gaussian distribution model, 
    a p(x_input) funtion get the data set x_input's epsilon density value,
    small density means far away from distribution center.

    A training data set with marked abnormal for a best epsilon density value

    Compare input data set density value p(x) with training data set density value  best_epsilon(x_training),
    if p(x_input) < best_epsilon(x_training), means data seems far away from gaussian distribution center , 
    and got the abnormal from input data set
    
    Output sample:
    
    Mean value : array([3.31875, 3.675  , 4.3125 ])
    Variance : array([6.89902344, 4.859375  , 4.83984375])
    Density value array([2.11708868e-03, 4.15097858e-03, 4.67402379e-03, 2.99782299e-03,
       3.83145840e-03, 3.50947618e-03, 2.69619770e-03, 3.64685154e-05,
       2.11708868e-03, 3.78100701e-05, 2.75568526e-03, 3.95168870e-03,
       1.70567760e-05, 2.11708868e-03, 3.95168870e-03, 2.70757386e-04])/
    Best Epsilon Density :0.0012666326909782852
    Abnormal Postition : array([ 7,  9, 12, 15])

##### Training data set
![N|Solid](training_data_set.png)

##### input data set
![N|Solid](input_data_set.png)

##### abnormal data set
![N|Solid](abnormal_data_set.png)

