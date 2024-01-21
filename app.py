from flask import Flask, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>", methods=["GET", "POST"])
def show_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    form.song.choices = [(song.id, song.title) for song in Song.query.all()]

    if form.validate_on_submit():
        new_playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=form.song.data)
        db.session.add(new_playlist_song)
        db.session.commit()

        return redirect(url_for('show_playlist', playlist_id=playlist_id))

    return render_template("playlist.html", playlist=playlist, form=form)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        return redirect("/playlists")
    return render_template("new_playlist.html", form=form)

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template("song_detail.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        return redirect("/songs")
    return render_template("new_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist and redirect to playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    
    curr_on_playlist = [song.id for song in playlist.songs]
    form.song.choices = [(s.id, s.title) for s in Song.query.filter(Song.id.notin_(curr_on_playlist)).all()]
    
    if form.validate_on_submit():
        song_id = form.song.data
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        
        return redirect(url_for('show_playlist', playlist_id=playlist_id))

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)
