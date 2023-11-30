from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[Length(min=0, max=300)])
    submit = SubmitField('Send Message')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    requirement = TextAreaField('Requirement', validators=[DataRequired()])
    benefit = StringField('Financial Benefit', validators=[DataRequired()])
    deadline = StringField('Deadline', validators=[DataRequired()])
    how_to_apply = TextAreaField("How To Apply", validators=[DataRequired()])
    region = SelectField('Region', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Post')

class RegionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create Region')

class CVReviewForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    cv = FileField('CV File', validators=[FileRequired()])
    submit = SubmitField('Submit CV')

class SOPReviewForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    sop = FileField('CV File', validators=[FileRequired()])
    submit = SubmitField('Submit SOP')


