import json 
from pathlib import Path


app_dir = Path(__file__).parents[0] 
config_file_path = app_dir / "config.json" 


with open(config_file_path, "rt") as json_file:
    config_data = json.load(json_file)