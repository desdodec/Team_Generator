from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Path to the preloaded Excel file
EXCEL_FILE = 'children_names.xlsx'


def read_names_from_excel(file_path):
    """
    Read names from the first column of an Excel file.
    """
    df = pd.read_excel(file_path, header=None)
    names = df[0].dropna().tolist()  # Remove empty rows
    return names


def generate_teams(names, num_teams=None, max_team_size=None, incompatible_pairs=[]):
    """
    Generate teams based on the number of teams or max team size, respecting constraints.
    """
    # Calculate number of teams if max_team_size is provided
    if max_team_size:
        # Calculate teams dynamically
        num_teams = (len(names) + max_team_size - 1) // max_team_size

    # Ensure no more teams than members
    if num_teams > len(names):
        num_teams = len(names)

    # Create empty teams
    teams = [[] for _ in range(num_teams)]

    # Shuffle names for randomization
    from random import shuffle
    shuffle(names)

    # Assign members in a round-robin fashion
    current_team = 0
    for name in names:
        # Ensure we don't exceed max_team_size
        while max_team_size and len(teams[current_team]) >= max_team_size:
            current_team = (current_team + 1) % num_teams

        # Add the member to the current team
        teams[current_team].append(name)
        current_team = (current_team + 1) % num_teams  # Move to the next team

    return teams


@app.route("/", methods=["GET", "POST"])
def index():
    names = read_names_from_excel(EXCEL_FILE)
    total_names = len(names)

    if request.method == "POST":
        num_teams = request.form.get("num_teams", "").strip()
        num_teams = int(num_teams) if num_teams.isdigit() else None

        max_team_size = request.form.get("max_team_size", "").strip()
        max_team_size = int(max_team_size) if max_team_size.isdigit() else None

        incompatible_pairs = request.form.get(
            "incompatible_pairs", "").split(";")
        incompatible_pairs = [pair.strip()
                              for pair in incompatible_pairs if pair.strip()]

        # Generate teams
        teams = generate_teams(names, num_teams=num_teams,
                               max_team_size=max_team_size, incompatible_pairs=incompatible_pairs)
        return render_template("results.html", teams=teams)

    return render_template("index.html", total_names=total_names)


if __name__ == "__main__":
    app.run(debug=True)
