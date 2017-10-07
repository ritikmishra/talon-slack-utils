"""This module takes in a tokenization and undoes all contractions."""
import nltk

# input: phrase
# output: phrase without contractions
# when the words are pregnant and in labor, the robots have no idea what to do
# this program is engineered to help them


class Decontract:
    """Does all the heavy lifting of decontraction."""

    def __init__(self, phrase):
        """Initialize the class with the tokenized phrase."""
        self.phrase = phrase
        self.tokenize = nltk.word_tokenize(self.phrase)
        self.tagged = nltk.pos_tag(self.tokenize)
        self.contractions = ["n't", "'re", "'ve", "'d", "'s", "'m", "'ll"]
        self.replacements = {"n't": "not", "'re": "are",
                             "'ve": "have", "'m": "am", "'ll": "will"}

    def decontract(self):
        """Decontract the tokenized phrase."""
        for cont in self.contractions:
            for word in self.tokenize:
                if cont == word and cont != "'s" and cont != "'d":
                    # if the word is a real contraction and is not 's or 'd
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
