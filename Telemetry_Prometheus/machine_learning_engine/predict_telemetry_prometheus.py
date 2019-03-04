'''
   Sample code to predict telemetry data trend fromprometheus with tensorflow LSTM RNN

   Class predictor and function predictor_LSTM , input time series source data ,
   result  return evaluated observed and prdicted value and all times ,

   demo code for predictor deep learning engine with LSTM RNN ,
   LSTM RNN parameter:
       ------------------------------------
       batch_size = 4
       window_size = 100
       num_features  = 1
       num_units = 128
       train_steps = 2000
       learning_rate = 0.001
       predict_steps = as you like
       -------------------------------------
   This variable parameter was tested by around 1000 data values with 8-10 repeated graph model .
   if you hate to tune the LSTM RNN parameters , source data has to be normalized ,
   the better source data should cover 8-10 repeated models , and sampled value counts around 1000.
   for each repeated model , around 100 values would be better for RNN window size.

   try to avoid data source abnormal. regular repeatable data would be better.

   Data source scale to range 0 to 1

   To decrease computer CPU or GPU run time , adjust the training steps, also adjust the learning rate for optimizer
   to reduce loss as possible , see estimator report in INFO log.

   Also , source data maybe range anywhere ,  data normalization keep the data range less than +-10, try to compress it.
   try to make data value difference extremely visible. RNN deep learning and optimizer will easy to make good loss or
   cross entropy.

   by Alex Feng
   alfeng@cisco.com
'''
import numpy as np
import requests
import json
import tensorflow as tf
import machine_learning_engine as MLE

from tensorflow.contrib.timeseries.python.timeseries import estimators as ts_estimators
from tensorflow.contrib.timeseries.python.timeseries import  NumpyReader

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)

  # Prepare the time series source data from prometheus
  prometheus_api_url = "http://10.75.58.17:9090/api/v1/query"

  #prometheus data stream sample 01
  prometheus_query = '''prometheus_tsdb_blocks_loaded{job="prometheus"}[168h]'''
  prometheus_sample_rate = 40
  prometheus_compress_rate = 10
  prometheus_time_sample = 60
  prometheus_time_metric = 1000

  #prometheus_query = '''ios_xr_system_uptime{instance="10.75.53.220:9997",job="alex_telemetry_exporter"}[5d]'''
  #prometheus_sample_rate = 1
  #prometheus_compress_rate = 225000
  #prometheus_time_sample = 15
  #prometheus_time_metric = 1000

  #prometheus_query = '''system_cpu_load{instance="10.75.58.20:9999",job="alex_enkins_exporter"}[7d]'''
  #prometheus_sample_rate = 8
  #prometheus_compress_rate = 1
  #prometheus_time_sample = 15
  #prometheus_time_metric = 1000


  #prometheus data stream sample 02
  #prometheus_query = '''prometheus_tsdb_head_chunks{job="prometheus"}[24h]'''
  #prometheus_sample_rate = 5
  #prometheus_compress_rate = 10000
  #prometheus_time_sample = 60
  #prometheus_time_metric = 1000


  #call data source get data from prometheus

  ds = MLE.data_source()
  data = ds.data_source_prometheus(url = prometheus_api_url,
                                   promql = prometheus_query,
                                   sample_rate = prometheus_sample_rate,
                                   compress_rate = prometheus_compress_rate,
                                   time_sample = prometheus_time_sample,
                                   time_metric = prometheus_time_metric)


  #data = ds.data_source_sample_sine_02() #try sample data source

  #call RNN LSTM training  evaluation and prediction ,train_steps
  p = MLE.predictor()
  result = p.predictor_LSTM(data=data, batch_size=4, window_size=100, num_features=1, num_units=128, train_steps=2000,
                            predict_steps=400, learning_rate=0.001)

  print(result["average_loss"])
  print(result["loss"])
  #plot result
  plt.figure(figsize=(15, 5))
  #plt.axvline(999, linestyle="dotted", linewidth=4, color='r')
  observed_lines = plt.plot(result["observed_times"], result["observed"], label="observation", color="k")
  evaluated_lines = plt.plot(result["evaluated_times"], result["evaluated"], label="evaluation", color="g")
  predicted_lines = plt.plot(result["predicted_times"], result["predicted"], label="prediction", color="r")

  plt.legend(handles=[observed_lines[0], evaluated_lines[0], predicted_lines[0]],loc="upper left")
  loss_info = 'Average loss :'+str(result["average_loss"])+'   Loss :'+str(result["loss"])
  plt.title(loss_info)
  #plt.show()
  
  plt.savefig('predict_result.png')