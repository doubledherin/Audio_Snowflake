import json, random
import model as m 
from time import sleep

from flask import Flask, jsonify, render_template, redirect, request, flash, url_for
# from flask import session as browser_session
from sqlalchemy import desc

from model import db_session
from api_calls import algorithm
from add_to_db import add_to_db

app = Flask(__name__)

@app.route("/")
def index():

    # Get a random song from the database to start with 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    track = db_session.query(m.Track)[rand]

    return render_template("index.html", track=track)

@app.route("/get_patterns")
def get_pattern():

    # Get the song title and artist name from the web form
    title = request.args.get("title").lower()
    artist_name = request.args.get("artist_name").lower()
    
    # Check to see if the track is in the database 
    track = m.search(artist_name, title)

    if track:
        return render_template("index.html", track=track)

    # If not, call Echonest to get it
    else:
        song_data = algorithm(artist_name, title)

        # Add it to the database
        add_to_db(db_session, song_data)

        # Get it from the database
        track = m.search(artist_name, title)
        
        return render_template("index.html", track=track) 


@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


