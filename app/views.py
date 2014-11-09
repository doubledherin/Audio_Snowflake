import random

from flask import Flask, render_template, redirect, request, flash
from flask import session as browser_session
import model as m 
from model import db_session

from sqlalchemy import desc

from api_calls import get_song_data

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"


@app.route("/")
def index():

    # ALWAYS SAME TRACK TO START
    spotify_track_uri = "spotify:track:5AMrnF761nziCWUfjBgRUI"
    
    # # TO DO: randomly get a spotify_track_id from database
    # rand = random.randrange(0, db_session.query(m.Track).count()) 
    # row = db_session.query(m.Track)[rand]

    # print row.spotify_track_uri


    return render_template("index.html", spotify_track_uri=spotify_track_uri)

@app.route("/new_song")
def get_new_song():
    
    title = request.args.get("title")
    artist_name = request.args.get("artist_name")

    # # check to see if song is in database. 
    # song = m.session.query(m.Track).filter_by(title=title).filter_by(artist_name=artist_name).first()

    # # TO DO: if it is, return information for it and render it on screen
    # # (placeholder below)
    # if song:
    #     song_data = None
    #     print song_data
    # # TO DO: if it is not, call Echonest
    # else:
    song_data = get_song_data(artist_name, title)
    spotify_track_uri = song_data["spotify_track_uri"]

    return render_template("new_song.html", spotify_track_uri=spotify_track_uri) 

if __name__ == "__main__":
    app.run(debug=True)
