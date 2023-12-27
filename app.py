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
    mycursor = get_db().cursor()
    sql = '''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques 
    '''
    mycursor.execute(sql)
    marques= mycursor.fetchall()

    return render_template('brand/show_marque.html', brand = marques)

@app.route('/marque/add', methods=['GET'])
def add_marque():
    mycursor = get_db().cursor()
    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques 
    '''

    mycursor.execute(sql)
    marques= mycursor.fetchall()

    sql='''
    SELECT motos.id_moto AS id,
    motos.libelle_moto AS nom,
    motos.puissance_moto AS puissance,
    motos.couleur_moto AS couleur,
    motos.date_mise_en_circulation AS miseEnCirculation,
    motos.photo_moto AS photo
    FROM motos INNER JOIN marques ON motos.marque_id = marques.id_marque
    '''

    mycursor.execute(sql)
    motos= mycursor.fetchall()

    return render_template('brand/add_marque.html', brand=marques, moto=motos)

@app.route('/marque/add', methods=['POST'])
def valid_add_marque():
    mycursor = get_db().cursor()

    libelle = request.form['libelle']
    logo = request.form['logo']
    tuple_insert = (libelle, logo)
    sql = '''
    INSERT INTO marques (libelle_marque, logo_marque)
    VALUES (%s, %s)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'Nouvelle marque , libelle : ', libelle, ' | logo : ', logo)
    message = u'Nouvelle marque , libelle : '+libelle + ' | logo : ' + logo
    flash(message, 'alert-success')
    return redirect('/marque/show')

@app.route('/marque/delete', methods=['GET'])
def delete_marque():
    mycursor = get_db().cursor()
    id_marque = request.args.get('id', '')
    tuple_delete = (id_marque)
    sql = '''
    DELETE FROM marques
    WHERE id_marque = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'Une marque supprimée ! id : ' + id_marque
    flash(message, 'alert-warning')
    return redirect('/ticket/show')


@app.route('/marque/edit', methods=['GET'])
def edit_marque():
    mycursor = get_db().cursor()
    id_marque = request.args.get('id', '')
    tuple_edit = (id_marque)
    sql = '''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques 
    WHERE id_marque = %s
    '''
    mycursor.execute(sql, tuple_edit)
    marque = mycursor.fetchone()
    return render_template('brand/edit_marque.html', marque=marque)

@app.route('/marque/edit', methods=['POST'])
def valid_edit_marque():
    mycursor = get_db().cursor()
    id_marque = request.form['id']
    libelle = request.form['libelle']
    logo = request.form['logo']
    tuple_edit = (libelle, logo, id_marque)
    sql = '''
    UPDATE marques
    SET libelle_marque = %s, logo_marque = %s
    WHERE id_marque = %s
    '''
    mycursor.execute(sql, tuple_edit)
    get_db().commit()
    print(u'marque modifiée , libelle : ', libelle, ' | logo : ', logo)
    message = u'marque modifiée , libelle : '+libelle + ' | logo : ' + logo
    flash(message, 'alert-success')
    return redirect('/marque/show')

@app.route('/moto/show')
def show_moto():
    mycursor = get_db().cursor()
    sql = '''
    SELECT 
        motos.id_moto AS id,
        motos.libelle_moto AS nom,
        motos.puissance_moto AS puissance,
        motos.couleur_moto AS couleur,
        motos.date_mise_en_circulation AS miseEnCirculation,
        motos.photo_moto AS photo,
        marques.libelle_marque AS marque,
        marques.logo_marque AS logo
    FROM motos INNER JOIN marques ON motos.marque_id = marques.id_marque
    '''
    mycursor.execute(sql)
    motos= mycursor.fetchall()

    return render_template('moto/show_moto.html', moto=motos)

@app.route('/moto/add', methods=['GET'])
def add_moto():
    mycursor = get_db().cursor()
    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques 
    '''

    mycursor.execute(sql)
    marques= mycursor.fetchall()

    sql='''
    SELECT motos.id_moto AS id,
    motos.libelle_moto AS nom,
    motos.puissance_moto AS puissance,
    motos.couleur_moto AS couleur,
    motos.date_mise_en_circulation AS miseEnCirculation,
    motos.photo_moto AS photo
    FROM motos INNER JOIN marques ON motos.marque_id = marques.id_marque
    '''

    mycursor.execute(sql)
    motos= mycursor.fetchall()

    return render_template('moto/add_moto.html', brand=marques, moto=motos)

@app.route('/moto/add', methods=['POST'])
def valid_add_moto():
    mycursor = get_db().cursor()

    libelle = request.form['nom']
    marque_id = request.form['marque_id']
    puissance = request.form['puissance']
    miseEnCirculation = request.form['miseEnCirculation']
    couleur = request.form['couleur']
    photo = request.form['photo']
    tuple_insert = (libelle, marque_id, puissance, miseEnCirculation, couleur, photo)
    sql = '''
    INSERT INTO motos (libelle_moto, marque_id, puissance_moto, date_mise_en_circulation, couleur_moto, photo_moto)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'Nouvelle moto , libelle : ', libelle, ' | marque_id : ', marque_id, ' | puissance : ', puissance, ' | mise en circulation : ', miseEnCirculation, ' | couleur : ', couleur, ' | photo : ', photo)
    message = u'Nouvelle moto , libelle : '+libelle + ' | marque_id : ' + marque_id + ' | puissance : ' + puissance + ' | mise en circulation : ' + miseEnCirculation + ' | couleur : ' + couleur + ' | photo : ' + photo
    flash(message, 'alert-success')
    return redirect('/moto/show')

@app.route('/moto/delete', methods=['GET'])
def delete_moto():
    mycursor = get_db().cursor()
    id_moto = request.args.get('id', '')
    tuple_delete = (id_moto)
    sql = '''
    DELETE FROM motos
    WHERE id_moto = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'Une moto supprimée ! id : ' + id_moto
    flash(message, 'alert-warning')
    return redirect('/ticket/show')

@app.route('/moto/edit', methods=['GET'])
def edit_moto():
    mycursor = get_db().cursor()
    id_moto = request.args.get('id', '')
    tuple_edit = (id_moto)
    sql = '''
    SELECT motos.id_moto AS id,
    motos.libelle_moto AS nom,
    motos.puissance_moto AS puissance,
    motos.couleur_moto AS couleur,
    motos.date_mise_en_circulation AS miseEnCirculation,
    motos.photo_moto AS photo,
    marques.libelle_marque AS marque
    FROM motos INNER JOIN marques ON motos.marque_id = marques.id_marque
    WHERE id_moto = %s
    '''
    mycursor.execute(sql, tuple_edit)
    moto = mycursor.fetchone()
    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques
    '''
    mycursor.execute(sql)
    marques= mycursor.fetchall()

    # Récupère les couleurs
    sql='''
    SELECT DISTINCT couleur_moto AS couleur
    FROM motos
    '''
    mycursor.execute(sql)
    couleurs= mycursor.fetchall()


    return render_template('moto/edit_moto.html', moto=moto, brand=marques, couleur=couleurs)

@app.route('/moto/edit', methods=['POST'])
# Requête préparée avec SET PREPARE et EXECUTE pour valid_edit_moto
def valid_edit_moto():
    mycursor = get_db().cursor()
    id_moto = request.form['id']
    libelle = request.form['nom']
    marque_id = request.form['marque_id']
    puissance = request.form['puissance']
    miseEnCirculation = request.form['miseEnCirculation']
    couleur = request.form['couleur']
    photo = request.form['photo']
    tuple_edit = (libelle, int(id_moto), int(puissance), miseEnCirculation, couleur, photo, int(marque_id))

    sql = '''
    SET @nouveau_nom = 'test';
    SET @id_moto = '25';
    SET @nouvelle_puissance = '3000';
    SET @nouvelle_mise_en_circulation = '2023-12-06';
    SET @nouvelle_couleur = 'bleu';
    SET @nouvelle_photo = 'hdsgih';
    SET @marque_id = 3;

    PREPARE stmt FROM 'UPDATE motos SET libelle_moto = ?, puissance_moto = ?, date_mise_en_circulation = ?, couleur_moto = ?, marque_id = ?, photo_moto = ? WHERE id_moto = ?';

    EXECUTE stmt USING @nouveau_nom, @nouvelle_puissance, @nouvelle_mise_en_circulation, @nouvelle_couleur, @marque_id, @nouvelle_photo, @id_moto;

    DEALLOCATE PREPARE stmt;
    '''

    mycursor.execute(sql)
    get_db().commit()

    message = f"Moto modifiée - Libelle: {libelle}, Marque_id: {marque_id}, Puissance: {puissance}, Mise en circulation: {miseEnCirculation}, Couleur: {couleur}, Photo: {photo}"
    
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


