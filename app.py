from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'phrasegigatopsecrete'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="jbfroehl",
            password="motdepassehehe",
            database="BDD_jbfroehl",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_layout():
    return render_template('layouteu.html')

@app.route('/marque/show')
def show_marque():
    return render_template('brand/show_marque.html', brand = marques)

@app.route('/marque/add', methods=['GET'])
def add_marque():
    return render_template('brand/add_marque.html')

@app.route('/marque/add', methods=['POST'])
def valid_add_marque():
    libelle = request.form.get('libelle', '')
    logo = request.form.get('logo', '')
    print(u'marque ajoutée , libellé : ', libelle, ' | logo : ', logo)
    message = u'marque ajoutée, libellé : '+libelle+' | logo : '+logo
    flash(message, 'alert-success')
    return redirect('/marque/show')

@app.route('/marque/delete', methods=['GET'])
def delete_marque():
    id = request.args.get('id', '')
    print ("une marque supprimée, id : ",id)
    message=u'une marque supprimée, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/marque/show')


@app.route('/marque/edit', methods=['GET'])
def edit_marque():
    id = request.args.get('id', '')
    id=int(id)
    marque = marques[id-1]
    return render_template('brand/edit_marque.html', marque=marque)

@app.route('/marque/edit', methods=['POST'])
def valid_edit_marque():
    libelle = request.form['libelle']
    id = request.form.get('id', '')
    logo = request.form.get('logo', '')
    print(u'marque modifiée, id: ',id, " libelle :", libelle, " | logo :", logo)
    message=u'une marque modifiée, id: ' + id + " libelle : " + libelle + " | logo : " + logo
    flash(message, 'alert-success')
    return redirect('/marque/show')

@app.route('/moto/show')
def show_moto():
    return render_template('moto/show_moto.html', moto=motos, brand=marques)

@app.route('/moto/add', methods=['GET'])
def add_moto():
    return render_template('moto/add_moto.html', brand=marques, moto=motos)

@app.route('/moto/add', methods=['POST'])
def valid_add_moto():
    nom = request.form.get('nom', '')
    brand_id = request.form.get('marque_id', '')
    puissance = request.form.get('puissance', '')
    couleur = request.form.get('couleur', '')
    miseEnCirculation = request.form.get('miseEnCirculation', '')
    photo = request.form.get('photo', '')
    print(u'Nouvelle moto , nom : ', nom, ' | id marque : ', brand_id, ' | Puissance : ', puissance, ' | couleur : ', couleur, ' | Mise en circulation : ', miseEnCirculation, ' | photo : ', photo)
    message = u'Nouvelle moto , nom : '+nom + ' | id marque : ' + brand_id + ' | Puissance : ' + puissance + ' | couleur : '+  couleur + ' | Mise en circulation : ' + miseEnCirculation + ' | photo : ' + photo
    flash(message, 'alert-success')
    return redirect('/moto/show')

@app.route('/moto/delete', methods=['GET'])
def delete_moto():
    id = request.args.get('id', '')
    print ("une moto supprimée, id : ",id)
    message=u'un article supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/moto/show')

@app.route('/moto/edit', methods=['GET'])
def edit_moto():
    id = request.args.get('id', '')
    id=int(id)
    moto1 = motos[id-1]
    return render_template('moto/edit_moto.html', moto=moto1, brand=marques)

@app.route('/moto/edit', methods=['POST'])
def valid_edit_moto():
    id = request.form.get('id', '')
    nom = request.form.get('nom', '')
    brand_id = request.form.get('marque_id')
    puissance = request.form.get('puissance', '')
    miseEnCirculation = request.form.get('miseEnCirculation', '')
    couleur = request.form.get('couleur', '')
    photo = request.form.get('photo', '')
    print(u'moto modifiée , nom : ', nom, ' | brand_id :', brand_id, ' | puissance:', puissance, ' | mise en circulation:', miseEnCirculation, ' | couleur :', couleur, ' | image:', photo)
    message = u'moto modifiée , nom:'+nom + ' | brand_id :' + str(brand_id) + ' | puissance:' + puissance + ' | mise en circulation:'+  miseEnCirculation + ' | couleur:' + couleur + ' | image:' + photo
    flash(message, 'alert-success')
    return redirect('/moto/show')

@app.route('/moto/filtre', methods=['GET'])
def filtre_moto():
    print("filtre")
    filter_word= request.args.get('filter_word', None)
    filter_value_min = request.args.get('filter_value_min', None)
    filter_value_max = request.args.get('filter_value_max', None)
    filter_items = request.args.getlist('filter_items', None)
    if filter_word and filter_word != "":
        message=u'filtre sur le mot  : '+filter_word
        flash(message, 'alert-success')
    if filter_value_min or filter_value_max :
        if filter_value_min.isdecimal() and filter_value_max.isdecimal():
            if int(filter_value_min) < int(filter_value_max):
                message=u'filtre sur la colonne avec un numérique entre : '+filter_value_min+' et '+filter_value_max
                flash(message, 'alert-success')
            else :
                message=u'min < max'
                flash(message, 'alert-warning')
        else :
            message=u'min et max doivent être des numériques'
            flash(message, 'alert-warning')
    if filter_items and filter_items != []:
        message=u'case à cocher selectionnée : '
        for case in filter_items :
            message+= 'id : '+case+' '
        flash(message, 'alert-success')
    return render_template('/moto/filtre_moto.html', moto=motos, brand=marques)
        


if __name__ == '__main__':
    app.run()


