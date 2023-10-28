from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, TextAreaField, BooleanField, \
    SelectField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from datetime import datetime
from application.annonces.city import CITY_SENEGAL


class AnnonceForm(FlaskForm):
    hour_choices = [(str(hour).zfill(2), str(hour).zfill(2)) for hour in range(24)]
    minute_choices = [(str(minute).zfill(2), str(minute).zfill(2)) for minute in range(0, 60, 10)]

    start_city = SelectField('Ville de départ', validators=[InputRequired()],
                             render_kw={'class': 'form-control form-select js-choice',
                                        'value': '', 'data-search-enabled': 'true'})
    end_city = SelectField('Ville d\'arrivée', validators=[InputRequired()],
                           render_kw={'class': 'form-control form-select js-choice',
                                      'value': '', 'data-search-enabled': 'true'})
    profile = RadioField(
        'Profile',
        choices=[('Conducteur', 'Conducteur'), ('Passager', 'Passager')],
        validators=[InputRequired()],
        render_kw={'class': 'form-check-input'}
    )
    trip = RadioField(
        'Type de trajet',
        choices=[('Aller Simple', 'Aller Simple'), ('Aller Retour', 'Aller Retour')],
        validators=[InputRequired()],
        render_kw={'class': 'form-check-input'},
        default='Aller Simple'
    )
    seats = IntegerField('Nombre de places disponibles', validators=[DataRequired(), NumberRange(min=1, max=9)],
                         default=1)
    luggage = IntegerField('Nombre de bagages', validators=[DataRequired(), NumberRange(min=1, max=9)], default=1)

    start_date = DateField('Date de départ', format='%d/%m/%Y', validators=[InputRequired()],
                           render_kw={'class': 'form-control flatpickr flatpickr-input',
                                      'type': 'date', 'data-date-format': 'd/m/Y',
                                      'data-min-date': 'today', 'data-toggle': 'date-picker', 'lang': 'fr'
                                      })

    start_hour = SelectField('Heure de départ', choices=hour_choices, validators=[InputRequired()],
                             render_kw={'class': 'form-control form-select js-choice'})
    start_minute = SelectField('Minute', choices=minute_choices, validators=[InputRequired()],
                               render_kw={'class': 'form-control'})

    end_date = DateField('Date de retour', format='%d/%m/%Y', validators=[InputRequired()],
                           render_kw={'class': 'form-control flatpickr flatpickr-input',
                                      'type': 'date', 'data-date-format': 'd/m/Y',
                                      'data-min-date': 'today', 'data-toggle': 'date-picker', 'lang': 'fr'})

    end_hour = SelectField('Heure de retour', choices=hour_choices, validators=[InputRequired()],
                           render_kw={'class': 'form-control form-select js-choice'})
    end_minute = SelectField('Minute', choices=minute_choices, validators=[InputRequired()],
                               render_kw={'class': 'form-control'})

    price = IntegerField('Prix', validators=[DataRequired(), NumberRange(min=0, max=20000)], default=1)
    description = TextAreaField('Informations sur les voyageurs')

    is_active = BooleanField('Trajet actif')
    created = datetime.now()
    user_id = HiddenField('User ID')
    submit = SubmitField("Publier votre trajet", render_kw={"class": "btn btn-success"})

    def __init__(self, *args, **kwargs):
        super(AnnonceForm, self).__init__(*args, **kwargs)
        self.start_city.choices = [city for city in CITY_SENEGAL]
        self.end_city.choices = [city for city in CITY_SENEGAL]
