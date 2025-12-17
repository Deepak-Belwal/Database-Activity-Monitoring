from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "simple_secret_key"

DB_NAME = "dam_db"

# -----------------------------
# Application users
# -----------------------------
USERS = {
    "root": "root@321",
    "Deepak": "Deepak@123"
}

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="glamsd"
    )
    cursor = db.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Activity_Log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            table_name VARCHAR(50),
            operation VARCHAR(10),
            old_data TEXT,
            new_data TEXT,
            user_name VARCHAR(50),
            activity_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Login_Log (
            login_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(50),
            host_name VARCHAR(100),
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    cursor.close()
    db.close()


# -----------------------------
# TRIGGER INITIALIZATION
# (single-statement triggers)
# -----------------------------
def init_triggers():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="glamsd",
        database=DB_NAME
    )
    cursor = db.cursor()

    # Drop old triggers (safe)
    cursor.execute("DROP TRIGGER IF EXISTS after_insert_users")
    cursor.execute("DROP TRIGGER IF EXISTS after_update_users")
    cursor.execute("DROP TRIGGER IF EXISTS after_delete_users")

    # INSERT trigger
    cursor.execute("""
        CREATE TRIGGER after_insert_users
        AFTER INSERT ON Users
        FOR EACH ROW
        INSERT INTO Activity_Log
        (table_name, operation, new_data, user_name)
        VALUES
        ('Users', 'INSERT',
         CONCAT('user_id=', NEW.user_id, ', username=', NEW.username),
         'APPLICATION')
    """)

    # UPDATE trigger
    cursor.execute("""
        CREATE TRIGGER after_update_users
        AFTER UPDATE ON Users
        FOR EACH ROW
        INSERT INTO Activity_Log
        (table_name, operation, old_data, new_data, user_name)
        VALUES
        ('Users', 'UPDATE',
         CONCAT('username=', OLD.username),
         CONCAT('username=', NEW.username),
         'APPLICATION')
    """)

    # DELETE trigger
    cursor.execute("""
        CREATE TRIGGER after_delete_users
        AFTER DELETE ON Users
        FOR EACH ROW
        INSERT INTO Activity_Log
        (table_name, operation, old_data, user_name)
        VALUES
        ('Users', 'DELETE',
         CONCAT('user_id=', OLD.user_id, ', username=', OLD.username),
         'APPLICATION')
    """)

    db.commit()
    cursor.close()
    db.close()


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="glamsd",
        database=DB_NAME,
        autocommit=True
    )


# -----------------------------
# INITIALIZE EVERYTHING
# -----------------------------
init_database()
init_triggers()

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["logged_in"] = True
            session["username"] = username

            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Login_Log (user_name, host_name) VALUES (%s, %s)",
                (username, request.remote_addr)
            )
            cursor.close()
            db.close()

            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Login_Log ORDER BY login_id DESC")
    login_logs = cursor.fetchall()

    cursor.execute("SELECT * FROM Activity_Log ORDER BY log_id DESC")
    activity_logs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        login_logs=login_logs,
        activity_logs=activity_logs
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
