# Setup instuctions
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/home")
@app.route("/")
def index():
    return render_template("index.html") 


if __name__ == "__main__":
    app.run(debug=True)