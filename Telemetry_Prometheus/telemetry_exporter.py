import prometheus_client
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import requests
import requests
import json
from requests.auth import HTTPBasicAuth



app = Flask(__name__)

alex_total = Counter("alex_count", "Total Alex  cout")

alex_value = Gauge("alex_value", "Alex test value")
system_uptime = Gauge("ios_xr_system_uptime", "IOS XR system uptime")

@app.route("/metrics")
def srte_metrics():
    alex_total.inc()
    # requests_total.inc(2)
    test_value = 100
    alex_value.set(test_value)
    
    with open('mdt_buff_uptime.tmp') as uptime_f:
        uptime_str = uptime_f.read()
        uptime_json = json.loads(uptime_str)
        print(uptime_json['data_json'][0]['content']['hostname'])
        print(uptime_json['data_json'][0]['content']['uptime'])

    uptime = uptime_json['data_json'][0]['content']['uptime']
    system_uptime.set(uptime)

    return Response((prometheus_client.generate_latest(system_uptime),
                     prometheus_client.generate_latest(alex_value),
                     prometheus_client.generate_latest(alex_total)),
                    mimetype="text/plain")

@app.route('/')
def index():
    alex_total.inc()
    return "Alex Test Python Prometheus exporter"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9997)
  