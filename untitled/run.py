from lcyframe.libs import yaml
import sys, os
from lcyframe.app import App
from timing import crontab
config = yaml.load_confog("aoao_boss.example.yml")
api_schema = yaml.load_api_schema("api_schema")

port = config["wsgi"]["port"] if len(sys.argv) == 1 else int(sys.argv[1])

config["api_schema"] = api_schema
config["ROOT"] = os.path.dirname(__file__)
# config["task"] = [(aaa.a, 1000)]
app = App(**config)
app.run()