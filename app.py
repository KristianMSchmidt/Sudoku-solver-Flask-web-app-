# Setup instuctions for Flask in Visual Studio Code
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
from random import choice as random_choice
from python.sudoku_algorithm import sudoku_solver 
import copy
app = Flask(__name__)

# Import sudoku collection from text-file
with open("python/sudokus_start.txt") as all_sudokus:
    sudokus = list(map(lambda s: s.strip(), all_sudokus))

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        # User has requested a custom sudoku
        request.form['custom']
        empty_sudoku = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        return render_template("index.html", title="Your Sudoku", sudoku = empty_sudoku) 
    except: 
        # User has requested a sample sudoku
        sample_number = random_choice(range(400))
        sample_sudoku = sudokus[sample_number]
        title = "Sample Sudoku #" + str(sample_number)
        return render_template("index.html", title=title, sudoku = sample_sudoku) 

@app.route('/solver', methods=['GET', 'POST'])
def solver():  
    try:
        sudoku = request.form['sudoku']
        title = request.form['title'] 
    except:
        #If user tries to acces this page without form submission, return the user to index page
        sample_number = random_choice(range(400))
        sample_sudoku = sudokus[sample_number]
        title = "Sample Sudoku #" + str(sample_number)
        return render_template("index.html", title=title, sudoku = sample_sudoku) 
    try:
        # Sudoku is solvable
        solution_feedback = sudoku_solver(sudoku).split()
        solved_sudoku = solution_feedback[0]
        if solution_feedback[1] == "BTS":
            solution_method = "Backtracking Search"
        else: 
            solution_method = "Arc Consistency #3 Algorithm"

        return render_template(
            'index.html',
            title=title,
            sudoku = sudoku,
            return_from_solver = True,
            is_solvable = True, 
            solved_sudoku = solved_sudoku,
            solution_method = solution_method
        )        
    except:
        #Sudoku is not solvable
        return render_template(
            'index.html',
            return_from_solver = True,
            is_solvable = False,
            title=title, 
            sudoku = sudoku, 
        )
        
if __name__ == "__main__":
    app.run(debug=True)