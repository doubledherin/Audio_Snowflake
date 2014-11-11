from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, PickleType
from sqlalchemy.orm import sessionmaker, scoped_session



engine = create_engine("sqlite:///audiosnowflake.db", echo=False)
db_session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()


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
    speechiness = Column(Float)
    artist_name = Column(String(100))
    mode = Column(Integer)
    acousticness = Column(Float)
    danceability = Column(Float)
    time_signature = Column(Integer)
    duration = Column(Float)
    loudness = Column(Float)
    artist_id = Column(String(50))
    valence = Column(Float) 
    audio_md5 = Column(String(50))
    instrumentalness = Column(Float)
    # echonest_track_id = Column(String(50))
    spotify_track_uri = Column(String(50))
    # analysis_url = Column(String(150))
    # artist_foreign_ids = Column(String (150))

    # values for the outer ring (epitrochoid; 1 per track)
    # epi_a = Column(Float)
    # epi_b = Column(Float)
    # epi_h = Column(Float)

    # # values for the interior rings (hypotrochoids; 1 per section; 5 sections max)
    # hypo0_a = Column(Float)
    # hypo0_b = Column(Float)
    # hypo0_h = Column(Float)

    # hypo1_a = Column(Float)
    # hypo1_b = Column(Float)
    # hypo1_h = Column(Float)

    # hypo2_a = Column(Float)
    # hypo2_b = Column(Float)
    # hypo2_h = Column(Float)

    # hypo3_a = Column(Float)
    # hypo3_b = Column(Float)
    # hypo3_h = Column(Float)

    # hypo4_a = Column(Float)
    # hypo4_b = Column(Float)
    # hypo4_h = Column(Float)

    # values for variables in patterns
    patterns = Column(PickleType)




