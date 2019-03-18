'''
   Telemetry kafka consumer , fetch data from kafka topic and handle data as you like.
'''
import json

from kafka import KafkaConsumer


KAFKA_SERVER = '10.75.58.26'
KAFKA_PORT = ':9092'

TOPIC = 'test'

#group_id for continue with the broken point
consumer = KafkaConsumer(TOPIC,bootstrap_servers=[KAFKA_SERVER+KAFKA_PORT],group_id='alex_group',value_deserializer=lambda m: json.loads(m.decode('utf-8')))



print(consumer.topics())
print(consumer.subscription())
print(consumer.assignment())
#if no group_id configed , output the beginning offset 0 and fetch from current offset
print(consumer.beginning_offsets(consumer.assignment()))



for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')` ,for value_deserializer json configed , direct ouput json
    print(message)
    print(message.topic)
    print(message.partition)
    print(message.offset)
    print(message.timestamp)
    print(message.value)
    print(message.serialized_value_size)
    print('-'*40)

    print(message.value)

    print('-'*40)
    '''
     Do what you want here to handle the consumer kafka message.
    '''

