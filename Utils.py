import time
from contextlib import suppress
from random import choice, randint
from uuid import uuid4

from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, ANIMALS, COLORS, COUNTRIES, LANGUAGES, NAMES, STAR_WARS


class Utils:
    @staticmethod
    def replace(text: str, new: dict) -> str:
        for old, new in new.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def makeString(string_length=8):
        while True:
            rnd = str(uuid4())
            rnd = rnd.upper()
            rnd = rnd.replace("-", "")
            if not rnd[0:string_length][:1].isdigit():
                return rnd[0:string_length]

    @staticmethod
    def logger(email: str, password: str):
        open('accounts.txt', 'a+').write(f'{email}:{password}\n')

    def eGen(self):
        while True:
            try:
                return self.randomize(get_random_name(
                    combo=[NAMES, choice([ADJECTIVES, ANIMALS, COLORS, COUNTRIES, LANGUAGES, NAMES, STAR_WARS])],
                    separator="").replace(" ", "") + (str(randint(0, 999)) if randint(0, 1) else ""))
            except:
                continue

    def randomize(self, string: str):
        return string.replace(string[randint(0, len(string))], self.makeString(1))


class Timer:
    def __init__(self):
        self.start_time = float
        self.now = float

    def start(self, t: time.time()):
        self.start_time = t

    def reset(self, t: time.time()):
        self.start_time = t

    def timer(self, t: time.time()):
        self.now = t - self.start_time
        return self.now
