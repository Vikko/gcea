from random import choice
from flask import render_template, flash, redirect, url_for, session, jsonify

from gcea import app, db
from gcea.engine import Engine
from gcea.models import Pokemon
from gcea.forms import PostPokemonForm, PickPokemonForm

@app.route('/')
@app.route('/menu')
def index():
    """
    Main menu
    """
    return render_template("index.html", content_header="Main menu")


@app.route('/pokemon')
def pokemon():
    """
    List all pokemon
    """
    pokemons = Pokemon.query.all()
    return render_template("pokemon/index.html", content_header="Manage pokemon", pokemons=pokemons)


@app.route('/pokemon/new', methods=["GET", "POST"])
def add_pokemon():
    """
    Add a pokemon to the database"
    """
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
    """
    Update stats of a pokemon in the database
    """
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
    """
    Remove a pokemon from the database
    """
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect(url_for("pokemon"))

@app.route("/pokemon/pick", methods=['GET','POST'])
def pick_pokemon():
    """
    Select a pokemon to fight with
    """
    pokemons = Pokemon.query.all()
    poke_list = [(p.id, p.name) for p in pokemons]
    form = PickPokemonForm()
    form.pick.choices = poke_list
    if form.validate_on_submit():
        session['current_pokemon'] = form.pick.data
        if form.set_main.data == True:
            session['main_pokemon'] = session['current_pokemon']
        if 'fight' in session and session['fight'] != None:
            # Reset HP and redirect to fight
            p = Pokemon.query.get(session['current_pokemon'])
            session['fight']['current_id'] = p.id
            session['fight']['current_hp'] = p.hp
            return redirect(url_for('fight'))
        else:
            # Redirect to main menu
            return redirect(url_for('index'))
    return render_template('pokemon/pick.html', form=form, legend="Pick a pokemon")


@app.route('/new_fight')
def new_fight():
    """
    Initiate a new fight
    """
    session['fight'] = None
    session['opponent'] = None
    session['current_pokemon'] = session['main_pokemon']
    return redirect(url_for('fight'))

@app.route('/fight')
def fight():
    """
    Initiate a new fight or return to the current fight
    """
    # Set pokemon for current fight, pick one if none is set
    if 'current_pokemon' not in session or session['current_pokemon'] is None:
        if 'main_pokemon' in session:
            session['current_pokemon'] = session['main_pokemon']
        else:
            return redirect(url_for('pick_pokemon'))
    # Pick opponent (random for now)
    if 'opponent' not in session or session['opponent'] is None:
        session['opponent'] = choice(Pokemon.query.all()).id
    # Setup fight object if not started
    if 'fight' not in session or session['fight'] is None:
        session['fight'] = Engine(session['current_pokemon'], session['opponent']).to_dict()
    fight = Engine(**session['fight'])
    fight.add_events(fight.next_turn())
    stats = fight.get_stats()
    session['fight'] = fight.to_dict()
    events = fight.get_events()
    return render_template("fight.html", legend="Fight!", engine=fight, stats=stats, events=events)

@app.route('/fight/forfeit')
def forfeit():
    session['fight'] = None
    session['opponent'] = None
    return redirect(url_for('index'))

@app.route('/fight/attack')
def attack():
    fight = Engine(**session['fight'])
    new_events = fight.my_turn()
    stats = fight.get_stats()
    session['fight'] = fight.to_dict()
    return jsonify({
        'events': new_events,
        'current_hp': stats['current_hp'],
        'opponent_hp': stats['opponent_hp']
    })