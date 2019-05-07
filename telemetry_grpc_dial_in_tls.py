'''
    Telemetry GRPC dial in mode , TLS
    scp user@x.x.x.x/misc/config/grpc/ems.pem ./

    Cisco IOS XR Software, Version 6.4.1
'''
import grpc
import telemetry_pb2
import ems_grpc_pb2
from google.protobuf.json_format import MessageToJson
from grpc.beta import implementations

host = '10.75.58.60'
port = 57400
options = 'ems.cisco.com'

ca_cert = 'ems.pem' # credential file scp from devices
creds = open(ca_cert).read()

target = '%s:%d' % (host, port)
creds = implementations.ssl_channel_credentials(creds.encode(('utf-8'))) # args with byte type
channel = grpc.secure_channel(target, creds, (('grpc.ssl_target_name_override', options,),))
channel = implementations.Channel(channel)


stub = ems_grpc_pb2.beta_create_gRPCConfigOper_stub(channel)
sub_id = 'test_sub' # Telemetry MDT subscribtion
sub_args = ems_grpc_pb2.CreateSubsArgs(ReqId=1, encode=3, subidstr=sub_id)

timeout = float(100000)
metadata = [('username', 'cisco'), ('password', 'cisco')]



stream = stub.CreateSubs(sub_args, timeout=timeout, metadata=metadata)

for segment in stream:
    telemetry_pb = telemetry_pb2.Telemetry()
    t = telemetry_pb.ParseFromString(segment.data)
    # Print Json Message
    print(MessageToJson(telemetry_pb))


