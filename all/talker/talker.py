"""Create fake english sentences."""
from __future__ import division

import json
import os
import random
import subprocess
import sys

import nltk

from .contractions import Decontract
from .install_nltk_modules import install


class Talker:
    """The class that creates English sentences with bad grammar."""

    def __init__(self):
        self.__PATH = "./"
        """Load word list, download necessary components."""
        self.__path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.dirname(os.path.realpath(__file__)) + "/words.json", "r+") as self.wordfile:
            self.used_words = json.loads(self.wordfile.read())
        try:
            test_tokens = nltk.word_tokenize("Test sentence")
            nltk.pos_tag(test_tokens)
        except LookupError:
            install()

    def __str__(self):
        """Return all the words that can be used by the program to make sentences."""
        return self.used_words

    def user_said_question(self, human_response):
        """Figure out if the user gave me a yes/no question."""
        qtype = subprocess.check_output(['node', self.__PATH + 'questions.js', str(human_response)]).strip().decode(
            "UTF-8")
        if qtype == "YN":
            return True
        else:
            return False

    def conjugator(self, form):
        """Conjugate verbs by passing them to a node script."""
        verb = subprocess.check_output(
            ['node', self.__PATH + 'conjugate.js', random.choice(self.used_words["verb"]), form]).strip().decode("UTF-8")
        if verb == "does" or verb == "makes" or verb == "doing":
            verb += " " + random.choice(self.used_words["determiner"]) + " " + random.choice(self.used_words["noun"])
        return verb

    def word_processor(self, tags):
        """
        Process words that are given to me into separate parts of speech.

        Don't worry if I'm too complex for you, baby.
        """
        for x, word in enumerate(tags):
            # print(word)
            # if self.dictionary.check(word[0]):

            if (word[1][0] == "N") and not (word[0] in self.used_words["noun"]):
                self.used_words["noun"].append(word[0].lower())
            elif word[1][0:2] == "PR" and not (word[0] in self.used_words["pronoun"]):
                self.used_words["pronoun"].append(word[0])
            elif (word[1][0:2] == "VB" or word[1][0:2] == "MD") and word[0] != "would" and word[0] != "could" and word[
                0] != "should" and not word[0] in self.used_words["verb"]:
                self.used_words["verb"].append(
                    subprocess.check_output(['node', 'conjugate.js', word[0], 'infinitive']).strip().decode("UTF-8"))
            elif word[1][0:2] == "JJ" and not (word[0] in self.used_words["adjective"]):
                self.used_words["adjective"].append(word[0].lower())
            elif word[1][0:2] == "RB" and not (word[0] in self.used_words["adverb"]):
                self.used_words["adverb"].append(word[0].lower())
            elif word[1][0:2] == "IN" and not (word[0] in self.used_words["preposition"]):
                self.used_words["preposition"].append(word[0].lower())
            elif word[1][0:2] == "CC" and not (word[0] in self.used_words["conjunction"]):
                self.used_words["conjunction"].append(word[0].lower())
            elif word[1][0:2] == "UH" and not (word[0] in self.used_words["interjection"]):
                self.used_words["interjection"].append(word[0].lower())
            elif word[1][0] == "W" and not (word[0] in self.used_words["question_word"]):
                self.used_words["question_word"].append(word[0].lower())
            elif word[1][0] == "DT" and not (word[0] in self.used_words["determiner"]):
                self.used_words["determiner"].append(word[0].lower())
            if x % 5000 == 0:
                print("Tag #" + str(x) + " scanned")
        # with open(os.path.dirname(os.path.realpath(__file__)) + "/words.json", "r+") as wordfile:
        #     json.dump(self.used_words, wordfile)

    def statement(self):
        """Generate a statement using the words in self.used_words."""
        if len(self.used_words["verb"]) == 0:
            self.phrase = "What are you doing?"
        elif len(self.used_words["noun"]) == 0:
            self.phrase = "Tell me what I look like."
        else:
            self.phrase = random.choice(self.used_words["determiner"]).capitalize()
            self.chosen_noun = [random.choice(self.used_words["noun"]), None]
            self.chosen_noun[1] = nltk.pos_tag(nltk.word_tokenize(self.chosen_noun[0]))

            # Pick adjective if possible
            if len(self.used_words["adjective"]) > 0:
                self.phrase += " " + random.choice(self.used_words["adjective"])

            # Throw in noun
            self.phrase += " " + self.chosen_noun[0]

            # Throw in adverb if possible
            if len(self.used_words["adverb"]) > 0:
                # adverbs
                self.phrase += " " + random.choice(self.used_words["adverb"])

            # Throw in verb and ensure subject-verb agreement
            if self.chosen_noun[1][0][1][-1] == 'S':
                self.phrase += " " + self.conjugator("infinitive") + "."
            else:
                self.phrase += " " + self.conjugator("present") + "."

        return self.phrase

    def question(self):
        """Generate a question using the words in self.used_words."""
        self.phrase = random.choice(self.used_words["question_word"]) + " "

        if len(self.used_words["verb"]) == 0:
            self.phrase = "What are you doing?"
        elif len(self.used_words["noun"]) == 0:
            self.phrase = "What is your favorite thing to eat?"
        elif len(self.used_words["adverb"]) == 0:
            self.phrase = "How do people " + random.choice(self.used_words["verb"]) + " the " + random.choice(
                self.used_words["noun"]) + "?"
        else:
            self.type = random.randint(1, 2)
            if self.type == 1:
                # Who eats messily?
                self.phrase += random.choice(self.used_words["verb"]) + " " + random.choice(
                    self.used_words["adverb"]) + "?"
            else:
                #
                self.noun_options = self.used_words["noun"]
                for word in self.tags:
                    if word[1][0] == "N" and not word[0] in self.noun_options:
                        self.noun_options.append(word[0])
                    else:
                        try:
                            self.noun_options.append(random.choice(self.used_words['noun']))
                        except IndexError:
                            self.noun_options.append(random.choice(self.used_words['pronoun']))
                self.noun_choice = [random.choice(self.noun_options), None]
                self.noun_choice[1] = nltk.pos_tag(nltk.word_tokenize(self.noun_choice[0]))
                if self.noun_choice[1][0][1][-1] == "S":
                    self.phrase += "are " + self.noun_choice[0] + "?"
                else:
                    self.phrase += "is " + self.noun_choice[0] + "?"

        return self.phrase

    def phrasemaker(self, human_response):
        """Make a phrase to give to the human."""
        if not self.user_said_question(human_response):
            self.q = self.question()
            self.s = self.statement()
            self.phrases = [self.q, self.s]
            self.phrase = random.choice(self.phrases)
        else:
            self.phrase = random.choice(["Yes", "No"])
        return self.phrase

    def speak(self, response):
        """Learn words the human tells me and give them a response."""
        self.phrasefix = Decontract(response)
        self.tags = nltk.pos_tag(self.phrasefix.decontract())
        self.word_processor(self.tags)
        return self.phrasemaker(response)


if __name__ == "__main__":
    try:
        print("Loading. . .")
        bot = Talker()
        while True:
            response = str(input("> "))
            print(bot.speak(response))
    except (EOFError, KeyboardInterrupt):
        sys.exit()
