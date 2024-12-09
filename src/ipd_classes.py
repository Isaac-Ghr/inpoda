from textblob import TextBlob
#import rich
#import pandas as pd
import json
import re

class tweet:
	id: int
	auteur: str
	texte: str
	mentions: list[str]
	hashtags: list[str]
	sentiment: str

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

	def writeCleanedData(self, path: str, dest: str):
		with open(dest, 'w') as f:
			jsd = self.getData(path)
			for i, tweet in enumerate(jsd):
				#print(tweet["id"], tweet["text"])
				tweet["text"] = _formats.P_NOSPEC.sub('', tweet["text"]).strip()
				tweet["index"] = i
				#print(tweet["id"], tweet["text"])
			json.dump(jsd, f, ensure_ascii=False, indent=4)

class inpoda:
	dm: _dataman
	data: list

	source: str
	DATAPATH = "./zone-atterrissage.json"

	def __init__(self, source: str) -> None:
		self.dm = _dataman()
		self.source = source
		try:
			self.load()
		except Exception:
			print("Chargement des données échoué")
			self.data = []

	def load(self):
		self.dm.writeCleanedData(self.source, self.DATAPATH)
		self.data = self.dm.getData(self.DATAPATH)

	def _isIndexOut(self, index: int):
		return index not in range(0, len(self.data))

	def listPosts(self):
		for tweet in self.data:
			print(f"({tweet.get("index", "Non Défini")}) {tweet.get("text", "Introuvable")}\n")

	def getText(self, index: int):
		if self._isIndexOut(index):
			return ""
		for tweet in self.data:
			if tweet["index"] == index:
				return tweet.get("text", "")
		return ""

	def getAuteur(self, index: int):
		if self._isIndexOut(index):
			return ""
		for tweet in self.data:
			if tweet["index"] == index:
				return tweet.get("author_id", "Inconnu")
		return ""

	def getEntities(self, index: int) -> dict:
		if self._isIndexOut(index):
			return {}
		for tweet in self.data:
			if tweet["index"] == index:
				return tweet.get("entities", {})
		return {}

	def getMentionned(self, index: int):
		if self._isIndexOut(index):
			return []
		ent = self.getEntities(index)
		mentions = ent.get("mentions", [])
		users = list()
		for mention in mentions:
			users.append(mention.get("username", "Inconnu"))
		return users

	def getHashtags(self, index: int):
		if self._isIndexOut(index):
			return []
		ent = self.getEntities(index)
		hashtags = ent.get("hashtags", [])
		tags = list()
		for hashtag in hashtags:
			tags.append(hashtag.get("tag", "Invalide"))
		return tags

	def getSentiment(self, index: int):
		text = self.getText(index)
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
