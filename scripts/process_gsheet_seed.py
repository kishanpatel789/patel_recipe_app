# %%
from datetime import datetime 
from pathlib import Path
import sys
sys.path.insert(1, '..')

import csv

# %%
# define global variables
PATH_GSHEET_CSV = '../seed_data/src/gsheet_seed_data.csv'
PATH_RECIPE_CSV = '../seed_data/data_recipe.csv'
PATH_DIRECTION_CSV = '../seed_data/data_direction.csv'
PATH_INGREDIENT_CSV = '../seed_data/data_ingredient.csv'

FIELD_NAMES_RECIPE = [
    'id',
    'name',
    'date_created',
    'date_modified',
    'created_by',
    'modified_by',
]
FIELD_NAMES_DIRECTION = [
    'id',
    'recipe_id',
    'order_id',
    'description_',
]
FIELD_NAMES_INGREDIENT = [
    'id',
    'direction_id',
    'order_id',
    'quantity',
    'unit_id',
    'item',
]

# %%
# initialize counters
recipe_id = 0
direction_id = 0
direction_order_id = 0
ingredient_id = 0
ingredient_order_id = 0

# define unit mapper
unit_mapper = {
    "units": 1,
    "tbsp": 3,
    "tsp": 2,
    "oz": 4,
    "c": 5,
    "leaves": 9,
}


# %%
# initialize output files
with open(PATH_RECIPE_CSV, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_RECIPE)
    writer.writeheader()

with open(PATH_DIRECTION_CSV, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_DIRECTION)
    writer.writeheader()

with open(PATH_INGREDIENT_CSV, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_INGREDIENT)
    writer.writeheader()


# %%
with open(PATH_GSHEET_CSV, newline='\n') as csvfile_gsheet:
    reader = csv.DictReader(csvfile_gsheet)
    for row in reader:

        if row['RecipeName'].strip():  # this starts a new recipe
            recipe_name = row['RecipeName'].strip()
            print(f"Beginning new recipe: {recipe_name}")
            recipe_id += 1
            direction_order_id = 0
            with open(PATH_RECIPE_CSV, 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_RECIPE)
                writer.writerow({
                    'id': recipe_id,
                    'name': recipe_name,
                    'created_by': 1,
                })

        if row['DirectionText'].strip(): # this starts a new direction
            direction_desc = row['DirectionText'].strip()
            direction_id += 1
            direction_order_id += 1
            ingredient_order_id = 0

            with open(PATH_DIRECTION_CSV, 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_DIRECTION)
                writer.writerow({
                    'id': direction_id,
                    'recipe_id': recipe_id,
                    'order_id': direction_order_id,
                    'description_': direction_desc,
                })
        else: # this is an ingredient line
            ingredient_id += 1
            ingredient_order_id += 1
            ingredient_quantity = row['IngredientQty']
            ingredient_unit_raw = row['IngredientUnit']
            ingredient_item = row['IngredientItem'].strip()

            ingredient_unit_id = unit_mapper[ingredient_unit_raw]

            with open(PATH_INGREDIENT_CSV, 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_INGREDIENT)
                writer.writerow({
                    'id': ingredient_id,
                    'direction_id': direction_id,
                    'order_id': ingredient_order_id,
                    'quantity': ingredient_quantity,
                    'unit_id': ingredient_unit_id,
                    'item': ingredient_item,
                })



