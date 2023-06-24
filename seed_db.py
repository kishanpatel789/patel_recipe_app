# %%
from datetime import datetime 
from pathlib import Path

from config import app, db
from models import User, Recipe

import csv

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
with app.app_context():
    for u in data_user:
        db.session.add(u)
    for r in data_recipe:
        db.session.add(r)

    db.session.commit()
    
    
    # db.drop_all()
    # db.create_all()
    # for data in PEOPLE_NOTES:
    #     new_person = Person(lname=data.get("lname"), fname=data.get("fname"))
    #     for content, timestamp in data.get("notes", []):
    #         new_person.notes.append(
    #             Note(
    #                 content=content,
    #                 timestamp=datetime.strptime(
    #                     timestamp, "%Y-%m-%d %H:%M:%S"
    #                 ),
    #             )
    #         )
    #     db.session.add(new_person)
    # db.session.commit()

# %%
csv_users = []
with open("./seed_data/data_user.csv", 'r') as f:

    cols = f.readline().replace('\n', '').split(',')
    for line in f:
        values = line.replace(',')

# %%
with open('./seed_data/data_user.csv', newline='\n') as csvfile:
    csv_users = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        u = User()
        for key, value in row.items():
            setattr(u, key, value)
        csv_users.append(u)

with app.app_context():
    for u in csv_users:
        db.session.add(u)
    db.session.commit()

# %%
