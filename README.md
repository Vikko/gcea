# GoCEA

Gotta Catch Em All! A simple (but flawed) pokemon game, hacked together in a short time. 
Main goal here was to get some experience with Python Flask and it's workings. The package includes a main menu 
to Start a fight, continue an ongoing fight (stored in cookies) or manage the list of available pokemon.

## Dependencies
Different library versions have not been thoroughly tested, but it runs on the following:
```
python 3.9
Flask 2.2.2
Flask-SQLAlchemy 3.0.3
Flask-WTF 1.1.1
```

## Usage
The flask server is started by running `app.py` in the root of the folder. The game is developed as a module in the 
folder `gcea`.

When the server runs, it is hosted at [localhost](http://localhost:5000), where the root is the main menu.
Bootstrap is loaded from a CDN, so an internet connection is required!

## Future development
The goal, breakdown of tasks and features is listed in FEATURES.md. This also includes some features or 'nice-to-haves'
that were ideas case I would continue this work. 

## License
[MIT](https://choosealicense.com/licenses/mit/)