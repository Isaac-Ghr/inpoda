from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import json
import re

def _printList(l: list, numbered: bool) -> None:
    if numbered:
        for i, element in enumerate(l):
            print(f'{i}) {element}')
    else:
        for element in l:
            print(element)

def _inputInt(prompt: str) -> int:
    try:
        out = int(re.sub(r"[^\d]", "", input(prompt)))
    except:
        return 0
    return out

def _minmax(min: int, val: int, max: int) -> int:
    if val < min:
        return min
    elif val > max:
        return max
    return val

class tweet:
    auteur: str
    texte: str
    sentiment: str
    mentions: list[str]
    hashtags: list[str]
    topics: list[str]

    def __init__(self, a, tx, s, m, h, to):
        self.auteur = a
        self.texte = tx
        self.sentiment = s
        self.mentions = m
        self.hashtags = h
        self.topics = to

    def toDict(self) -> dict:
        return {
            "auteur": self.auteur,
            "texte": self.texte,
            "sentiment": self.sentiment,
            "mention": self.mentions,
            "hashtags": self.hashtags,
            "topics": self.topics
        }

class tweetManager:
    tweets: list[tweet]

    def toDict(self):
        out = []
        for tweet in self.tweets:
            out.append(tweet.toDict())
        return out

class _formats:
    P_FILEPATH = re.compile(r"^(?:[\w]\:|\/)(\/[a-z_\-\s0-9\.]+)+\.(txt|js)$")
    P_NOSPEC = re.compile(r"[^\w\sà-üÀ-Ü#@\.,!?;:'\"()\[\]\/\\{}-]", re.UNICODE)

class _dataman:
    def __init__(self) -> None:
        pass

    def fetchfile(self, path: str):
        if len(_formats.P_FILEPATH.findall(path)) == 0:
            raise Exception("Le chemin saisi n'est pas valide.\n")
        try:
            f = open(path, 'r')
        except FileNotFoundError:
            raise Exception(f"Aucun fichier ne se trouve à l'adresse : \"{path}\"\n")
        return f

    def getData(self, path: str):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Le fichier est introuvable.\n")

    def cleanData(self, path: str):
        jsd = self.getData(path)
        for i, tweet in enumerate(jsd):
            tweet["text"] = _formats.P_NOSPEC.sub('', tweet["text"]).strip()
            tweet["index"] = i
        return jsd

    def write(self, data, dest: str):
        with open(dest) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

class _tweetParser:
    dm: _dataman
    data: list
    source: str

    def __init__(self, source: str) -> None:
        self.dm = _dataman()
        self.source = source
        try:
            self.load()
        except Exception:
            print("Chargement des données échoué")
            self.data = []

    def load(self):
        self.data = self.dm.cleanData(self.source)

    def listPosts(self):
        for tweet in self.data:
            print(f"({tweet.get("index", "Non Défini")}) {tweet.get("text", "Introuvable")}\n")

    def getText(self, p: dict):
        return p.get("text", "")

    def getAuteur(self, p: dict):
        return p.get("author_id", "inconnu")

    def getEntities(self, p: dict) -> dict:
        return p.get("entities", {})

    def getMentionned(self, p: dict):
        ent = self.getEntities(p)
        mentions = ent.get("mentions", [])
        users = list()
        for mention in mentions:
            users.append(mention.get("id", "Inconnu"))
        return users

    def getHashtags(self, p: dict):
        ent = self.getEntities(p)
        hashtags = ent.get("hashtags", [])
        tags = list()
        for hashtag in hashtags:
            tags.append(hashtag.get("tag", "Invalide"))
        return tags

    def getSentiment(self, p: dict):
        text = self.getText(p)
        if not text.split():
            return "Invalide"
        tb = TextBlob(text)

        polarite = tb.polarity
        if polarite > 0:
            return "positif"
        elif polarite < 0:
            return "négatif"
        else:
            return "neutre"

    def getTopics(self, p: dict):
        context = p.get("context_annotations", [])
        topics = set()
        for topic in context:
            topics.add(topic["domain"]["name"])
        return topics

    def readTweet(self, p: dict):
        return tweet(
            self.getAuteur(p),
            self.getText(p),
            self.getSentiment(p),
            self.getMentionned(p),
            self.getHashtags(p),
            self.getTopics(p)
        )

    def parseTweets(self):
        tweets = list()
        for tweetData in self.data:
            tweets.append(self.readTweet(tweetData))
        return tweets

class inpoda:
    parser: _tweetParser
    data: list
    tweets: tweetManager

    source: str
    DATAPATH = "./zone-atterrissage.json"

    def __init__(self, source: str) -> None:
        self.source = source
        self.parser = _tweetParser(self.source)
        self.tweets = tweetManager()
        try:
            self.load()
        except Exception:
            print("Chargement des données échoué")
            self.data = []

    def load(self):
        tweetManager.tweets = self.parser.parseTweets()
  
    def getDF(self) -> pd.DataFrame:
        return pd.DataFrame(self.tweets.toDict())

    # opérations d'analyse
    def explodeCol(self, mode: int) -> pd.DataFrame:
        col = "mention"
        match mode % 3:
            case 0:
                col = "mention"
            case 1:
                col = "hashtags"
            case 2:
                col = "topics"
        df = self.getDF()
        return df.explode(col).dropna()
    
    def countPostByUser(self):
        df = self.getDF()
        dfb = df["auteur"].value_counts()
        dfb.plot(
            kind='bar',
            title='Nombre de publications par utilisateurs'
            )
        plt.show()
    
    def countPostByHashtags(self):
        df = self.explodeCol(1)
        dfb = df["hashtags"].value_counts()
        dfb.plot(
            kind='bar',
            title='Nombre de publications par hashtags'
            )
        plt.show()

    def countPostByTopics(self):
        df = self.explodeCol(2)
        dfb = df["topics"].value_counts()
        dfb.plot(
            kind='bar',
            title='Nombre de publications par topics'
            )
        plt.show()

    def postsByUsers(self):
        df = self.getDF()
        auteurs = df["auteur"].unique().tolist()
        adf = df[["auteur", "texte"]]
        print("Liste des auteurs :")
        _printList(auteurs, True)
        choix = _inputInt("Choisissez l'auteur : ")
        print(f'Publication(s) écrite(s) par l\'auteur "{auteurs[choix]} :"')
        print(df.loc[df["auteur"] == auteurs[choix]])

    def postsByMentions(self):
        df = self.explodeCol(0)
        mentions = df["mention"].to_numpy().tolist()
        print("Liste des utilisateurs mentionnés :")
        _printList(mentions, True)
        choix = _inputInt("Choisissez l'utilisateur : ")
        print(f'Publication(s) mentionnant l\'utilisateur "{mentions[choix]} :"')
        print(df[df["mention"] == mentions[choix]])

    def auteursByHashtags(self):
        df = self.explodeCol(1)
        hashtags = df["hashtags"].unique().tolist()
        print("Liste des hashtags :")
        _printList(hashtags, True)
        choix = _inputInt("Choisissez un hashtag : ")
        adf = df[df["hashtags"] == hashtags[choix]]
        print(f'Auteurs ayant mentionné le hashtag "{hashtags[choix]}" :')
        print(adf["auteur"])

    def mentionnedByUser(self):
        df = self.explodeCol(0)
        auteurs = df["auteur"].unique().tolist()
        print("Liste des auteurs :")
        _printList(auteurs, True)
        choix = _inputInt("Choisissez un auteur : ")
        rdf = df[df["auteur"] == auteurs[choix]]
        print(f"Utilisateur(s) mentionnés par l'auteur {auteurs[choix]} :")
        print(rdf["mention"])

    def topHashtags(self):
        df = self.explodeCol(1)
        k = _minmax(0, _inputInt("Saisissez l'effectif du classement : "), 10)
        df = df["hashtags"].value_counts()
        df.head(k).plot(
            kind='barh',
            title=f'Top {k} hashtags'
            )
        plt.gca().invert_yaxis()
        plt.show()

    def topUsers(self):
        df = self.getDF()
        k = _minmax(0, _inputInt("Saisissez l'effectif du classement : "), 10)
        df = df["auteur"].value_counts()
        print(df)
        df.head(k).plot(
            kind='barh',
            title=f'Top {k} auteurs'
            )
        plt.gca().invert_yaxis()
        plt.show()

    def topMentionned(self):
        df = self.explodeCol(0)
        k = _minmax(0, _inputInt("Saisissez l'effectif du classement : "), 10)
        df = df["mention"].value_counts()
        df.head(k).plot(
            kind='barh',
            title=f'Top {k} utilisateurs mentionnés'
            )
        plt.gca().invert_yaxis()
        plt.show()

    def topTopics(self):
        df = self.explodeCol(2)
        k = _minmax(0, _inputInt("Saisissez l'effectif du classement : "), 10)
        df = df["topics"].value_counts()
        df.head(k).plot(
            kind='barh',
            title=f'Top {k} topics'
            )
        plt.gca().invert_yaxis()
        plt.show()
        
    def test_everything(self):
        print("DEBUT")
        # top k
        self.topHashtags()
        self.topUsers()
        self.topMentionned()
        self.topTopics()
        
        # count
        self.countPostByUser()
        self.countPostByHashtags()
        self.countPostByTopics()

        # posts
        self.postsByUsers()
        input("Press enter")
        self.postsByMentions()
        input("Press enter")

        # users
        self.auteursByHashtags()
        input("Press enter")
        self.mentionnedByUser()
        input("Press enter")
        print("FIN")
