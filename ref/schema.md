# Schema

## Recipe
| col           | type | nullable | unique | ref      |
| ------------- | ---- | :------: | :----: | -------- |
| id            | int  |          |   1    |          |
| name          | str  |          |   1    |          |
| date_created  | dt   |          |        |          |
| date_modified | dt   |    1     |        |          |
| created_by    | int  |          |        | User(id) |
| modified_by   | int  |    1     |        | User(id) |
| is_active     | bool |    1     |        |          |


## User
| col       | type | nullable | unique | ref |
| --------- | ---- | :------: | :----: | --- |
| id        | int  |          |   1    |     |
| user_name | str  |          |   1    |     |
| password  | str  |          |   1    |     |
| role      | str  |          |   1    |     |
| is_active | bool |    1     |        |     |

## Tag
| col       | type | nullable | unique | ref |
| --------- | ---- | :------: | :----: | --- |
| id        | int  |          |   1    |     |
| name      | str  |          |   1    |     |
| is_active | bool |    1     |        |     |

## RecipeTag
| col       | type | nullable | unique | ref        |
| --------- | ---- | :------: | :----: | ---------- |
| recipe_id | int  |          |        | Recipe(id) |
| tag_id    | int  |          |        | Tag(id)    |

- Unique by both recipe_id and tag_id

## Direction
| col         | type | nullable | unique | ref        |
| ----------- | ---- | :------: | :----: | ---------- |
| id          | int  |          |   1    |            |
| recipe_id   | int  |          |        | Recipe(id) |
| order_id    | int  |          |        |            |
| description | str  |          |        |            |

## Ingredient
| col          | type  | nullable | unique | ref        |
| ------------ | ----- | :------: | :----: | ---------- |
| id           | int   |          |   1    |            |
| direction_id | int   |          |        | Recipe(id) |
| order_id     | int   |          |        |            |
| quantity     | float |    1     |        |            |
| unit_id      | int   |    1     |        | Unit(id)   |
| item         | str   |          |        |            |

## Unit
| col           | type | nullable | unique | ref |
| ------------- | ---- | :------: | :----: | --- |
| id            | int  |          |   1    |     |
| name          | str  |          |   1    |     |
| name_plural   | str  |          |   1    |     |
| abbr_singular | str  |    1     |        |     |
| abbr_plural   | str  |    1     |        |     |
| is_active     | bool |    1     |        |     |


## ComplementaryDish
| col            | type | nullable | unique | ref        |
| -------------- | ---- | :------: | :----: | ---------- |
| recipe_id      | int  |          |        | Recipe(id) |
| comp_recipe_id | int  |          |        | Recipe(id) |

- Unique by recipe_id and comp_recipe_id