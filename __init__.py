from .anidbmodel import AnidbModel, Anime, AnimeTitle, Settings
from .titlesearch import TitleSearch

__all__ = ['AnidbModel', 'AnimeTitle', 'Anime', 'Settings', 'TitleSearch']
__version__ = "0.1.0"

configfile = os.path.dirname(os.path.realpath(__file__)) + "/py3anidb.cfg"
