'''
    Telemetry GRPC dial out mode , no TLS
    tested by Cisco IOS XR Software, Version 6.4.1
'''
from concurrent import futures
import time
import json
from google.protobuf.json_format import MessageToJson
import grpc
import telemetry_pb2
import cisco_grpc_dialout_pb2
import cisco_grpc_dialout_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24  #grpc time out


class gRPCMdtDialoutServicer(cisco_grpc_dialout_pb2_grpc.gRPCMdtDialoutServicer):
    def __init__(self):
        print("Initializing gRPCMdtDialoutServicer()")

    def MdtDialout(self, message, context):

        grpcPeerStr = context.peer()


        grpcPeer = {}
        (grpcPeerProto, grpcPeer['telemetry_node'], grpcPeer['telemetry_node_port']) = grpcPeerStr.split(":")
        jsonTelemetryNode = json.dumps(grpcPeer)
        print(jsonTelemetryNode)

        for new_msg in message:
            telemetry_msg = telemetry_pb2.Telemetry()
            telemetry_msg.ParseFromString(new_msg.data)
            jsonStrTelemetry = MessageToJson(telemetry_msg)
            #dictTelemetry = json.loads(jsonStrTelemetry)

            #print telemetry json message
            print(jsonStrTelemetry)
        return cisco_grpc_dialout_pb2.MdtDialoutArgs()

def serve():
    with open('ems.key','rb') as f:
        private_key = f.read()

    with open('ems.pem','rb') as f:
        certificate_chain = f.read()

    #server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    server_credentials = grpc.ssl_server_credentials([(private_key, certificate_chain)])
    gRPCserver = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cisco_grpc_dialout_pb2_grpc.add_gRPCMdtDialoutServicer_to_server(gRPCMdtDialoutServicer(), gRPCserver)
    #gRPCserver.add_insecure_port('10.79.99.174:50051')
    gRPCserver.add_secure_port('192.168.1.128:50051',server_credentials)

    gRPCserver.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        gRPCserver.stop(0)

if __name__ == '__main__':
    serve()
