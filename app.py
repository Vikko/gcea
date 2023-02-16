'''
 Main class, handles routing and communications between modules
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/menu')
def index():
    return render_template("index.html")

@app.route('/fight')
def index():
    return render_template("fight.html")

if __name__ == "__main__":
    app.run(debug=True)