from flask import Flask, render_template
import json
import requests
import datetime
import os

app = Flask(__name__)
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
  {
    "field": "cluster_id", # which is the field's name of data key 
    "title": "Cluster Name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "value",
    "title": "Metric Value",
    "sortable": True,
  },
  {
    "field": "value_type",
    "title": "Metric Value Type",
    "sortable": True,
  },
  {
    "field": "metric_name",
    "title": "Metric Name",
    "sortable": True,
  },
  {
    "field": "timestamp",
    "title": "Metric Timestamp",
    "sortable": True,
  }
]

#jdata=json.dumps(data)
BACKEND_PORT = os.environ['BACKEND_PORT']
BACKEND_HOST = os.environ['BACKEND_HOST']


@app.route('/')
def index():
    def formalize_value(value):
        return {
            "timestamp": datetime.datetime.fromtimestamp(
                int(value["timestamp"])).strftime("%d/%m/%Y %H:%M:%S"),
            "cluster_id": value["cluster_id"],
            "value": value["value"],
            "value_type": value["value_type"],
            "metric_name": value["metric_name"]
        }

    data = requests.get("http://%s:%s/metric" % (BACKEND_HOST, BACKEND_PORT))
    data = json.loads(data.text)
    data = list(map(formalize_value, data))

    return render_template("table.html",
        data=data,
        columns=columns,
        title='Barograph Screen')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
