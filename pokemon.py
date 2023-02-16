"""
 Storage class to handle everything related to pokemon properties and their storage.
"""
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import DataRequired, Length

class AddPokemonForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(),Length(min=3,max=20)])
    hp = IntegerField('Hitpoints',
                        validators=[DataRequired(), Length(min=1, max=255)])
    attack = IntegerField('AttackPower',
                        validators=[DataRequired(),Length(min=5,max=250)])
    defence = IntegerField('DefensePower',
                        validators=[DataRequired(),Length(min=5,max=250)])
    speed = IntegerField('Speed',
                        validators=[DataRequired(), Length(min=5, max=200)])