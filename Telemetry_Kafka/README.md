Telemetry Kafka Lab
    
    Producer log
    
        RecordMetadata(topic='telemetry', partition=0, topic_partition=TopicPartition(topic='telemetry', partition=0), offset=8, timestamp=1552888466172, checksum=None, serialized_key_size=-1, serialized_value_size=36, serialized_header_size=-1)
        RecordMetadata(topic='telemetry', partition=0, topic_partition=TopicPartition(topic='telemetry', partition=0), offset=9, timestamp=1552900093081, checksum=None, serialized_key_size=-1, serialized_value_size=36, serialized_header_size=-1)


    Consumer log
    
        {'telemetry', 'test'}
        {'telemetry'}
        set()
        {}
        
        
        ConsumerRecord(topic='telemetry', partition=0, offset=8, timestamp=1552888466172, timestamp_type=0, key=None, value={'node_id': 'XTC', 'uptime': 350807}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=36, serialized_header_size=-1)
        telemetry
        0
        8
        1552888466172
        {'node_id': 'XTC', 'uptime': 350807}
        36
        ----------------------------------------
        {'node_id': 'XTC', 'uptime': 350807}
        ----------------------------------------
        ConsumerRecord(topic='telemetry', partition=0, offset=9, timestamp=1552900093081, timestamp_type=0, key=None, value={'node_id': 'XTC', 'uptime': 350808}, headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=36, serialized_header_size=-1)
        telemetry
        0
        9
        1552900093081
        {'node_id': 'XTC', 'uptime': 350808}
        36
        ----------------------------------------
        {'node_id': 'XTC', 'uptime': 350808}
        ----------------------------------------
