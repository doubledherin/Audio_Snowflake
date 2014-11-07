from flask import Flask, render_template, redirect, request, flash
from flask import session as browser_session
import model as m 

from sqlalchemy import desc

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"

@app.route("/")
def index():
    
    # TO DO: randomly get a spotify_track_id from database


    # Right now, it always starts with Southern Belle (Elliott Smith)
    spotify_track_id = "0um6CMHbyaJCr0aHL2OdRU"

    return render_template("index.html", spotify_track_id=spotify_track_id)

@app.route("/new_song")
def get_new_song():
    
    title = request.args.get("title")
    artist_name = request.args.get("artist_name")

    # check to see if song is in database. 
    song = m.session.query(m.Track).filter_by(title=title).filter_by(artist_name=artist_name).first()

    # TO DO: if it is, return information for it and render it on screen
    # (placeholder below)
    if song:
        song_data = None

    # TO DO: if it is not, call Echonest
    else:
        pass

    # TO DO: then call Spotify for the music player



    # TO DO: then store Echonest and Spotify data in database

    return render_template("index.html", spotify_track_id=spotify_track_id)


if __name__ == "__main__":
    app.run(debug=True)
