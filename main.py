from __future__ import division

#natural language toolkit
import nltk,sys,random,subprocess,enchant
from contractions import Decontract
#word_history = open('words.json', 'a+'))
#get this working plzroces

class Talker:
    def __init__(self):
        self.dictionary = enchant.Dict("en_US")

        self.used_words = {
                "noun":[] ,
                "pronoun":[] ,
                "verb":[] ,
                "adjective":[] ,
                "adverb":[] ,
                "preposition":[] ,
                "conjunction":[] ,
                "interjection":[] ,
                "question_word":["Who"],
                "determiner": ["a", "the"]

                }
    def __str__(self):
        return self.used_words

    def user_said_question(self, human_response):
        self.qtype = subprocess.check_output(['nodejs','questions.js', str(human_response)]).strip().decode("UTF-8")
        if self.qtype == "YN":
            return True
        else:
            return False

    def conjugator(self, form):
        self.verb = subprocess.check_output(['nodejs','conjugate.js',random.choice(self.used_words["verb"]),form]).strip().decode("UTF-8")
        if self.verb == "does" or self.verb == "makes" or self.verb == "doing":
            self.verb +=  " " + random.choice(self.used_words["determiner"]) + " " + random.choice(self.used_words["noun"])
        return self.verb

    def word_processor(self, tags):
        for word in tags:
            #print(word)
            if self.dictionary.check(word[0]):

                if word[1][0] == "N":
                    self.used_words["noun"].append(word[0].lower())
                elif word[1][0:2] == "PR":
                    self.used_words["pronoun"].append(word[0])
                elif (word[1][0:2] == "VB" or word[1][0:2] == "MD") and word[0] != "would" and word[0] != "could" and word[0] != "should"  :
                    self.used_words["verb"].append(subprocess.check_output(['nodejs','conjugate.js',word[0],'infinitive']).strip().decode("UTF-8"))
                elif word[1][0:2] == "JJ":
                    self.used_words["adjective"].append(word[0].lower())
                elif word[1][0:2] == "RB":
                    self.used_words["adverb"].append(word[0].lower())
                elif word[1][0:2] == "IN":
                    self.used_words["preposition"].append(word[0].lower())
                elif word[1][0:2] == "CC":
                    self.used_words["conjunction"].append(word[0].lower())
                elif word[1][0:2] == "UH":
                    self.used_words["interjection"].append(word[0].lower())
                elif word[1][0] == "W":
                    self.used_words["question_word"].append(word[0].lower())
                elif word[1][0] == "DT":
                    self.used_words["determiner"].append(word[0].lower())
        # print(self.used_words)
        #used for debug purposes only

    def statement(self):
        """Generate a statement using the words in self.used_words"""
        if len(self.used_words["verb"]) == 0:
            self.phrase = "What are you doing?"
        elif len(self.used_words["noun"]) == 0:
            self.phrase = "Tell me what I look like."
        else:
            self.phrase = random.choice(self.used_words["determiner"]).capitalize()
            self.chosen_noun = [random.choice(self.used_words["noun"]),None]
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
        """Generate a question using the words in self.used_words"""
        self.phrase = random.choice(self.used_words["question_word"]) + " "

        if len(self.used_words["verb"]) == 0:
            self.phrase = "What are you doing?"
        elif len(self.used_words["noun"]) == 0:
            self.phrase = "What is your favorite thing to eat?"
        elif len(self.used_words["adverb"]) == 0:
            self.phrase = "How do people " + random.choice(self.used_words["verb"]) + " the " + random.choice(self.used_words["noun"]) + "?"
        else:
            self.type = random.randint(1,2)
            if self.type == 1:
                # Who eats messily?
                self.phrase += random.choice(self.used_words["verb"]) +  " " + random.choice(self.used_words["adverb"]) + "?"
            else:
                # Who
                self.noun_options = []
                for word in self.tags:
                    if word[1][0] == "N":
                        self.noun_options.append(word[0])
                    else:
                        try:
                            self.noun_options.append(random.choice(self.used_words['noun']))
                        except IndexError:
                            self.noun_options.append(random.choice(self.used_words['pronoun']))
                self.noun_choice =  [random.choice(self.noun_options),None]
                self.noun_choice[1] = nltk.pos_tag(nltk.word_tokenize(self.noun_choice[0]))
                if self.noun_choice[1][0][1][-1] == "S":
                    self.phrase += "are " + self.noun_choice[0] + "?"
                else:
                    self.phrase += "is " + self.noun_choice[0] + "?"

        return self.phrase

    def phrasemaker(self, human_response):
        if not self.user_said_question(human_response):
            self.q = self.question()
            self.s = self.statement()
            self.phrases = [self.q, self.s]
            self.phrase = random.choice(self.phrases)
        else:
            self.phrase = random.choice(["Yes","No"])
        return self.phrase



    def speak(self, response):
        self.phrasefix = Decontract(response)
        self.tags = nltk.pos_tag(self.phrasefix.decontract())
        self.word_processor(self.tags)
        return self.phrasemaker(response)

if __name__ == "__main__":
    try:
        bot = Talker()
        while True:
            response = str(input("> "))
            print(bot.speak(response))
    except (EOFError, KeyboardInterrupt):
        sys.exit()
