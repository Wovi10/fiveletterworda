from itertools import groupby
import math
import time

WORD_LENGTH = 5
CHECKING_STEP = 1000
CUSTOM_ORDER = ['q', 'x', 'j', 'z', 'v', 'f', 'w', 'b', 'k', 'g', 'p', 'm',
                'h', 'd', 'c', 'y', 't', 'l', 'n', 'u', 'r', 'o', 'i', 's', 'e', 'a']

MAX_NUM_WORDS = 26 // WORD_LENGTH


def get_all_words():
    words_txt = './words_alpha.txt'
    with open(words_txt, 'r', encoding="utf-8") as word_file:
        all_words_in_list = list(word_file.read().split())

    print(f"There are {len(all_words_in_list)} words in total.")

    right_length = []
    for word_to_check in all_words_in_list:
        if len(word_to_check) == WORD_LENGTH:
            right_length.append(word_to_check)

    print(f"There are {len(right_length)} words with the right length.")

    valid_words = []
    for word in right_length:
        is_valid = check_word(word)
        if is_valid:
            valid_words.append(word)

    print(f"There are {len(valid_words)} words without repeating letters.")

    no_anagrams = []
    sorted_words = []
    for word in valid_words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in sorted_words:
            continue
        sorted_words.append(sorted_word)
        no_anagrams.append(word)

    print(f"There are {len(no_anagrams)} words that aren't anagrams.")

    sorted_list = sorted(no_anagrams, key=lambda word:
        [CUSTOM_ORDER.index(letter) for letter in word])
    print("Sorted according to custom order")
    return sorted_list


def check_word(word):
    temp_used_letter = []
    for letter in sorted(word):
        if letter in temp_used_letter:
            return False
        temp_used_letter.append(letter)
    return True


def check_word_to_other_word(used_letters, word):
    index = 0
    for letter in sorted(word):
        if letter in sorted(used_letters, key=lambda word:
            [CUSTOM_ORDER.index(letter) for letter in word]):
            return False
        index += 1
    return True


def make_all_combinations():
    word_loop("", [], [])


def word_loop(previous_tried_groups, previous_words, possibility,
              depth = 1, counter = 0, start_time = time.time()):
    groups = groupby(all_words, key=lambda x:x[0])
    tried_groups = ""
    for current_letter, group in groups:
        tried_groups += current_letter
        if current_letter in previous_tried_groups:
            continue
        group_list = list(group)
        for word in group_list:
            if len(previous_words) == depth:
                previous_words.pop()
            if depth == 1:
                possibility = []
                previous_words = []
            used_letters, possibility = default_loop_actions(word, previous_words, possibility)
            if used_letters == "":
                continue
            previous_words.append(word)
            words = previous_words[:]
            all_combinations.append(words)
            if len(words) == MAX_NUM_WORDS:
                print("WOOHOOOOOW")
                print(words)
            if len(words)+1 > MAX_NUM_WORDS:
                return possibility
            possibility = word_loop(tried_groups, words, possibility,
                                    depth+1, counter, start_time)
            if depth == 1:
                counter += 1
                if counter % CHECKING_STEP == 0:
                    print(f"Found {counter-CHECKING_STEP}-{counter} in " +
                          f"{time.time() - start_time} seconds")
                    start_time = time.time()
    return possibility


def default_loop_actions(word_in_loop, previous_words, possibility):
    used_letters = "".join(previous_words)
    if word_in_loop in previous_words:
        return "", possibility
    is_valid = check_word_to_other_word(used_letters, word_in_loop)
    if not is_valid:
        return "", possibility
    possibility = previous_words[:]
    possibility.append(word_in_loop)
    if len(possibility) <= len(possibility):
        possibility = possibility[:]
    return "".join(possibility), possibility


def main():
    make_all_combinations()
    for combination in all_combinations:
        # if len(combination) == MAX_NUM_WORDS:
        #     print("Found a combination:")
        print(combination)


def calculate_time_passed(start_time, end_time):
    total_time = end_time - start_time
    total_hours = 0
    total_minutes = 0
    total_seconds = total_time / 60
    if total_time / 60 > 1:
        total_seconds = total_time % 60
        total_minutes = total_time / 60
        if total_minutes / 60 > 1:
            total_minutes %= 60
            total_hours = total_minutes / 60
    return f"{total_hours}h:{total_minutes}m:{total_seconds}s"


program_start_time = time.time()
all_words = get_all_words()
all_combinations = []
main()

passed_time = calculate_time_passed(program_start_time, time.time())
print(f"====== Finished running in {passed_time}. ======")
