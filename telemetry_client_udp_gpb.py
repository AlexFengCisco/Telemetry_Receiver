'''
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |          MSG TYPE             |           ENCODING_TYPE       |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |         MSG_VERSION           |           FLAGS               |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |                           MSG_LENGTH                          |
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     ~                                                               ~
     ~                      PAYLOAD (MSG_LENGTH bytes)               ~
     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

     MSG TYPE (2 bytes)  = 1 (for MDT)
     ENCODING_TYPE (2 bytes) = 1 (GPB), 2 (JSON)
     MSG_VERSION (2 bytes) = 1
     FLAGS (2 bytes) = 0
     MSG_LENGTH (4 bytes)
'''


import socket, struct
import json
from google.protobuf.descriptor import FieldDescriptor
import time
import pprint
import telemetry_pb2
import uptime_pb2 # Telemetry compact GPB proto for uptime
import qos_pb2 # Telemetry compact GPB proto for QoS policy-map interface statistics
from google.protobuf.json_format import MessageToJson

DECODE_FN_MAP = {
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_INT64: int, #long
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_UINT64: int,#long
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,#long
    FieldDescriptor.TYPE_FIXED32: int,
    FieldDescriptor.TYPE_FIXED64: int,#long
    FieldDescriptor.TYPE_SFIXED32: int,
    FieldDescriptor.TYPE_SFIXED64: int,#long
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_BYTES: bytes,#lambda b: bytes_to_string(b),
    FieldDescriptor.TYPE_ENUM: int,
}

def field_type_to_fn(msg, field):
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        # For embedded messages recursively call this function. If it is
        # a repeated field return a list
        result = lambda msg: proto_to_dict(msg)
    elif field.type in DECODE_FN_MAP:
        result = DECODE_FN_MAP[field.type]
    else:
        raise TypeError("Field %s.%s has unrecognised type id %d" % (
                         msg.__class__.__name__, field.name, field.type))
    return result


def proto_to_dict(msg):
    result_dict = {}
    extensions = {}
    for field, value in msg.ListFields():
        conversion_fn = field_type_to_fn(msg, field)

        # Skip extensions
        if not field.is_extension:
            # Repeated fields result in an array, otherwise just call the
            # conversion function to store the value
            if field.label == FieldDescriptor.LABEL_REPEATED:
                result_dict[field.name] = [conversion_fn(v) for v in value]
            else:
                result_dict[field.name] = conversion_fn(value)
    return result_dict




# Bind Socket UDP port 57500 as Telemetry recevice server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 57501))

count = 0

start_time = time.time()


while True:
    count += 1
    buf, addr = sock.recvfrom(65535)
    Telemetry_content = telemetry_pb2.Telemetry()

    print(buf.hex())
    print(buf)
    print("Message Length {}".format(len(buf)))
    #print(len(str(buf)))
    #handle Telemetry UDP GPB kv from NX OS

    if buf[0:1] == b'\x01': #check the binary daa , no official document
        print("Telemetry GPB message from NX OS")
        Telemetry_content.ParseFromString(buf[6:])
        print('Node :'+Telemetry_content.node_id_str)
        print('IP Address (source port) :'+str(addr))
        print('Encodig Path :'+Telemetry_content.encoding_path)
        Top_Fields_List = Telemetry_content.data_gpbkv[0].fields
        #print(Top_Fields_List)
        #print('GPB format')
        for top_field in Top_Fields_List:
            #print(top_field.name)
            if str(top_field.name) == "content":
                for field in top_field.fields[0].fields[0].fields[0].fields[0].fields[0].fields:

                    if field.string_value:
                        print(field.name+':'+str(field.string_value))
                    if field.uint32_value:
                        print(field.name+':'+str(field.uint32_value))
                    if field.uint64_value:
                        print(field.name+':'+str(field.uint64_value))

    #Handle Telemetry UDP GPB and GPB-kv  from IOX
    if buf[0:1] == b'\x00': ##check the binary daa , no official document
        print("Telemetry GPB  message from IOX")
        Telemetry_content.ParseFromString(buf[12:])
        print('Node :'+Telemetry_content.node_id_str)
        print('IP Address (source port) :' + str(addr))
        print('Encodig Path :' + Telemetry_content.encoding_path)
        content_json_dict = proto_to_dict(Telemetry_content.data_gpb)
        print(MessageToJson(Telemetry_content))
        print("*"*20)
        print(content_json_dict)


        if len(str(Telemetry_content.data_gpbkv)) > 2: # Handle GPB kv , in case of unstable A9KV , sometimes sent empty content message
            print('GPB kv format')
            Fields_list = Telemetry_content.data_gpbkv[0].fields[1].fields
            #print(Fields_list)

            json_dict = proto_to_dict(Telemetry_content.data_gpbkv[0])
            #pprint.pprint(json_dict)
            print(json_dict)

            for field in Fields_list:

                #print(field.fields)
                if field.string_value:
                    print(field.name + ':' + field.string_value)
                if field.uint32_value:
                    print(field.name + ':' + str(field.uint32_value))

        if len(str(Telemetry_content.data_gpb))> 0: # Handle GPB compact GPB-kv
            '''
               GPB compact / GPB-kv needs proto files for each message decode, compile proto file to _pb2.py and import them.
               Choose parse decode proto according to message encoding path .....
            '''
            print('GPB compact format')

            row_content_buf = (Telemetry_content.data_gpb.row[0].content)


            if Telemetry_content.encoding_path == 'Cisco-IOS-XR-qos-ma-oper:qos/nodes/node/policy-map/interface-table/interface/input/service-policy-names/service-policy-instance/statistics':
                print('QoS ')
                Telemetry_row_content = qos_pb2.qos_stats()
                Telemetry_row_content.ParseFromString(row_content_buf)
                print('Content decoded here :')

                json_dict = proto_to_dict(Telemetry_row_content) #convert to  json format
                print(json_dict)

            if Telemetry_content.encoding_path == 'Cisco-IOS-XR-shellutil-oper:system-time/uptime':
                print('uptime')
                Telemetry_row_content = uptime_pb2.system_uptime()

                Telemetry_row_content.ParseFromString(row_content_buf)
                print('Content decoded here :')

                json_dict = proto_to_dict(Telemetry_row_content) #convert to  json format
                print(json_dict)

                print('Host Name :' + Telemetry_row_content.hostname)
                print('System Up Time :' + str(Telemetry_row_content.uptime) + ' Seconds')


    print("="*200)

