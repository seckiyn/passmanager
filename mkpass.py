"""
    What a password generator needs:
        - Length of password
        - What should password contains
            - Lower case
            - Upper case
            - Numbers
            - Symbols
            - Whitespace?
        - Fun Ideas Maybe
            - Funny numbers add
            - Any unicode character
            - Funny names


"""
import random
import math
import string
class Char:
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation


def getLower():
    return random.choice(Char.lowercase)

def getUpper():
    return random.choice(Char.uppercase)

def getDigit():
    return random.choice(Char.digits)

def getSymbol():
    return random.choice(Char.symbols)

def shuffle(word):
    word = list(word)
    random.shuffle(word)
    new_word = ''.join(word)
    return new_word
def getPassword(length, isLower, isUpper, isDigit, isSymbol):
    password = ""
    options = {
            "isLower": (isLower, getLower),
            "isUpper": (isUpper, getUpper),
            "isDigit": (isDigit, getDigit),
            "isSymbol": (isSymbol, getSymbol)
            }
    for key, value in options.items():
        isIt, func = value
        if isIt:
            password += func()

    trueoptions = dict()
    for key, value in options.items():
        isIt, func = value
        if isIt:
            trueoptions[key] = func
    # DEBUG
    print(trueoptions)
    print(password)

    keys = list(trueoptions.keys())

    for char in range(length-len(password)):
        key = random.choice(keys)
        func = trueoptions[key]
        password += func()

    # Scramble the password
    password = shuffle(password)

    # DEBUG
    print(password)
    print("Length of password: ", len(password))









def main():
    length = int(input("Length: "))
    isLower = input("Is Lower: ")
    isUpper = input("Is Upper: ")
    isDigit = input("Is Digit: ")
    isSymbol = input("Is Symbol: ")
    getPassword(length, isLower, isUpper, isDigit, isSymbol)


if __name__ == "__main__":
    main()
