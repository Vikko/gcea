"""
 This game engine class will do some calculations on fights and determine a winner.
"""
from random import random, randrange, seed
from gcea.models import Pokemon

SPEEDCAP = 100  #


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
        """
        Serialize object to a dict to store in a session
        """
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
        """
        Update stats relevant for battle after swapping current pokemon
        """
        pokemon = Pokemon.query.get(pokemon_id)
        self.current = pokemon
        self.current_hp = pokemon.hp

    def get_stats(self):
        """
        Get stats of both pokemon in battle
        """
        return {
            'current_name': self.current.name,
            'opponent_name': self.opponent.name,
            'current_hp': [self.current_hp, self.current.hp],
            'opponent_hp': [self.opponent_hp, self.opponent.hp],
            'current_ADS': [self.current.attack,self.current.defence,self.current.speed],
            'opponent_ADS': [self.opponent.attack, self.opponent.defence, self.opponent.speed]
        }

    def next_turn(self, events=None, after_me=False):
        """
        Determine considering the time in battle and speed who's turn it is and call the opponents actions.
        Returns set of events that happened between current and next turn
        """

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
            # If opponent is next or at the same turn and I already had my turn
            if next_op < next_me or (next_op == next_me and after_me):
                self.time += int(next_op)
                events.append(self.opponent_turn())
                # Recursive call in case of multiple turns before own turn
                events = self.next_turn(events)
            elif next_op > next_me:
                # If I am is next
                self.time += int(next_me)
        return events

    def opponent_turn(self):
        """
        When the opponent has a turn, it always attacks
        Returns the attack event.
        """
        dmg = calculate_attack(self.opponent.attack, self.current.defence)
        event = [self.time, "", f"{self.opponent.name} hits your {self.current.name} for {dmg}."]
        self.current_hp -= dmg
        if self.current_hp <= 0:
            event[1] = "Oh no! It seems you ran out of hitpoints. You lose :("
        return event

    def my_turn(self):
        """
        On my turn, if not swapping or forfeiting the fight, attack the opponent.
        After my turn, calls for the next turn(s) to be determined.
        Returns events between my current and my next turn
        """
        if self.opponent_hp <= 0 or self.current_hp <= 0:
            return []
        dmg = calculate_attack(self.current.attack, self.opponent.defence)
        new_events = []
        event = [self.time, f"Your {self.current.name} hits {self.opponent.name} for {dmg}.",""]
        new_events.append(event)
        self.opponent_hp -= dmg
        if self.opponent_hp <= 0:
            event[2] = f"Good job! You manage to beat {self.opponent.name}. Congratulations! :)"
        new_events = self.next_turn(new_events, after_me=True)
        self.add_events(new_events)
        return new_events
    def add_events(self, events):
        """
        Adds a list of events to to the instance or initializes a new array
        """
        if self.events is None:
            self.events = []
        for event in events:
            self.events.append(event)

    def get_events(self):
        """
        Returns all events stored in the instance
        """
        return self.events

def calculate_attack(atk, dfc):
    """
    Damage calculation considering attack and defence power.
    Returns damage (int)
    """
    lo_dmg = int((atk - dfc)/4)
    # Make sure low bound is at least 1
    lo_dmg = max(lo_dmg, 1)
    hi_dmg = int(atk/4)
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
