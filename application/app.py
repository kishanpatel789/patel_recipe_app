from flask import render_template

import config
from config import db
from models import Recipe

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    recipes = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()
    
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)



