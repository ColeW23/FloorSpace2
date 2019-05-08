from flask import render_template, url_for, flash, redirect, request

from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, TicketSearchForm, TicketSubmit, AdminTickSubmit
from game_store.models import Tenant, Ticket
from flask_login import login_user, current_user, logout_user, login_required
import datetime


# Renders the home.html template
@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')


# Renders the about.html template
@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Register route
# Loads the Registration Form
# Checks if current user is authenticated
# Checks the validity of all fields on submit. If valid, adds user information to the database.
# Redirects to login after successful registration
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


# Login route
# Loads the Login Form
# If the fields are valid, checks if password matches, and redirects to next.
# If the user is an admin, redirects to employee template
# Otherwise, redirects to account template.
# If invalid, flashes an unsuccessful message.
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Tenant.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.is_admin():
                flash("Employee Login Successful!", 'success')
                return redirect(next_page) if next_page else redirect(url_for('account'))
            else:
                flash("Tenant Login Successful!", 'success')
                return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Logs the user our and renders home.html template
@app.route("/logout")
def logout():
    logout_user()
    flash("Logout Successful", 'danger')
    return redirect(url_for('home'))


# Renders template for account.html. Login in required.
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


# Gets all tickets and renders tickets.html
@app.route("/tickets")
def tickets():
    ticketdata = Ticket.query.all()
    return render_template('tickets.html', ticketdata=ticketdata)


# Ticket submission route
# Loads Ticket Form
# If form data is valid, add the ticket to the session and commit.
# Redirect to account.html template
@app.route("/ticket_submit", methods=['GET', 'POST'])
def ticket_submit():
    form = TicketSubmit()
    if form.validate_on_submit():
        tick = Ticket(email=current_user.email, room_id=form.room_number.data, build_id=form.building_number.data, description=form.description.data, submitdate=datetime.datetime.now(), mtype=form.maint_type.data, resolvedate=None)
        db.session.add(tick)
        db.session.commit()
        flash("Ticket was submitted successfully!", 'success')
        return redirect(url_for('tickets'))
    return render_template('ticket_submit.html', form=form)


# Admin ticket submission route.
# Ticket ID is passed in the route
# Loads Admin Ticket Submit Form
# If the form dat ais valid, update the description and resolve date, then add and commit.
# Redirect for account.html
@app.route("/admin_submit/<ticket_id>", methods=['GET', 'POST'])
def admin_submit(ticket_id):
    form = AdminTickSubmit()
    the_ticket = Ticket.query.filter_by(id=ticket_id).first()
    if form.validate_on_submit():
        the_ticket.description = form.description.data
        the_ticket.resolvedate = datetime.date.today()
        db.session.commit()
        flash("Ticket was resolved successfully", 'success')
        return redirect(url_for('tickets'))
    return render_template('admin_submit.html', form=form, ticket=the_ticket)


# Passes tickets and renders closed_tickets.html template
@app.route("/closed_tickets")
def closed_tickets():
    ticketdata = Ticket.query.all()
    return render_template('closed_tickets.html', ticketdata=ticketdata)