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

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html") 

@app.route('/show', methods=['GET', 'POST'])
def show():

    try:
        sudoku_string = request.form['board'] 
        sudoku_title = request.form['sudoku_title']

    except:
        return render_template("index.html")

    if not (len(sudoku_string) == 81 and sudoku_string.isdigit()):
    
        return render_template(
            'index.html', 
            error = "Sudoku must be a 81 character string containing only digits" ,
            sudoku_string = sudoku_string
        )

    return render_template(
        'index.html', 
        sudoku_string = format(sudoku_string),
        sudoku_title = sudoku_title,
        show = True
    )

@app.route('/solver', methods=['POST'])
def solver():
  
    sudoku_string = request.form['board']  

    if not (len(sudoku_string) == 81 and sudoku_string.isdigit()):
        return render_template(
            'index.html', 
            error = "Sudoku must be a 81 character string containing only digits" ,
            sudoku_string = sudoku_string
        )

    try:
        solved_sudoku = sudoku_solver(sudoku_string)
        return render_template(
            'index.html', 
            solved_sudoku = solved_sudoku,
            sudoku_string = sudoku_string)
        
    except:
        return render_template(
            'index.html', 
            error = "Sudoku not solvable",
            sudoku_string = sudoku_string
        )
        

if __name__ == "__main__":
    app.run(debug=True)