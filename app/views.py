import json, random

import numpy as np
import pandas as pd

from flask import Flask, render_template, redirect, request, flash, url_for
from flask import session as browser_session
import model as m 
from model import db_session

from sqlalchemy import desc

from api_calls import get_song_data

from seed import add_to_db

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"


@app.route("/")
def index():

    # get random song from db to start 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    row = db_session.query(m.Track)[rand]

    spotify_track_uri = row.spotify_track_uri

    return render_template("index.html", spotify_track_uri=spotify_track_uri)

@app.route("/new_song")
def get_new_song():
    
    title = request.args.get("title")
    artist_name = request.args.get("artist_name")

    # check to see if song is in database. 
    song = m.db_session.query(m.Track).filter_by(title=title).filter_by(artist_name=artist_name).first()

    if song:
        spotify_track_uri = song.spotify_track_uri


    # If it is not in the db yet, call Echonest to get it
    else:
        song_data = get_song_data(artist_name, title)

        add_to_db(db_session, song_data)
        
        # keep track uri for web player
        spotify_track_uri = song_data["spotify_track_uri"]

    return render_template("new_song.html", spotify_track_uri=spotify_track_uri) 

@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


