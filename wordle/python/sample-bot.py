# sample-bot.py

# sample bot to play wordle. see wordle.py for how to play.


import random


g_wordlist = None
def get_wordlist():
    global g_wordlist
    if None == g_wordlist:
        g_wordlist = []
        for i in open('wordlist.txt').readlines():
            i = i[:-1]
            g_wordlist.append(i)
    return g_wordlist


# this has lots of false positives, only pay attention to 3s
#
def could_match(target, guess, feedback):
    for i, ch in enumerate(feedback):
        if '3' == ch:
            if target[i] != guess[i]:
                return False
        else:
            if target[i] == guess[i]:
                return False
    return True


def play(state):
    # state looks like: "-----:00000,arose:31112,amend:31211"
    possible = get_wordlist()
    for pair in state.split(','):
        guess, feedback = pair.split(':')
        possible = list(filter(lambda x: could_match(x, guess, feedback), possible))
    return random.choice(possible)

