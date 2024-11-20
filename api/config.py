import json 
from pathlib import Path


app_dir = Path(__file__).parent
config_file_path = app_dir / "config.json" 


with open(config_file_path, "rt") as json_file:
    config_data = json.load(json_file)

# convert db path to absolute if needed
if config_data['db_path_relative']:
    _db_path = app_dir / config_data['db_path']
    _db_path = _db_path.resolve()
    config_data.update({'db_path': str(_db_path)})

    _db_path_test = app_dir / config_data['db_path_test']
    _db_path_test = _db_path_test.resolve()
    config_data.update({'db_path_test': str(_db_path_test)})