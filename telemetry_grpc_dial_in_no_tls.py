'''
    Telemetry GRPC dial in mode , no-TLS

    Cisco IOS XR Software, Version 6.4.1


     _____________________________________
    |   Encoding Technique   |    Code    |
     -------------------------------------
    |           gpb          |     2      |
     -------------------------------------
    |           gpbkv        |     3      |
     -------------------------------------
    |           json         |     4      |
     -------------------------------------

    code 1 for test only
'''

import grpc
import telemetry_pb2
import cisco_grpc_dialin_pb2
import cisco_grpc_dialin_pb2_grpc
from google.protobuf.json_format import MessageToJson
import json
import pprint

encoding_code = 3
channel = grpc.insecure_channel("10.75.58.60:57400")

stub = cisco_grpc_dialin_pb2_grpc.gRPCConfigOperStub(channel)

sub_id = 'test_sub' # Telemetry MDT subscription

sub_args = cisco_grpc_dialin_pb2.CreateSubsArgs(ReqId=1, encode=encoding_code, subidstr=sub_id)  #encoding code see doc


timeout = float(100000)
metadata = [('username', 'cisco'), ('password', 'cisco')]
stream = stub.CreateSubs(sub_args, timeout=timeout, metadata=metadata)

for segment in stream:
    telemetry_pb = telemetry_pb2.Telemetry()
    #print(MessageToJson(telemetry_pb.encoding_path))
    if encoding_code != 4:
        #t = telemetry_pb.ParseFromString(segment.data)
        telemetry_pb.ParseFromString(segment.data)
        # print json message
        print(MessageToJson(telemetry_pb))

        telemetry_gpb_table = telemetry_pb2.TelemetryGPBTable()
        telemetry_gpb_table.CopyFrom(telemetry_pb.data_gpb)



        gpb_rows = []

        while (len(telemetry_gpb_table.row)):
            gpb_row_dict = {}
            gpb_row_dict["keys"] = {}
            gpb_row_dict["content"] = {}

            telemetry_gpb_row = telemetry_pb2.TelemetryRowGPB()
            telemetry_gpb_row.CopyFrom(telemetry_gpb_table.row.pop())

            print(telemetry_gpb_row.keys)
            print(telemetry_gpb_row.content)

        #TBD if gpb-compact ,encoding code = 2
    else:
        #print(json.loads(segment.data.decode(encoding='utf-8')))
        pprint.pprint(json.loads(segment.data.decode(encoding='utf-8')))



