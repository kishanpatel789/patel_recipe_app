import json
from pathlib import Path


app_dir = Path(__file__).parent
config_file_path = app_dir / "config.json"


with open(config_file_path, "rt") as json_file:
    config_data = json.load(json_file)

# convert db path to absolute if needed
config_db_data = config_data["database"]
if config_db_data["path_relative"]:
    _db_path = app_dir / config_db_data["path"]
    _db_path = _db_path.resolve()
    config_db_data.update({"path": str(_db_path)})

    _db_path_test = app_dir / config_db_data["path_test"]
    _db_path_test = _db_path_test.resolve()
    config_db_data.update({"path_test": str(_db_path_test)})
