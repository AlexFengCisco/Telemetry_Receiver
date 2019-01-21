
'''


b'\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x01Q

{"node_id_str":"A9KV",
 "subscription_id_str":"health",
 "encoding_path":"Cisco-IOS-XR-shellutil-oper:system-time/uptime",
 "collection_id":46,
 "collection_start_time":1547142057043,
 "msg_timestamp":1547142057060,
 "data_json":[{"timestamp":1547142057056,
               "keys":{},
               "content":{"hostname":"A9KV",
                          "uptime":1648
                         }
              }
             ],
 "collection_end_time":1547142057060}
 '


b'\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x03y

{"node_id_str":"A9KV",
 "subscription_id_str":"health",
 "encoding_path":"Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary",
 "collection_id":33,
 "collection_start_time":1547141907315,
 "msg_timestamp":1547141907332,
 "data_json":[{"timestamp":1547141907331,
               "keys":{"node-name":"0/RP0/CPU0"},
               "content":{"page-size":4096,
                          "ram-memory":15032385536,
                          "free-physical-memory":10592419840,
                          "system-ram-memory":15032385536,
                          "free-application-memory":11047075840,
                          "image-memory":4194304,
                          "boot-ram-size":0,
                          "reserved-memory":0,
                          "io-memory":0,
                          "flash-system":0
                         }
               },
               {"timestamp":1547141907338,
                "keys":{"node-name":"0/0/CPU0"},
                "content":{"page-size":4096,
                           "ram-memory":8589934592,
                           "free-physical-memory":5439266816,
                           "system-ram-memory":8589934592,
                           "free-application-memory":5439307776,
                           "image-memory":4194304,
                           "boot-ram-size":0,
                           "reserved-memory":0,
                           "io-memory":0,
                           "flash-system":0}
                          }
                ],
"collection_end_time":1547141907339
}
'


'''


import socket, struct
import json
import time

from socket import inet_ntoa


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 57500))

End = '''}\''''
Start = '''b\''''
Left = '''{'''
bug_left = '''{{'''
miss_start = 0
miss_end = 0
miss_left = 0
count = 0

start_time = time.time()

while True:

    whole_buf = []
    data=''
    while True:
        count += 1
        buf, addr = sock.recvfrom(50000)

        #print(buf)
        text_buf = str(buf)

        #workaround, cos find a9kv telemetry random add more { in message , if find {{ just move right 1 position
        if bug_left in text_buf:
            json_buff = json.loads(text_buf[text_buf.find('{')+1:-1])
            #print('bug')
        else:
            json_buff = json.loads(text_buf[text_buf.find('{'):-1])
            #print('no bug')


        tele_node_id = json_buff['node_id_str']
        tele_path = json_buff['encoding_path']
        tele_collection_id = str(json_buff['collection_id'])
        tele_data = json_buff['data_json'][0]['content']

        if tele_path == 'Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization':

            print(addr)
            print('This is a CPU utilization telemetry messgae')
            print('Node =' + tele_node_id)
            print('Collection ID =' + tele_collection_id)
            print('CPU 1 Min ='+ str(tele_data['total-cpu-one-minute']))
            print('CPU 5 Min ='+ str(tele_data['total-cpu-five-minute']))
            print('CPU 15 Min ='+ str(tele_data['total-cpu-fifteen-minute']))
            print('Recevice Count =' + str(count))
            print('Timestamp from Start ='+str(time.time() - start_time))
            print('=' * 200)

        if tele_path == 'Cisco-IOS-XR-shellutil-oper:system-time/uptime':

            print(addr)
            print('This is a System Uptime telemetry messgae')
            print('Node =' + tele_node_id)
            print('Collection ID =' + tele_collection_id)
            print('Host Name =' + str(tele_data['hostname']))
            print('Uptime =' + str(tele_data['uptime']))
            print('Recevice Count =' + str(count))
            print('Timestamp from Start =' + str(time.time() - start_time))
            print('=' * 200)



