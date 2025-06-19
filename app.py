from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from werkzeug.utils import secure_filename
import sqlite3
import datetime
from ai_model import predict_accessibility

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Sprachunterstützung ---
def load_translations(lang='en'):
    try:
        with open(f'translations/{lang}.json', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# --- Hilfsfunktionen ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('data/accessai.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT,
            filename TEXT,
            timestamp TEXT,
            path_clear INTEGER,
            lift_working INTEGER,
            readable_info INTEGER,
            confidence_path REAL,
            confidence_lift REAL,
            confidence_readable REAL
        )
    ''')
    conn.commit()
    conn.close()

# --- Startseite / Upload ---
@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "en")
    t = load_translations(lang)

    if request.method == "POST":
        station = request.form['station']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            conn = sqlite3.connect('data/accessai.db')
            c = conn.cursor()
            c.execute("INSERT INTO uploads (station_name, filename, timestamp) VALUES (?, ?, ?)",
                      (station, filename, datetime.datetime.now().isoformat()))
            conn.commit()

            c.execute("SELECT last_insert_rowid()")
            upload_id = c.fetchone()[0]

            prediction = predict_accessibility(filepath)
            if prediction:
                c.execute("""
                    UPDATE uploads SET path_clear=?, lift_working=?, readable_info=?,
                                       confidence_path=?, confidence_lift=?, confidence_readable=?
                    WHERE id=?
                """, (
                    prediction["path_clear"],
                    prediction["lift_working"],
                    prediction["readable_info"],
                    prediction["confidence"]["path_clear"],
                    prediction["confidence"]["lift_working"],
                    prediction["confidence"]["readable_info"],
                    upload_id
                ))
                conn.commit()

            conn.close()
            return redirect(url_for('questions', id=upload_id, lang=lang))

    return render_template("index.html", t=t, lang=lang)

# --- Fragen-Seite ---
@app.route("/questions", methods=["GET", "POST"])
def questions():
    lang = request.args.get("lang", "en")
    t = load_translations(lang)

    if request.method == "POST":
        path_clear = request.form.get("path_clear")
        lift_working = request.form.get("lift_working")
        readable_info = request.form.get("readable_info")
        upload_id = request.form.get("upload_id")

        conn = sqlite3.connect("data/accessai.db")
        c = conn.cursor()
        c.execute("""
            UPDATE uploads
            SET path_clear=?, lift_working=?, readable_info=?
            WHERE id=?
        """, (path_clear, lift_working, readable_info, upload_id))

        c.execute("""SELECT station_name, filename, path_clear, lift_working, readable_info,
                            confidence_path, confidence_lift, confidence_readable
                     FROM uploads WHERE id=?""", (upload_id,))
        result = c.fetchone()

        conn.commit()
        conn.close()

        if result:
            station, filename, path_clear, lift_working, readable_info, c_path, c_lift, c_read = map(str, result)
            return render_template("result.html", filename=filename, station=station,
                                   path_clear=path_clear, lift_working=lift_working,
                                   readable_info=readable_info,
                                   c_path=c_path, c_lift=c_lift, c_read=c_read, t=t, lang=lang)

    upload_id = request.args.get("id")
    return render_template("questions.html", upload_id=upload_id, t=t, lang=lang)

# --- Ergebnisseite ---
@app.route("/result")
def result():
    lang = request.args.get("lang", "en")
    t = load_translations(lang)

    filename = request.args.get('filename')
    station = request.args.get('station')
    path_clear = request.args.get('path_clear')
    lift_working = request.args.get('lift_working')
    readable_info = request.args.get('readable_info')

    c_path = c_lift = c_read = "–"

    if not (path_clear and lift_working and readable_info):
        conn = sqlite3.connect("data/accessai.db")
        c = conn.cursor()
        c.execute("""SELECT path_clear, lift_working, readable_info,
                            confidence_path, confidence_lift, confidence_readable
                     FROM uploads
                     WHERE filename = ? AND station_name = ?
                     ORDER BY id DESC LIMIT 1""", (filename, station))
        result = c.fetchone()
        conn.close()

        if result:
            path_clear, lift_working, readable_info, c_path, c_lift, c_read = map(str, result)

    return render_template("result.html", filename=filename, station=station,
                           path_clear=path_clear, lift_working=lift_working,
                           readable_info=readable_info,
                           c_path=c_path, c_lift=c_lift, c_read=c_read, t=t, lang=lang)

# --- Suchseite ---
@app.route("/search", methods=["GET"])
def search():
    lang = request.args.get("lang", "en")
    t = load_translations(lang)

    query = request.args.get("q")
    results = []
    if query:
        conn = sqlite3.connect("data/accessai.db")
        c = conn.cursor()
        c.execute("""
            SELECT station_name, filename, timestamp, path_clear, lift_working, readable_info
            FROM uploads
            WHERE station_name LIKE ?
            ORDER BY timestamp DESC
            LIMIT 10
        """, ('%' + query + '%',))
        results = c.fetchall()
        conn.close()
    return render_template("search.html", query=query, results=results, t=t, lang=lang)

# --- Autocomplete ---
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    term = request.args.get("term", "")
    suggestions = []
    if term:
        conn = sqlite3.connect("data/accessai.db")
        c = conn.cursor()
        c.execute("""
            SELECT DISTINCT station_name
            FROM uploads
            WHERE station_name LIKE ?
            ORDER BY station_name ASC
            LIMIT 8
        """, (term + '%',))
        suggestions = [row[0] for row in c.fetchall()]
        conn.close()
    return jsonify(suggestions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5050)