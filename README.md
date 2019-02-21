# Telemetry_Receiver
    
### Python Telemetry Receiver for collection Cisco NX-OS IOS-XR
    
    Telemetry format includes JSON GPB GPB-kv (Self-Description)
    This Python sample demo how to collect Telemetry mesasge via UDP and how to Parse message.
    
    Demo enviroment has N9K and XRv9K 
     N9K x.x.x.x     version : nx-os 9.2.2    JSON GPB-kv
     xrv9k x.x.x.x    version : xrv9k 6.4.1   JSON GPB GPB-kv
     
    Telemetry Receiver UDP : port 57500
    
    NOTE: max UDP protobuf length = 675535 ,header=28 ,real content = 65507 bytes
    
    Inside internal MDT header, IOS-XR has 12 bytes header, NX-OS has 6 bytes 
    
    
     IOS-XR inside interanl header:
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

     
### Telemetry proto file for both GPB and GPB-kv

    use the follwoing command to make python proto output
    
    protoc --python_out=. ./telemetry.proto 
    
    //for GPB compact , demo message is system uptime ,use the following proto file generated by IOS-XR
    protoc --python_out=. ./uptime.proto 
    
### Telemetry GPB GPB-kv Collection and parsed result as below. Also output with json result, not shown here(see code). 

    Telemetry GPB message from NX OS
    Node :DUT02
    IP Address (source port) :('10.75.58.198', 41532)
    Encodig Path :sys/procsys/sysmem
    GPB kv format
    dn:sys/procsys/sysmem
    free:26164608
    memstatus:OK
    name:sysmem
    total:32828228
    used:6663620
    ==================================================================
    Telemetry GPB message from NX OS
    Node :DUT02
    IP Address (source port) :('10.75.58.198', 41532)
    Encodig Path :show process cpu
    GPB kv format
    pid:1
    runtime:16411
    invoked:306652
    usecs:53
    onesec:0.00
    process:init
    =================================================================
    Telemetry GPB  message from IOX
    Node :XTC
    IP Address (source port) :('10.75.58.60', 32898)
    Encodig Path :Cisco-IOS-XR-shellutil-oper:system-time/uptime
    GPB compact format
    Content decoded here :
    Host Name :XTC
    System Up Time :1660 Seconds
    =================================================================

### Telemetry JSON Collection ans parsed result as below 

    =================================================================
    ('10.75.58.60', 33208)
    This is a System Uptime telemetry messgae
    Node =XTC
    Encoding Path =Cisco-IOS-XR-shellutil-oper:system-time/uptime
    Collection ID =5233
    Host Name =XTC
    Uptime =58169
    Recevice Count =1
    Timestamp from Start =7.964596271514893
    =================================================================
    ('10.75.58.60', 33208)
    This is a System Uptime telemetry messgae
    Node =XTC
    Encoding Path =Cisco-IOS-XR-shellutil-oper:system-time/uptime
    Collection ID =5235
    Host Name =XTC
    Uptime =58191
    Recevice Count =2
    Timestamp from Start =29.962813138961792
    =================================================================

### IOS-XR Generate Telemetry GPB compact proto files

    RP/0/RP0/CPU0:XTC#telemetry generate gpb-encoding path RootOper.QOS.Node.PolicyMap.Interface.Input.Statistics file disk0:/qos.proto
    Tue Jan 22 06:54:59.603 UTC
    Created /disk0:/qos.proto
    
    * NOTE 
    For Telemetry generate protofile , path should be a yang to xml schema path,
    How to find yang to xml schema path?
    
    RP/0/RP0/CPU0:XTC#run
    Tue Jan 22 06:58:56.512 UTC
    [xr-vm_node0_RP0_CPU0:~]$cd /pkg/telemetry/mdt/protogen
    [xr-vm_node0_RP0_CPU0:/pkg/telemetry/mdt/protogen]$ls
    yang_to_schema.txt
    [xr-vm_node0_RP0_CPU0:/pkg/telemetry/mdt/protogen]$
    
    yang_to_Schema.txt has all yang path to xml schema path maps.


### Will consolidate Json and GPB in one py file soon

    Base on Binary code , 1-4 bytes indicate mesage type ...
    
### gRPC receiver is under construction