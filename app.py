  
# Setup instuctions for Flask in Visual Studio Code
# 1) Open folder with flask project
# 2) In therminal: "pip install flask" (if necessary)
# 3) In terminal: "python app.py"

from flask import Flask, render_template, request
from random import choice as random_choice
from backend.sudoku_algorithm import sudoku_solver 
import timeit, json

# Import collection of 400 sudokus from text-file
with open("backend/sudokus_start.txt") as all_sudokus:
    sudokus = list(map(lambda s: s.strip(), all_sudokus))

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        action = "new_sample"

    else: 
        data = json.loads(request.form["json_data"])   #return(json.dumps(data))
        action = data["requested_action"]
        sudoku = data["sudoku"]

    if action == 'new_sample':        
        sample_number = random_choice(range(400))
        sudoku = sudokus[sample_number]
        title = "Sample Sudoku #" + str(sample_number)
        data = {}
        data["requested_action"] = "new_sample"
        data["sudoku"] = sudoku
        data["title"] = title
    
    elif action == 'new_custom':
        empty_sudoku =  "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        data["sudoku"] = empty_sudoku
        data["title"]= "Your Sudoku"

    elif action == 'solve':

        try:
            starttime = timeit.default_timer()
            solution_feedback = sudoku_solver(sudoku).split() # returns error if sudoku not solvable
            data["solution_time"] = round(timeit.default_timer() - starttime,3)
            data["is_solvable"] = True
            data["solved_sudoku"] = solution_feedback[0]
            if solution_feedback[1] == "BTS":
                data["solution_method"] = "Backtracking Search"
            else: 
                data["solution_method"] = "Arc Consistency #3 Algorithm"

        except:
            data["is_solvable"] = False

    return render_template("index.html", data = data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
