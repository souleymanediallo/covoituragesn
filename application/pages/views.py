from flask import render_template
from application import app, db


@app.route("/")
def home():
    annonces_ref = db.collection('annonces').get()
    annonces = []
    for annonce_ref in annonces_ref:
        annonce = annonce_ref.to_dict()
        annonce['id'] = annonce_ref.id
        user_id = annonce.get('user_id')
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get().to_dict()
        annonce['user'] = user
        annonces.append(annonce)
    return render_template('pages/index.html', annonces=annonces)