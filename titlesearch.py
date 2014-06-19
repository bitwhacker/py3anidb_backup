"""Load anime-titles.xml into database and search for id by title"""

import xml.etree.ElementTree as ET
from ..utils.config import Config
import os.path
import zlib
from . import AnidbModel, AnimeTitle

class TitleSearch:
    """Load anime-titles.xml into database and search for id by title"""

    def __init__(self):
        self.model = AnidbModel()
        config = Config()

    def search(self, title):
        for id in self.model.get_id_by_title(title):
             mtitle = self.model.get_title(id, 'x-jat', 'main')
             otitle = self.model.get_title(id, 'en', 'official')

             if mtitle != None and otitle != None:
                 print(str(otitle.anidbid) + ")  " + otitle.title + " (" + mtitle.title + ")")
             elif mtitle == None and otitle != None:
                 print(str(otitle.anidbid) + ")  " + otitle.title)
             elif mtitle != None and otitle == None:
                 print(str(mtitle.anidbid) + ")  " + mtitle.title)

    def load_titles(self):
        url = 'http://anidb.net/api/anime-titles.xml.gz'
        with urllib.request.urlopen(url) as response:
#        path = os.path.dirname(__file__)
#        with open(path + '/anime-titles.xml.gz', 'rb') as response:
            data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS).decode()

        for child in ET.fromstring(data):
            aid = child.attrib['aid']
            for t in child:
                if t.attrib['{http://www.w3.org/XML/1998/namespace}lang'] in ('en', 'x-jat'):
                    anime_title = AnimeTitle(anidbid = aid, 
                        language = t.attrib['{http://www.w3.org/XML/1998/namespace}lang'],
                        type = t.attrib['type'],
                        title = t.text)
                    print ("Adding: ", anime_title.anidbid, anime_title.title, 
                           anime_title.language, anime_title.type)
                    self.model.add_title(anime_title)
