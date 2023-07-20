from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Optional

def strip_whitespace(s):
    # if isinstance(s, str):
    #     s.strip()
    # return s.strip()

    if s is not None and hasattr(s, 'strip'):
        return s.strip()
    return s

class TagForm(FlaskForm):
    """Tag form."""
    id = IntegerField(
        'Id',
    )
    name = StringField(
        'Tag Name',
        validators=[
            InputRequired(),
            Length(min=1, max=20)
        ],
        filters=[
            strip_whitespace
        ]
    )
    
    submit = SubmitField('Submit')

class UnitForm(FlaskForm):
    """Unit form."""
    id = IntegerField(
        'Id',
    )
    name = StringField(
        'Unit Name',
        validators=[
            InputRequired(),
            Length(min=1, max=20)
        ],
        filters=[
            strip_whitespace
        ]
    )
    name_plural = StringField(
        'Unit Name Plural',
        validators=[
            InputRequired(),
            Length(min=1, max=20)
        ],
        filters=[
            strip_whitespace
        ]
    )
    abbr_singular = StringField(
        'Unit Abbreviation',
        validators=[
            Length(max=20)
        ],
        filters=[
            strip_whitespace
        ]
    )
    abbr_plural = StringField(
        'Unit Abbreviation Plural',
        validators=[
            Length(max=20)
        ],
        filters=[
            strip_whitespace
        ]
    )
    
    submit = SubmitField('Submit')