from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker


ENGINE = None
Session = None

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key = True)

    # the below come from get_song_data function
    song_id = Column(String(50))
    key = Column(Integer)
    title = Column(String(100))
    tempo = Column(Float)
    energy = Column(Float)
    liveness = Column(Float)
    # analysis_url = Column(String(200)) not sure I want this in the dbase

    speechiness = Column(Float)
    artist_name = Column(String(100))

    mode = Column(Integer)

    acousticness = Column(Float)
    danceability = Column(Float)

    time_sig = Column(Integer)
    duration = Column(Float)
    loudness = Column(Float)
    
    artist_id = Column(String(50))
    valence = Column(Float) 


    audio_md5 = Column(String(50))


    instrumentalness = Column(Float)

    # the below come from add_sections function
    num_sections = Column(Integer) # not sure if I should keep; this is precollapse

    # maybe the below should be MULTISET data type?
    # pickle type
    sections = Column(Array) # not sure if I should keep; this is precollapse



    # Still need to get the below into song_data
    track_id = Column(String(50))
    

    album = Column(String(150))
    year = Column(Integer)

    key_confidence = Column(Float)
    mode_confidence = Column(Float)
    time_sig_confidence = Column(Float)

def connect():
    global ENGINE
    global Session 

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

if __name__ == "__main__":
    db_session = connect()
