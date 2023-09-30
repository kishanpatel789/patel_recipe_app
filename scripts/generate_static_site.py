# %%
import os
import requests
from bs4 import BeautifulSoup

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
]

static_resources = [
    
]

# for i in range(1, recipe_count+1):
#     recipe_urls.append('/'.join([BASE_URL, f"recipe/{i}"]))


# %%

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.content, 'html.parser')

file_name = os.path.join(OUTPUT_DIRECTORY, f'index.html')
        
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(str(soup))

# %%
# Loop through each URL and convert it to a static HTML file
for url in urls:
    # Fetch the content of the URL
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title of the page
        title = soup.title.string
        
        # Define the filename for the static HTML page (you can customize this)
        filename = os.path.join(OUTPUT_DIRECTORY, f'{title}.html')
        
        # Save the parsed HTML content to the static HTML file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f'Converted {url} to {filename}')
    else:
        print(f'Failed to fetch {url}')

print('Conversion complete.')
