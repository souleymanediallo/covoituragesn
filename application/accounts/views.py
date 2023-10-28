from flask import render_template, redirect, url_for, flash
from application import app
import hashlib
from application import db, auth, bcrypt
from application.accounts.forms import RegistrationForm, LoginForm, UpdateProfileForm

from application.accounts.models import User
from flask_login import login_user, login_required, logout_user, current_user
from application import login_manager


def hash_password(password):
    # Utilisez une fonction de hachage sécurisée (par exemple SHA-256) pour stocker les mots de passe
    return hashlib.sha256(password.encode()).hexdigest()


@login_manager.user_loader
def load_user(uid):
    return User(uid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Formulaire valide")
        print(form.display_name.data)
        print(form.last_name.data)
        print(form.email.data)
        print(form.password.data)
        print(form.phone_number.data)
        print(form.sexe.data)
        
        display_name = form.display_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        phone_number = form.phone_number.data
        sexe = form.sexe.data
        try:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = auth.create_user(
                display_name=display_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            # Enregistrez l'utilisateur dans Firestore
            user_ref = db.collection('users').document(new_user.uid)
            user_ref.set({
                'email': email,
                'display_name': display_name,
                'last_name': last_name,
                'password_hash': password_hash,  # Stockez le hash du mot de passe
                'phone_number': phone_number,
                'sexe': sexe,
                'description': 'Mettre à jour votre présentation',
            })
            return redirect(url_for('home'))  # Redirige vers la page d'accueil
        except Exception as e:
            print("Erreur lors de l'enregistrement:", e)
            return render_template('accounts/register.html', form=form, error="Erreur lors de la création de l'utilisateur")

    return render_template('accounts/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        users_db = db.collection('users').where("email", "==", email).stream()
        for user_doc in users_db:
            user_data = user_doc.to_dict()
            stored_password_hash = user_data.get('password_hash')
            if bcrypt.check_password_hash(stored_password_hash, password):
                user = User(user_doc.id)
                login_user(user)
                return redirect(url_for('home'))
        return render_template('accounts/login.html', form=form, error="Adresse e-mail ou mot de passe incorrect")
    return render_template('accounts/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/dashboard")
def dashboard():
    return render_template("accounts/dashboard.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("accounts/profile.html")


@app.route("/bookings")
@login_required
def bookings():
    user_id = current_user.id
    annonces_ref = db.collection('annonces').where('user_id', '==', user_id).get()
    annonces = []
    for annonce_ref in annonces_ref:
        annonce = annonce_ref.to_dict()
        annonce['id'] = annonce_ref.id
        annonces.append(annonce)
    # Récupérer les informations de l'utilisateur
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get().to_dict()
    return render_template("accounts/bookings.html", annonces=annonces, user=user)


# Dans votre route update_profile
@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = auth.get_user(current_user.id)
    form = UpdateProfileForm()
    if form.validate_on_submit():
        display_name = form.display_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        sexe = form.sexe.data
        description = form.presentation.data
        phone_number = form.phone_number.data
        city = form.city.data
        
        try:
            # Mettez à jour les informations de l'utilisateur dans Firestore
            user_ref = db.collection('users').document(current_user.id)
            user_ref.update({
                'email': email,
                'display_name': display_name,
                'last_name': last_name,
                'sexe': sexe,
                'description': description,
                'phone_number': phone_number,
                'city': city
            })
            flash('Vos informations ont été mises à jour avec succès', 'success')
            return redirect(url_for('home'))  # Redirige vers la page d'accueil après la mise à jour
        except Exception as e:
            flash('Erreur lors de la mise à jour des informations', 'danger')
            return redirect(url_for('update_profile'))
        
    form.display_name.data = user.display_name
    form.email.data = user.email
    form.phone_number.data = user.phone_number

    return render_template('accounts/update_profile.html', form=form)


