# Make a Flask server that boots up a SQLite instance for each session
from flask import Flask, render_template, request, session, redirect, url_for
import os
import datetime, threading
import sqlite3
import traceback

# Create the Flask application
app = Flask(__name__)

app.secret_key = "26115f592adbb689c20411fcd96e5d5e0b0fac079021456959dc5e9c713440a7"

reset_period = 15

next_restart = datetime.datetime.now() + datetime.timedelta(minutes=reset_period)

flag = open("flag.txt", "r").read()

sql_connections = {}

def restart():
    global next_restart
    next_restart = datetime.datetime.now() + datetime.timedelta(minutes=reset_period)
    # Delete all files in folder dbs
    for f in os.listdir("dbs"):
        os.remove("dbs/" + f)
    print("Clearing databases.")
    for conn in sql_connections.values():
        conn.close()
    sql_connections.clear()
    threading.Timer(reset_period * 60, restart).start()


def time_to_restart():
    # format as mm:ss
    return str(next_restart - datetime.datetime.now())[2:-7]

def get_conn(db):
    if db not in sql_connections:
        conn = sqlite3.connect("dbs/" + db + ".db")
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        sql_connections[db] = conn
        return conn
    return sql_connections[db]


def init_db(db):
    role_table = "roles_" + os.urandom(8).hex()
    conn = get_conn(db)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    c.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
    )
    c.execute(
        f"CREATE TABLE IF NOT EXISTS {role_table} (id INTEGER, admin INTEGER, FOREIGN KEY(id) REFERENCES users(id) ON UPDATE CASCADE)"
    )
    # Add user if they don't exist
    c.execute("SELECT * FROM users")
    if not c.fetchone():
        c.execute('INSERT INTO users (id, name) VALUES (0, "admin")')
        c.execute('INSERT INTO users (id, name) VALUES (1, "temp-username")')
        c.execute(f"INSERT INTO {role_table} (id, admin) VALUES (0, 1)")
        c.execute(f"INSERT INTO {role_table} (id, admin) VALUES (1, 0)")
    conn.commit()
    return role_table


@app.route("/set-username", methods=["POST"])
def set_name():
    print(request.form["username"], session["db"])
    try:
        conn = get_conn(session["db"])
        c = conn.cursor()
        c.execute(f'UPDATE users SET name="{request.form["username"]}" WHERE id=1')
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        return redirect(f"/?error={str(e)}")
    return redirect("/")


@app.route("/")
def index():
    print(session.get("db"), session.get("role_table"))
    if not session.get("db") or not session.get("role_table") or request.args.get("reset"):
        session["db"] = os.urandom(16).hex()
        session["role_table"] = init_db(session["db"])
        return redirect(f"/?error={request.args.get('error')}")
    # Fetch username from db

    try:
        conn = get_conn(session["db"])
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE id=1")
        username = c.fetchone()[0]
        c.execute(f'SELECT admin FROM {session["role_table"]} WHERE id=1')
        admin = c.fetchone()[0]
    except Exception as e:
        print(traceback.format_exc())
        return redirect(f"/?reset=1&error={str(e)}")

    return render_template(
        "index.html",
        username=username,
        admin=admin,
        flag=flag,
        time_to_restart=time_to_restart(),
        error = request.args.get("error")
    )


if __name__ == "__main__":
    restart()
    app.run()
