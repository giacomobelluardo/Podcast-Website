import sqlite3
import datetime

#Funzione che mi restituisce tutti i podcast presenti nel Database del sito
def get_podcasts():
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PODCAST.id_podcast, PODCAST.id_creatore, PODCAST.titolo, PODCAST.descrizione, PODCAST.categoria, PODCAST.immagine FROM PODCAST'
    cursor.execute(sql)
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts

#Funzione che mi restituisce il nome di una categoria
def get_categoria(id):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT CATEGORIE.categoria FROM CATEGORIE WHERE CATEGORIE.id=?'
    cursor.execute(sql, (id,))
    categoria = cursor.fetchone()

    cursor.close()
    conn.close()

    return categoria

#Funzione che mi restituisce tutti i podcast appartenenti ad una categoria
def get_podcasts_categoria(categoria):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM PODCAST WHERE PODCAST.categoria=?'
    cursor.execute(sql, (categoria,))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts

#Funzione che mi restituisce un singolo podcast 
def get_podcast(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PODCAST.id_podcast, PODCAST.id_creatore, PODCAST.titolo, PODCAST.descrizione, PODCAST.categoria, PODCAST.immagine FROM PODCAST WHERE id_podcast = ?'
    cursor.execute(sql, (id_podcast,))
    podcast = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast

#Funzione che mi restituisce il nome di un creatore podcast dato il suo id
def get_name_creator(id_utente):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT UTENTI.nome FROM UTENTI WHERE UTENTI.id_utente = ?'
    cursor.execute(sql, (id_utente,))
    nome = cursor.fetchone()

    cursor.close()
    conn.close()

    return nome

#Funzione che mi restituisce gli episodi relativi ad un podcast, dato il suo id
def get_episodes(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT EPISODI.id_episodio, EPISODI.id_podcast, EPISODI.file_audio, EPISODI.titolo, EPISODI.descrizione, EPISODI.data FROM EPISODI  WHERE EPISODI.id_podcast = ?'
    cursor.execute(sql, (id_podcast,))
    episodes = cursor.fetchall()

    cursor.close()
    conn.close()

    return episodes

#Funzione che mi crea un podcast
def new_podcast(podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO PODCAST(id_creatore, titolo, descrizione, categoria, immagine) VALUES(?,?,?,?,?)'
    cursor.execute(sql, (podcast['id_creatore'], podcast['titolo'], podcast['descrizione'], podcast['categoria'], podcast['immagine']))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE CREAZIONE PODCAST', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi modifica un podcast relativo al suo creatore
def mod_podcast(id_podcast, titolo, descrizione, immagine):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE PODCAST SET titolo=?, descrizione=?, immagine=? WHERE id_podcast=?'
    cursor.execute(sql, (titolo, descrizione, immagine, id_podcast))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE MODIFICA PODCAST', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi elimina un podcast relativo al suo creatore
def delete_podcast(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM PODCAST WHERE id_podcast = ?'
    cursor.execute(sql, (id_podcast, ))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE ELIMINAZIONE PODCAST', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi crea un episodio
def new_episode(episode):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    x = datetime.datetime.now()

    success = False
    sql = 'INSERT INTO EPISODI(id_podcast, file_audio, titolo, descrizione, data) VALUES(?,?,?,?,?)'
    cursor.execute(sql, (episode['id_podcast'], episode['file_audio'], episode['titolo'], episode['descrizione'], x.strftime("%Y-%m-%d")))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE CREAZIONE EPISODIO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi modifica un episodio
def mod_episode(id_episodio, titolo, descrizione, audio):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    x = datetime.datetime.now()

    success = False
    sql = 'UPDATE EPISODI SET titolo=?, descrizione=?, data=?, file_audio=? WHERE id_episodio=?'
    cursor.execute(sql, (titolo, descrizione, x.strftime("%Y-%m-%d"), audio, id_episodio))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE MODIFICA EPISODIO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzioen che mi cancella un episodio
def delete_episode(id_episode):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")

    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM EPISODI WHERE id_episodio = ?'
    cursor.execute(sql, (id_episode, ))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE ELIMINAZIONE EPISODIO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che gestisce l'inserimento di un nuovo follower
def new_follow(id_utente, id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'INSERT INTO FOLLOW(id_utente, id_podcast) VALUES (?, ?)'
    cursor.execute(sql, (id_utente, id_podcast))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE, SEGUI GIA\'', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che gestisce la rimozione di un follower
def less_follow(id_utente, id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'DELETE FROM FOLLOW WHERE id_utente=? AND id_podcast=?'
    cursor.execute(sql, (id_utente, id_podcast))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE, NON LO SEGUIVI', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi restituisce l'elenco di podcast seguiti da un utente
def get_follows(id_utente):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT COUNT(id_podcast) FROM FOLLOW WHERE id_utente = ?'
    cursor.execute(sql, (id_utente, ))
    follows = cursor.fetchone()

    cursor.close()
    conn.close()

    return follows

#Funzione che mi restituisce il numero complessivo di follower di un podcast
def num_follows(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT COUNT(FOLLOW.id_utente) FROM FOLLOW WHERE FOLLOW.id_podcast = ?'
    cursor.execute(sql, (id_podcast, ))
    num = cursor.fetchone()

    cursor.close()
    conn.close()

    return num[0]

#Funzione che mi restituisce i podcast seguiti in base all'utente
def get_idpodcast(id_utente):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT FOLLOW.id_podcast FROM FOLLOW WHERE FOLLOW.id_utente=?'
    cursor.execute(sql, (id_utente,))
    ids = cursor.fetchall()

    cursor.close()
    conn.close()

    return ids

def get_podcastname_from_id(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PODCAST.titolo FROM PODCAST WHERE PODCAST.id_podcast=?'
    cursor.execute(sql, (id_podcast,))
    tit = cursor.fetchone()

    cursor.close()
    conn.close()

    return tit


#Funzione che mi elimina una entry dalla tabella dei follower di un podcast
def delete_follows(id_podcast):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM FOLLOW WHERE id_podcast = ?'
    cursor.execute(sql, (id_podcast, ))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE ELIMINAZIONE ENTRY FOLLOW', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return

#Funzione che mi dice quante volte quel podcast è seguito da un utente
def is_in_db(id_podcast, id_utente):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    success = False
    sql = 'SELECT * FROM FOLLOW WHERE id_podcast=? AND id_utente=?'
    cursor.execute(sql, (id_podcast, id_utente))
    result = cursor.fetchone()

    if result is None:
        success = False
    else:
        success = True

    cursor.close()
    conn.close()

    return success

#Funzione che mi restituisce i commenti relativi ad un episodio, dato il suo id
def get_comments(id):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM COMMENTI WHERE COMMENTI.id_episodio=?'
    cursor.execute(sql, (id, ))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments

#Funzione che mi crea un nuovo commento
def add_comment(commento, id_utente, nome):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'INSERT INTO COMMENTI(id_utente, id_episodio, nome, testo, data) VALUES(?,?,?,?,?)'
    cursor.execute(sql, (id_utente, commento['id_episodio'], nome, commento['testo'], x.strftime("%Y-%m-%d")))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE INSERIMENTO COMMENTO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che modifica un commento
def change_comment(commento):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'UPDATE COMMENTI SET testo = ?, data = ? WHERE id_commento = ?'
    cursor.execute(sql, (commento['testo'], x.strftime("%Y-%m-%d"), commento['id_commento']))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE MODIFICA COMMENTO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi elimina un commento
def delete_comment(id_commento):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'DELETE FROM COMMENTI WHERE id_commento = ?'
    cursor.execute(sql, (id_commento, ))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE MODIFICA COMMENTO', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi restituisce il nome dell'utente che ha lasciato il commento
def get_name_by_id(id):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT UTENTI.nome FROM UTENTI WHERE UTENTI.id_utente=?'
    cursor.execute(sql, (id, ))
    name = cursor.fetchall()

    cursor.close()
    conn.close()

    return name

#Funzione che mi restituisce l'utente inserendo la mail come input
def get_user_by_email(email):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT UTENTI.id_utente, UTENTI.email, UTENTI.password, UTENTI.nome, UTENTI.tipo FROM UTENTI WHERE UTENTI.email=?'
    cursor.execute(sql, (email, ))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#Funzione che aggiunge un nuovo utente all'interno della tabella UTENTI
def add_user(new_user):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO UTENTI(email,password, nome, tipo) VALUES(?,?,?,?)'

    try:
        cursor.execute(
            sql, (new_user['email'], new_user['password'], new_user['nome'], new_user['tipo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERRORE INSERIMENTO UTENTE', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#Funzione che mi restituisce un utente dato l'id
def get_user_by_id(id):
    conn = sqlite3.connect('db/podcast_site.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE id_utente = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user