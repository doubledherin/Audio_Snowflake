# -*- coding: utf-8 -*-
import json, model
from model import db_session
from sys import argv


def add_song_to_db(session, song_data):

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
    track.rotation_speed = song_data["rotation_speed"]

    db_session.add(track)
    db_session.commit()

def add_image_to_db(session, filename, artist_name, title):

    image = model.Image()

    image.filename = filename
    image.artist_name = artist_name
    image.title = title

    db_session.add(image)
    db_session.commit()

