"""
 Main class, handles routing and communications between modules
"""
from flask import Flask, render_template, flash, redirect
from pokemon import AddPokemonForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '0123456789abcdef'  # Not very secret, but functional


@app.route('/')
@app.route('/menu')
def index():
    return render_template("index.html", content_header="Main menu")


@app.route('/pokemon')
def pokemon():
    return render_template("pokemon/index.html", content_header="Manage pokemon")

@app.route('/pokemon/new', methods=["get"])
def add_pokemon():
    form = AddPokemonForm()
    if form.validate_on_submit():
        flash("{{ form.name.data }} was added to the list!", "success")
    return render_template("pokemon/new.html", content_header="Add new pokemon", form=form)


@app.route('/fight')
def fight():
    return render_template("fight.html")


if __name__ == "__main__":
    app.run(debug=True)
