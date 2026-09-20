from flask import Flask, render_template, request, redirect, session, jsonify, Response
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = "toxishield_secret"

CORS(app)

DB = "database.db"

def get_db():
    return sqlite3.connect(DB)

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == "admin" and pwd == "1234":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM comments ORDER BY id DESC")
    comments = cur.fetchall()

    total = len(comments)
    toxic = len([c for c in comments if c[2] == "toxic"])
    neutral = total - toxic

    conn.close()

    return render_template(
        "dashboard.html",
        comments=comments,
        total=total,
        toxic=toxic,
        neutral=neutral
    )

# ---------- TOXIC ----------
@app.route("/toxic")
def toxic():
    if not session.get("admin"):
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM comments WHERE label='toxic'")
    comments = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        comments=comments,
        total=len(comments),
        toxic=len(comments),
        neutral=0
    )

# ---------- NEUTRAL ----------
@app.route("/neutral")
def neutral():
    if not session.get("admin"):
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM comments WHERE label='neutral'")
    comments = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        comments=comments,
        total=len(comments),
        toxic=0,
        neutral=len(comments)
    )

# ---------- CLEAR DATABASE ----------
@app.route("/clear", methods=["POST"])
def clear():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM comments")

    conn.commit()
    conn.close()

    return jsonify({"status": "cleared"})

# ---------- SAVE ----------
@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO comments (text, label, platform) VALUES (?, ?, ?)",
        (data.get("text"), data.get("label"), data.get("platform"))
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})

# ---------- DELETE ----------
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM comments WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

# ---------- EXPORT ----------
@app.route("/export")
def export():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM comments")
    data = cur.fetchall()

    def generate():
        yield "id,text,label,platform\n"
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

    return Response(generate(), mimetype="text/csv")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
