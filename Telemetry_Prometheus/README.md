##Telemetry receiver and prometheus lab

    Telemetry receiver gathering source informatin from telemetry source devices, 
    and export to prometheus server via exporter or push gateway.
    
    Grafana shows the data graphic.
    
    Prometheus alert manager triggered by metric values and invoke webhook to do actions. 
    for a monito alert feedback action loop.
    
    Prometheus REST like API provides query service via promQL.
    
 ![N|Solid](grafana.png)
 
 ##Test bed 
 
 ![N|Solid](test_bed.png)
 
 ##Machine learning engie 
     Test code with Tensorflow LSTM ,trained time series data pulled from prometheus server , 
     and output predicted data with plot graph.