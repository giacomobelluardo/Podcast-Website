from flask import Flask, render_template, request, session, redirect, flash, url_for
from datetime import date, datetime
from flask_session import Session
import dao
import os

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from PIL import Image

# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

#FUNZIONI RELATIVE ALL'INTERAZIONE DI UN UTENTE/NAVIGATORE

#Visualizza la home del sito web, con tutti i singoli podcast
@app.route('/', methods=['GET', 'POST'])
def home():
    podcasts = dao.get_podcasts()

    return render_template('home.html', podcasts = podcasts)

#Visualizza la home del sito web, con un filtro attivato in base alla categoria selezionata
@app.route('/home/<int:id>')
def home_filtr(id):
    categoria = dao.get_categoria(id)
    podcasts = dao.get_podcasts_categoria(categoria[0])

    return render_template('home.html', podcasts = podcasts)

#Visualizza un singolo podcast, con tutti i suoi episodi
@app.route('/podcasts/<int:id>')
def podcast(id):
    podcast = dao.get_podcast(id)
    episodes = dao.get_episodes(id)
    follows = dao.num_follows(id)
    creator = dao.get_name_creator(podcast['id_creatore'])
    comments = []

    #Gestione commenti
    episodio = [dict(episode) for episode in episodes]
    for i in range(len(episodio)):
        ep_comments = dao.get_comments(episodio[i]['id_episodio'])
        for ep_comment in ep_comments:
            comments.append(ep_comment)
    
    return render_template('podcast.html', podcast = podcast, episodes = episodes, follows = follows, creator = creator[0], comments = comments)

#Gestione del pulsante follow eseguito da un utente loggato
@app.route('/follow', methods=['GET', 'POST'])
def follow():
    id_podcast = request.form.get('id_podcast')

    is_in_it = dao.is_in_db(id_podcast, current_user.id)

    if is_in_it is True:
        flash('Attenzione lo segui già', 'danger')
    else:
        dao.new_follow(current_user.id, id_podcast)

    return redirect(url_for('podcast', id = id_podcast))

#Gestione dell'unfollow eseguito da un utente loggato
@app.route('/unfollow', methods=['GET', 'POST'])
def unfollow():
    id_podcast = request.form.get('id_podcast')

    is_in_it = dao.is_in_db(id_podcast, current_user.id)

    if is_in_it is True:
          dao.less_follow(current_user.id, id_podcast)
    else:
        flash('Attenzione, non lo segui', 'danger')

    return redirect(url_for('podcast', id = id_podcast))

#Gestione dell'inserimento di un nuovo commento relativo all'episodio
@app.route('/commenti/new', methods=['POST'])
def new_comment():
    commento = request.form.to_dict()

    if commento['testo'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        flash(
            'Commento non creato correttamente: il commento non può essere vuoto!', 'danger')
        return redirect(url_for('podcast', id=commento['id_podcast']))                 

    success = dao.add_comment(commento, current_user.id, current_user.nome)
             
    if success:
        flash('Commento creato correttamente', 'success')
    else:
        flash('Errore nella creazione del commento: riprova!', 'danger')

    return redirect(url_for('podcast', id=commento['id_podcast']))

#Gestione della modifica di un commento relativo ad un episodio e col suo rispettivo utente 
@app.route('/commenti/change', methods=['POST'])
def change_comment():
    commento = request.form.to_dict()
    if commento['testo'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        flash(
            'Commento non modificato correttamente: il commento non può essere vuoto!', 'danger')
        return redirect(url_for('podcast', id=commento['id_episodio']))                 #NOTA: questa parte potrebbe dare problems, la parte di id_episodio

    success = dao.change_comment(commento)

    if success:
        flash('Commento modificato correttamente', 'success')
    else:
        flash('Errore nella modifica del commento: riprova!', 'danger')

    return redirect(url_for('podcast', id=commento['id_podcast']))

#Gestione della cancellazione di un commento
@app.route('/commenti/delete', methods=['GET', 'POST'])
def delete_comment():
    commento = request.form.to_dict()

    success = dao.delete_comment(commento['id_commento'])

    if success:
        flash('Commento eliminato correttamente', 'success')
    else:
        flash('Errore nella cancellazione del commento: riprova!', 'danger')

    return redirect(url_for('podcast', id = commento['id_podcast']))

#Gestione dell'inserimento di un nuovo podcast
@app.route('/podcasts/new', methods=['GET', 'POST'])
def new_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated:

            podcast = request.form.to_dict()

            if podcast['titolo'] == '':
                app.logger.error('Il podcast deve avere un titolo!')
                flash(
                    'Podcast non creato correttamente: il podcast deve avere un titolo!', 'danger')
                return redirect(url_for('home'))
            
            if podcast['categoria'] == '':
                app.logger.error('Il podcast deve avere una categoria!')
                flash(
                    'Podcast non creato correttamente: il podcast deve avere una categoria!', 'danger')
                return redirect(url_for('home'))
            
            print(podcast['categoria'])
            
            if podcast['descrizione'] == '':
                app.logger.error('Il podcast deve avere una descrizione!')
                flash(
                    'Podcast non creato correttamente: il podcast deve avere una descrizione!', 'danger')
                return redirect(url_for('home'))

            podcast_image = request.files['immagine']

            if podcast_image:
                if podcast_image.filename.endswith(".jpeg") or podcast_image.filename.endswith('.jpg') or podcast_image.filename.endswith(".png"):
                    img = Image.open(podcast_image)

                    width, height = img.size
                    new_height = height/width * POST_IMG_WIDTH
                    size = POST_IMG_WIDTH, new_height

                    img.thumbnail(size, Image.ANTIALIAS)

                    img.save('static/' + podcast_image.filename)
                    podcast['immagine'] = podcast_image.filename
                
                    podcast['id_creatore'] = current_user.id

                    success = dao.new_podcast(podcast)
                else:
                    success = False

            if success:
                flash('Podcast creato correttamente', 'success')
            else:
                flash('Errore nella creazione del podcast, riprova!', 'danger')

    return redirect(url_for('home'))

#Gestione della modifica di un podcast
@app.route('/podcasts/change', methods=['GET', 'POST'])
def change_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated:

            podcast = request.form.to_dict()

            if podcast['titolo'] == '':
                titolo = podcast['old_tit']
            else:
                titolo = podcast['titolo']
            
            if podcast['descrizione'] == '':
                descrizione = podcast['old_descr']
            else:
                descrizione = podcast['descrizione']
            
            podcast_image = request.files['immagine']

            if podcast_image.filename == '':
                immagine = podcast['old_immagine']
            else:
                os.remove(os.path.join('static', podcast['old_immagine']))

                if podcast_image.filename.endswith(".jpeg") or podcast_image.filename.endswith('.jpg') or podcast_image.filename.endswith(".png"):

                    img = Image.open(podcast_image)

                    width, height = img.size
                    new_height = height/width * POST_IMG_WIDTH
                    size = POST_IMG_WIDTH, new_height

                    img.thumbnail(size, Image.ANTIALIAS)

                    img.save('static/' + podcast_image.filename)
                    immagine = podcast_image.filename
                else:
                    flash('Errore nella modifica del podcast, riprova!', 'danger')
                    return redirect(url_for('podcast', id = podcast['id_podcast']))

            success = dao.mod_podcast(podcast['id_podcast'], titolo, descrizione, immagine)

            if success:
                flash('Podcast modificato correttamente', 'success')
            else:
                flash('Errore nella modifica del podcast, riprova!', 'danger')
    
    return redirect(url_for('podcast', id = podcast['id_podcast']))

#Gestione dell'eliminazione di un podcast
@app.route('/podcasts/delete', methods=['GET', 'POST'])
def delete_podcast():
    if request.method == 'POST':
        if current_user.is_authenticated:

            #Rimozione file all'interno di un podcast
            podcast = request.form.to_dict()
            os.remove(os.path.join('static', podcast['old_immagine']))

            episodes = dao.get_episodes(podcast['id_podcast'])
            episodio = [dict(episode) for episode in episodes]
            for i in range(len(episodio)):
                os.remove(os.path.join('static', episodio[i]['file_audio']))

            success = dao.delete_podcast(podcast['id_podcast'])

            if success:
                flash('Podcast eliminato correttamente', 'success')
            else:
                flash('Errore nella cancellazione del podcast, riprova!', 'danger')
    
    return redirect(url_for('home'))

#Gestione dell'inserimento di un nuovo episodio
@app.route('/episodi/new', methods=['GET', 'POST'])
def new_episode():
    if request.method == 'POST':
        if current_user.is_authenticated:

            episode = request.form.to_dict()

            if episode['titolo'] == '':
                app.logger.error('L\'episodio deve avere un titolo!')
                flash(
                    'Episodio non creato correttamente: l\'episodio deve avere un titolo!', 'danger')
                return redirect(url_for('home'))
            
            if episode['descrizione'] == '':
                app.logger.error('L\'episodio deve avere una categoria!')
                flash(
                    'Episodio non creato correttamente: l\'episodio deve avere una categoria!', 'danger')
                return redirect(url_for('home'))

            episode_audio = request.files['file_audio']

            if episode_audio:
                if episode_audio.filename.endswith(".m4a") or episode_audio.filename.endswith('.mp3'):
                    episode_audio.save('static/' + episode_audio.filename)
                    episode['file_audio'] = episode_audio.filename

                    success = dao.new_episode(episode)
                else:
                    success = False

            if success:
                flash('Episodio creato correttamente', 'success')
            else:
                flash('Errore nella creazione dell\'episodio, riprova!', 'danger')

    return redirect(url_for('home'))

#Gestione della modifica di un episodio
@app.route('/episodi/change', methods=['GET', 'POST'])
def change_episode():
    if request.method == 'POST':
        if current_user.is_authenticated:

            episode = request.form.to_dict()

            if episode['titolo'] == '':
                titolo = episode['old_tit']
            else:
                titolo = episode['titolo']
            
            if episode['descrizione'] == '':
                descrizione = episode['old_descr']
            else:
                descrizione = episode['descrizione']

            episode_audio = request.files['file_audio']

            if episode_audio.filename == '':
                audio = episode['old_audio']
            else:
                if episode_audio.filename.endswith(".m4a") or episode_audio.filename.endswith('.mp3'):
                    os.remove(os.path.join('static', episode['old_audio']))
                    episode_audio.save('static/' + episode_audio.filename)
                    audio = episode_audio.filename
                else:
                    flash('Errore nella modifica dell\'episodio, riprova!', 'danger')
                    return redirect(url_for('podcast', id = episode['id_podcast']))

            success = dao.mod_episode(episode['id_episodio'], titolo, descrizione, audio)     

            if success:
                flash('Episodio modificato correttamente', 'success')
            else:
                flash('Errore nella modifica dell\'episodio, riprova!', 'danger')
    
    return redirect(url_for('podcast', id = episode['id_podcast']))

#Gestione della cancellazione di un episodio
@app.route('/episodi/delete', methods=['GET', 'POST'])
def delete_episode():
    if request.method == 'POST':
        if current_user.is_authenticated:

            episode = request.form.to_dict()
            os.remove(os.path.join('static', episode['old_audio']))

            success = dao.delete_episode(episode['id_episodio'])

            if success:
                flash('Episodio eliminato correttamente', 'success')
            else:
                flash('Errore nella cancellazione dell\'episodio, riprova!', 'danger')
    
    return redirect(url_for('podcast', id=episode['id_podcast']))

#Visualizzazione del profilo di un utente loggato
@app.route('/profile')
def about():
    follow_podcasts = []

    num_fol = dao.get_follows(current_user.id)
    followings = dao.get_idpodcast(current_user.id)
    follow = [dict(following) for following in followings]
    for i in range(len(follow)):
        title = dao.get_podcastname_from_id(follow[i]['id_podcast'])
        follow_podcasts.append(title[0])

    return render_template("profile.html", followers = num_fol[0], follow_p = follow_podcasts)

#Gestione pagina di errore 404
@app.errorhandler(404)
def invalid_request(e):
    return render_template("error.html", error = "URL non valido, si prega di riprovare.")


#FUNZIONI RELATIVE AL LOGIN/SIGNUP/LOGOUT

#Gestione della registrazione di un utente al sito web
@app.route('/iscriviti')
def signup():
    return render_template('signup.html')

@app.route('/iscriviti', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db = dao.get_user_by_email(email)

    if user_in_db:
        flash('Esiste già un utente registrato con questa email', 'danger')
        return redirect(url_for('signup'))
    else:
        nome = request.form.get('nome')
        usr_tipo = request.form.get('tipo')

        if usr_tipo == 'Creatore':
            tipo = 1
        elif usr_tipo == 'Ascoltatore':
            tipo = 2
        new_user = {
            "email": email,
            "password": generate_password_hash(password, method='sha256'),
            "nome": nome,
            "tipo": tipo
        }

        success = dao.add_user(new_user)

        if success:
            if tipo == 1:
                flash('Utente creatore creato correttamente', 'success')
                return redirect(url_for('home'))
            elif tipo == 2:
                flash('Utente ascoltatore creato correttamente', 'success')
                return redirect(url_for('home'))
        else:
            flash('Errore nella creazione dell\'utente: riprova!', 'danger')

    return redirect(url_for('signup'))

#Gestione del caricamento di un utente
@login_manager.user_loader
def load_user(id):

    utente = dao.get_user_by_id(id)

    if utente is not None:
        user = User(id=utente['id_utente'], email=utente['email'], password=utente['password'], nome=utente['nome'], tipo=utente['tipo'])
    else:
        user = None

    return user

#Gestione del login di un utente
@app.route('/accedi')
def login():
    return render_template('login.html')


@app.route('/accedi', methods=['POST'])
def login_podcast():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.get_user_by_email(email)
    print(check_password_hash(user['password'], password))

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    else:
        new = User(id=user['id_utente'], email=user['email'], password=user['password'],
                   nome=user['nome'], tipo=user['tipo'])
        print(new)
        login_user(new, True)

        return redirect(url_for('home'))

#Gestione del logout di un utente
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)