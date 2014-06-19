from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, sessionmaker
from ..py3utils import ModelHelper
import sys

Base = declarative_base()
class AnimeTitle(Base):
    __tablename__ = 'anime_title'
    anidbid = Column(Integer, primary_key = True) 
    language = Column(String(10), primary_key = True) 
    type = Column(String(10), primary_key = True) 
    title = Column(String(250), primary_key = True) 

class Anime(Base):
    __tablename__ = 'anime'
    anidbid = Column(Integer, primary_key = True) 
    title = Column(String(250), nullable = False) 

class Settings(Base):
    __tablename__ = 'settings'
    key = Column(String(20), primary_key = True) 
    value = Column(String(250), nullable = False) 

class AnidbModel():
    def __init__(self):
        configfile = os.path.dirname(os.path.realpath(__file__)) + "/py3anidb.cfg"
        enginestring = ModelHelper().getenginestring('anidb', Config(configfile))
        print (enginestring)
        return
        engine = create_engine(ModelHelper().getenginestring('anidb', Config(configfile)))
        self.DBSession = sessionmaker(bind = engine)
        self.db = self.DBSession()
#        if self.get_version() != __modelversion__:
#            self.update_database()

    def update_database(self):
        print("Updating Database")

        # todo Create/Update tables

        self.db.add(Settings(key = 'version', value = __modelversion__))
        self.db.commit()

    def get_version(self):
        try:
            version = self.db.query(Settings).filter(Settings.key == 'version').one().value
            return version
        except:
            print("Unable to load version", sys.exc_info())
            return None

    def get_session(self):
        return self.db

    def add_title(self, anime_title):
        try:
            self.db.add(anime_title)
            self.db.commit()
        except(IntegrityError):
            self.db.rollback()
            print("Duplicate Entry: ", anime_title.anidbid, 
                   anime_title.language, anime_title.type, anime_title.title)

    def get_titles(self):
        return self.db.query(AnimeTitle).all()

    def get_id_by_title(self, title):
        titles = self.db.query(AnimeTitle).filter(AnimeTitle.title.ilike('%' + title + '%')).all()
        ids = []
        for title in titles:
            ids.append(title.anidbid)
        return sorted(set(ids))

    def get_title(self, anidbid, language, type):
        return self.db.query(AnimeTitle).filter(AnimeTitle.anidbid == anidbid,
                                                AnimeTitle.language == language,
                                                AnimeTitle.type == type).first()
