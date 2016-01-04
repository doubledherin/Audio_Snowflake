# -*- coding: utf-8 -*-
import json
from models import db_session, Image, Track


def add_song_to_db(session, song_data):

    patterns = song_data["patterns"]
    patterns_json = json.dumps(patterns)

    sections = song_data["sections"]
    sections_json = json.dumps(sections)

    track = Track()

    track.song_id = song_data["song_id"]
    track.key = song_data["key"]
    track.title = song_data["title"]
    track.tempo = song_data["tempo"]
    track.energy = song_data["energy"]
    track.artist_name = song_data["artist_name"]
    track.mode = song_data["mode"]
    track.time_signature = song_data["time_signature"]
    track.duration = song_data["duration"]
    track.loudness = song_data["loudness"]
    track.artist_id = song_data["artist_id"]
    track.valence = song_data["valence"]
    track.audio_md5 = song_data["audio_md5"]
    track.spotify_track_uri = song_data["spotify_track_uri"]
    track.patterns = patterns_json
    track.sections = sections_json
    track.rotation_duration = song_data["rotation_duration"]

    db_session.add(track)
    db_session.commit()


def add_image_to_db(session, filename, artist_name, title):

    image = Image()

    image.filename = filename
    image.artist_name = artist_name
    image.title = title

    db_session.add(image)
    db_session.commit()
