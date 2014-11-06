import model
from get_song_data import get_song_data

def main(session):
    songs = [("Radiohead", "Weird Fishes"), ("Radiohead", "No Surprises"), ("Radiohead", "Nude"), ("Radiohead", "Paranoid Android")]
    for song in songs:
        song_data = get_song_data(song[0], song[1])

        #TO DO check to see if song is already in db
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

        session.add(track)

    session.commit()

if __name__ == "__main__":
    session = model.connect()
    main(session)
