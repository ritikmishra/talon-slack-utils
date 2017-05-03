"""Download all the necessary modules for the server."""
import nltk
if __name__ == "__main__":
    modules = open("nltk.txt", "r")
    for corpus in modules:
        print("Installing " + corpus + ". . .")
        nltk.download(corpus)
