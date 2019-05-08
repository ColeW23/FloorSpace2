from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from game_store.models import Tenant


# If the field is empty for building, then an error is raised
def validate_building(self, field):
    if field.data == "":
        raise ValidationError("Invalid building number!")


# If the field for maintenance type is empty, then an error is raised
def validate_mainttype(self, field):
    if field.data == "":
        raise ValidationError("Invalid Maintenance type!")


# A registration form that has a field for username, email, password, confirm_password, and a submit button
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account')

    # Checks if the email is already associated with a user in the database
    def validate_email(self, email):
        user = Tenant.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')


# A ticket form that has fields for building_number, room_number, maint_type, description, and a submit button
class TicketSubmit(FlaskForm):
    building_number = SelectField('Building Number', choices=[("", " "), ('1', '1'), ('1', '2')],
                                  validators=[validate_building, DataRequired()])
    room_number = IntegerField('Room Number', validators=[DataRequired()])
    choices=[("", " "), ("Repair", "Repair"), ("Plumbing", "Plumbing"), ("Electrical", "Electrical"), ("Other", "Other")]
    maint_type = SelectField("Maintenance Type", choices=choices, validators=[validate_mainttype, DataRequired()])
    description = TextAreaField("Maintenance Description", validators=[DataRequired()])
    submit = SubmitField("SubmitTicket")


# A login form that has fields for email, password, remember, and a submit button
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# A ticket search form that has fields for selecting tickets
class TicketSearchForm(FlaskForm):
    choices = [('id', "ID"), ('Email', 'Email')]
    select = SelectField('Search for ticket:', choices=choices)
    search = StringField('')


# Am admin ticket submit form with a description field
class AdminTickSubmit(FlaskForm):
    description = TextAreaField("Closing Response", validators=[DataRequired()])
    submit = SubmitField("Resolve Ticket")