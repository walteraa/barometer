from flask import Flask, render_template
import json
import requests
import datetime

app = Flask(__name__)
data = [{
  "name": "bootstrap-table",
  "value": "0.30123",
  "count": "122",
},
 {
  "name": "multiple-select",
  "value": "0.288123",
  "count": "20",
}, {
  "name": "Testing",
  "value": "0.3401235",
  "count": "20",
}]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
  {
    "field": "cluster_id", # which is the field's name of data key 
    "title": "Cluster Name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "avg",
    "title": "Ping Average",
    "sortable": True,
  },
  {
    "field": "count",
    "title": "Node Count",
    "sortable": True,
  },
  {
    "field": "timestamp",
    "title": "Metric time",
    "sortable": True,
  }
]

#jdata=json.dumps(data)

@app.route('/')
def index():
    data = requests.get("http://localhost:9001/metric").text
    data = json.loads(data)
    data = list(map(lambda m: {"timestamp": datetime.datetime.fromtimestamp(int(m["timestamp"])).strftime("%d/%m/%Y %H:%M:%S"),
                                "cluster_id": m["cluster_id"], "avg":m["avg"], "count":m["count"]
                                }, data))
    return render_template("table.html",
      data=data,
      columns=columns,
      title='Barograph Screen - Ping Metric')


if __name__ == '__main__':
	#print jdata
  app.run(debug=True, port=10000)
