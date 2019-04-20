from sqlalchemy import CheckConstraint, UniqueConstraint

from game_store import db, login_manager, bcrypt
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Tenant.query.get(int(user_id))


ACCESS = {
    'guest': 0,
    'tenant': 1,
    'admin': 2
}

class Tenant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.Integer, nullable=False)

    def __init__(self, username, email, password, access=ACCESS['tenant']):
        self.name = username
        self.email = email
        self.password = password
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level

    def __repr__(self):
        return f"Customer('{self.name}', '{self.email}')"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_email = db.Column(db.String(120), db.ForeignKey("tenant.email"))
    room_id = db.Column(db.Integer, nullable=False)
    build_id = db.Column(db.Integer, nullable=False)
    mtype = db.Column(db.String(40), nullable=False)
    submitdate = db.Column(db.Date, nullable=False)
    resolvedate = db.Column(db.Date)
    description = db.Column(db.String(720), nullable=False)

    def __init__(self, email, room_id, build_id, mtype, description, submitdate, resolvedate):
        self.tenant_email=email
        self.room_id=room_id
        self.build_id=build_id
        self.mtype=mtype
        self.description=description
        self.submitdate=submitdate
        self.resolvedate=resolvedate



db.drop_all()
db.create_all()

# Admin login
hashed_password = bcrypt.generate_password_hash('Test').decode('utf-8')
Admin1 = Tenant(email="Admin1@gmail.com", username="Admin1", password=hashed_password, access=2)

db.session.add(Admin1)
db.session.commit()

# Tenant login
TestTenant = Tenant('cole', 'williamson.cole23@gmail.com', 'cunt', access=1)

db.session.add(TestTenant)
db.session.commit()

# Tickets
Ticket1 = Ticket('williamson.cole23@gmail.com', room_id=406, build_id=1, mtype='repair', description='my fucking toilet broke', submitdate=datetime.date(2018, 4, 20), resolvedate=datetime.date(2000, 1, 10))

db.session.add(Ticket1)
db.session.commit()





