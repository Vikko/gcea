"""
 Logic to handle everything related to pokemon properties and their storage.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from gcea.models import Pokemon


class PostPokemonForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=3, max=20)])
    hp = IntegerField('Hitpoints',
                      validators=[DataRequired(), NumberRange(min=1, max=255)])
    attack = IntegerField('AttackPower',
                          validators=[DataRequired(), NumberRange(min=5, max=250)])
    defence = IntegerField('DefensePower',
                           validators=[DataRequired(), NumberRange(min=5, max=250)])
    speed = IntegerField('Speed',
                         validators=[DataRequired(), NumberRange(min=5, max=200)])
    submit = SubmitField("Add pokemon")

    def validate_name(self, name):
        pokemon = Pokemon.query.filter_by(name=name.data).first()
        if pokemon:
            raise ValidationError('A pokemon with that name is already in the database.')