from flask import Flask, request, jsonify, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path(__file__).with_name("recipes.db")

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS recipes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, cuisine TEXT DEFAULT 'Other',
            category TEXT DEFAULT 'Lunch', prep_time INTEGER DEFAULT 20,
            difficulty TEXT DEFAULT 'Easy', ingredients TEXT NOT NULL,
            steps TEXT NOT NULL, likes INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        if con.execute("SELECT COUNT(*) FROM recipes").fetchone()[0] == 0:
            samples = [
                ("Creamy Tomato Pasta","Italian","Lunch",25,"Easy",
                 "Pasta\\nTomatoes\\nGarlic\\nCream\\nOlive oil",
                 "Boil pasta until al dente.\\nCook garlic and tomatoes in olive oil.\\nStir in cream and combine with pasta."),
                ("Fresh Mango Bowl","Indian","Breakfast",10,"Easy",
                 "Mango\\nYogurt\\nOats\\nNuts",
                 "Dice the mango.\\nAdd yogurt to a bowl.\\nTop with mango, oats and nuts."),
                ("Garden Veggie Wrap","Mediterranean","Vegan",20,"Easy",
                 "Tortilla\\nCucumber\\nTomato\\nLettuce\\nHummus",
                 "Chop all vegetables.\\nSpread hummus on tortilla.\\nAdd vegetables, roll and serve.")
            ]
            con.executemany("""INSERT INTO recipes(title,cuisine,category,prep_time,difficulty,ingredients,steps)
                               VALUES(?,?,?,?,?,?,?)""", samples)

def serialize(row):
    d = dict(row)
    d["ingredients"] = d["ingredients"].splitlines()
    d["steps"] = d["steps"].splitlines()
    return d

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/recipes")
def recipes():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()
    sql = "SELECT * FROM recipes WHERE 1=1"
    args = []
    if q:
        like = f"%{q}%"
        sql += " AND (title LIKE ? OR ingredients LIKE ? OR cuisine LIKE ?)"
        args += [like, like, like]
    if category and category != "All":
        sql += " AND category=?"
        args.append(category)
    sql += " ORDER BY id DESC"
    with db() as con:
        rows = con.execute(sql, args).fetchall()
    return jsonify([serialize(r) for r in rows])

@app.post("/api/recipes")
def add_recipe():
    d = request.get_json(silent=True) or {}
    title = (d.get("title") or "").strip()
    ingredients = d.get("ingredients") or []
    steps = d.get("steps") or []
    if not title or not ingredients or not steps:
        return jsonify({"error": "Title, ingredients and steps are required."}), 400
    try:
        prep = max(1, min(1440, int(d.get("prep_time", 20))))
    except (ValueError, TypeError):
        return jsonify({"error": "Preparation time must be a number."}), 400
    with db() as con:
        cur = con.execute("""INSERT INTO recipes(title,cuisine,category,prep_time,difficulty,ingredients,steps)
            VALUES(?,?,?,?,?,?,?)""",
            (title[:100], (d.get("cuisine") or "Other")[:40],
             (d.get("category") or "Lunch")[:30], prep,
             (d.get("difficulty") or "Easy")[:20],
             "\\n".join(str(x).strip() for x in ingredients if str(x).strip()),
             "\\n".join(str(x).strip() for x in steps if str(x).strip())))
        rid = cur.lastrowid
    return jsonify({"id": rid, "message": "Recipe created."}), 201

@app.get("/api/recipes/<int:recipe_id>")
def recipe_detail(recipe_id):
    with db() as con:
        row = con.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,)).fetchone()
    if not row:
        return jsonify({"error": "Recipe not found."}), 404
    return jsonify(serialize(row))

@app.post("/api/recipes/<int:recipe_id>/like")
def like_recipe(recipe_id):
    with db() as con:
        cur = con.execute("UPDATE recipes SET likes=likes+1 WHERE id=?", (recipe_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "Recipe not found."}), 404
        likes = con.execute("SELECT likes FROM recipes WHERE id=?", (recipe_id,)).fetchone()["likes"]
    return jsonify({"likes": likes})

@app.delete("/api/recipes/<int:recipe_id>")
def delete_recipe(recipe_id):
    with db() as con:
        cur = con.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
        if cur.rowcount == 0:
            return jsonify({"error": "Recipe not found."}), 404
    return jsonify({"message": "Recipe deleted."})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
