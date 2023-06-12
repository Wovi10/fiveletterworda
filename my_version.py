from itertools import groupby, tee
import time

WORD_LENGTH = 5
CHECKING_STEP = 500
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
CUSTOM_ORDER = ['q', 'x', 'j', 'z', 'v', 'f', 'w', 'b', 'k', 'g', 'p', 'm', 'h', 'd', 'c', 'y', 't', 'l', 'n', 'u', 'r', 'o', 'i', 's', 'e', 'a']

MAX_NUM_WORDS = len(ALPHABET) // WORD_LENGTH


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

    sorted_list = sorted(no_anagrams, key=lambda word: [CUSTOM_ORDER.index(letter) for letter in word])
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
    for current_letter_1, group_1 in groups_1:
        tried_groups_1 += current_letter_1
        group_1_list = list(group_1)
        for word1 in group_1_list:
            start_time = time.time()
            used_letters_1 = ""
            longest_possibility_of_word = []
            longest_possibility_of_word.append(word1)
            used_letters_1 = word1

            groups_2 = groupby(all_words, key=lambda x:x[0])
            tried_groups_2 = ""
            for current_letter_2, group_2 in groups_2:
                tried_groups_2 += current_letter_2
                if current_letter_2 in tried_groups_1:
                    continue
                group_2_list = list(group_2)
                possibility_2 = []
                possibility_2.append(word1)
                for word2 in group_2_list:
                    if word2 == word1:
                        continue
                    is_valid = check_word_to_other_word(used_letters_1, word2)
                    if not is_valid:
                        continue
                    used_letters_2 = ""
                    used_letters_2 = word1 + word2
                    if len(possibility_2) == 2:
                        possibility_2.pop()
                    possibility_2.append(word2)
                    if len(longest_possibility_of_word) < 2:
                        longest_possibility_of_word = possibility_2[:]
                    groups_3 = groupby(all_words, key=lambda x:x[0])
                    tried_groups_3 = ""
                    for current_letter_3, group_3 in groups_3:
                        tried_groups_3 += current_letter_3
                        if current_letter_3 in tried_groups_2:
                            continue
                        group_3_list = list(group_3)
                        possibility_3 = possibility_2[:]
                        for word3 in group_3_list:
                            if word3 in (word1, word2):
                                continue
                            is_valid = check_word_to_other_word(used_letters_2, word3)
                            if not is_valid:
                                continue
                            used_letters_3 = word1 + word2 + word3
                            if len(possibility_3) == 3:
                                possibility_3.pop()
                            possibility_3.append(word3)
                            if len(longest_possibility_of_word) <= 3:
                                longest_possibility_of_word = possibility_3[:]
                            groups_4 = groupby(all_words, key=lambda x:x[0])
                            tried_groups_4 = ""
                            for current_letter_4, group_4 in groups_4:
                                tried_groups_4 += current_letter_4
                                if current_letter_4 in tried_groups_3:
                                    continue
                                group_4_list = list(group_4)
                                possibility_4 = possibility_3[:]
                                for word4 in group_4_list:
                                    if word4 in (word1, word2, word3):
                                        continue
                                    is_valid = check_word_to_other_word(used_letters_3, word4)
                                    if not is_valid:
                                        continue
                                    used_letters_4 = word1 + word2 + word3 + word4
                                    if len(possibility_4) == 4:
                                        possibility_4.pop()
                                    possibility_4.append(word4)
                                    if len(longest_possibility_of_word) <= 4:
                                        longest_possibility_of_word = possibility_4[:]
                                    groups_5 = groupby(all_words, key=lambda x:x[0])
                                    for current_letter_5, group_5 in groups_5:
                                        if current_letter_5 in tried_groups_4:
                                            continue
                                        group_5_list = list(group_5)
                                        possibility_5 = possibility_4[:]
                                        for word5 in group_5_list:
                                            if word5 in (word1, word2, word3, word4):
                                                continue
                                            is_valid = check_word_to_other_word(used_letters_4, word5)
                                            if not is_valid:
                                                continue
                                            if len(possibility_5) == 5:
                                                possibility_5.pop()
                                            possibility_5.append(word5)
                                            if len(longest_possibility_of_word) <= 5:
                                                longest_possibility_of_word = possibility_5[:]
            copy_of_longest = longest_possibility_of_word[:]
            all_combinations.append(copy_of_longest)
            print(f"found one in {time.time() - start_time} seconds")

    return all_combinations

def main():
    all_words_to_check = get_all_words()
    all_combinations = []
    all_combinations = make_all_combinations(all_words_to_check)
    for combination in all_combinations:
        if len(combination) == MAX_NUM_WORDS:
            print("Found a combination:")
            print(combination)

    # old_way(all_words_to_check, words_tried)


def old_way(all_words_to_check, words_tried):
    for word in all_words_to_check:
        start_time = time.time()
        words_tried.append(index)
        longest_row_for_word = []
        words_tried_2 = []
        used_letters_1 = []
        possibility = []
        possibility.append(word)
        used_letters_1 = sorted(word)

        index2 = 0
        for word2 in all_words_to_check:
            words_tried_2.append(index2)
            if index2 in words_tried:
                index2 += 1
                continue
            index2 += 1

            is_valid = check_word_to_other_word(used_letters_1, word2)
            if not is_valid:
                continue

            used_letters_2 = sorted(word + word2)

            possibility_2 = possibility[:]
            possibility_2.append(word2)

            if len(possibility_2) >= len(longest_row_for_word):
                longest_row_for_word = possibility_2[:]

            words_tried_3 = []
            index3 = 0
            for word3 in all_words_to_check:
                words_tried_3.append(index3)
                if index3 in words_tried_2:
                    index3 += 1
                    continue
                index3 += 1

                is_valid = check_word_to_other_word(used_letters_2, word3)
                if not is_valid:
                    continue

                used_letters_3 = sorted(word + word2 + word3)

                possibility_3 = possibility_2[:]
                possibility_3.append(word3)

                if len(possibility_3) >= len(longest_row_for_word):
                    longest_row_for_word = possibility_3[:]

                words_tried_4 = []
                index4 = 0
                for word4 in all_words_to_check:
                    words_tried_4.append(index4)
                    if index4 in words_tried_3:
                        index4 +=1
                        continue
                    index4 +=1

                    is_valid = check_word_to_other_word(used_letters_3, word4)
                    if not is_valid:
                        continue

                    used_letters_4 = sorted(word + word2 + word3 + word4)

                    possibility_4 = possibility_3[:]
                    possibility_4.append(word4)

                    if len(possibility_4) >= len(longest_row_for_word):
                        longest_row_for_word = possibility_4[:]

                    index5 = 0
                    for word5 in all_words_to_check:
                        if index5 in words_tried_4:
                            index5 += 1
                            continue
                        index5 += 1

                        is_valid = check_word_to_other_word(used_letters_4, word5)
                        if not is_valid:
                            continue

                        if (len(possibility_4) + 1) > len(longest_row_for_word):
                            longest_row_for_word = possibility_4[:]
                            longest_row_for_word.append(word5)

        if len(possibility) >= len(longest_row_for_word):
            longest_row_for_word = possibility[:]
        if len(longest_row_for_word) >= len(longest_row):
            longest_row = longest_row_for_word[:]

        index += 1
        if index % CHECKING_STEP == 0:
        # if word == "dwarf":
            print(f"Tested {index} words.")
            print(longest_row)

def check_word2(all_words_to_check, used_letters, possibility):
    possibility_2 = check_word_row(all_words_to_check, used_letters, possibility)
    if len(possibility_2) >= len(possibility):
        return possibility_2
    return possibility

def check_word3(all_words_to_check, used_letters_2, possibility_2):
    possibility_3 = check_word_row(all_words_to_check, used_letters_2, possibility_2)
    if len(possibility_3) >= len(possibility_2):
        return possibility_3
    return possibility_2

def check_word4(all_words_to_check, used_letters_3, possibility_3):
    possibility_4 = check_word_row(all_words_to_check, used_letters_3, possibility_3)
    if len(possibility_4) >= len(possibility_3):
        return possibility_4
    return possibility_3

def check_word_row(all_words_to_check:list, used_letters:list, possibility:list) -> list:
    for word in all_words_to_check:
        is_valid = check_word_to_other_word(used_letters, word)
        if not is_valid:
            continue

        used_letters_1 = used_letters
        possibility_1 = possibility
        possibility_1.append(word)
        for letter in word:
            used_letters_1.append(letter)

        if len(possibility_1) >= len(possibility):
            possibility = possibility_1

    return possibility

main()
