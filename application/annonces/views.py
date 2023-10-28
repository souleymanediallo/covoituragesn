from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user

from application import app, db, auth, annonce_ref, user_ref as user_ref_sn
from application.annonces.forms import AnnonceForm
from datetime import datetime





@app.route('/annonce/<annonce_id>', methods=['GET'])
def annonce_detail(annonce_id):
    annonce = annonce_ref.document(annonce_id).get()
    if annonce.exists:
        annonce_data = annonce.to_dict()
        annonce_data['id'] = annonce.id
        user_id = annonce_data.get('user_id')
        try:
            user_ref = db.collection('users').document(user_id)
            user = user_ref.get().to_dict()
        except Exception as e:
            app.logger.error(f"Erreur lors de la récupération de l'utilisateur {user_id} : {e}")
            user = None

        annonce_data['user'] = user
        return render_template('annonces/annonce_detail.html', annonce=annonce_data)
    else:
        # Gérer le cas où l'annonce n'existe pas (par exemple, renvoyer une erreur 404)
        return render_template('404.html'), 404


@app.route('/new-annonce', methods=['GET', 'POST'])
@login_required
def annonce_create():
    user = auth.get_user(current_user.id)
    form = AnnonceForm(request.form)  # Create the form instance using request.form
    if request.method == 'POST' and form.validate():
        print("Formulaire valide")
        if user:
            annonce_data = {
                'start_city': form.start_city.data,
                'end_city': form.end_city.data,
                'profile': form.profile.data,
                'trip': form.trip.data,
                'seats': form.seats.data,
                'luggage': form.luggage.data,
                'start_date': form.start_date.data.strftime('%d/%m/%Y'),  # Adjusted date format
                'start_hour': form.start_hour.data,  # Store hours and minutes separately
                'start_minute': form.start_minute.data,
                'end_date': form.end_date.data.strftime('%d/%m/%Y') if form.end_date.data else None,
                'end_hour': form.end_hour.data if form.end_hour.data else None,
                'end_minute': form.end_minute.data if form.end_minute.data else None,
                'price': form.price.data,
                'description': form.description.data,
                'is_active': form.is_active.data,
                'created': datetime.now().strftime('%d %B %Y'),  # Adjusted date format
                'user_id': user.uid  # Use the user ID from your authentication module
            }
            # Add the annonce_data to your database (Firestore or any other)
            db.collection('annonces').add(annonce_data)
            return redirect(url_for('home'))  # Redirect to the home page or another route
    else:
        print(form.errors)
    return render_template('annonces/annonce_create.html', form=form)


@app.route('/annonces', methods=['GET'])
def annonce_list():
    try:
        annonces_ref = db.collection('annonces').get()
    except Exception as e:
        app.logger.error(f"Erreur lors de la récupération des annonces : {e}")
        return render_template('error.html', message="Erreur lors de la récupération des annonces"), 500

    annonces = []
    for annonce_ref in annonces_ref:
        annonce = annonce_ref.to_dict()
        annonce['id'] = annonce_ref.id
        user_id = annonce.get('user_id')
        try:
            user_ref = db.collection('users').document(user_id)
            user = user_ref.get().to_dict()
        except Exception as e:
            app.logger.error(f"Erreur lors de la récupération de l'utilisateur {user_id} : {e}")
            user = None

        annonce['user'] = user
        annonces.append(annonce)

    return render_template('annonces/annonce_list.html', annonces=annonces)


@app.route('/annonce/<annonce_id>/update', methods=['GET', 'POST'])
@login_required
def annonce_update(annonce_id):
    user = auth.get_user(current_user.id)
    annonce_doc = db.collection('annonces').document(annonce_id)
    annonce = annonce_doc.get().to_dict()
    annonce['id'] = annonce_id
    print(annonce['id'])

    # Vérifiez si l'utilisateur est le propriétaire de l'annonce
    if annonce['user_id'] != user.uid:
        flash('Vous n\'êtes pas autorisé à modifier cette annonce.', 'danger')
        return redirect(url_for('home'))  # Redirigez vers la page d'accueil ou une autre page appropriée

    form = AnnonceForm(request.form)

    if request.method == 'POST' and form.validate():
        # Créez un dictionnaire pour les données de l'annonce à mettre à jour
        annonce_data = {
            'start_city': form.start_city.data,
            'end_city': form.end_city.data,
            'profile': form.profile.data,
            'type': form.type.data,
            'seats': form.seats.data,
            'luggage': form.luggage.data,
            'start_date': form.start_date.data.strftime('%d/%m/%Y'),  # Formatage de la date de départ
            'start_hour': form.start_hour.data,
            'start_minute': form.start_minute.data,
            'end_date': form.end_date.data.strftime('%d/%m/%Y') if form.end_date.data else None,  # Formatage de la date de retour
            'end_hour': form.end_hour.data if form.end_hour.data else None,
            'end_minute': form.end_minute.data if form.end_minute.data else None,
            'price': form.price.data,
            'description': form.description.data,
            'is_active': form.is_active.data,
        }

        # Mettez à jour l'annonce avec les nouvelles données
        annonce_doc.update(annonce_data)

        flash('Annonce mise à jour avec succès.', 'success')
        return redirect(url_for('home'))  # Redirigez vers la page d'accueil ou une autre page appropriée

    # Pré-remplir manuellement les champs du formulaire avec les données de l'annonce
    form.start_city.data = annonce['start_city']
    form.end_city.data = annonce['end_city']
    form.profile.data = annonce['profile']
    form.type.data = annonce['type']
    form.seats.data = annonce['seats']
    form.luggage.data = annonce['luggage']
    form.start_date.data = datetime.strptime(annonce['start_date'], '%d/%m/%Y')  # Conversion en objet datetime
    form.start_hour.data = annonce['start_hour']
    form.start_minute.data = annonce['start_minute']
    if annonce['end_date']:
        form.end_date.data = datetime.strptime(annonce['end_date'], '%d/%m/%Y')  # Conversion en objet datetime
    form.end_hour.data = annonce['end_hour']
    form.end_minute.data = annonce['end_minute']
    form.price.data = annonce['price']
    form.description.data = annonce['description']
    form.is_active.data = annonce['is_active']

    return render_template('annonces/annonce_update.html', form=form, annonce_id=annonce_id, annonce=annonce)


@app.route('/annonce/<annonce_id>/annonce_delete', methods=['POST'])
@login_required
def annonce_delete(annonce_id):
    user = auth.get_user(current_user.id)
    annonce_ref = db.collection('annonces').document(annonce_id)
    annonce = annonce_ref.get().to_dict()

    if annonce['user_id'] != user.uid:
        flash('Vous n\'êtes pas autorisé à supprimer cette annonce.', 'danger')
        return redirect(url_for('home'))

    annonce_ref.delete()
    flash('Annonce supprimée avec succès.', 'success')
    return redirect(url_for('home'))


@app.route('/annonce/<annonce_id>/confirm_delete', methods=['GET', 'POST'])
@login_required
def annonce_confirm_delete(annonce_id):
    user = auth.get_user(current_user.id)
    annonce_ref = db.collection('annonces').document(annonce_id)
    annonce = annonce_ref.get().to_dict()

    if annonce['user_id'] != user.uid:
        flash('Vous n\'êtes pas autorisé à supprimer cette annonce.', 'danger')
        return redirect(url_for('home'))
    return render_template('annonces/annonce_confirm_delete.html', annonce=annonce, annonce_id=annonce_id)

