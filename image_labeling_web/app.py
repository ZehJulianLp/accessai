from flask import Flask, render_template, request, redirect, url_for
import os
import json
import shutil
import random

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "images", "training_images")
DELETED_FOLDER = os.path.join(BASE_DIR, "static", "images", "deleted_images")
LABEL_FILE = os.path.join(BASE_DIR, "training_labels.json")

# Sicherstellen, dass Ordner existieren
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(DELETED_FOLDER, exist_ok=True)

# Lade existierende Labels oder leeres Dict
if os.path.exists(LABEL_FILE):
    with open(LABEL_FILE, "r") as f:
        labels = json.load(f)
else:
    labels = {}

# Lade verfügbare, noch nicht gelabelte Bilder in zufälliger Reihenfolge
def get_images():
    all_images = [
        img for img in os.listdir(IMAGE_FOLDER)
        if img.lower().endswith((".png", ".jpg", ".jpeg")) and img not in labels
    ]
    random.shuffle(all_images)
    return all_images

@app.route("/", methods=["GET", "POST"])
def index():
    images = get_images()
    if not images:
        return "✅ All images labeled or deleted!"

    if request.method == "POST":
        filename = request.form["filename"]
        action = request.form.get("action")

        image_path = os.path.join(IMAGE_FOLDER, filename)
        target_path = os.path.join(DELETED_FOLDER, filename)

        if action == "delete":
            if os.path.exists(image_path):
                shutil.move(image_path, target_path)
                print(f"🗑️ Moved to deleted: {filename}")

            if filename in labels:
                del labels[filename]
                with open(LABEL_FILE, "w") as f:
                    json.dump(labels, f, indent=2)

            return redirect(url_for("index"))

        # Speichern
        labels[filename] = {
            "step_free_access": int("step_free_access" in request.form),
            "clear_path": int("clear_path" in request.form),
            "readable_timetable": int("readable_timetable" in request.form)
        }
        with open(LABEL_FILE, "w") as f:
            json.dump(labels, f, indent=2)

        return redirect(url_for("index"))

    # GET
    current_img = request.args.get("img")
    images = get_images()
    if current_img and current_img in images:
        selected_img = current_img
    elif images:
        selected_img = images[0]
    else:
        return "✅ All images labeled or deleted!"

    return render_template("index.html", filename=selected_img)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
