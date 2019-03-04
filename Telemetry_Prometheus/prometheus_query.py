'''
  Prometheus REST API ProSQL query sample
'''
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

url = "http://10.75.58.17:9090/api/v1/query"

querystring = {"query":"some_metric{exported_job='some_job',instance='10.75.53.220:9091',job='alex_push_gateway'}[3h]"}

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
    print(response_json["data"]["result"][0]["metric"])
    for time,value in response_json["data"]["result"][0]["values"]:
        #print(time)
        #print(value)
        value_series.append(float(value))
        time_index.append(time)
        i += 1
print(value_series)
print(len(value_series))
print(time_index)

plt.figure(1)

plt.plot(time_index,value_series)
plt.xlabel('time index')
plt.ylabel('metric value')
plt.show()

