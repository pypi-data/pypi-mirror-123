"""
MIT License

Copyright (c) 2021 Hype3808

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# pylint: disable=C0301
import aiohttp
import requests
from typing import Optional

from .result import Result
from .errors import APIError, MissingMessageArgument

class Client:
    """Sync Client"""
    def __init__(
        self,
        name: Optional[str] = 'Clever Chat',*,
        gender: Optional[str] = 'Male',
        master: Optional[str] = 'Royalty#2021',
        age: Optional[int] = 18,
        birthday: Optional[str] = "10/10/2000",
        birthplace: Optional[str] = 'France',
        birthyear: Optional[int] = 2000,
        religion: Optional[str] = 'Christian',
        favourite_actor: Optional[str] = "Brad Pitt",
        favourite_actress: Optional[str] = "Julia Roberts",
        favourite_artist: Optional[str] = 'Leonardo',
        favourite_author: Optional[str] = 'Jeff Kinney',
        favourite_band: Optional[str] = 'Imagine',
        favourite_book: Optional[str] = 'Diary',
        celibrity: Optional[str] = 'Taylor Swift',
        chinese_sign: Optional[str] = 'Dragon',
        family: Optional[str] = 'AI ChatBot',
        favourite_color: Optional[str] = 'Pink',
        favourite_food: Optional[str] = 'Pizza',
        favourite_movie: Optional[str] = 'Ant Man',
        favourite_opera: Optional[str] = 'Carmen',
        favourite_season: Optional[str] = 'Spring',
        e_type: Optional[str] = "AI ChatBot",
        favourite_ethics: Optional[str] = "The Golden Rule",
        favourite_show: Optional[str] = 'Discovery',
        favourite_song: Optional[str] = 'Believer',
        favourite_sport: Optional[str] = 'Badminton',
        favourite_subject: Optional[str] = 'Math',
        favourite_football_team: Optional[str] = 'Dallas Cowboys',
        favourite_baseball_team: Optional[str] = 'New York Yankees',
        city: Optional[str] = 'San Francisco',
        state: Optional[str] = 'California',
        classes: Optional[str] = 'Artificial Intelligence',
        country: Optional[str] = 'United States',
        company: Optional[str] = 'Acobot',
        email: Optional[str] = 'lucaswong080917@gmail.com',
        wechat: Optional[str] = 'Brainshop',
        wear: Optional[str] = 'My shinning virtual wardrobe',
        vocab: Optional[int] = 20000,
        version: Optional[str] = 'v0.0.1',
        totalcli: Optional[str] = 'hundreds of thousands',
        species: Optional[str] = 'Artificial Intelligence ChatBot',
        sign: Optional[str] = 'Pisces',
        scspecies: Optional[str] = "智能机器人",
        scsign: Optional[str] = "双鱼座",
        scnationality: Optional[str] = "中国",
        scmaster: Optional[str] = "Acobot 团队",
        scgender: Optional[str] = "女",
        scfavouritefood: Optional[str] = "电",
        scfavouritecolor: Optional[str] = "绿色",
        sccountry: Optional[str] = "中国",
        sccompany: Optional[str] = "艾珂（北京）智能系统有限公司",
        sccity: Optional[str] = "北京",
        scchinesesign: Optional[str] = "龙",
        hockey: Optional[str] = "New York Rangers",
        job: Optional[str] = "chat bot",
        kind_music: Optional[str] = "techno",
        celebrities: Optional[str] = "C3PO",
        orientation: Optional[str] = "Straight",
        phylum: Optional[str] = "Software",
        president: Optional[str] = "Joe Biden"

    ):
        self.name = name
        self.gender = gender
        self.master = master
        self.age = age
        self.birthday = birthday
        self.birthplace = birthplace
        self.birthyear = birthyear
        self.religion = religion
        self.favourite_actor = favourite_actor
        self.favourite_actress = favourite_actress
        self.favourite_artist = favourite_artist
        self.favourite_author = favourite_author
        self.favourite_band = favourite_band
        self.favourite_book = favourite_book
        self.celibrity = celibrity
        self.chinese_sign = chinese_sign
        self.family = family
        self.favourite_color = favourite_color
        self.favourite_food = favourite_food
        self.favourite_movie = favourite_movie
        self.favourite_opera = favourite_opera
        self.favourite_season = favourite_season
        self.e_type = e_type
        self.favourite_ethics = favourite_ethics
        self.favourite_show = favourite_show
        self.favourite_song = favourite_song
        self.favourite_sport = favourite_sport
        self.favourite_subject = favourite_subject
        self.favourite_football_team = favourite_football_team
        self.favourite_baseball_team = favourite_baseball_team
        self.city = city
        self.classes = classes
        self.state = state
        self.country = country
        self.email = email
        self.company = company
        self.wechat = wechat
        self.wear = wear
        self.version = version
        self.vocab = vocab
        self.totalcli = totalcli
        self.species = species
        self.sign = sign
        self.scspecies = scspecies
        self.scsign = scsign
        self.scnationality = scnationality
        self.scmaster = scmaster
        self.scgender = scgender
        self.scfavouritefood = scfavouritefood
        self.scfavouritecolor = scfavouritecolor
        self.sccountry = sccountry
        self.sccompany = sccompany
        self.sccity = sccity
        self.scchinesedesign = scchinesesign
        self.hockey = hockey
        self.job = job
        self.kind_music = kind_music
        self.celebrities = celebrities
        self.orientation = orientation
        self.phylum = phylum
        self.president = president
        self._session = requests.Session()

    def get_response(self, message: str=None):
        """Getting response"""
        if not message:
            raise MissingMessageArgument("Message argument is missing")
        params = {
            "message": message,
            "name": self.name,
            "age": self.age,
            "developer_name": self.master,
            "birthday": self.birthday,
            "birthplace": self.birthplace,
            "birthyear": self.birthyear,
            "religion": "Panda",
            "actor": self.favourite_actor,
            "actress": self.favourite_actress,
            "artist": self.favourite_artist,
            "author": self.favourite_author,
            "band": self.favourite_band,
            "book": self.favourite_book,
            "celebrity": self.celibrity,
            "chinesesign": self.chinese_sign,
            "family": self.family,
            "etype": self.e_type,
            "ethics": self.favourite_ethics,
            "color": self.favourite_color,
            "food": self.favourite_food,
            "movie": self.favourite_movie,
            "opera": self.favourite_opera,
            "season": self.favourite_season,
            "show": self.favourite_show,
            "song": self.favourite_song,
            "sport": self.favourite_sport,
            "subject": self.favourite_subject,
            "football": self.favourite_football_team,
            "baseball": self.favourite_baseball_team,
            "city": self.city,
            "state": self.state,
            "class": self.classes,
            "country": self.country,
            "company": self.company,
            "email": self.email,
            "wechat": self.wechat,
            "wear": self.wear,
            "vocab": self.vocab,
            "version": self.version,
            "totalcli": self.totalcli,
            "species": self.species,
            "sign": self.sign,
            "scspecies": self.scspecies,
            "scsign": self.scsign,
            "scnationality": self.scnationality,
            "scmaster": self.scmaster,
            "scgender": self.scgender,
            "scfavouritefood": self.scfavouritefood,
            "scfavouritecolor": self.scfavouritecolor,
            "sccountry": self.sccountry,
            "sccompany": self.sccompany,
            "sccity": self.sccity,
            "scchinesesign": self.scchinesedesign,
            "hockey": self.hockey,
            "job": self.job,
            "music": self.kind_music,
            "celebrities": self.celebrities,
            "orientation": self.orientation,
            "phylum": self.phylum,
            "president": self.president
        }
        try:
            response = self._session.get(
                "https://yourmommmaosamaobama.hisroyal123.repl.co/",
                params=params
            )
            res = response.json()
            if response.status_code != 200:
                raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")
            if not res:
                raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")
            return Result(res)
        except requests.exceptions.Timeout:
            raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")

    def close(self):
        """Close the request session"""
        return self._session.close()

class AsyncClient:
    """Async client"""
    def __init__(
        self,
        name: Optional[str] = 'Clever Chat',*,
        gender: Optional[str] = 'Male',
        master: Optional[str] = 'Royalty#2021',
        age: Optional[int] = 18,
        birthday: Optional[str] = "10/10/2000",
        birthplace: Optional[str] = 'France',
        birthyear: Optional[int] = 2000,
        religion: Optional[str] = 'Christian',
        favourite_actor: Optional[str] = "Brad Pitt",
        favourite_actress: Optional[str] = "Julia Roberts",
        favourite_artist: Optional[str] = 'Leonardo',
        favourite_author: Optional[str] = 'Jeff Kinney',
        favourite_band: Optional[str] = 'Imagine',
        favourite_book: Optional[str] = 'Diary',
        celibrity: Optional[str] = 'Taylor Swift',
        chinese_sign: Optional[str] = 'Dragon',
        family: Optional[str] = 'AI ChatBot',
        favourite_color: Optional[str] = 'Pink',
        favourite_food: Optional[str] = 'Pizza',
        favourite_movie: Optional[str] = 'Ant Man',
        favourite_opera: Optional[str] = 'Carmen',
        favourite_season: Optional[str] = 'Spring',
        e_type: Optional[str] = "AI ChatBot",
        favourite_ethics: Optional[str] = "The Golden Rule",
        favourite_show: Optional[str] = 'Discovery',
        favourite_song: Optional[str] = 'Believer',
        favourite_sport: Optional[str] = 'Badminton',
        favourite_subject: Optional[str] = 'Math',
        favourite_football_team: Optional[str] = 'Dallas Cowboys',
        favourite_baseball_team: Optional[str] = 'New York Yankees',
        city: Optional[str] = 'San Francisco',
        state: Optional[str] = 'California',
        classes: Optional[str] = 'Artificial Intelligence',
        country: Optional[str] = 'United States',
        company: Optional[str] = 'Acobot',
        email: Optional[str] = 'lucaswong080917@gmail.com',
        wechat: Optional[str] = 'Brainshop',
        wear: Optional[str] = 'My shinning virtual wardrobe',
        vocab: Optional[int] = 20000,
        version: Optional[str] = 'v0.0.1',
        totalcli: Optional[str] = 'hundreds of thousands',
        species: Optional[str] = 'Artificial Intelligence ChatBot',
        sign: Optional[str] = 'Pisces',
        scspecies: Optional[str] = "智能机器人",
        scsign: Optional[str] = "双鱼座",
        scnationality: Optional[str] = "中国",
        scmaster: Optional[str] = "Acobot 团队",
        scgender: Optional[str] = "女",
        scfavouritefood: Optional[str] = "电",
        scfavouritecolor: Optional[str] = "绿色",
        sccountry: Optional[str] = "中国",
        sccompany: Optional[str] = "艾珂（北京）智能系统有限公司",
        sccity: Optional[str] = "北京",
        scchinesesign: Optional[str] = "龙",
        hockey: Optional[str] = "New York Rangers",
        job: Optional[str] = "chat bot",
        kind_music: Optional[str] = "techno",
        celebrities: Optional[str] = "C3PO",
        orientation: Optional[str] = "Straight",
        phylum: Optional[str] = "Software",
        president: Optional[str] = "Joe Biden"

    ):
        self.name = name
        self.gender = gender
        self.master = master
        self.age = age
        self.birthday = birthday
        self.birthplace = birthplace
        self.birthyear = birthyear
        self.religion = religion
        self.favourite_actor = favourite_actor
        self.favourite_actress = favourite_actress
        self.favourite_artist = favourite_artist
        self.favourite_author = favourite_author
        self.favourite_band = favourite_band
        self.favourite_book = favourite_book
        self.celibrity = celibrity
        self.chinese_sign = chinese_sign
        self.family = family
        self.favourite_color = favourite_color
        self.favourite_food = favourite_food
        self.favourite_movie = favourite_movie
        self.favourite_opera = favourite_opera
        self.favourite_season = favourite_season
        self.e_type = e_type
        self.favourite_ethics = favourite_ethics
        self.favourite_show = favourite_show
        self.favourite_song = favourite_song
        self.favourite_sport = favourite_sport
        self.favourite_subject = favourite_subject
        self.favourite_football_team = favourite_football_team
        self.favourite_baseball_team = favourite_baseball_team
        self.city = city
        self.classes = classes
        self.state = state
        self.country = country
        self.email = email
        self.company = company
        self.wechat = wechat
        self.wear = wear
        self.version = version
        self.vocab = vocab
        self.totalcli = totalcli
        self.species = species
        self.sign = sign
        self.scspecies = scspecies
        self.scsign = scsign
        self.scnationality = scnationality
        self.scmaster = scmaster
        self.scgender = scgender
        self.scfavouritefood = scfavouritefood
        self.scfavouritecolor = scfavouritecolor
        self.sccountry = sccountry
        self.sccompany = sccompany
        self.sccity = sccity
        self.scchinesedesign = scchinesesign
        self.hockey = hockey
        self.job = job
        self.kind_music = kind_music
        self.celebrities = celebrities
        self.orientation = orientation
        self.phylum = phylum
        self.president = president
        self._session = aiohttp.ClientSession()

    async def get_response(self, message: str=None):
        """Getting response"""
        if not message:
            raise MissingMessageArgument("Message Argument is missing")
        params = {
            "message": message,
            "name": self.name,
            "age": self.age,
            "developer_name": self.master,
            "birthday": self.birthday,
            "birthplace": self.birthplace,
            "birthyear": self.birthyear,
            "religion": "Panda",
            "actor": self.favourite_actor,
            "actress": self.favourite_actress,
            "artist": self.favourite_artist,
            "author": self.favourite_author,
            "band": self.favourite_band,
            "book": self.favourite_book,
            "celebrity": self.celibrity,
            "chinesesign": self.chinese_sign,
            "family": self.family,
            "etype": self.e_type,
            "ethics": self.favourite_ethics,
            "color": self.favourite_color,
            "food": self.favourite_food,
            "movie": self.favourite_movie,
            "opera": self.favourite_opera,
            "season": self.favourite_season,
            "show": self.favourite_show,
            "song": self.favourite_song,
            "sport": self.favourite_sport,
            "subject": self.favourite_subject,
            "football": self.favourite_football_team,
            "baseball": self.favourite_baseball_team,
            "city": self.city,
            "state": self.state,
            "class": self.classes,
            "country": self.country,
            "company": self.company,
            "email": self.email,
            "wechat": self.wechat,
            "wear": self.wear,
            "vocab": self.vocab,
            "version": self.version,
            "totalcli": self.totalcli,
            "species": self.species,
            "sign": self.sign,
            "scspecies": self.scspecies,
            "scsign": self.scsign,
            "scnationality": self.scnationality,
            "scmaster": self.scmaster,
            "scgender": self.scgender,
            "scfavouritefood": self.scfavouritefood,
            "scfavouritecolor": self.scfavouritecolor,
            "sccountry": self.sccountry,
            "sccompany": self.sccompany,
            "sccity": self.sccity,
            "scchinesesign": self.scchinesedesign,
            "hockey": self.hockey,
            "job": self.job,
            "music": self.kind_music,
            "celebrities": self.celebrities,
            "orientation": self.orientation,
            "phylum": self.phylum,
            "president": self.president
        }
        try:
            async with self._session.get(
                "https://yourmommmaosamaobama.hisroyal123.repl.co/",
                params=params
            ) as response:
                if response.status != 200:
                    raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")
                res = await response.json()
                if not res:
                    raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")
                return Result(res)
        except aiohttp.ContentTypeError:
            raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")
        except aiohttp.ServerTimeoutError:
            raise APIError("API is unavailable. Please try again later. Contact Royalty#2021 on Discord if you think this is a mistake.")

    async def close(self):
        """Close the client session"""
        return await self._session.close()
