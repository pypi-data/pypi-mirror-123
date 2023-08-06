import requests
import datetime
import json

class Error(Exception):
    pass

class InvalidTokenOrUser(Error):
    pass

class InvalidVersion(Error):
    pass

class BunkResult:
    def __init__(self,method,image,raw,title=None,subreddit=None,author=None,id=None,upvote=None,downvote=None,comments=None,nsfw=None,created_at=None,score=None):
        self.method = method
        self.title = title
        self.subreddit = subreddit
        self.author = author
        self.image = image
        self.id = id
        self.upvote = upvote
        self.downvote = downvote
        self.comments = comments
        self.nsfw = nsfw
        if created_at != None:
            self.created_at = datetime.datetime.fromtimestamp(float(created_at))
        self.score = score

class BunkWeather:
    def __init__(self,location,country,last_updated,condition,img,temp_c,temp_f,wind_mph,wind_kph,wind_dir,humidity,feelslike_c,feelslike_f,raw):
        self.location = location
        self.country = country
        self.last_updated = datetime.datetime.fromtimestamp(float(last_updated))
        self.condition = condition
        self.img = img
        self.temp = {"Celsius": temp_c, "C": temp_c, "Farenheit": temp_f, "F": temp_f}
        self.temp_c = temp_c
        self.temp_f = temp_f
        self.wind_mph = wind_mph
        self.wind_kph = wind_kph
        self.wind_dir = wind_dir
        self.humidity = self.humidity
        self.feelslike_c = feelslike_c
        self.feelslike_f = feelslike_f
        self.raw = raw

class BunkAPI:
    def __init__(self,token,id,version=1):
        self.token = token
        self.id = id
        self.version = version
        self.credits = 'Created and Maintained by DaWinnerIsHere#1264.'

    def donkey(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/donkey/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/donkey/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='donkey',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def meme(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/meme/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/meme/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='meme',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def llama(self):
        x = requests.get(f'https://bunkapi.xyz/api/v1/donkey/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='llama',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def alpaca(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/alpaca/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/alpaca/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='alpaca',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def giraffe(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/giraffe/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='giraffe',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def potato(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/potato/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='potato',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def aww(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/aww/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/aww/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='aww',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def moose(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/moose/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/moose/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='moose',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def camel(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/camel/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='camel',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def seal(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/seal/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/seal/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='seal',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def elephant(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/elephant/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/elephant/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='elephant',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def zebra(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/zebra/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='zebra',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def amongus(self):
        if self.version == 1:
            x = requests.get(f'https://bunkapi.xyz/api/v1/amongus/{self.id}?token={self.token}')
        elif self.version == 2:
            headers = {
            "token": self.token
            }
            x = requests.post(f'https://bunkapi.xyz/api/v2/amongus/{self.id}',headers=headers)
        else:
            raise InvalidVersion
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='amongus',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def space(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/space/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            image = x['image']
            return BunkResult(method='space',image=image,raw=x)

    def anime_wallpaper(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/anime-wallpaper/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            image = x['data']['title']
            image = x['data']['image']
            return BunkResult(method='anime_wallpaper',title=title,image=image,raw=x)

    def _8ball(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/8ball/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            return x['data']

    def shorten(self,url):
        xdata = {"longUrl": url}
        headers = {"token": self.token}
        x = requests.post(f'https://bunkapi.xyz/api/v2/shorten/{self.id}',headers=headers,json=xdata)
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            return x['data']['short']

    def weather(self,city):
        headers = {"token": self.token}
        xdata = {"city": city}
        x = requests.post(f'https://bunkapi.xyz/api/v2/weather/{self.id}',headers=headers,json=xdata)
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            location = x['data']['location']
            country = x['data']['country']
            last_updated = x['data']['last_updated']
            condition = x['data']['condition']
            img = x['data']['img']
            temp_c = x['data']['temp_c']
            temp_f = x['data']['temp_f']
            wind_mph = x['data']['wind_mph']
            wind_kph = x['data']['wind_kph']
            wind_dir = x['data']['wind_dir']
            humidity = x['data']['humidity']
            feelslike_c = x['data']['feelslike_c']
            feelslike_f = x['data']['feelslike_f']
            return BunkWeather(location=location,country=country,last_updated=last_updated,condition=condition,img=img,temp_c=temp_c,temp_f=temp_f,wind_mph=wind_mph,wind_kph=wind_kph,wind_dir=wind_dir,humidity=humidity,feelslike_c=feelslike_c,feelslike_f=feelslike_f,raw=x)
