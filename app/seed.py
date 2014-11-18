# -*- coding: utf-8 -*-


# This is meant to be run only on the command line; 
# a version without a list of songs (add_to_db.py) is run by the app

import json
from sys import argv
from time import sleep

import model
from model import db_session
from api_calls import algorithm

def add_to_db(session):

    songs = [("Radiohead", "Weird Fishes"), 
             ("Elliott Smith", "XO"),
             ("Cyndi Lauper", "True Colors"), 
             ("Mozart", "Symphony No. 40 in G Minor"),
             ("Madonna", "La Isla Bonita"), 
             ("Jose Gonzalez", "Heartbeats"), 
             ("Erik Satie", "Gymnopedie No. 1"),
             ("Metallica", "Enter Sandman")]

    for song in songs:

        song_data = algorithm(song[0], song[1])

        values = song_data["patterns"]
        values_json = json.dumps(values)


        track = model.Track()

        track.song_id = song_data["song_id"]
        track.key = song_data["key"]
        track.title = song_data["title"]
        track.tempo = song_data["tempo"]
        track.energy = song_data["energy"]
        track.liveness = song_data["liveness"]
        track.speechiness = song_data["speechiness"]
        track.artist_name = song_data["artist_name"]
        track.mode = song_data["mode"]
        track.acousticness = song_data["acousticness"]
        track.danceability = song_data["danceability"]
        track.time_signature = song_data["time_signature"]
        track.duration = song_data["duration"]
        track.loudness = song_data["loudness"]
        track.artist_id = song_data["artist_id"]
        track.valence = song_data["valence"]    
        track.audio_md5 = song_data["audio_md5"]
        track.instrumentalness = song_data["instrumentalness"]
        track.spotify_track_uri = song_data["spotify_track_uri"]
        track.patterns = values_json

        db_session.add(track)
        db_session.commit()
        sleep(5)


if __name__ == "__main__":

    # script, artist, title = argv
    add_to_db(db_session)
