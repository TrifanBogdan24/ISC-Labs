import requests

TARGET_URL = "http://localhost:8080"
WORDLIST_PATH = "wordlist.txt"


def fuzz_directories(target_url, wordlist_path):

    # TODO1 - open the wordlist file
    directories = []

    for dir_name in directories:

        # TODO2 - remove all whitelines and newlines from the directories

        # TODO3 - build the url

        # TODO4 - send a GET request to the constructed URL

        # TODO5 - verify if the directory exists or not by checking the
        #         response and print a meaningful message

        pass


fuzz_directories(TARGET_URL, WORDLIST_PATH)
