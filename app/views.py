import json, random

from flask import Flask, jsonify, render_template, redirect, request, flash, url_for
from flask import session as browser_session
import model as m 
from model import db_session

from sqlalchemy import desc

from api_calls import algorithm

from seed import add_to_db

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"


@app.route("/")
def index():

    # get random song from db to start 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    row = db_session.query(m.Track)[rand]

    spotify_track_uri = row.spotify_track_uri
    patterns = row.patterns

    print "PATTERNS: ", patterns
    print type(patterns)

    return render_template("index.html", patterns=patterns, spotify_track_uri=spotify_track_uri)

@app.route("/get_random_patterns")
def get_random_pattern():

    # get random song from db to start 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    row = db_session.query(m.Track)[rand]

    spotify_track_uri = row.spotify_track_uri
    patterns = row.patterns

    return patterns

# @app.route("/new_song")
# def get_new_song():
    
#     title = request.args.get("title")
#     artist_name = request.args.get("artist_name")

#     # check to see if song is in database. 
#     song = m.search(artist_name, title)

#     if song:
#         spotify_track_uri = song.spotify_track_uri
#         patterns = song.patterns


#     # If it is not in the db yet, call Echonest to get it
#     else:
#         song_data = algorithm(artist_name, title)

#         add_to_db(db_session, song_data)
        
#         # keep track uri for web player
#         spotify_track_uri = song_data["spotify_track_uri"]
#         patterns = song_data["patterns"]

#     return render_template("new_song.html", patterns=patterns, spotify_track_uri=spotify_track_uri) 

@app.route("/get_patterns")
def get_pattern():

    title = request.args.get("title")
    artist_name = request.args.get("artist_name")
    print title, artist_name
    
    # check to see if song is in database. 
    song = m.search(artist_name, title)

    if song:
        patterns = song.patterns
        return patterns
    # If it is not in the db yet, call Echonest to get it
    else:
        song_data = algorithm(artist_name, title)

        add_to_db(db_session, song_data)
        
        # keep track uri for web player
        spotify_track_uri = song_data["spotify_track_uri"]
        patterns = song_data["patterns"]

        return patterns
    # return render_template("new_song.html", patterns=patterns, spotify_track_uri=spotify_track_uri) 


@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


