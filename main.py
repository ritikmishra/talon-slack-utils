from __future__ import division

#natural language toolkit
import nltk,sys,random,subprocess,enchant
from contractions import Decontract
#word_history = open('words.json', 'a+'))
#get this working plzroces
dictionary = enchant.Dict("en_US")

used_words = {
        "noun":[] ,
        "pronoun":[] ,
        "verb":[] ,
        "adjective":[] ,
        "adverb":[] ,
        "preposition":[] ,
        "conjunction":[] ,
        "interjection":[] ,
        "question_word":["Who"]

        }
def close():

    sys.exit()


def word_processor(tags):
    global used_words
    #print "funct called"
    for word in tags:
        #print word

        if dictionary.check(word[0]):

            if word[1][0] == "N":
                used_words["noun"].append(word[0].lower())

            elif word[1][0:2] == "PR":
                used_words["pronoun"].append(word[0])
            elif (word[1][0:2] == "VB" or word[1][0:2] == "MD") and word[0] != "would" and word[0] != "could" and word[0] != "should"  :
                used_words["verb"].append(subprocess.check_output(['nodejs','conjugate.js',word[0],'infinitive']).rstrip())
            elif word[1][0:2] == "JJ":
                used_words["adjective"].append(word[0].lower())
            elif word[1][0:2] == "RB":
                used_words["adverb"].append(word[0].lower())
            elif word[1][0:2] == "IN":
                used_words["preposition"].append(word[0].lower())
            elif word[1][0:2] == "CC":
                used_words["conjunction"].append(word[0].lower())
            elif word[1][0:2] == "UH":
                used_words["interjection"].append(word[0].lower())
            elif word[1][0] == "W":
                used_words["question_word"].append(word[0].lower())
    #print used_words
    #used for debug purposes only

def statement():
    global used_words
    if len(used_words["verb"]) == 0:
        phrase = "What are you doing?"
    elif len(used_words["noun"]) == 0:
        phrase = "Tell me what I look like."
    else:
        phrase = "The "
        chosen_noun = [random.choice(used_words["noun"]),None]
        chosen_noun[1] = nltk.pos_tag(nltk.word_tokenize(chosen_noun[0]))
        if len(used_words["adjective"]) == 0:
            #adjective not exist

            phrase += chosen_noun[0]
            if len(used_words["adverb"]) == 0:
                if chosen_noun[1][0][1][-1] == 'S':
                    phrase += " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'infinitive']).rstrip() + "."
                else:
                    phrase += " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'present']).rstrip() + "."
            else:
                if chosen_noun[1][0][1][-1] == 'S':
                    phrase += " " + random.choice(used_words["adverb"]) + " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'infinitive']).rstrip() + "."
                else:
                    phrase += " " + random.choice(used_words["adverb"]) + " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'present']).rstrip() + "."
        else:
            #adjective exists
            phrase += " " + random.choice(used_words["adjective"]) + " " +  chosen_noun[0]
            if len(used_words["adverb"]) == 0:
                if chosen_noun[1][0][1][-1] == 'S':
                    phrase += " " +  subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'infinitive']).rstrip() + "."
                else:
                    phrase += " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'present']).rstrip() + "."

            else:
                if chosen_noun[1][0][1][-1] == 'S':
                    phrase += " " + random.choice(used_words["adverb"]) + " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'infinitive']).rstrip() + "."
                else:
                    phrase += " " + random.choice(used_words["adverb"]) + " " + subprocess.check_output(['nodejs','conjugate.js',random.choice(used_words["verb"]),'present']).rstrip() + "."

    #phrase = "The " + random.choice(used_words["adjective"]) + " " + random.choice(used_words["noun"]) + " " + random.choice(used_words["adverb"]) + " " + random.choice(used_words["verb"]) + "."
    return phrase
def question():
    global used_words, tags
    phrase = random.choice(used_words["question_word"]) + " "

    if len(used_words["verb"]) == 0:
        phrase = "What are you doing?"
    elif len(used_words["adverb"]) == 0:
        phrase = "How do people " + random.choice(used_words["verb"]) + " the " + random.choice(used_words["noun"]) + "?"
    else:
        z = random.randint(1,2)
        if z == 1:
            phrase += random.choice(used_words["verb"]) +  " " + random.choice(used_words["adverb"]) + "?"
        else:
            noun_options = []
            for word in tags:
                if word[1][0] == "N":
                    noun_options.append(word[0])
                else:
                    try:
                        noun_options.append(random.choice(used_words['noun']))
                    except IndexError:
                        noun_options.append(random.choice(used_words['pronoun']))
            noun_choice =  [random.choice(noun_options),None]
            noun_choice[1] = nltk.pos_tag(nltk.word_tokenize(noun_choice[0]))
            if noun_choice[1][0][1][-1] == "S":
                phrase += "are " + noun_choice[0] + "?"
            else:
                phrase += "is " + noun_choice[0] + "?"

    return phrase
def phrasemaker():
    q = question()
    s = statement()
    phrases = [q, s]
    phrase = random.choice(phrases)
    return phrase


def main():
    global tags
    init_speech = "Type 'exit' to stop talking\n\n\nHello, how may I help you?"
    print init_speech
    speech = subprocess.Popen(['espeak',init_speech])
    while True:
        human_response = str(raw_input("> "))
        if human_response == "exit":
            close()
        else:
            phrasefix = Decontract(human_response)
        tags = nltk.pos_tag(phrasefix.decontract())
        #tags = nltk.pos_tag(nltk.word_tokenize(human_response))

        word_processor(tags)
        bot_response = phrasemaker()
        speech = subprocess.Popen(['espeak',bot_response])
        print bot_response
try:
    main()
except (EOFError, KeyboardInterrupt):
    close()
