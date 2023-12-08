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

marques = [
 {'id' : 1, 'libelle':'Yamaha', 'logo':'logo-yamaha.jpg'},
 {'id' : 2, 'libelle':'Honda', 'logo':'logo-Honda.png'},
 {'id' : 3, 'libelle':'Kawasaki','logo':'logo-kawasaki.jpg'},
 {'id' : 4, 'libelle':'BMW', 'logo':'logo-bmw.png'},
 {'id' : 5, 'libelle':'Suzuki', 'logo':'logo-Suzuki.png'},
 {'id' : 6, 'libelle':'Triumph','logo':'logo-Triumph.jpg'},
 {'id' : 7, 'libelle':'Piaggio','logo':'logo-Piaggio.png'},
 {'id' : 8, 'libelle':'KTM', 'logo':'logo-KTM.png'},
 {'id' : 9, 'libelle':'Ducati', 'logo':'logo-Ducati.png'},
 {'id' : 10, 'libelle':'Harley Davidson', 'logo':'logo-Harley-Davidson.png'},
 {'id' : 11, 'libelle':'Kymco', 'logo':'logo-kymco.jpg'},
 {'id' : 12, 'libelle':'Aprilia','logo':'logo-aprilia.jpg'}
]

motos = [
 {'id' : 1, 'nomMoto':'T-MAX', 'puissance':400, 'DateMiseEnCirculation':'2012-06-15', 'couleur':'black', 'marque_id':1, 'photo':'T-MAX-noir.jpg'},
 {'id' : 2, 'nomMoto':'Niken', 'puissance':350, 'DateMiseEnCirculation':'2007-06-15', 'couleur':'yellow', 'marque_id':1, 'photo':'niken.jpg'},
 {'id' : 3, 'nomMoto':'MT09', 'puissance':250, 'DateMiseEnCirculation':'2015-06-15', 'couleur':'red', 'marque_id':1, 'photo':'mt09.jpg'},
 {'id' : 4, 'nomMoto':'X-MAX', 'puissance':450, 'DateMiseEnCirculation':'2019-06-15', 'couleur':'orange', 'marque_id':1, 'photo':'xmax.jpg'},
 {'id' : 5, 'nomMoto':'MT09-Tracer', 'puissance':100, 'DateMiseEnCirculation':'2001-06-15', 'couleur':'purple', 'marque_id':1, 'photo':'mt09tracer.jpg'},
 {'id' : 6, 'nomMoto':'Africa Twin', 'puissance':500, 'DateMiseEnCirculation':'1999-07-21', 'couleur':'white', 'marque_id':2, 'photo':'AFRICA_TWIN.jpg'},
 {'id' : 7, 'nomMoto':'Pan European', 'puissance':1500, 'DateMiseEnCirculation':'2000-09-30', 'couleur':'black', 'marque_id':2, 'photo':'panEuropean.jpg'},
 {'id' : 8, 'nomMoto':'Sh','puissance':150, 'DateMiseEnCirculation':'2020-09-30', 'couleur':'black', 'marque_id':2, 'photo':'sh.jpg'},
 {'id' : 8, 'nomMoto':'Swing', 'puissance':200, 'DateMiseEnCirculation':'2021-09-30', 'couleur':'black', 'marque_id':2, 'photo':'swing.jpg'},
 {'id' : 10, 'nomMoto':'PS','puissance':6, 'DateMiseEnCirculation':'2017-09-30', 'couleur':'black', 'marque_id':2, 'photo':'ps.jpeg'},
 {'id' : 11, 'nomMoto':'Deauville', 'puissance':100, 'DateMiseEnCirculation':'2010-09-30', 'couleur':'black', 'marque_id':2, 'photo':'deauville.jpg'},
 {'id' : 12, 'nomMoto':'A1','puissance':100, 'DateMiseEnCirculation':'2025-08-27', 'couleur':'green', 'marque_id':3, 'photo':'a1.jpg'},
 {'id' : 13, 'nomMoto':'H2','puissance':1000, 'DateMiseEnCirculation':'2020-08-27', 'couleur':'green', 'marque_id':3, 'photo':'h2.jpg'},
 {'id' : 14, 'nomMoto':'VN','puissance':500, 'DateMiseEnCirculation':'2024-08-27', 'couleur':'green', 'marque_id':3, 'photo':'vn.jpg'},
 {'id' : 15, 'nomMoto':'Z', 'puissance':200, 'DateMiseEnCirculation':'2023-08-27', 'couleur':'green', 'marque_id':3, 'photo':'z.jpg'},
 {'id' : 16, 'nomMoto':'Ninja 400', 'puissance':400, 'DateMiseEnCirculation':'2022-08-27', 'couleur':'green', 'marque_id':3, 'photo':'ninja400.jpg'},
 {'id' : 17, 'nomMoto':'Vulcan 650', 'puissance':650, 'DateMiseEnCirculation':'2021-08-27', 'couleur':'green', 'marque_id':3, 'photo':'vulcan250.jpg'},
 {'id' : 18, 'nomMoto':'K 1600', 'puissance':1600, 'DateMiseEnCirculation':'2010-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'k1600.jpg'},
 {'id' : 19, 'nomMoto':'F 900 XR', 'puissance':900, 'DateMiseEnCirculation':'2011-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'f900xr.jpg'},
 {'id' : 20, 'nomMoto':'R 1250 R', 'puissance':1250, 'DateMiseEnCirculation':'2012-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'r1250r.jpeg'},
 {'id' : 21, 'nomMoto':'R 1200 RT', 'puissance':1200, 'DateMiseEnCirculation':'2013-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'r1200rt.jpg'},
 {'id' : 22, 'nomMoto':'R 900 RT', 'puissance':900, 'DateMiseEnCirculation':'2014-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'r900rt.jpg'},
 {'id' : 23, 'nomMoto':'S 1000 SR', 'puissance':1000, 'DateMiseEnCirculation':'2015-08-27', 'couleur':'blue', 'marque_id':4, 'photo':'s1000sr.jpeg'}
]

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


