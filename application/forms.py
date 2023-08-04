from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, SubmitField, IntegerField, FloatField, FormField, FieldList, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Optional

def strip_whitespace(s):
    # if isinstance(s, str):
    #     s.strip()
    # return s.strip()

    if s is not None and hasattr(s, 'strip'):
        return s.strip()
    return s

def read_none(x):
    return x or None



class Meta:
    @staticmethod
    def bind_field(form, unbound_field, options):
        filters = unbound_field.kwargs.get('filters', [])
        if not issubclass(unbound_field.field_class, FieldList):
            if strip_whitespace not in filters:
                filters.append(strip_whitespace)
            if read_none not in filters:
                filters.append(read_none)
        return unbound_field.bind(form=form, filters=filters, **options)

class BaseFormUnsecure(wtforms.Form): # used for form field
    Meta = Meta

class BaseForm(FlaskForm):
    Meta = Meta
    # class Meta:
    #     def bind_field(self, form, unbound_field, options):
    #         filters = unbound_field.kwargs.get('filters', [])
    #         if not issubclass(unbound_field.field_class, FieldList):
    #             if strip_whitespace not in filters:
    #                 filters.append(strip_whitespace)
    #             if read_none not in filters:
    #                 filters.append(read_none)
    #         return unbound_field.bind(form=form, filters=filters, **options)


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

class IngredientForm(BaseFormUnsecure):
    "Ingredient line item form"

    id = IntegerField(
        'Id',
    )
    recipe_id = IntegerField(
        'Recipe Id',
    )
    order_id = IntegerField(
        'Order Id',
    )
    quantity = FloatField(
        'Quantity',
        validators=[
            InputRequired(),
        ],
        render_kw={'type': 'number', 'step': 'any'}
    )
    unit_id = SelectField('Unit', coerce=int)
    item = StringField(
        'Item',
        validators=[
            InputRequired(),
            Length(min=1, max=20)
        ],
    )

class DirectionForm(BaseFormUnsecure):
    "Direction line item form"

    id = IntegerField(
        'Id',
    )
    recipe_id = IntegerField(
        'Recipe Id',
    )
    order_id = IntegerField(
        'OrderId',
    )
    description_ = StringField(
        'Description',
        validators=[
            InputRequired(),
            Length(min=1, max=500)
        ],
    )
    ingredients = FieldList(FormField(IngredientForm), min_entries=0)


class RecipeForm(BaseForm):
    """Recipe form"""

    id = IntegerField(
        'Id',
    )
    name = StringField(
        'Recipe Name',
        validators=[
            InputRequired(),
            Length(min=1, max=50)
        ],
    )
    directions = FieldList(FormField(DirectionForm), min_entries=1)

    submit = SubmitField('Submit')
