from flask import Flask, request, render_template, redirect, abort, flash, g, session

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

def check_if_empty_marque(id_marque):
    mycursor = get_db().cursor()
    tuple_check = (id_marque)
    sql = '''
    SELECT COUNT(*) AS nb
    FROM motos
    WHERE marque_id = %s
    '''
    mycursor.execute(sql, tuple_check)
    nb = mycursor.fetchone()
    return nb['nb']

@app.route('/marque/delete', methods=['GET'])
def delete_marque():
    mycursor = get_db().cursor()
    id_marque = request.args.get('id', '')
    if check_if_empty_marque(id_marque) == 0 :
        tuple_delete = (id_marque)
        sql = '''
        DELETE FROM marques
        WHERE id_marque = %s
        '''
        mycursor.execute(sql, tuple_delete)
        get_db().commit()
        message=u'Une marque supprimée ! id : ' + id_marque
        flash(message, 'alert-warning')
    else :
        return redirect('/marque/delete/confirm?id='+id_marque)
    return redirect('/marque/show')



@app.route('/marque/delete/confirm', methods=['GET'])
def delete_marque_confirm():
    mycursor = get_db().cursor()
    id_marque = request.args.get('id', '')
    tuple_delete = (id_marque)
    sql = '''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques 
    WHERE id_marque = %s
    '''
    mycursor.execute(sql, tuple_delete)
    marque = mycursor.fetchone()

    sql = '''
    SELECT motos.id_moto AS id,
    motos.libelle_moto AS nom,
    motos.puissance_moto AS puissance,
    motos.couleur_moto AS couleur,
    motos.date_mise_en_circulation AS miseEnCirculation,
    motos.photo_moto AS photo,
    motos.marque_id AS marque_id
    FROM motos INNER JOIN marques ON motos.marque_id = marques.id_marque
    WHERE marque_id = %s
    '''
    mycursor.execute(sql, tuple_delete)
    motos = mycursor.fetchall()

    # Nombres de motos dans la marque
    sql = '''
    SELECT COUNT(*) AS nb
    FROM motos
    WHERE marque_id = %s
    '''
    mycursor.execute(sql, tuple_delete)
    nb = mycursor.fetchone()
    
    return render_template('brand/delete_marque.html', marque=marque, moto=motos, nb=nb['nb'])

@app.route('/marque/delete/confirm/cascade', methods=['GET'])
def delete_marque_anyway():
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
    return redirect('/marque/show')

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
    FROM motos LEFT JOIN marques ON motos.marque_id = marques.id_marque
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
    return redirect('/moto/show')

@app.route('/moto/delete/confirm', methods=['GET'])
def delete_moto_confirm():
    mycursor = get_db().cursor()
    id_moto = request.args.get('id', '')
    id_marque = request.args.get('id_marque', '')
    tuple_delete = (id_moto)
    sql = '''
    DELETE FROM motos
    WHERE id_moto = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'Une moto supprimée ! id : ' + id_moto
    flash(message, 'alert-warning')
    return redirect('/marque/delete/confirm?id='+id_marque)

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

    sql='''
    SELECT DISTINCT couleur_moto AS couleur
    FROM motos
    '''
    mycursor.execute(sql)
    couleurs= mycursor.fetchall()

    return render_template('moto/edit_moto.html', moto=moto, brand=marques, couleur=couleurs)

@app.route('/moto/edit', methods=['POST'])
def valid_edit_moto():
    mycursor = get_db().cursor()
    id_moto = request.form['id']
    libelle = request.form['nom']
    marque_id = request.form['marque_id']
    puissance = request.form['puissance']
    miseEnCirculation = request.form['miseEnCirculation']
    couleur = request.form['couleur']
    photo = request.form['photo']
    tuple_edit = (libelle, marque_id, puissance, miseEnCirculation, couleur, photo, id_moto)
    sql = '''
    UPDATE motos
    SET libelle_moto = %s, marque_id = %s, puissance_moto = %s, date_mise_en_circulation = %s, couleur_moto = %s, photo_moto = %s
    WHERE id_moto = %s
    '''
    mycursor.execute(sql, tuple_edit)
    get_db().commit()
    print(u'moto modifiée , libelle : ', libelle, ' | marque_id : ', marque_id, ' | puissance : ', puissance, ' | mise en circulation : ', miseEnCirculation, ' | couleur : ', couleur, ' | photo : ', photo)
    message = u'moto modifiée , libelle : '+libelle + ' | marque_id : ' + marque_id + ' | puissance : ' + puissance + ' | mise en circulation : ' + miseEnCirculation + ' | couleur : ' + couleur + ' | photo : ' + photo
    flash(message, 'alert-success')
    return redirect('/moto/show')

# Mon filtre de base
@app.route('/moto/filtre', methods=['GET'])
def filtre_moto():
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

    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques
    '''
    mycursor.execute(sql)
    marques= mycursor.fetchall()

    filter_word= request.args.get('filter_word', None)
    filter_value_min = request.args.get('filter_value_min', None)
    filter_value_max = request.args.get('filter_value_max', None)
    filter_items = request.args.getlist('filter_items', None)
    if filter_word and filter_word != "":
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
        WHERE libelle_moto LIKE %s
        '''
        tuple_filter = ('%'+filter_word+'%')
        mycursor.execute(sql, tuple_filter)
        motos= mycursor.fetchall()
        message=u'filtre sur le mot  : '+filter_word
        # flash(message, 'alert-success')
    if filter_value_min or filter_value_max :
        if filter_value_min.isdecimal() and filter_value_max.isdecimal():
            if int(filter_value_min) < int(filter_value_max):
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
                WHERE puissance_moto BETWEEN %s AND %s
                '''
                tuple_filter = (filter_value_min, filter_value_max)
                mycursor.execute(sql, tuple_filter)
                motos= mycursor.fetchall()
                message=u'filtre sur la colonne avec un numérique entre : '+filter_value_min+' et '+filter_value_max
                # flash(message, 'alert-success')
            else :
                message=u'min < max'
                flash(message, 'alert-warning')
        else :
            message=u'min et max doivent être des numériques'
            flash(message, 'alert-warning')
    if filter_items and filter_items != []:
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
        FROM motos
        INNER JOIN marques ON motos.marque_id = marques.id_marque
        WHERE marque_id IN ({})
        '''.format(', '.join(['%s'] * len(filter_items)))
        mycursor.execute(sql, filter_items)
        motos = mycursor.fetchall()
        print(motos)
        message = 'case à cocher selectionnée : '
        for case in filter_items:
            message += 'id : ' + case + ' '
        # flash(message, 'alert-success')

    return render_template('/moto/filtre_moto.html', moto=motos, brand=marques, filter_word=filter_word, filter_value_min=filter_value_min, filter_value_max=filter_value_max, filter_items=filter_items)


# Filtre avec les cookies de session que je n'arrive pas encore à faire fonctionner
@app.route('/moto/filtre2', methods=['GET'])
def filtre_moto_session():
    mycursor = get_db().cursor()

    # Récupérer les valeurs des filtres depuis la session
    filter_word = session.get('filter_word', None)
    filter_value_min = session.get('filter_value_min', None)
    filter_value_max = session.get('filter_value_max', None)
    filter_items = session.get('filter_items', [])

    # Appliquer les filtres
    motos = apply_filters(mycursor, filter_word, filter_value_min, filter_value_max, filter_items)

    # Récupérer les marques
    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques
    '''
    mycursor.execute(sql)
    marques= mycursor.fetchall()

    return render_template('/moto/filtre_moto.html', moto=motos, brand=marques,filter_word=filter_word, filter_value_min=filter_value_min, filter_value_max=filter_value_max, filter_items=filter_items)

def apply_filters(mycursor, filter_word=None, filter_value_min=None, filter_value_max=None, filter_items=None):
    # Initialisation des variables SQL et des paramètres
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
    list_param = []

    # Conditions basées sur les filtres
    if filter_word:
        sql += " WHERE nom LIKE %s "
        recherche = "%" + filter_word + "%"
        list_param.append(recherche)

    if filter_value_min or filter_value_max:
        if filter_word:
            sql += " AND "
        else:
            sql += " WHERE "
        sql += "puissance_moto BETWEEN %s AND %s "
        list_param.append(filter_value_min or 0)
        list_param.append(filter_value_max or float('inf'))

    if filter_items:
        if filter_word or filter_value_min or filter_value_max:
            sql += " AND ("
        else:
            sql += " WHERE ("

        last_item = filter_items[-1]
        for item in filter_items:
            sql += " marque_id = %s "
            if item != last_item:
                sql += " or "
            list_param.append(item)
        sql += ")"

    # Exécution de la requête
    mycursor.execute(sql, tuple(list_param))
    motos = mycursor.fetchall()

    return motos

@app.route('/moto/filtre2', methods=['POST'])
def valid_moto_filtre_session():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    return redirect('/moto/filtre2')



@app.route('/moto/filtre/suppr', methods=['POST'])
def filtre_moto_suppr():
    session.pop('filter_word', None)
    session.pop('filter_value_min', None)
    session.pop('filter_value_max', None)
    session.pop('filter_items', None)
    return redirect('/moto/filtre')


@app.route('/moto/etat', methods=['GET'])
def etat_moto():
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

    sql='''
    SELECT marques.id_marque AS id,
    marques.libelle_marque AS nom,
    marques.logo_marque AS logo
    FROM marques
    '''
    mycursor.execute(sql)
    marques= mycursor.fetchall()

    sql = '''
    SELECT COUNT(*) AS nb, marque_id
    FROM motos
    GROUP BY marque_id
    '''
    mycursor.execute(sql)
    nb_motos_marque = mycursor.fetchall()
    
    return render_template('/etat.html', moto=motos, brand=marques, nb_motos_marque=nb_motos_marque)


if __name__ == '__main__':
    app.run() 


