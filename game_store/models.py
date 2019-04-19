from sqlalchemy import CheckConstraint, UniqueConstraint

from game_store import db, login_manager, bcrypt
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
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, email, name, password):
        self.email  = email
        self.name = name
        self.password = password

db.drop_all()
db.create_all()

# Admin login
hashed_password = bcrypt.generate_password_hash('Test').decode('utf-8')
Admin1 = Admin(email="Admin1@gmail.com", name="Admin", password=hashed_password)

db.session.add(Admin1)
db.session.commit()

# Tickets

# db.session.bulk_save_objects(platforms)
# db.session.commit()



