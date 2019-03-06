'''
  InfluxDb lab 
  Alex Feng
  Mar 6,2019
'''

from influxdb import InfluxDBClient
import json
import time

INFLUXDB_SERVER = '10.75.53.220'
INFLUXDB_PORT = 8086
USER = 'cisco'
PASSWORD = 'cisco'
DB = 'testdb'
SEND_INTERVAL = 10 #seconds

client = InfluxDBClient(INFLUXDB_SERVER,INFLUXDB_PORT,USER,PASSWORD,DB)

while True:

    with open('mdt_buff_uptime.tmp') as uptime_f:
        uptime_str = uptime_f.read()
        uptime_json = json.loads(uptime_str)
        print(uptime_json['data_json'][0]['content']['hostname'])
        print(uptime_json['data_json'][0]['content']['uptime'])
    
    uptime = uptime_json['data_json'][0]['content']['uptime']


    json_body = [
        {
            "measurement": "test_metric",
            "tags": {
                "tag01": "tag01.1",
                "tag02": "tag02.2"
            },

            "fields": {
                "value": float(uptime)
            }
        }
    ]
    print('uptime :'+str(uptime))
    client.write_points(json_body)
    time.sleep(SEND_INTERVAL)



#result = client.query('select * from test_metric')

#value_list = list(result)[0]

#for v in value_list:
    #print(v['time'])
    #print(v['value'])
    #print(v)