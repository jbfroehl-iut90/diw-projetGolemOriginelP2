DROP TABLES IF EXISTS motos, marques;

CREATE TABLE marques (
    id_marque INT NOT NULL AUTO_INCREMENT,
    libelle_marque VARCHAR(255) NOT NULL,
    logo_marque VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_marque)
);

CREATE TABLE motos (
    id_moto INT NOT NULL AUTO_INCREMENT,
    libelle_moto VARCHAR(255) NOT NULL,
    puissance_moto INT NOT NULL,
    date_mise_en_circulation DATE NOT NULL,
    couleur_moto VARCHAR(255) NOT NULL,
    marque_id INT NOT NULL,
    photo_moto VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_moto),
    FOREIGN KEY (marque_id) REFERENCES marques(id_marque) ON DELETE CASCADE
);

INSERT INTO marques VALUES 
    (NULL, 'Yamaha', 'logo-yamaha.jpg'),
    (NULL, 'Honda', 'logo-Honda.png'),
    (NULL, 'Kawasaki', 'logo-kawasaki.jpg'),
    (NULL, 'BMW', 'logo-bmw.png'),
    (NULL, 'Suzuki', 'logo-Suzuki.png'),
    (NULL, 'Triumph', 'logo-Triumph.jpg'),
    (NULL, 'Piaggio', 'logo-Piaggio.png'),
    (NULL, 'KTM', 'logo-KTM.png'),
    (NULL, 'Ducati', 'logo-Ducati.png'),
    (NULL, 'Harley Davidson', 'logo-Harley-Davidson.png'),
    (NULL, 'Kymco', 'logo-kymco.jpg'),
    (NULL, 'Aprilia', 'logo-aprilia.jpg');

INSERT INTO motos VALUES 
    (NULL, 'T-MAX', 400, '2012-06-15', 'black', 1, 'T-MAX-noir.jpg'),
    (NULL, 'Niken', 350, '2007-06-15', 'yellow', 1, 'niken.jpg'),
    (NULL, 'MT09', 250, '2015-06-15', 'red', 1, 'mt09.jpg'),
    (NULL, 'X-MAX', 450, '2019-06-15', 'orange', 1, 'xmax.jpg'),
    (NULL, 'MT09-Tracer', 100, '2001-06-15', 'purple', 1, 'mt09tracer.jpg'),
    (NULL, 'Africa Twin', 500, '1999-07-21', 'white', 2, 'AFRICA_TWIN.jpg'),
    (NULL, 'Pan European', 1500, '2000-09-30', 'black', 2, 'panEuropean.jpg'),
    (NULL, 'Sh', 150, '2020-09-30', 'black', 2, 'sh.jpg'),
    (NULL, 'Swing', 200, '2021-09-30', 'black', 2, 'swing.jpg'),
    (NULL, 'PS', 6, '2017-09-30', 'black', 2, 'ps.jpeg'),
    (NULL, 'Deauville', 100, '2010-09-30', 'black', 2, 'deauville.jpg'),
    (NULL, 'A1', 100, '2025-08-27', 'green', 3, 'a1.jpg'),
    (NULL, 'H2', 1000, '2020-08-27', 'green', 3, 'h2.jpg'),
    (NULL, 'VN', 500, '2024-08-27', 'green', 3, 'vn.jpg'),
    (NULL, 'Z', 200, '2023-08-27', 'green', 3, 'z.jpg'),
    (NULL, 'Ninja 400', 400, '2022-08-27', 'green', 3, 'ninja400.jpg'),
    (NULL, 'Vulcan 650', 650, '2021-08-27', 'green', 3, 'vulcan250.jpg'),
    (NULL, 'K 1600', 1600, '2010-08-27', 'blue', 4, 'k1600.jpg'),
    (NULL, 'F 900 XR', 900, '2011-08-27', 'blue', 4, 'f900xr.jpg'),
    (NULL, 'R 1250 R', 1250, '2012-08-27', 'blue', 4, 'r1250r.jpeg'),
    (NULL, 'R 1200 RT', 1200, '2013-08-27', 'blue', 4, 'r1200rt.jpg'),
    (NULL, 'R 900 RT', 900, '2014-08-27', 'blue', 4, 'r900rt.jpg'),
    (NULL, 'S 1000 SR', 1000, '2015-08-27', 'blue', 4, 's1000sr.jpeg');


-- Exemple de requête préparée pour modifier une moto (celle avec l'id 9) :
SET @nouveau_nom = 'Yamaha YZF R6';
SET @nouvelle_photo = 'ninja400.jpg';
SET @id_moto = '9';
SET @nouvelle_puissance = '3000';
SET @nouvelle_mise_en_circulation = '2023-12-06';
SET @nouvelle_couleur = 'bleu';
SET @marque_id = 1;

PREPARE stmt FROM 'UPDATE motos SET libelle_moto = ?, puissance_moto = ?, date_mise_en_circulation = ?, couleur_moto = ?, marque_id = ?, photo_moto = ? WHERE id_moto = ?'

EXECUTE stmt USING @nouveau_nom, @nouvelle_puissance, @nouvelle_mise_en_circulation, @nouvelle_couleur, @marque_id, @nouvelle_photo, @id_moto

DEALLOCATE PREPARE stmt