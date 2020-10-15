# Setup instuctions
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
from lib.format import format_sudoku_string as format
from lib.sudoku_solver import sudoku_solver 

app = Flask(__name__)

sample_sudokus = [
     {"title": "Sample Sudoku #1",
     "board": "000260701680070090190004500820100040004602900050003028009300074040050036703018000"},
    {"title": "Sample Sudoku #2",
     "board": "000000000302540000050301070000000004409006005023054790000000050700810000080060009"},
    {"title": "Your Sudoku",
     "board": ""}
]

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", sample_sudokus = sample_sudokus) 

@app.route('/solver', methods=['GET', 'POST'])
def solver():  
    try:
        sudoku_string = request.form['board'] 
        sudoku_number = request.form['sudoko_number']
    except:
        return render_template("index.html", sample_sudokus = sample_sudokus)

    try:
        solved_sudoku = sudoku_solver(sudoku_string).split(" ")[0]
        return render_template(
            'index.html',
            return_from_solver = True,
            is_solvable = True, 
            solved_sudoku = solved_sudoku,
            sudoku_string = sudoku_string,
            sudoku_number = sudoku_number,
            sample_sudokus = sample_sudokus
        )        
    except:
        return render_template(
            'index.html',
            return_from_solver = True,
            is_solvable = False, 
            sudoku_string = sudoku_string,
            sudoku_number = sudoku_number,
            sample_sudokus = sample_sudokus
        )
        
if __name__ == "__main__":
    app.run(debug=True)