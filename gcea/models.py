from gcea import app, db

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defence = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"#{self.id} {self.name}: HP={self.hp}, ATK={self.attack}, DEF={self.defence}, SPD={self.speed}"


with app.app_context():
    db.create_all()
