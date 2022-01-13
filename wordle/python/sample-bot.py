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
def could_match(target, last_guess, last_score):
    for i, ch in enumerate(last_score):
        if '3' == ch:
            if target[i] != last_guess[i]:
                return False
        else:
            if target[i] == last_guess[i]:
                return False
    return True


def play(state):
    guess_num, secret_hash, last_guess, last_score = state.split()
    possible = list(filter(lambda x: could_match(x, last_guess, last_score), get_wordlist()))
    return random.choice(possible)

