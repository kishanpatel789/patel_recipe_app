from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TagForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'Name',
        [DataRequired()],
    )
    
    submit = SubmitField('Submit')