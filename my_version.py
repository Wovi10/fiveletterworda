import time

WORD_LENGTH = 5
CHECKING_STEP = 100
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

MAX_NUM_WORDS = len(ALPHABET) // WORD_LENGTH

# def get_valid_words():
#     valids = []
#     for word in ALL_WORDS:
#         if len(word) != WORD_LENGTH:
#             continue
#         temp_used_letter = []
#         for letter in word:
#             if letter in temp_used_letter:
#                 continue
#             temp_used_letter.append(letter)
#         valids.append(word)
#     return valids

# VALID_WORDS = get_valid_words()

# used_letters = []
# succesful_words = []


# def check_word(word):
#     if len(word) != WORD_LENGTH:
#         return False
#     temp_used_letter = []
#     for letter in word:
#         if letter in used_letters or letter in temp_used_letter:
#             return False
#         temp_used_letter.append(letter)
#     return True

# def go_over_words():
#     index = 1
#     for word in ALL_WORDS:
#         if index % CHECKING_STEP == 0:
#             print(f"Already checked {index} words. Found {len(succesful_words)} so far.")
#         is_valid = check_word(word)
#         if is_valid:
#             succesful_words.append(word)
#             for letter in word:
#                 used_letters.append(letter)
#         index = index + 1


# def main():
#     print(f"{len(ALL_WORDS)} words in total")
#     start_time = time.time()
#     while len(succesful_words) != MAX_NUM_WORDS:
#         go_over_words()
#     end_time = time.time()
#     print("\nFound following words:")
#     for word in succesful_words:
#         print(word)
#     print(f"\nTotal time: {end_time - start_time}")
#     print(start_time)
#     print(end_time)

# main()


####################################################################################################


words_different_letters = []

# def get_words():
#     all_words = []
#     words_txt = './words_alpha.txt'
#     with open(words_txt, 'r', encoding="utf-8") as word_file:
#         all_words = list(word_file.read().split())

#     valid_words = []
#     sorted_words = []
#     index = 0
#     for word_to_check in all_words:
#         if len(word_to_check) != WORD_LENGTH:
#             continue
#         temp_used_letter = []
#         for letter in word_to_check:
#             if letter in temp_used_letter:
#                 continue
#             temp_used_letter.append(letter)
#         sorted_word = ''.join(sorted(word_to_check))
#         if sorted_word in sorted_words:
#             continue
#         sorted_words.append(sorted_word)
#         valid_words.append(word_to_check)
#         index += 1

#     return valid_words


# def word_is_valid(word):
#     for letter in word:
#         if letter in used_letters:
#             return False
#     return True

# def iterate_words(valid_words):
#     temp_words_list = []
#     for word in valid_words:
#         is_valid = word_is_valid(word)
#         if not is_valid:
#             continue
#         temp_words_list.append(word)


# def main_for_real():
#     valid_words = get_words()
#     iterate_words(valid_words)



# main_for_real()



def get_all_words():
    words_txt = './words_alpha.txt'
    with open(words_txt, 'r', encoding="utf-8") as word_file:
        all_words_in_list = list(word_file.read().split())

    print(f"There are {len(all_words_in_list)} words in total.")
    return all_words_in_list

def all_word_length_words(all_words_correct_length):
    valid_words = []
    for word_to_check in all_words_correct_length:
        if len(word_to_check) != WORD_LENGTH:
            continue
        valid_words.append(word_to_check)

    print(f"There are {len(valid_words)} words with the right length.")
    return valid_words

def check_word(word):
    temp_used_letter = []
    for letter in word:
        if letter in temp_used_letter:
            return False
        temp_used_letter.append(letter)
    return True

def all_different_letter_words(words):
    valid_words = []
    for word in words:
        is_valid = check_word(word)
        if is_valid:
            valid_words.append(word)

    print(f"There are {len(valid_words)} words without repeating letters.")
    return valid_words

def no_angram_words(words):
    no_anagrams = []
    sorted_words = []
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in sorted_words:
            continue
        sorted_words.append(sorted_word)
        no_anagrams.append(word)

    print(f"There are {len(no_anagrams)} words that aren't anagrams.")
    return no_anagrams


all_words = get_all_words()
correct_length = all_word_length_words(all_words)
different_letters = all_different_letter_words(correct_length)
no_angram_words(different_letters)