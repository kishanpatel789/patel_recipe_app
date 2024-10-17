
from fastapi import FastAPI

# import routers
from .routers import tags, units, recipes

# initialize
app = FastAPI()
app.include_router(tags.router)
app.include_router(units.router)
app.include_router(recipes.router)

@app.get('/')
def read_root():
    return {'Hello': 'World'}
