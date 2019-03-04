


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

    whole_buf=[]
    data=''
    while True:
        count+=1
        buf, addr = sock.recvfrom(65535)

        print(buf)
        text_buf = str(buf)


        #workaround, cos find a9kv telemetry random add more { in message , if find {{ just move right 1 position
        if bug_left in text_buf:
            json_buff = json.loads(text_buf[text_buf.find('{')+1:-1])
        else:
            json_buff = json.loads(text_buf[text_buf.find('{'):-1])



        tele_node_id = json_buff['node_id_str']
        tele_path = json_buff['encoding_path']
        tele_collection_id = str(json_buff['collection_id'])
        tele_data = json_buff['data_json'][0]['content']

        if tele_path == 'Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization':
            with open('mdt_buff_cpu.tmp', 'w+') as buff_f:
                buff_f.write(json.dumps(json_buff))



        if tele_path == 'Cisco-IOS-XR-shellutil-oper:system-time/uptime':
            with open('mdt_buff_uptime.tmp','w+') as buff_f:
                buff_f.write(json.dumps(json_buff))








