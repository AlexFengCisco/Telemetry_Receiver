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
            #print(telemetry_msg)
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

            if dictTelemetry["encodingPath"] == "analytics:test_query" and "dataGpb" in dictTelemetry:
                '''
                MDS 97 32G line card SAN Analytics feature,
                encoding path should be predefined push analytics query name.
                
                So far , NX OS 8.4.1 only support gRPC GPB/GPB-kv
                for GPB-kv encoding with fabrc_telemetry.proto file.
                
                MDS 9710 sample configuration:
                 
                telemetry
                    sensor-group 1
                    path analytics:test_query
                    path show_stats_fc2/1
                    path show_stats_fc2/2
                    sensor-group 2
                    path analytics:dcnminitITL
                    destination-group 1
                    ip address 10.79.98.77 port 50051 protocol gRPC encoding GPB-compact
                    destination-group 2
                    ip address 10.124.2.116 port 57500 protocol gRPC encoding GPB-compact
                    subscription 1
                    snsr-grp 1 sample-interval 30000
                    dst-grp 1
                    subscription 2
                    snsr-grp 2 sample-interval 30000
                    dst-grp 2
                    
                sw-core1-9710# sh analytics query all
                Total queries:2
                ============================
                Query Name      :test_query
                Query String    :select all from fc-scsi.port
                Query Type      :periodic, interval 30
                
                Query Name      :dcnminitITL
                Query String    :select port, vsan, app_id, initiator_id, target_id, lun, active_io_read_count, active_io_write_count, total_read_io_count, total_write
                _io_count, total_time_metric_based_read_io_count, total_time_metric_based_write_io_count,total_read_io_time, total_write_io_time, total_read_io_initiat
                ion_time, total_write_io_initiation_time,total_read_io_bytes, total_write_io_bytes, total_time_metric_based_read_io_bytes, total_time_metric_based_writ
                e_io_bytes, read_io_rate, write_io_rate, read_io_bandwidth, write_io_bandwidth,read_io_size_min, read_io_size_max, write_io_size_min, write_io_size_max
                ,read_io_completion_time_min, read_io_completion_time_max, write_io_completion_time_min, write_io_completion_time_max,read_io_initiation_time_max, writ
                e_io_initiation_time_max, read_io_aborts, write_io_aborts,read_io_failures, write_io_failures, read_io_timeouts, write_io_timeouts from fc-scsi.scsi_in
                itiator_itl_flow
                Query Type      :periodic, interval 30
                Query Options   :differential
                    
                '''

                gpb_compact_content = telemetry_msg.data_gpb.row[0].content  # should be use list method tohandle it
                #gpb_compact_content = telemetry_msg.data_gpb.row[0]
                Telemetry_row_content = fabric_telemetry_pb2.FlowRecordsTable()


                #Telemetry_row_content = fabric_telemetry_pb2.FlowRecordRow()

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
