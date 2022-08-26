from adventkit import parse


def solve(puzzle_input):
    phrases = parse.string_rows(puzzle_input)

    duplicate_free_count = 0
    for phrase in phrases:
        if all_words_unique(phrase):
            duplicate_free_count += 1
    print(duplicate_free_count)

    anagram_free_count = 0
    for phrase in phrases:
        tidied_phrase = [''.join(sorted(word)) for word in phrase]
        if all_words_unique(tidied_phrase):
            anagram_free_count += 1
    print(anagram_free_count)


def all_words_unique(phrase):
    return len(set(phrase)) == len(phrase)
