'''
    Telemetry GRPC dial in mode , no-TLS

    Cisco IOS XR Software, Version 6.4.1

'''
import grpc
import telemetry_pb2
import cisco_grpc_dialin_pb2
import cisco_grpc_dialin_pb2_grpc
from google.protobuf.json_format import MessageToJson


channel = grpc.insecure_channel("10.75.58.60:57400")

stub = cisco_grpc_dialin_pb2_grpc.gRPCConfigOperStub(channel)

sub_id = 'test_sub' # Telemetry MDT subscription

sub_args = cisco_grpc_dialin_pb2.CreateSubsArgs(ReqId=1, encode=3, subidstr=sub_id)

timeout = float(100000)
metadata = [('username', 'cisco'), ('password', 'cisco')]
stream = stub.CreateSubs(sub_args, timeout=timeout, metadata=metadata)

for segment in stream:
    telemetry_pb = telemetry_pb2.Telemetry()
    t = telemetry_pb.ParseFromString(segment.data)
    # print json message
    print(MessageToJson(telemetry_pb))


