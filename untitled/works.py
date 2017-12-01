from lcyframe.worker import Worker
from lcyframe.libs import yaml
import os

config = yaml.load_confog("aoao_boss.example.yml")
config["ROOT"] = os.path.dirname(__file__)
w = Worker(**config)
w.start()