'''
    Alert manager got prometheus server alert message , and route alert to receiver ,
    this ia a web hook receiver , when alex value >4 web hook reset the value =4
'''
import prometheus_client
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Info
from prometheus_client import push_to_gateway
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask ,request



app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
def index():

    print(request.json)
    alert_json = request.json
    print(str(alert_json["alerts"][0]["annotations"]["alex_value"]))
    print(type(float(alert_json["alerts"][0]["annotations"]["alex_value"])))
    print(alert_json["status"])
    # data = float(alert_json["alerts"][0]["annotations"]["alex_value"])/2
    data = 4.0

    registry = CollectorRegistry()

    metric_test = Gauge('some_metric', 'test counter to push gateway', registry=registry)
    metric_test.set(data)

    if alert_json["status"] == 'firing':
        push_to_gateway('10.75.53.220:9091', job='some_job', registry=registry)
    else:
        print("resolved")
    
    
    return "Alex Test Python Prometheus exporter"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)
