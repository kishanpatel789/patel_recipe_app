
from fastapi import FastAPI

# import routers
from .routers import tags

# initialize
app = FastAPI()
app.include_router(tags.router)

@app.get('/')
def read_root():
    return {'Hello': 'World'}
