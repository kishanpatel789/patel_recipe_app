# %%
import os
import requests
from bs4 import BeautifulSoup
import shutil
import sys
sys.path.insert(1, '..')

from application import create_app
from application.models import db, Recipe

# %%
app = create_app()

# %%
BASE_URL = 'http://localhost:5000'
APP_DIR = '../application'
OUTPUT_DIRECTORY = '../static_site'

# %%
# get recipe count
with app.app_context():
    recipe_count = db.session.execute(
        db.select(db.func.max(Recipe.id))
    ).scalar()

# %%
# Define a list of URLs to convert to static pages
# index.html
# 404.html
# recipe pages
# static/
#   js/jquery
#   json/search_data
#   scss/styles.css
#   svg/CurryLeafBorder.svg
#   svg/SingleCurryBranch.svg
#   favicon
#   sorry.png

recipe_urls = [
    (BASE_URL, 'index.html'),
    ('/'.join([BASE_URL, '404.html']), '404.html')
]

# map recipe card pages
for i in range(1, recipe_count+1):
    recipe_urls.append(
        ('/'.join([BASE_URL, f'recipe/{i}']), f'recipe/{i}/index.html')
        )


static_resources = [
    'js/jquery-3.7.0.js',
    'json/search_recipe_data.json',
    'scss/styles.css',
    'svg/CurryLeafBorder.svg',
    'svg/SingleCurryBranch.svg',
    'svg/SingleCurryBranch_short.svg',
    'favicon.ico',
    'sorry.png',
]

# %%
# Loop through each URL and convert it to a static HTML file
for url, file_name in recipe_urls:
    # Fetch the content of the URL
    response = requests.get(url)
    
    if (response.status_code == 200) or (response.status_code == 404 and file_name == '404.html'):
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # remove edit button if applicable
        edit_button = soup.find(id='editButton')
        if edit_button:
            edit_button.extract()
        
        # Define the filename for the static HTML page (you can customize this)
        file_path = os.path.join(OUTPUT_DIRECTORY, file_name)

        dest_dir = os.path.split(file_path)[0]
        os.makedirs(dest_dir, exist_ok=True)
        
        # Save the parsed HTML content to the static HTML file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f'Converted {url} to {file_name}')
    else:
        print(f'Failed to fetch {url}')


# %%
# copy static resources
for static_res in static_resources:
    src_path = '/'.join([APP_DIR, 'static', static_res])
    dest_path = '/'.join([OUTPUT_DIRECTORY, 'static', static_res])

    dest_dir = os.path.split(dest_path)[0]
    os.makedirs(dest_dir, exist_ok=True)

    shutil.copy2(src_path, dest_path)
    print(f'Copied {src_path} to {dest_path}')

# %%
