# Setup instuctions for Flask in Visual Studio Code
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
from lib.sudoku_solver import sudoku_solver 

app = Flask(__name__)

sudokus = [
     {"title": "Sample Sudoku #1",
     "board": "000260701680070090190004500820100040004602900050003028009300074040050036703018000"},
    {"title": "Sample Sudoku #2",
     "board": "000000000302540000050301070000000004409006005023054790000000050700810000080060009"},
    {"title": "Sample Suduko #3",
     "board": "530070000600195000098000060800060003400803001700020006060000280000419005000080079"},
]

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", sudokus = sudokus) 

@app.route('/solver', methods=['GET', 'POST'])
def solver():  
    try:
        sudoku_string = request.form['board'] 
        sudoku_number = request.form['sudoko_number']
    except:
        return render_template("index.html", sudokus = sudokus)

    try:
        solution_feedback = sudoku_solver(sudoku_string).split()
        solved_sudoku = solution_feedback[0]
        if solution_feedback[1] == "BTS":
            solution_method = "Arc Consistency Algorithm #3 & Backtracking Search"
        else: 
            solution_method = "Arc Consistency Algorithm #3"

        return render_template(
            'index.html',
            return_from_solver = True,
            is_solvable = True, 
            solved_sudoku = solved_sudoku,
            sudoku_string = sudoku_string,
            sudoku_number = sudoku_number,
            sudokus = sudokus,
            solution_method = solution_method
        )        
    except:
        return render_template(
            'index.html',
            return_from_solver = True,
            is_solvable = False, 
            sudoku_string = sudoku_string,
            sudoku_number = sudoku_number,
            sudokus = sudokus
        )
        
if __name__ == "__main__":
    app.run(debug=True)