# sample-bot-iii.py

# sample bot to play in BOTFIGHTS III on botfights.ai


import random


FN_WORDLIST = 'wordlist-big.txt'


g_wordlists = None
def get_wordlist(wordlen):
    global g_wordlists
    if None == g_wordlists:
        g_wordlists = {}
        for i in open(FN_WORDLIST).readlines():
            i = i[:-1]
            if not len(i) in g_wordlists:
                g_wordlists[len(i)] = []
            g_wordlists[len(i)].append(i)
    return g_wordlists[wordlen]


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
    pairs = state.split(',')
    possible = get_wordlist(len(pairs[0].split(':')[0]))
    for pair in state.split(','):
        guess, feedback = pair.split(':')
        possible = list(filter(lambda x: could_match(x, guess, feedback), possible))
    return random.choice(possible)

