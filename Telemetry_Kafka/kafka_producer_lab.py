'''
   Telemetry kafka producer , read telemetry data from tmp file and send to kafka server with json format,
   Real case may read telemetry from receiver buffer queue and send to kafka without missing data.
   Queue store telemetry data in memory and de-queue to kafka use FIFO method. It's a store forwarding architecture to
   solve mismatch handling performance between telemetry receiver and Kafka server. maybe queue limitation is necessary.
'''
import json
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError


KAFKA_SERVER = '10.75.58.26'
KAFKA_PORT = ':9092'

TOPIC = 'telemetry'


producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER+KAFKA_PORT], value_serializer=lambda m: json.dumps(m).encode('utf-8'))

pre_uptime = ''
while True:
    with open('mdt_buff_uptime.tmp') as uptime_f:
        uptime_str = uptime_f.read()
        uptime_json = json.loads(uptime_str)

    hostname = uptime_json['data_json'][0]['content']['hostname']
    uptime = uptime_json['data_json'][0]['content']['uptime']

    if str(uptime) == pre_uptime:
        pass
    else:
        kafka_payload = {
            "node_id": hostname,
            "uptime": uptime
        }

        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')` ,for value_deserializer json configed , direct ouput json

        future = producer.send(TOPIC, kafka_payload)

        try:
            record_metadata = future.get(timeout=10)
            print(record_metadata)
        except KafkaError as e:
            print(e)
        pre_uptime = str(uptime)

    time.sleep(2)  #just for testing , read data from file and store in a memory queue , real telemetry read the buffer and direct send to kafka broker.


producer.close()