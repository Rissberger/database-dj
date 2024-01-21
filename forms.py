from wtforms import SelectField, StringField, TextAreaField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class PlaylistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit_playlist = SubmitField('Create Playlist')

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    submit_song = SubmitField('Add Song')

class NewSongForPlaylistForm(FlaskForm):
    song = SelectField('Song To Add', coerce=int, validators=[DataRequired()])
    submit_add_song = SubmitField('Add Song')
