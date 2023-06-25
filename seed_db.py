# %%
from datetime import datetime 
from pathlib import Path

from config import app, db
from models import User, Recipe, Tag

import csv

# %%
# data_user = [
#     User(
#         id = 1,
#         user_name = 'brynna',
#         password = 'patel123',
#         role = 'cook',
#     ),
#     User(
#         id = 2,
#         user_name = 'kishan',
#         password = 'patel123',
#         role = 'cook',
#     ),
# ]

# data_recipe = [
#     Recipe(
#         id = 1,
#         name = 'Chicken Biryani',
#         date_created = datetime(2023,6,22,17,2,31),
#         date_modified = datetime(2023,6,22,17,2,31),
#         created_by = 1,
#         modified_by = 1,
#     ),
# ]

# %%
# with app.app_context():
#     for u in data_user:
#         db.session.add(u)
#     for r in data_recipe:
#         db.session.add(r)

#     db.session.commit()
    
    
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
# csv_users = []
# with open("./seed_data/data_user.csv", 'r') as f:

#     cols = f.readline().replace('\n', '').split(',')
#     for line in f:
#         values = line.replace(',')

# %%
seed_map = [
    {
        'name': 'user',
        'cls': User,
        'file': 'data_user.csv',
        'dt_cols': [],
    },
    {
        'name': 'recipe',
        'cls': Recipe,
        'file': 'data_recipe.csv',
        'dt_cols': ['date_created', 'date_modified'],
    },
    {
        'name': 'tag',
        'cls': Tag,
        'file': 'data_tag.csv',
        'dt_cols': [],

    }
]
# %%
with app.app_context():
    db.drop_all()
    db.create_all()

    for mapper in seed_map:
        print(mapper['name'])
        mod_inst_items = []

        with open(f'./seed_data/{mapper["file"]}', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                mod_inst = mapper['cls']()
                for key, value in row.items():
                    if key in mapper['dt_cols']:
                        if value != '':
                            value = datetime.strptime(value, '%Y-%m-%d')
                        else:
                            value = None
                    setattr(mod_inst, key, value)
                mod_inst_items.append(mod_inst)

        for mod_inst in mod_inst_items:
            db.session.add(mod_inst)

    db.session.commit()


# %%
