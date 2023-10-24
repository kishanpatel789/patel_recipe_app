# %%
import sys
sys.path.insert(1, '..')

from application import create_app
from application.models import db, Recipe, Ingredient, Direction, Unit, Tag, recipe_tag

# %%
app = create_app()

# %%
with app.app_context():
    # rep = db.session.execute(
    #     db.select(Recipe).where(Recipe.id==2)
    # ).scalars().unique().one_or_none()
    # db.session.delete(rep)
    # existing_dirs = {d.order_id for d in rep.directions}

    # comp = rep.complementary_dishes.all()

    # ingredients = db.session.execute(
    #     db.select(Ingredient).where(Ingredient.recipe_id==1)
    # ).scalars().unique().all()

    # new_tag = Tag(name='hello')
    # t1 = db.session.add(new_tag)
    # t2 = db.session.commit()

    # units = db.session.execute(
    #         db.select(Unit).order_by(Unit.name)
    #     ).scalars().all()
    
    # directions = db.session.execute(
    #     db.select(Direction).where(Direction.recipe_id==2)
    # ).scalars().unique().all()

    # direction = db.session.execute(
    #     db.select(Direction).where(Direction.id==13)
    # ).scalars().unique().one_or_none()
    # db.session.delete(direction)

    # db.session.commit()

    # recipes = db.session.execute(
    #     db.select(Recipe).order_by(Recipe.name)
    # ).scalars().unique().all()
    # recipes = db.session.execute(
    #     db.select(Recipe.name.label('recipe_name'), Tag.name.label('tag_name'))\
    #         .select_from(Recipe).join(recipe_tag, isouter=True)\
    #             .join(Tag, isouter=True)
    # ).all()

    # for r in recipes:
    #     print(r.name)
    #     for t in r.tags:
    #         print(t.name)

    # tt = db.session.execute(
    # db.select(Recipe, Tag).\
    # join(Recipe.tags).\
    # join(Tag, Recipe.tags).\
    # order_by(Recipe.id)
    # )

    subquery = (db.select(
        Ingredient.item, 
        Ingredient.unit_id,
        db.func.sum(Ingredient.quantity).label('quantity'),
        db.func.min(Ingredient.direction_id * 100 + Ingredient.order_id).label('comb_order_id'),
        )
        .select_from(Recipe)
        .join(Direction)
        .join(Ingredient)
        .where(Recipe.id==16)
        .group_by(
            Ingredient.item,
            Ingredient.unit_id,
        )
        .order_by('comb_order_id')
    ).subquery()

    ingr = db.session.execute(
        db.select(
        subquery.c.comb_order_id,
        subquery.c.item,
        subquery.c.quantity,
        subquery.c.unit_id,
        Unit.name.label('unit_name'),
        Unit.name_plural.label('unit_name_plural'),
        Unit.abbr_singular.label('unit_abbr_singular'),
        Unit.abbr_plural.label('unit_abbr_plural'),
        )
        .select_from(subquery)
        .join(Unit, isouter=True)
    ).all()

# %%
subquery = (db.select(
        Ingredient.item, 
        Ingredient.unit_id,
        db.func.sum(Ingredient.quantity).label('quantity'),
        db.func.min(Ingredient.direction_id * 100 + Ingredient.order_id).label('comb_order_id'),
        )
        .select_from(Recipe)
        .join(Direction)
        .join(Ingredient)
        .where(Recipe.id==16)
        .group_by(
            Ingredient.item,
            Ingredient.unit_id,
        )
        .order_by('comb_order_id')
).subquery()

print(str(
    # db.select(Recipe, Ingredient).where(Recipe.id==16)
    db.select(
        subquery.c.comb_order_id,
        subquery.c.item,
        subquery.c.quantity,
        subquery.c.unit_id,
        Unit.name,
        Unit.name_plural,
        Unit.abbr_singular,
        Unit.abbr_plural,
        )
        .select_from(subquery)
        .join(Unit, isouter=True)
))
# %%
