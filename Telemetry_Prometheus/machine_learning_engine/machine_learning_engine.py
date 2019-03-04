from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.contrib.timeseries.python.timeseries import model as ts_model
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader
from tensorflow.contrib.timeseries.python.timeseries import estimators as ts_estimators

import requests
import json
import numpy as np

class LSTMModel(ts_model.SequentialTimeSeriesModel):
    """A time series model-building example using an RNNCell."""

    def __init__(self, num_units, num_features, dtype=tf.float32):
        """Initialize/configure the model object.
        Note that we do not start graph building here. Rather, this object is a
        configurable factory for TensorFlow graphs which are run by an Estimator.
        Args:
          num_units: The number of units in the model's LSTMCell.
          num_features: The dimensionality of the time series (features per
            timestep).
          dtype: The floating point data type to use.
        """
        super(LSTMModel, self).__init__(
            # Pre-register the metrics we'll be outputting (just a mean here).
            train_output_names=["mean"],
            predict_output_names=["mean"],
            num_features=num_features,
            dtype=dtype)
        self._num_units = num_units
        # Filled in by initialize_graph()
        self._lstm_cell = None
        self._lstm_cell_run = None
        self._predict_from_lstm_output = None

    def initialize_graph(self, input_statistics):
        """Save templates for components, which can then be used repeatedly.
        This method is called every time a new graph is created. It's safe to start
        adding ops to the current default graph here, but the graph should be
        constructed from scratch.
        Args:
          input_statistics: A math_utils.InputStatistics object.
        """
        super(LSTMModel, self).initialize_graph(input_statistics=input_statistics)
        self._lstm_cell = tf.nn.rnn_cell.LSTMCell(num_units=self._num_units)
        # Create templates so we don't have to worry about variable reuse.
        self._lstm_cell_run = tf.make_template(
            name_="lstm_cell",
            func_=self._lstm_cell,
            create_scope_now_=True)
        # Transforms LSTM output into mean predictions.
        self._predict_from_lstm_output = tf.make_template(
            name_="predict_from_lstm_output",
            func_=lambda inputs: tf.layers.dense(inputs=inputs, units=self.num_features),
            create_scope_now_=True)

    def get_start_state(self):
        """Return initial state for the time series model."""
        return (
            # Keeps track of the time associated with this state for error checking.
            tf.zeros([], dtype=tf.int64),
            # The previous observation or prediction.
            tf.zeros([self.num_features], dtype=self.dtype),
            # The state of the RNNCell (batch dimension removed since this parent
            # class will broadcast).
            [tf.squeeze(state_element, axis=0)
             for state_element
             in self._lstm_cell.zero_state(batch_size=1, dtype=self.dtype)])

    def _transform(self, data):
        """Normalize data based on input statistics to encourage stable training."""
        mean, variance = self._input_statistics.overall_feature_moments
        return (data - mean) / variance

    def _de_transform(self, data):
        """Transform data back to the input scale."""
        mean, variance = self._input_statistics.overall_feature_moments
        return data * variance + mean

    def _filtering_step(self, current_times, current_values, state, predictions):
        """Update model state based on observations.
        Note that we don't do much here aside from computing a loss. In this case
        it's easier to update the RNN state in _prediction_step, since that covers
        running the RNN both on observations (from this method) and our own
        predictions. This distinction can be important for probabilistic models,
        where repeatedly predicting without filtering should lead to low-confidence
        predictions.
        Args:
          current_times: A [batch size] integer Tensor.
          current_values: A [batch size, self.num_features] floating point Tensor
            with new observations.
          state: The model's state tuple.
          predictions: The output of the previous `_prediction_step`.
        Returns:
          A tuple of new state and a predictions dictionary updated to include a
          loss (note that we could also return other measures of goodness of fit,
          although only "loss" will be optimized).
        """
        state_from_time, prediction, lstm_state = state
        with tf.control_dependencies(
                [tf.assert_equal(current_times, state_from_time)]):
            transformed_values = self._transform(current_values)
            # Use mean squared error across features for the loss.
            predictions["loss"] = tf.reduce_mean(
                (prediction - transformed_values) ** 2, axis=-1)
            # Keep track of the new observation in model state. It won't be run
            # through the LSTM until the next _imputation_step.
            new_state_tuple = (current_times, transformed_values, lstm_state)
        return (new_state_tuple, predictions)

    def _prediction_step(self, current_times, state):
        """Advance the RNN state using a previous observation or prediction."""
        _, previous_observation_or_prediction, lstm_state = state
        lstm_output, new_lstm_state = self._lstm_cell_run(
            inputs=previous_observation_or_prediction, state=lstm_state)
        next_prediction = self._predict_from_lstm_output(lstm_output)
        new_state_tuple = (current_times, next_prediction, new_lstm_state)
        return new_state_tuple, {"mean": self._de_transform(next_prediction)}

    def _imputation_step(self, current_times, state):
        """Advance model state across a gap."""
        # Does not do anything special if we're jumping across a gap. More advanced
        # models, especially probabilistic ones, would want a special case that
        # depends on the gap size.
        return state

    def _exogenous_input_step(
            self, current_times, current_exogenous_regressors, state):
        """Update model state based on exogenous regressors."""
        raise NotImplementedError(
            "Exogenous inputs are not implemented for this example.")


class predictor(object):
    """A time series LSTM predictor."""

    def __init__(self):
        self.Description = "Alex Test for LSTM time series predictor"

    def predictor_LSTM(self, data, batch_size, window_size, num_features, num_units, train_steps, predict_steps,
                       learning_rate):
        reader = NumpyReader(data)

        train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(reader, batch_size=batch_size,
                                                                   window_size=window_size)

        estimator = ts_estimators.TimeSeriesRegressor(model=LSTMModel(num_features=num_features, num_units=num_units),
                                                      optimizer=tf.train.AdamOptimizer(learning_rate))

        estimator.train(input_fn=train_input_fn, steps=train_steps) 
        evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
        evaluation = estimator.evaluate(input_fn=evaluation_input_fn, steps=1)

        # Predict starting after the evaluation
        (predictions,) = tuple(estimator.predict(
            input_fn=tf.contrib.timeseries.predict_continuation_input_fn(evaluation,
                                                                         steps=predict_steps))) 
        print(self.Description)
        observed_times = evaluation["times"][0]
        observed = evaluation["observed"][0, :, :]
        evaluated_times = evaluation["times"][0]
        evaluated = evaluation["mean"][0]
        predicted_times = predictions['times']
        predicted = predictions["mean"]
        result = {}
        result["observed_times"] = observed_times
        result["observed"] = observed
        result["evaluated_times"] = evaluated_times
        result["evaluated"] = evaluated
        result["predicted_times"] = predicted_times
        result["predicted"] = predicted
        result["average_loss"] = evaluation['average_loss']
        result["loss"] = evaluation["loss"]
              
        return result

class data_source(object):
    """A time series LSTM predictor."""

    def __init__(self):
        self.Description = "Alex Test for LSTM time series data source"
        
    def data_source_prometheus(self,url,promql,sample_rate,compress_rate,time_sample,time_metric):
        url = url
        promQL = promql
        sample_rate = sample_rate
        compress_rate = compress_rate
        time_sample = time_sample
        time_metric = time_metric
        
        querystring = {
            "query": promQL}

        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        value_series = []
        time_index = []
        i = 0
        if response_json["status"] == "success":
            #print(response_json["data"]["result"][0]["metric"])
            for time, value in response_json["data"]["result"][0]["values"]:
                i += 1
                if i == sample_rate:  # for source data normalization , best practice is 1000 values and 8-10 repeats sample rate
                    value_series.append(float(value) / compress_rate)  # for MSE or RSME a big difference ,compress rate
                    time_index.append(time / time_metric * time_sample / sample_rate)
                    i = 0

        data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: time_index,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: value_series,
        }
        
        return data
    
    def data_source_sample_sine_01(self):
        '''
          A sample sine data source for demo and verification machine learning engine
          sine sample 01 , add noise and another sine wave 
        '''
        x = np.array(range(1000))
        noise = np.random.uniform(-0.2, 0.2, 1000)
        
        y = np.sin(np.pi * x / 50 ) + np.cos(np.pi * x / 50) + np.sin(np.pi * x / 25) + noise

        data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
        }
        
        return data

    def data_source_sample_sine_02(self):
        '''
          A sample sine data source for demo and verification machine learning engine
          sine sample 02 , add noise
        '''
        x = np.array(range(1000))
        noise = np.random.uniform(-0.2, 0.2, 1000)
       
        y = np.sin(np.pi * x / 50) + np.cos(np.pi * x / 50) + noise
        data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
        }

        return data