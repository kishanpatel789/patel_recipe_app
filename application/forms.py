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

class BaseForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            if strip_whitespace not in filters:
                filters.append(strip_whitespace)
            return unbound_field.bind(form=form, filters=filters, **options)

class TagForm(BaseForm):
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
        # filters=[
        #     strip_whitespace
        # ]
    )
    
    submit = SubmitField('Submit')

class UnitForm(BaseForm):
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
    )
    name_plural = StringField(
        'Unit Name Plural',
        validators=[
            InputRequired(),
            Length(min=1, max=20)
        ],
    )
    abbr_singular = StringField(
        'Unit Abbreviation',
        validators=[
            Length(max=20)
        ],
    )
    abbr_plural = StringField(
        'Unit Abbreviation Plural',
        validators=[
            Length(max=20)
        ],
    )
    
    submit = SubmitField('Submit')