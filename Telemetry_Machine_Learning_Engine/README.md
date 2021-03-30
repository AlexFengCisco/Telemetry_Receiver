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
    Abnormal Position : array([ 7,  9, 12, 15])

##### Training data set

    Marked training data set with marked y value , to calculate p(Xval) and compare with Yval to select best epsilon
    Yval 0 means normal , 1 means abnormal
    
    Xval_list = [[1,1,1],[2,2,3],[7,7,7],[1,2,3],[2,3,4],[3,3,4],[4,5,6],[4,5,5],[2,3,3],[6,6,6],[0,0,0]]
    Yval_list = [[1],[0],[1],[0],[0],[0,],[0],[0],[0],[1],[1]]
    
![N|Solid](training_data_set.png)

##### input data set

    X_list = [[1,2,3],[2,3,4],[3,3,4],[4,5,6],[4,5,5],[2,3,3],[1,3,3],[8,8,8],[1,2,3],[9,7,8],
              [2,2,3],[3,3,3],[8.1,7.8,9],[1,2,3],[3,3,3],[1,0,1]]
    
![N|Solid](input_data_set.png)

##### abnormal data set
    
    X_list = [[1,2,3],[2,3,4],[3,3,4],[4,5,6],[4,5,5],[2,3,3],[1,3,3],[8,8,8],[1,2,3],[9,7,8],
                                                                        #7              #9
             [2,2,3],[3,3,3],[8.1,7.8,9],[1,2,3],[3,3,3],[1,0,1]]
                                 #12                        #15
                                 
    Abnormal Position : array([ 7,  9, 12, 15])
                                                                                            
![N|Solid](abnormal_data_set.png)

