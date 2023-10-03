# %%
import sys
sys.path.insert(1, '..')

from application import create_app
from application.models import db, Recipe
import json

# %%
OUTPUT_FILE = '../application/static/json/search_recipe_data.json'

# %%
app = create_app()

# %%
search_lib = []

with app.app_context():
    recipes = db.session.execute(
        db.select(Recipe).order_by(Recipe.name)
    ).scalars().all()

    for r in recipes:
        dict_recipe = {
            'id': r.id,
            'name': r.name,
            'tags': []
        }
        for t in r.tags:
            dict_recipe['tags'].append(f"#{t.name}")
        dict_recipe['tags'].sort()

        search_lib.append(dict_recipe)
# %%
with open(OUTPUT_FILE, 'w') as f:
    json.dump(search_lib, f, indent=4)
# %%
