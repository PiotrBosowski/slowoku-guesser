def load_wordlist(dict_path, word_length):
    wordlist = []
    with open(dict_path, encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if len(word) == word_length:
                wordlist.append(word)
    return wordlist
