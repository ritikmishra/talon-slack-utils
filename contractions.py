import nltk, re
#input: phrase
#output: phrase without contractions
#when the words are pregnant and in labor, the robots have no idea what to do
#this program is engineered to help them
"""
Takes in a phrase
It uses python's natural language toolkit to tokenize the phrase
It then uses the same toolkit to analyze the tokenization and tag each word with its part of speech
Then, it looks for tokens that are contractions
It can easily translate all of them to f
"""
class Decontract:
	def __init__(self, phrase):
		self.phrase = phrase
		self.tokenize = nltk.word_tokenize(self.phrase)
		self.tagged = nltk.pos_tag(self.tokenize)
		self.contractions = ["n't","'re","'ve","'d","'s","'m","'ll"]
		self.replacements = {"n't":"not","'re":"are","'ve":"have","'m":"am","'ll":"will"}
	def decontract(self):
		for cont in self.contractions:
			for word in self.tokenize:
				if cont == word and cont != "'s" and cont != "'d":
					#if the word is a real contraction and is not 's or 'd
					self.tokenize[self.tokenize.index(word)] = self.replacements[cont]
				elif cont == word and cont != "'s":
					self.index = self.tokenize.index(word)
					self.pos = self.tagged[self.index][1]
					if self.pos == "DT":
						self.tokenize[self.index] = "is"
					elif self.pos[0:2] == "VB":
						self.tokenize[self.index] = "has"
				elif cont == word and cont != "'d":
					self.index = self.tokenize.index(word)
					self.pos = self.tagged[self.index][1]
					if self.pos == "VB":
						self.tokenize[self.index] = "would"
					elif self.pos == "VBN":
						self.tokenize[self.index] = "had"
		return self.tokenize
	
