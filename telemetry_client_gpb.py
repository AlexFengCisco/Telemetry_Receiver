
import socket, struct
import json
import time
import telemetry_pb2
import uptime_pb2 # Telemetry compact GPB special for uptime


# Bind Socket UDP port 57500 as Telemetry recevice server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 57500))

count = 0

start_time = time.time()


while True:
    count += 1
    buf, addr = sock.recvfrom(50000)
    Telemetry_content = telemetry_pb2.Telemetry()

    #print(buf)
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
        print('GPB kv format')
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

    #Handle Telemetry UDP GPB  from IOX
    if buf[0:1] == b'\x00': ##check the binary daa , no official document
        print("Telemetry GPB  message from IOX")
        Telemetry_content.ParseFromString(buf[12:])
        print('Node :'+Telemetry_content.node_id_str)
        print('IP Address (source port) :' + str(addr))
        print('Encodig Path :' + Telemetry_content.encoding_path)


        if len(str(Telemetry_content.data_gpbkv)) > 2: # Handle GPB kv , in case of unstable A9KV , sometimes sent empty content message
            print('GPB kv format')
            Fields_list = Telemetry_content.data_gpbkv[0].fields[1].fields
            #print(Fields_list)
            for field in Fields_list:

                #print(field.fields)
                if field.string_value:
                    print(field.name + ':' + field.string_value)
                if field.uint32_value:
                    print(field.name + ':' + str(field.uint32_value))

        if len(str(Telemetry_content.data_gpb))> 0: # Handle GPB compact
            print('GPB compact format')
            row_content_buf = (Telemetry_content.data_gpb.row[0].content)

            Telemetry_row_content = uptime_pb2.system_uptime() #Decode content , may base on encoding path to choose content ptoto file

            Telemetry_row_content.ParseFromString(row_content_buf)
            print('Content decoded here :')

            print('Host Name :'+Telemetry_row_content.hostname)
            print('System Up Time :'+str(Telemetry_row_content.uptime)+' Seconds')

    print("="*200)

