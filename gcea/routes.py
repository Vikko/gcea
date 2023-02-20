from flask import render_template, flash, redirect, url_for, request
from gcea import app, db
from gcea.models import Pokemon
from gcea.forms import PostPokemonForm

@app.route('/')
@app.route('/menu')
def index():
    return render_template("index.html", content_header="Main menu")


@app.route('/pokemon')
def pokemon():
    pokemons = Pokemon.query.all()
    return render_template("pokemon/index.html", content_header="Manage pokemon", pokemons=pokemons)


@app.route('/pokemon/new', methods=["GET", "POST"])
def add_pokemon():
    form = PostPokemonForm()
    if form.validate_on_submit():
        pokemon = Pokemon(name=form.name.data, hp=form.hp.data, attack=form.attack.data, defence=form.defence.data, speed=form.speed.data)
        db.session.add(pokemon)
        db.session.commit()
        flash(f"{form.name.data} was added to the list!", "success")
        return redirect(url_for('pokemon'))
    return render_template("pokemon/form.html", content_header="Add new pokemon", form=form, legend="Add new pokemon")

@app.route("/pokemon/<int:pokemon_id>/update", methods=['GET', 'POST'])
def update_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    form = PostPokemonForm(obj=pokemon)
    if form.validate_on_submit():
        pokemon.name = form.name.data
        pokemon.hp = form.hp.data
        pokemon.attack = form.attack.data
        pokemon.defence = form.defence.data
        pokemon.speed = form.speed.data
        db.session.commit()
        flash('Your pokemon has been updated!', 'success')
        return redirect(url_for('pokemon'))
    return render_template("pokemon/form.html", content_header="Update pokemon", form=form, legend="Update pokemon")

@app.route("/pokemon/<int:pokemon_id>", methods=['POST'])
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect(url_for("pokemon"))

@app.route('/fight')
def fight():
    return render_template("fight.html")
