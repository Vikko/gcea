"""
 This game engine class will do some calculations on fights and determine a winner.
"""
from random import random, randrange, seed
from gcea.models import Pokemon

SPEEDCAP = 200  #


class Engine():
    def __init__(self, current_id, opponent_id, time=1, seed_token=None, current_hp=None, opponent_hp=None, events=None):
        # Get pokemon objects
        self.current = Pokemon.query.get(current_id)
        self.opponent = Pokemon.query.get(opponent_id)
        # Set or intialize HP
        if current_hp == None:
            self.current_hp = self.current.hp
        else:
            self.current_hp = current_hp
        if opponent_hp == None:
            self.opponent_hp = self.opponent.hp
        else:
            self.opponent_hp = opponent_hp
        # Set or initialize seed token
        self.seed_token = seed_token
        if self.seed_token == None:
            self.seed_token = seed()
        # Set or initialize Events
        self.events = events
        # Set or initialize time counter
        self.time = time

    def to_dict(self):
        return {
            'time': self.time,
            'current_id': self.current.id,
            'opponent_id': self.opponent.id,
            'seed_token': self.seed_token,
            'current_hp': self.current_hp,
            'opponent_hp': self.opponent_hp,
            'events': self.events
        }

    def update_current(self, pokemon_id):
        pokemon = Pokemon.query.get(pokemon_id)
        self.current = pokemon
        self.current_hp = pokemon.hp

    def get_stats(self):
        return {
            'current_name': self.current.name,
            'opponent_name': self.opponent.name,
            'current_hp': [self.current_hp, self.current.hp],
            'opponent_hp': [self.opponent_hp, self.opponent.hp],
            'current_ADS': [self.current.attack,self.current.defence,self.current.speed],
            'opponent_ADS': [self.opponent.attack, self.opponent.defence, self.opponent.speed]
        }

    def next_turn(self, events=None):
        #Setup events in case of non-recursive call
        if events is None:
            events = []
        # Check for death
        if self.current_hp > 0 and self.opponent_hp > 0:
            max_speed = 1.5*SPEEDCAP
            # Determine the next turn
            me = (max_speed - self.current.speed)

            op = (max_speed - self.opponent.speed)
            next_me = me - self.time % me
            next_op = op - self.time % op
            # Bugfix: When me is 0 (for instance refresh on your turn), it is reset to maximum due to the modulo
            if me == next_me:
                next_me = 0
            # If opponent is next
            if next_op < next_me:
                events.append(self.opponent_turn())
                self.time += next_op
                events = self.next_turn(events)  # Recursive call in case of multiple turns before own turn
            else:
            # If I am is next
                self.time += next_me
        return events

    def opponent_turn(self):
        dmg = calculate_attack(self.opponent.attack, self.current.defence)
        event = [self.time, "", f"{self.opponent.name} hits your {self.current.name} for {dmg}."]
        self.current_hp -= dmg
        if self.current_hp <= 0:
            event[1] = "Oh no! It seems you ran out of hitpoints. You lose :("
        return event

    def my_turn(self):
        dmg = calculate_attack(self.current.attack, self.opponent.defence)
        new_events = []
        event = [self.time, f"Your {self.current.name} hits {self.opponent.name} for {dmg}.",""]
        new_events.append(event)
        self.opponent_hp -= dmg
        if self.opponent_hp <= 0:
            event[2] = f"Good job! You manage to beat {self.opponent.name}. Congratulations! :)"
        new_events = self.next_turn(new_events)
        self.add_events(new_events)
        return new_events
    def add_events(self, events):
        if self.events is None:
            self.events = []
        for event in events:
            self.events.append(event)

    def get_events(self):
        return self.events

def calculate_attack(atk, dfc):
    lo_dmg = atk - dfc
    # Make sure low bound is at least 1
    lo_dmg = max(lo_dmg, 1)
    hi_dmg = atk
    dmg = 0
    if random() < (atk / (atk + dfc)):
        # Attack success
        dmg = randrange(lo_dmg, hi_dmg)
        if random() >= 0.95:
            dmg = dmg + randrange(lo_dmg, hi_dmg)
    else:
        # Defence success
        dmg = randrange(0, lo_dmg)
        if random() < 0.05:
            dmg = dmg + randrange(0, lo_dmg)
    return dmg
