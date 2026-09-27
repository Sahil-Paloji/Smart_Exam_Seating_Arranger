from flask import Flask, render_template, request, jsonify
import subprocess
from pathlib import Path

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

C_PROGRAM = Path(__file__).resolve().parent / "seating"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    try:
        n = int(data.get("gridSize", 0))
        subjects = data.get("subjects", [])
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid input."
        }), 400

    if not 1 <= n <= 10:
        return jsonify({
            "success": False,
            "message": "Grid size must be between 1 and 10."
        }), 400

    if not isinstance(subjects, list) or not 1 <= len(subjects) <= 10:
        return jsonify({
            "success": False,
            "message": "Enter between 1 and 10 subjects."
        }), 400

    cleaned = []
    total = 0

    for item in subjects:
        if not isinstance(item, dict):
            return jsonify({
                "success": False,
                "message": "Invalid subject details."
            }), 400

        name = str(item.get("name", "")).strip()

        try:
            count = int(item.get("students", 0))
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Student count must be a whole number."
            }), 400

        if not name:
            return jsonify({
                "success": False,
                "message": "Every subject needs a name."
            }), 400

        if count < 0:
            return jsonify({
                "success": False,
                "message": "Student count cannot be negative."
            }), 400

        cleaned.append({
            "name": name,
            "students": count
        })

        total += count

    if total > n * n:
        return jsonify({
            "success": False,
            "message": f"{total} students cannot fit in {n*n} seats."
        }), 400

    c_input = f"{n} {len(cleaned)}\n"

    for subject in cleaned:
        c_input += f"{subject['students']}\n"

    try:
        result = subprocess.run(
            [str(C_PROGRAM)],
            input=c_input,
            capture_output=True,
            text=True,
            timeout=60,
            check=False
        )

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "message": "The calculation took too long. Try smaller student counts."
        }), 500

    except OSError:
        return jsonify({
            "success": False,
            "message": "C program not found. Compile seating.c first."
        }), 500

    if result.returncode != 0:
        return jsonify({
            "success": False,
            "message": "The C program encountered an error."
        }), 500

    output = result.stdout.strip().split()

    if not output:
        return jsonify({
            "success": False,
            "message": "The C program returned no output."
        }), 500

    if output[0] == "NO":
        return jsonify({
            "success": False,
            "message": "No valid arrangement found. Try different counts or a larger grid."
        })

    if output[0] != "OK":
        return jsonify({
            "success": False,
            "message": "Unexpected output from the C program."
        }), 500

    try:
        values = list(map(int, output[1:]))
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid seating data returned by C."
        }), 500

    if len(values) != n * n:
        return jsonify({
            "success": False,
            "message": "The C program returned an incomplete seating grid."
        }), 500

    grid = [
        values[i * n:(i + 1) * n]
        for i in range(n)
    ]

    codes = []

    for i, subject in enumerate(cleaned):
        words = subject["name"].split()
        code = "".join(word[0] for word in words[:3]).upper()

        if not code:
            code = f"S{i + 1}"

        codes.append(code[:5])

    return jsonify({
        "success": True,
        "grid": grid,
        "subjects": [
            {
                "name": cleaned[i]["name"],
                "students": cleaned[i]["students"],
                "code": codes[i]
            }
            for i in range(len(cleaned))
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)
