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


def make_all_combinations(all_words):
    all_combinations = []
    groups_1 = groupby(all_words, key=lambda x:x[0])
    tried_groups_1 = ""
    index = 0
    start_time = time.time()
    for current_letter_1, group_1 in groups_1:
        tried_groups_1 += current_letter_1
        group_1_list = list(group_1)
        for word1 in group_1_list:
            longest_possibility_of_word = []
            longest_possibility_of_word.append(word1)
            previous_words_2 = []
            previous_words_2.append(word1)
            longest_possibility_of_word = word_loop(all_words, tried_groups_1, previous_words_2,
                                                    longest_possibility_of_word, 2)
            copy_of_longest = longest_possibility_of_word[:]
            all_combinations.append(copy_of_longest)
            index += 1
            if len(copy_of_longest) == MAX_NUM_WORDS:
                print(f"YESSSSSSSSSSSS, {copy_of_longest}")
            if index % CHECKING_STEP == 0:
                print(f"Checked {index} in {time.time() - start_time} seconds")
                print(copy_of_longest)
                start_time = time.time()

    return all_combinations


def word_loop(all_words, previous_tried_groups, previous_words, longest_possibility_of_word, depth):
    groups = groupby(all_words, key=lambda x:x[0])
    tried_groups = ""
    for current_letter, group in groups:
        tried_groups += current_letter
        if current_letter in previous_tried_groups:
            continue
        group_list = list(group)
        for word in group_list:
            used_letters, longest_possibility_of_word = default_loop_actions(word, previous_words,
                                                                             longest_possibility_of_word)
            if used_letters == "":
                continue
            if len(previous_words) == depth:
                previous_words.pop()
            previous_words.append(word)
            words = previous_words[:]
            if depth >= 5:
                return longest_possibility_of_word
            longest_possibility_of_word = word_loop(all_words, tried_groups, words,
                                                    longest_possibility_of_word, depth+1)
    return longest_possibility_of_word


def default_loop_actions(word_in_loop, previous_words, longest_possibility_of_word):
    used_letters = "".join(previous_words)
    if word_in_loop in previous_words:
        return "", longest_possibility_of_word
    is_valid = check_word_to_other_word(used_letters, word_in_loop)
    if not is_valid:
        return "", longest_possibility_of_word

    possibility = previous_words[:]
    possibility.append(word_in_loop)
    if len(longest_possibility_of_word) <= len(possibility):
        longest_possibility_of_word = possibility[:]
    return "".join(possibility), longest_possibility_of_word


def main():
    program_start_time = time.time()
    all_words_to_check = get_all_words()
    all_combinations = []
    all_combinations = make_all_combinations(all_words_to_check)
    longest_combo = []
    for combination in all_combinations:
        if len(combination) > len(longest_combo):
            longest_combo = combination[:]
        if len(combination) == MAX_NUM_WORDS:
            print("Found a combination:")
            print(combination)
    print(f"Longest combo is {longest_combo}")
    total_time_hours = 0
    total_time_minutes = 0
    total_time_seconds = time.time() - program_start_time
    if total_time_seconds / 60 > 1:
        total_time_minutes = math.floor(total_time_seconds / 60)
        total_time_seconds %= 60
        if total_time_minutes / 60 > 1:
            total_time_hours = math.floor(total_time_minutes / 60)
            total_time_minutes %= 60
    total_time = ""
    if total_time_hours > 0:
        total_time = f"{total_time_hours} hours {total_time_minutes} minutes and {total_time_seconds} seconds"
    elif total_time_minutes > 0:
        total_time = f"{total_time_minutes} minutes and {total_time_seconds} seconds"
    else:
        total_time = f"{total_time_seconds} seconds"
    print(f"Finished in {total_time}")


main()
