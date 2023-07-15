from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired


class TagForm(FlaskForm):
    """Contact form."""
    id = IntegerField(
        'Id',
    )
    name = StringField(
        'Tag Name',
        [InputRequired(),
         Length(min=1, max=20)],
    )
    
    submit = SubmitField('Create')