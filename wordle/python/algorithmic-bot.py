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

        for letter, idx in gray_letters:
            if letter in word:
                yellow_letters_subset = [p[0] for p in yellow_letters]
                green_letters_subset = [p[0] for p in green_letters]
                
                if letter not in yellow_letters_subset and letter not in green_letters_subset:
                    viable_word = False
                    break
                else:
                    indices = [pos for pos, char in enumerate(word) if char == letter]

                    if idx in indices:
                        viable_word = False
                        break

        if viable_word is True:
            for letter, idx in yellow_letters:
                if letter not in word:
                    viable_word = False
                    break

                indices = [pos for pos, char in enumerate(word) if char == letter]

                if idx in indices:
                    viable_word = False
                    break

        if viable_word is True:
            for letter, idx in green_letters:
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

guessed_words = []
correct_words = []

def play(state):
    global guessed_words
    global correct_words
    
    # state looks like: "-----:00000,arose:31112,amend:31211"
    wordlist = get_wordlist()

    green_letters = []
    yellow_letters = []
    gray_letters = []

    split_states = state.split(',')

    num_states = len(split_states)

    last_guess, last_feedback = split_states[-1].split(':')
    
    if num_states > 1:
        for pair in split_states:
            guess, feedback = pair.split(':')

            if guess != '-----':
                for idx, evaluation in enumerate(feedback):
                    if evaluation == '3':
                        green_letters.append((guess[idx], idx))
                    elif evaluation == '2':
                        yellow_letters.append((guess[idx], idx))
                    elif evaluation == '1':
                        gray_letters.append((guess[idx], idx))

        # Might be picking same word as those already guessed
        word_table = get_word_table(gray_letters, yellow_letters, green_letters, wordlist, verbose=False)

        word_table = [w for w in word_table if w not in correct_words]

        word = random.choice(word_table)

        guessed_words.append(word)

        return word
    else:
        if len(guessed_words) > 0:
            correct_words.append(guessed_words[-1])
            # print(correct_words)

            guessed_words = []
        
        return 'arise'

