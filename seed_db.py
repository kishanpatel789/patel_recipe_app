# %%
from datetime import datetime 
from pathlib import Path
import pandas as pd

from config import app, db
from models import User, Recipe

# %%
data_user = [
    User(
        id = 1,
        user_name = 'brynna',
        password = 'patel123',
        role = 'cook',
    ),
    User(
        id = 2,
        user_name = 'kishan',
        password = 'patel123',
        role = 'cook',
    ),
]

data_recipe = [
    Recipe(
        id = 1,
        name = 'Chicken Biryani',
        date_created = datetime(2023,6,22,17,2,31),
        date_modified = datetime(2023,6,22,17,2,31),
        created_by = 1,
        modified_by = 1,
    ),
]

# %%
with open("./seed_data/data_user.csv", 'r') as f:
    f.readline()
    for line in f:
        print(line)
# %%
df = pd.read_csv(Path('seed_data', 'data_user.csv' ))
# %%
tt = User()