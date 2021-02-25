'''
    Telemetry GRPC dial out mode , no TLS
    tests passed with :
        IOS XR Software, Version 6.4.1
        Nexus NX-OS 9.2.2
        MDS NX-OS 8.4.1
'''
from concurrent import futures
import time
import json
from google.protobuf.json_format import MessageToJson
from google.protobuf.descriptor import FieldDescriptor
import grpc
import telemetry_pb2
import fabric_telemetry_pb2
import cisco_grpc_dialout_pb2
import cisco_grpc_dialout_pb2_grpc
import uptime_pb2

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
            #print("RAW message")
            print(telemetry_msg)
            print("="*100)
            #print(type(telemetry_msg))
            #print(telemetry_msg.data_gpb.row[0].content)
            jsonStrTelemetry = MessageToJson(telemetry_msg)
            dictTelemetry = json.loads(jsonStrTelemetry)

            #print telemetry json message

            print(jsonStrTelemetry)
            print("Message Length {}".format(len(jsonStrTelemetry)))
            print("="*40)

            print(dictTelemetry["encodingPath"])
            if "dataGpb" in dictTelemetry:
                print("Message in GPB compact mode")

            if "dataGpbkv" in dictTelemetry:
                print("message in GPB-kv mode")

            # according to encoding path and dataGpb OR dataGpbkv to select which gpb-compact pb2 to be used
            if dictTelemetry["encodingPath"] == "Cisco-IOS-XR-shellutil-oper:system-time/uptime" and "dataGpb" in dictTelemetry:


                gpb_compact_content = telemetry_msg.data_gpb.row[0].content # should be use list method tohandle it
                #TBD
                Telemetry_row_content = uptime_pb2.system_uptime()
                Telemetry_row_content.ParseFromString(gpb_compact_content)

                print(Telemetry_row_content)
                print("="*40)

            #if dictTelemetry["encodingPath"] == "analytics:test_query" and "dataGpb" in dictTelemetry:
            if dictTelemetry["encodingPath"] == "analytics:dcnminitITL" and "dataGpb" in dictTelemetry:
                '''
                MDS 97 32G line card SAN Analytics feature,
                encoding path should be predefined push analytics query name.
                
                
                '''

                gpb_compact_content = telemetry_msg.data_gpb.row[0].content  # should be use list method tohandle it
                #gpb_compact_content = telemetry_msg.data_gpb.row[0]
                Telemetry_row_content = fabric_telemetry_pb2.FlowRecordsTable()


                #Telemetry_row_content = fabric_telemetry_pb2.FlowRecordRow()

                Telemetry_row_content.ParseFromString(gpb_compact_content)

                fabric_jsonStrTelemetry = MessageToJson(Telemetry_row_content)

                print(fabric_jsonStrTelemetry)
                print("=" * 40)

            if dictTelemetry["encodingPath"] == "show_stats_fc2/2" and "dataGpb" in dictTelemetry:
                '''
                MDS 97 32G line card SAN Analytics feature,
                encoding path should be predefined push analytics query name.


                '''

                gpb_compact_content = telemetry_msg.data_gpb.row[0].content  # should be use list method tohandle it
                # gpb_compact_content = telemetry_msg.data_gpb.row[0]
                Telemetry_row_content = fabric_telemetry_pb2.FlowRecordsTable()

                # Telemetry_row_content = fabric_telemetry_pb2.FlowRecordRow()

                Telemetry_row_content.ParseFromString(gpb_compact_content)

                fabric_jsonStrTelemetry = MessageToJson(Telemetry_row_content)

                print(fabric_jsonStrTelemetry)
                print("=" * 40)

            #json_dict = proto_to_dict(Telemetry_row_content)
            #print(json_dict)


        return cisco_grpc_dialout_pb2.MdtDialoutArgs()  # no return should be ok , if get telemetry stream only

def serve():
    gRPCserver = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cisco_grpc_dialout_pb2_grpc.add_gRPCMdtDialoutServicer_to_server(gRPCMdtDialoutServicer(), gRPCserver)
    gRPCserver.add_insecure_port('0.0.0.0:50051')

    gRPCserver.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        gRPCserver.stop(0)

if __name__ == '__main__':


    serve()
