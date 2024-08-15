# %%
import sys
sys.path.insert(1, '..')

import csv
import re

# %%
# define global variables
PATH_GSHEET_CSV = '../seed_data/src/gsheet_seed_data.csv'
PATH_RECIPE_CSV = '../seed_data/data_recipe.csv'
PATH_DIRECTION_CSV = '../seed_data/data_direction.csv'
PATH_INGREDIENT_CSV = '../seed_data/data_ingredient.csv'
PATH_RECIPETAG_CSV = '../seed_data/data_recipetag.csv'
PATH_COMPLEMENTARYDISH_CSV = '../seed_data/data_complementarydish.csv'
PATH_COMPLEMENTARYDISH_TMP = '../seed_data/data_complementarydish_tmp.csv'


FIELD_NAMES_RECIPE = [
    'id',
    'name',
    'slug',
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
FIELD_NAMES_RECIPETAG = [
    'recipe_id',
    'tag_id',
]
FIELD_NAMES_COMPLEMENTARYDISH = [
    'recipe_id',
    'comp_recipe_id',
]
FIELD_NAMES_COMPLEMENTARYDISH_TMP = [
    'recipe_id',
    'recipe_name',
    'comp_recipe_name',
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
    "unit": 1,
    "tbsp": 3,
    "tsp": 2,
    "oz": 4,
    "c": 5,
    "leaves": 9,
}

# define tag mapper
tag_mapper = {
    'MainDish': 1,
    'SideItem': 2,
    'Dessert': 3,
    'Snack': 4,
    'Veggie': 5,
    'Chicken': 6,
    'Dressing': 7,
    'Bread': 8,
    'Chutney': 9,
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

with open(PATH_RECIPETAG_CSV, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_RECIPETAG)
    writer.writeheader()

with open(PATH_COMPLEMENTARYDISH_CSV, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_COMPLEMENTARYDISH)
    writer.writeheader()

with open(PATH_COMPLEMENTARYDISH_TMP, 'w', newline='\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_COMPLEMENTARYDISH_TMP)
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
            recipe_slug = re.sub(r'[^\w\s]', '', recipe_name).replace(' ', '-').lower()
            with open(PATH_RECIPE_CSV, 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_RECIPE)
                writer.writerow({
                    'id': recipe_id,
                    'name': recipe_name,
                    'slug': recipe_slug,
                    'created_by': 1,
                })

            # parse tags
            if row['Tags'].strip():
                for new_tag_raw in row['Tags'].strip().split(';'):
                    new_tag_name = new_tag_raw.strip().replace(' ', '') # strip and remove white spaces
                    new_tag_id = tag_mapper[new_tag_name]
                    with open(PATH_RECIPETAG_CSV, 'a', newline='\n') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_RECIPETAG)
                        writer.writerow({
                            'recipe_id': recipe_id,
                            'tag_id': new_tag_id,
                        })

            # parse complementary dishes
            if row['ComplementaryDishes'].strip():
                for comp_dish_raw in row['ComplementaryDishes'].strip().split(';'):
                    comp_dish = comp_dish_raw.strip() # strip and remove white spaces
                    with open(PATH_COMPLEMENTARYDISH_TMP, 'a', newline='\n') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_COMPLEMENTARYDISH_TMP)
                        writer.writerow({
                            'recipe_id': recipe_id,
                            'recipe_name': recipe_name,
                            'comp_recipe_name': comp_dish,
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
            ingredient_quantity = row['IngredientQty'].strip()
            ingredient_unit_raw = row['IngredientUnit'].strip()
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




# %%
# clean complementary dish file
recipe_mapper = {}
with open(PATH_RECIPE_CSV, newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        recipe_mapper[row['name']] = row['id']

# loop through tmp comp file, map id, write to comp file
with open(PATH_COMPLEMENTARYDISH_TMP, newline='\n') as tmpfile:
    reader = csv.DictReader(tmpfile)
    with open(PATH_COMPLEMENTARYDISH_CSV, 'a', newline='\n') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES_COMPLEMENTARYDISH)
        for row in reader:
            recipe_id = row['recipe_id']
            try:
                comp_recipe_id = recipe_mapper[row['comp_recipe_name']]
                writer.writerow({
                    'recipe_id': recipe_id,
                    'comp_recipe_id': comp_recipe_id,
                })
                print(f"'{row['recipe_name']}' ({recipe_id}) has '{row['comp_recipe_name']}' ({comp_recipe_id}) as a complement")
            except KeyError:
                print(f"No ID found for recipe '{row['comp_recipe_name']}'")


# %%
