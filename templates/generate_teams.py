import pandas as pd
import random
import os


def read_names_from_excel(file_path):
    """Read names from the first column of an Excel file."""
    df = pd.read_excel(file_path, header=None)
    return df[0].tolist()


def generate_teams(names, num_teams, incompatible_pairs):
    """Generate teams while respecting incompatible constraints."""
    random.shuffle(names)
    teams = [[] for _ in range(num_teams)]
    incompatibility_map = {}

    # Build incompatibility map
    for pair in incompatible_pairs:
        name1, name2 = pair.split(",")
        name1, name2 = name1.strip(), name2.strip()
        if name1 not in incompatibility_map:
            incompatibility_map[name1] = []
        if name2 not in incompatibility_map:
            incompatibility_map[name2] = []
        incompatibility_map[name1].append(name2)
        incompatibility_map[name2].append(name1)

    # Assign names to teams
    for name in names:
        placed = False

        for team in teams:
            if all(incompatibility_map.get(name, []).count(member) == 0 for member in team):
                team.append(name)
                placed = True
                break

        # If the name couldn't be placed, assign it to the smallest team
        if not placed:
            smallest_team = min(teams, key=len)
            smallest_team.append(name)

    return teams


def generate_html_output(teams, output_path="output.html"):
    """Generate an HTML file displaying the teams."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Teams</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .team { margin-bottom: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            h2 { color: #007BFF; }
        </style>
    </head>
    <body>
        <h1>Generated Teams</h1>
    """
    for i, team in enumerate(teams):
        html_content += f"<div class='team'><h2>Team {i + 1}</h2><ul>"
        for member in team:
            html_content += f"<li>{member}</li>"
        html_content += "</ul></div>"
    html_content += "</body></html>"

    with open(output_path, "w") as file:
        file.write(html_content)

    print(f"Teams generated and saved to {output_path}")


def main():
    # Configuration
    excel_file = "children_names.xlsx"  # The Excel file in the root directory
    if not os.path.exists(excel_file):
        print(f"File '{excel_file}' not found in the root directory.")
        return

    num_teams = int(input("Enter the number of teams: ").strip())
    incompatible_pairs_input = input(
        "Enter incompatible pairs (comma-separated, e.g., 'Alice,Bob Charlie,David'): ").strip()
    incompatible_pairs = [pair.strip()
                          for pair in incompatible_pairs_input.split()]

    # Read names
    names = read_names_from_excel(excel_file)

    # Generate teams
    teams = generate_teams(names, num_teams, incompatible_pairs)

    # Generate HTML output
    output_file = "teams_output.html"
    generate_html_output(teams, output_file)

    print(
        f"Open {os.path.abspath(output_file)} in your browser to view the results.")


if __name__ == "__main__":
    main()
