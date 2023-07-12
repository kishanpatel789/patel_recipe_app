from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class TagForm(FlaskForm):
    """Contact form."""
    id = IntegerField(
        'Id',
    )
    name = StringField(
        'Name',
        [DataRequired()],
    )
    
    submit = SubmitField('Submit')