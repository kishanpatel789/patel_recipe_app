# %%
import os
import requests
from bs4 import BeautifulSoup
import shutil

# %%
BASE_URL = 'http://localhost:5000'
APP_DIR = '../application'
OUTPUT_DIRECTORY = '../static_site'


# %%
# Define a list of URLs to convert to static pages
# index.html
# 404.html
# recipe pages
# static/
#   js/jquery
#   json/search_data
#   scss/styles.css
#   favicon
#   sorry.png

recipe_count = 5
recipe_urls = [
    (BASE_URL, 'index.html'),
    ('/'.join([BASE_URL, '404.html']), '404.html')
]

static_resources = [
    'js/jquery-3.7.0.js',
    'json/search_recipe_data.json',
    'scss/styles.css',
    'svg/CurryLeafBorder.svg',
    'svg/SingleCurryBranch.svg',
    'favicon.ico',
    'sorry.png',
]

for i in range(1, recipe_count+1):
    recipe_urls.append(
        ('/'.join([BASE_URL, f'recipe/{i}']), f'recipe/{i}')
        )


# %%

# # Create the output directory if it doesn't exist
# os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# response = requests.get(BASE_URL)
# soup = BeautifulSoup(response.content, 'html.parser')

# file_name = os.path.join(OUTPUT_DIRECTORY, f'index.html')
        
# with open(file_name, 'w', encoding='utf-8') as f:
#     f.write(str(soup))

# %%
# Loop through each URL and convert it to a static HTML file
for url, file_name in recipe_urls:
    # Fetch the content of the URL
    response = requests.get(url)
    
    if (response.status_code == 200) or (response.status_code == 404 and file_name == '404.html'):
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
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

print('Conversion complete.')

# %%
for static_res in static_resources:
    src_path = '/'.join([APP_DIR, 'static', static_res])
    dest_path = '/'.join([OUTPUT_DIRECTORY, 'static', static_res])

    dest_dir = os.path.split(dest_path)[0]
    os.makedirs(dest_dir, exist_ok=True)

    shutil.copy2(src_path, dest_path)
    print(f'Copied {src_path} to {dest_path}')

# %%
