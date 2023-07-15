# %%
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired

# %%
tt = FlaskForm(formdata=None)
dir(tt)
# %%
