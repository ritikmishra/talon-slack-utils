"""Download all the necessary modules for the server."""
import nltk

def install():
    modules = open("nltk.txt", "r")
    for corpus in modules:
        corpus = corpus[:-1]
        print("Installing " + corpus + ". . .")
        nltk.download(corpus)

if __name__ == "__main__":
    install()