'''

   test prometheus push gateway , rest api likely action send metrics to push gateway 
   prometheus server add static exporter for push gateway
'''
import prometheus_client
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Info
from prometheus_client import push_to_gateway
from prometheus_client.core import CollectorRegistry

data = 7.14

registry = CollectorRegistry()

metric_test = Gauge('some_metric','test counter to push gateway',registry=registry)
metric_test.set(data)

push_to_gateway('10.75.53.220:9091',job='some_job',registry=registry)