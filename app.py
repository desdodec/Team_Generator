import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import pandas as pd
import math
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_names_from_excel(file_path):
    df = pd.read_excel(file_path, header=None)
    return df[0].dropna().tolist()


def generate_teams(names, num_teams=None, max_team_size=None, incompatible_pairs=[]):
    if max_team_size:
        num_teams = math.ceil(len(names) / max_team_size)

    if num_teams > len(names):
        num_teams = len(names)

    teams = [[] for _ in range(num_teams)]
    random.shuffle(names)

    current_team = 0
    for name in names:
        while max_team_size and len(teams[current_team]) >= max_team_size:
            current_team = (current_team + 1) % num_teams
        teams[current_team].append(name)
        current_team = (current_team + 1) % num_teams

    return teams


@app.route("/", methods=["GET", "POST"])
def index():
    total_names = None
    error_message = None

    # Check if a file has already been uploaded
    if 'uploaded_file' in session:
        file_path = session['uploaded_file']
        if os.path.exists(file_path):
            names = read_names_from_excel(file_path)
            total_names = len(names)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "upload":
            # Handle file upload
            if 'file' in request.files and request.files['file'].filename != '':
                file = request.files['file']

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    # Store the uploaded file in the session
                    session['uploaded_file'] = file_path

                    names = read_names_from_excel(file_path)
                    total_names = len(names)
                    flash(
                        f"File uploaded successfully! {total_names} names loaded.")
                else:
                    flash("Invalid file type. Please upload a valid Excel file.")
            else:
                flash("No file selected. Please choose a file to upload.")

        elif action == "generate":
            # Handle team generation
            if 'uploaded_file' in session:
                file_path = session['uploaded_file']
                names = read_names_from_excel(file_path)

                # Process inputs
                num_teams = request.form.get("num_teams", "").strip()
                num_teams = int(num_teams) if num_teams.isdigit() else None

                max_team_size = request.form.get("max_team_size", "").strip()
                max_team_size = int(
                    max_team_size) if max_team_size.isdigit() else None

                incompatible_pairs = request.form.get(
                    "incompatible_pairs", "").split(";")
                incompatible_pairs = [pair.strip()
                                      for pair in incompatible_pairs if pair.strip()]

                if num_teams and max_team_size:
                    error_message = "Please fill only one field: Number of Teams or Maximum Team Size."
                elif not num_teams and not max_team_size:
                    error_message = "Please fill in either Number of Teams or Maximum Team Size."
                else:
                    teams = generate_teams(
                        names,
                        num_teams=num_teams,
                        max_team_size=max_team_size,
                        incompatible_pairs=incompatible_pairs
                    )
                    return render_template("results.html", teams=teams)
            else:
                flash("No file uploaded. Please upload a file first.")

    return render_template("index.html", total_names=total_names, error_message=error_message)


@app.route("/clear", methods=["GET"])
def clear_session():
    # Clear the uploaded file from the session
    session.pop('uploaded_file', None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
