import base64, json, os, random
import model as m 
from time import sleep

from flask import Flask, jsonify, render_template, redirect, request, flash, url_for

from sqlalchemy import desc
from werkzeug import secure_filename

from model import db_session
from api_calls import algorithm
from add_to_db import add_song_to_db, add_image_to_db



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
    
    # If nothing entered into form, get random song from database
    if artist_name == "" and title == "":
        return redirect("/")

    # If only title entered, check database for that title
    elif artist_name == "":
        track = db_session.query(m.Track).filter_by(title=title).first()

    # If only artist name entered, check database for that artist
    elif title == "":
        track = db_session.query(m.Track).filter_by(artist_name=artist_name).first()

    # If both artist and title entered, check database
    else:
        track = db_session.query(m.Track).filter_by(artist_name=artist_name).filter_by(title=title).first()

    if track:
        return render_template("index.html", track=track)

    # If not, call Echonest to get it
    else:
        try:
            print "MADE IT TO HERE"  
            song_data = algorithm(artist_name, title)

            # Check if the track is in the database 
            # (using the song id supplied by Echonest)
            song_id = song_data["song_id"]

            track = db_session.query(m.Track).filter_by(song_id=song_id).first()


            # If it is in the database
            if track:
                return render_template("index.html", track=track)

            else:
                # Add it to the database
                add_song_to_db(db_session, song_data)

                # Get it from the database
                track = db_session.query(m.Track).filter_by(song_id=song_id).first()
                
                return render_template("index.html", track=track) 

        except:

            # Print error message to screen
            return render_template("index.html", track=None)

@app.route("/add_snowflake", methods=["POST"])
def add_snowflake():
    filename = request.form["song_id"] + ".png"
    image = request.form["img"]
    artist_name = request.form["artist_name"].title()
    title = request.form["title"].title()

    if image:

        # decode base64
        img_type, img_b64data = image.split(",", 1)
        image_data = base64.b64decode(img_b64data)

        # write to a file using the song id as the filename
        fout = open(os.path.join("static/uploads", filename), "wb")
        fout.write(image_data)
        fout.close()

        add_image_to_db(db_session, filename, artist_name, title)

    return "FOO"



@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/gallery")
def gallery_page():

    images = db_session.query(m.Image).all()
    return render_template("gallery.html", images=images)    


if __name__ == "__main__":
    app.run(debug=True)


