from flask import render_template, url_for, flash, redirect, request

from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, TicketSearchForm, TicketSubmit, AdminTickSubmit
from game_store.models import Tenant, Ticket
from flask_login import login_user, current_user, logout_user, login_required
import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Tenant(username=form.username.data, email=form.email.data, password=hashed_password, access='tenant')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Tenant.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_admin():
                return redirect(url_for('employee'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/employee")
def employee():
    return render_template('employee.html', title="Welcome")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/tickets")
def tickets():
    ticketdata = Ticket.query.all()
    return render_template('tickets.html', ticketdata=ticketdata)


@app.route("/ticket_submit", methods=['GET', 'POST'])
def ticket_submit():
    form = TicketSubmit()
    if form.validate_on_submit():
        tick = Ticket(email=current_user.email, room_id=form.room_number.data, build_id=form.building_number.data, description=form.description.data, submitdate=datetime.datetime.now(), mtype=form.maint_type.data, resolvedate=None)
        db.session.add(tick)
        db.session.commit()
        flash("Ticket was submitted successfully!", 'success')
        return redirect(url_for('account'))

    return render_template('ticket_submit.html', form=form)


@app.route("/admin_submit/<ticket_id>", methods=['GET', 'POST'])
def admin_submit(ticket_id):
    form = AdminTickSubmit()
    flash("Ticket id = "+ticket_id, 'warning')
    the_ticket = Ticket.query.filter_by(id=ticket_id).first()
    if form.validate_on_submit():
        the_ticket.description = form.description.data
        the_ticket.resolvedate = datetime.date.today()
        db.session.commit()
        flash("Ticket was resolved successfully", 'success')
        return redirect(url_for('account'))

    return render_template('admin_submit.html', form=form, ticket=the_ticket)


@app.route("/closed_tickets")
def closed_tickets():
    ticketdata = Ticket.query.all()
    return render_template('closed_tickets.html', ticketdata=ticketdata)