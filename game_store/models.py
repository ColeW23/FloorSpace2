from sqlalchemy import CheckConstraint, UniqueConstraint

from game_store import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Tenant.query.get(int(user_id))


class Tenant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    build_id = db.Column(db.Integer, nullable=False)
    tenant_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "room_id", "build_id"),
    )

    def __init__(self, room_number, build_number, username, email, password):
        self.room_id = room_number
        self.build_id = build_number
        self.tenant_name = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Customer('{self.tenant_name}', '{self.email}')"


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)


db.drop_all()
db.create_all()
Tenants = [
    # Game(game_name="Assassin's Creed", genre="action-adventure", release_date=datetime.date(2007, 11, 13), price=10.00,
    #      publisher_id=1),

]

# db.session.bulk_save_objects(games)
# db.session.commit()

# Admins


# db.session.bulk_save_objects(publishers)
# db.session.commit()

# Tickets

# db.session.bulk_save_objects(platforms)
# db.session.commit()



