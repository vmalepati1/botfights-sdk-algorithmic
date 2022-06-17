import random

FN_WORDLIST = 'wordlist.txt'

g_wordlist = None

def get_wordlist():
    global g_wordlist
    if None == g_wordlist:
        g_wordlist = []
        for i in open(FN_WORDLIST).readlines():
            i = i[:-1]
            g_wordlist.append(i)
    return g_wordlist

def get_word_table(gray_letters, yellow_letters, green_letters, subset, verbose=True):
    table_result = []
        
    for word in (tqdm(subset) if verbose else subset):
        # Innocent till proven guilty
        viable_word = True

        for letter, idx in gray_letters.items():
            if letter in word:
                if letter not in yellow_letters and letter not in green_letters:
                    viable_word = False
                    break
                else:
                    indices = [pos for pos, char in enumerate(word) if char == letter]

                    if idx in indices:
                        viable_word = False
                        break

        if viable_word is True:
            for letter, idx in yellow_letters.items():
                if letter not in word:
                    viable_word = False
                    break

                indices = [pos for pos, char in enumerate(word) if char == letter]

                if idx in indices:
                    viable_word = False
                    break

        if viable_word is True:
            for letter, idx in green_letters.items():
                if letter not in word:
                    viable_word = False
                    break

                indices = [pos for pos, char in enumerate(word) if char == letter]

                if idx not in indices:
                    viable_word = False
                    break

        if viable_word is True:
            table_result.append(word)

    return table_result

already_solved_words = []

def play(state):
    # state looks like: "-----:00000,arose:31112,amend:31211"
    wordlist = get_wordlist()

    green_letters = {}
    yellow_letters = {}
    gray_letters = {}

    split_states = state.split(',')

    num_states = len(split_states)
    
    if num_states > 1:
        for pair in split_states:
            guess, feedback = pair.split(':')

            if guess != '-----':
                for idx, evaluation in enumerate(feedback):
                    if evaluation == '3':
                        green_letters[guess[idx]] = idx
                    elif evaluation == '2':
                        yellow_letters[guess[idx]] = idx
                    else:
                        gray_letters[guess[idx]] = idx

        word_table = get_word_table(gray_letters, yellow_letters, green_letters, wordlist, verbose=False)

        return random.choice(word_table)
    else:
        return 'slate'

