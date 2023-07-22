# %%
from datetime import datetime 
from pathlib import Path

# from config import db
from application.models import db, User, Recipe, Tag, recipe_tag, Unit, Ingredient, Direction, complementary_dish
from application import create_app

import csv

# %%
app = create_app()

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
        'float_cols': [],
    },
    {
        'name': 'recipe',
        'cls': Recipe,
        'file': 'data_recipe.csv',
        'dt_cols': ['date_created', 'date_modified'],
        'float_cols': [],
    },
    {
        'name': 'tag',
        'cls': Tag,
        'file': 'data_tag.csv',
        'dt_cols': [],
        'float_cols': [],
    },
    {
        'name': 'unit',
        'cls': Unit,
        'file': 'data_unit.csv',
        'dt_cols': [],
        'float_cols': [],
    },
    {
        'name': 'ingredient',
        'cls': Ingredient,
        'file': 'data_ingredient.csv',
        'dt_cols': [],
        'float_cols': ['quantity'],
    },
    {
        'name': 'direction',
        'cls': Direction,
        'file': 'data_direction.csv',
        'dt_cols': [],
        'float_cols': [],
    },
]

seed_map_assoc = [
    {
        'name': 'recipe_tag',
        'tbl': recipe_tag,
        'file': 'data_recipetag.csv',
    },
    {
        'name': 'complementary_dish',
        'tbl': complementary_dish,
        'file': 'data_complementarydish.csv',
    },
]
# %%
with app.app_context():
    db.drop_all()
    db.create_all()

    # models
    for mapper in seed_map:
        print(mapper['name'])
        mod_inst_items = []

        with open(f'./seed_data/{mapper["file"]}', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                mod_inst = mapper['cls']()
                for key, value in row.items():
                    if value == '':  # overwrite empty value with None (null)
                        value = None
                    if key in mapper['dt_cols'] and value != None:
                        value = datetime.strptime(value, '%Y-%m-%d')
                    setattr(mod_inst, key, value)
                mod_inst_items.append(mod_inst)

        for mod_inst in mod_inst_items:
            db.session.add(mod_inst)

    # association tables
    for mapper in seed_map_assoc:
        print(mapper['name'])
        records = []
        with open(f'./seed_data/{mapper["file"]}', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                records.append(row)
        multiple_insert = mapper['tbl'].insert().values(records)
        db.session.execute(multiple_insert)

    db.session.commit()


# %%
# with app.app_context():
#     records = []
#     with open(f'./seed_data/data_recipetag.csv', newline='\n') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             records.append(row)

#     multiple_insert = recipe_tag.insert().values(records)
#     db.session.execute(multiple_insert)

#     db.session.commit()

# # %%
# with open(f'./seed_data/data_recipetag.csv', newline='\n') as csvfile:
#     records = []
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         records.append(row)
#     print(values)
# %%
