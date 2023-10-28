from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, TextAreaField, SelectField, \
    ValidationError, IntegerField, RadioField, TelField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, InputRequired
from application import auth
from application.annonces.city import CITY_SENEGAL

# Create a class for the registration form
class RegistrationForm(FlaskForm):
    # Create an email field
    display_name = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=20)],
                        render_kw={"class": "form-control", "placeholder": "Prénom"})
    last_name = StringField("Nom", validators=[DataRequired(), Length(min=2, max=20)],
                        render_kw={"class": "form-control", "placeholder": "Nom"})
    
    email = StringField("Email", validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control", "placeholder": "Adresse email"})
    # Create a password field
    password = PasswordField("Mot de Passe", validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Mot de passe"})
    # Create a confirm password field
    confirm_password = PasswordField("Confirmer le Mot de Passe", validators=[DataRequired(), EqualTo("password")],
                                     render_kw={"class": "form-control", "placeholder": "Confirmer le mot de passe"})
    
    phone_number = StringField("Numero", validators=[DataRequired(), Length(min=8, max=20)],
                        render_kw={"class": "form-control", "placeholder": "Numéro de téléphone"})
    
    sexe = RadioField(
        'Vous êtes',
        choices=[('Homme', 'Homme'), ('Femme', 'Femme')],
        validators=[InputRequired()],
        render_kw={'class': 'form-check-input'}
    )
    
    description = TextAreaField('Présentation', render_kw={'rows': 5})
    
    submit = SubmitField("Inscription", render_kw={"class": "btn btn-primary"})

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError("Les mots de passe ne correspondent pas")


class UpdateProfileForm(FlaskForm):
    display_name = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=20)],
                               render_kw={"class": "form-control", "placeholder": "Prénom"})
    email = StringField('Email', )
    phone_number = IntegerField('Numéro de téléphone', validators=[NumberRange(min=9, max=15)])
    description = TextAreaField('Présentation', render_kw={'rows': 5})
    city = SelectField('Ville de départ', validators=[InputRequired()],
                             render_kw={'class': 'form-control form-select js-choice',
                                        'value': '', 'data-search-enabled': 'true'})
    
    submit = SubmitField('Mettre à jour')
    
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.city.choices = [city for city in CITY_SENEGAL]


class LoginForm(FlaskForm):
    # Create an email field
    email = StringField("Email", validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control", "placeholder": "Adresse email"})
    # Create a password field
    password = PasswordField("Mot de Passe", validators=[DataRequired()],
                             render_kw={"class": "form-control", "placeholder": "Mot de passe"})
    submit = SubmitField("Connexion", render_kw={"class": "btn btn-primary"})