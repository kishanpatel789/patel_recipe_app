import json 
from pathlib import Path

appDir = Path(__file__).parent
configFilePath = appDir / "config.json" 

with open(configFilePath, "rt") as json_file:
    configData = json.load(json_file)

class Config:
  pass

# apply base config from json file
for k, v in configData.items():
  setattr(Config, k, v)

