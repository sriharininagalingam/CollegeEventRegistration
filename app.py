from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            register_number TEXT,
            department TEXT,
            event TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

create_database()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        name = request.form["name"]
        register_number = request.form["register_number"]
        department = request.form["department"]
        event = request.form["event"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO registrations
            (name, register_number, department, event)
            VALUES (?, ?, ?, ?)
        """, (name, register_number, department, event))

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("index.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")
    registrations = cursor.fetchall()

    conn.close()

    return render_template(
        "registrations.html",
        registrations=registrations
    )


if __name__ == "__main__":
    app.run(debug=True)