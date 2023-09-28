# %%
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired

import sys
sys.path.insert(1, '..')

from application.forms import RecipeForm, BaseForm
from application import create_app

# %%
app = create_app()

# %%
with app.test_request_context():
    form_base = BaseForm()
    form_flask = FlaskForm()
    form_recipe = RecipeForm()
# %%
