# Smart Exam Seating Arranger

A web interface for the DAA capstone project. It uses recursive backtracking to place subjects in an N×N grid so that the same subject is not immediately adjacent horizontally, vertically, or diagonally.

## Folder structure

Smart_Exam_Seating_Arranger/
- backend/app.py
- backend/solver.py
- frontend/templates/index.html
- frontend/static/style.css
- frontend/static/script.js
- README.md

## Install

Use Python 3.

    pip install flask

## Run

From the project folder:

    cd backend
    python app.py

Open:

    http://127.0.0.1:5000

## Example

5×5 grid:

Innovation and Creativity: 7
Accounts: 6
Emerging Trends in Technology: 6
BEC: 6

Total = 25 students.

The website also accepts a different number of subjects, from 1 to 10.

## Viva explanation

The C/algorithmic idea is preserved in `solver.py`:

1. Select the next empty seat.
2. Try each subject with students remaining.
3. Check the eight neighboring seats.
4. Place the subject if safe.
5. Recursively continue.
6. If the choice leads to a dead end, undo it and try another subject.

This is a backtracking approach adapted from the constraint-solving idea used in N-Queens; it is not the standard N-Queens problem itself.
