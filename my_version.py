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

def check_word_to_other_word(used_letters, word2):
    for letter in sorted(word2):
        if letter in used_letters:
            return False
    return True

def main():
    longest_row = []
    all_words_to_check = get_all_words()
    index = 0
    words_tried = []
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
