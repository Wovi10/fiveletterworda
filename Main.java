import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    private static final int WORD_LENGTH = 5;
    private static final int CHECKING_STEP = 500;
    private static final List<Character> ALPHABET = Arrays.asList('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
    private static final List<Character> CUSTOM_ORDER = Arrays.asList('q', 'x', 'j', 'z', 'v', 'f', 'w', 'b', 'k', 'g', 'p', 'm', 'h', 'd', 'c', 'y', 't', 'l', 'n', 'u', 'r', 'o', 'i', 's', 'e', 'a');

    private static final int MAX_NUM_WORDS = ALPHABET.size() / WORD_LENGTH;

    public static List<String> getAllWords() {
        String wordsTxt = "./words_alpha.txt";
        List<String> allWordsInList = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(wordsTxt))) {
            String line;
            while ((line = reader.readLine()) != null) {
                allWordsInList.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("There are " + allWordsInList.size() + " words in total.");

        List<String> rightLength = new ArrayList<>();
        for (String word : allWordsInList) {
            if (word.length() == WORD_LENGTH) {
                rightLength.add(word);
            }
        }

        System.out.println("There are " + rightLength.size() + " words with the right length.");

        List<String> validWords = new ArrayList<>();
        for (String word : rightLength) {
            if (checkWord(word)) {
                validWords.add(word);
            }
        }

        System.out.println("There are " + validWords.size() + " words without repeating letters.");

        List<String> noAnagrams = new ArrayList<>();
        List<String> sortedWords = new ArrayList<>();
        for (String word : validWords) {
            String sortedWord = sortString(word).toString();
            if (sortedWords.contains(sortedWord)) {
                continue;
            }
            sortedWords.add(sortedWord);
            noAnagrams.add(word);
        }

        System.out.println("There are " + noAnagrams.size() + " words that aren't anagrams.");

        List<String> sortedList = new ArrayList<>(noAnagrams);
        sortedList.sort((word1, word2) -> {
            char[] chars1 = word1.toCharArray();
            char[] chars2 = word2.toCharArray();
            for (int i = 0; i < chars1.length; i++) {
                int index1 = CUSTOM_ORDER.indexOf(chars1[i]);
                int index2 = CUSTOM_ORDER.indexOf(chars2[i]);
                if (index1 != index2) {
                    return Integer.compare(index1, index2);
                }
            }
            return 0;
        });

        System.out.println("Sorted according to custom order");
        return sortedList;
    }

    public static boolean checkWord(String word) {
        List<Character> tempUsedLetters = new ArrayList<>();
        char[] sortedChars = word.toCharArray();
        Arrays.sort(sortedChars);

        for (char letter : sortedChars) {
            if (tempUsedLetters.contains(letter)) {
                return false;
            }
            tempUsedLetters.add(letter);
        }
        return true;
    }

    public static boolean checkWordToOtherWord(List<Character> usedLetters, String word2) {
        for (char letter : word2.toCharArray()) {
            if (usedLetters.contains(letter)) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        List<String> longestRow = new ArrayList<>();
        List<String> allWordsToCheck = getAllWords();
        int index = 0;
        List<Integer> wordsTried = new ArrayList<>();
        long startTime = System.currentTimeMillis();
        for (String word : allWordsToCheck) {
            wordsTried.add(index);
            List<Integer> wordsTried2 = new ArrayList<>();
            List<Character> usedLetters1 = sortString(word);
            List<String> possibility = new ArrayList<>();
            possibility.add(word);

            List<String> longestRowForWord = new ArrayList<>();
            int index2 = 0;
            for (String word2 : allWordsToCheck) {
                wordsTried2.add(index2);
                if (wordsTried.contains(index2)) {
                    index2++;
                    continue;
                }
                index2++;

                boolean isValid = checkWordToOtherWord(usedLetters1, word2);
                if (!isValid) {
                    continue;
                }

                List<Character> usedLetters2 = sortString(word + word2);

                List<String> possibility2 = new ArrayList<>(possibility);
                possibility2.add(word2);

                if (possibility2.size() >= longestRowForWord.size()) {
                    longestRowForWord = new ArrayList<>(possibility2);
                }

                List<Integer> wordsTried3 = new ArrayList<>();
                int index3 = 0;
                for (String word3 : allWordsToCheck) {
                    wordsTried3.add(index3);
                    if (wordsTried3.contains(index3)) {
                        index3++;
                        continue;
                    }
                    index3++;

                    boolean isValid3 = checkWordToOtherWord(usedLetters2, word3);
                    if (!isValid3) {
                        continue;
                    }

                    List<Character> usedLetters3 = sortString(word + word2 + word3);

                    List<String> possibility3 = new ArrayList<>(possibility2);
                    possibility3.add(word3);

                    if (possibility3.size() >= longestRowForWord.size()) {
                        longestRowForWord = new ArrayList<>(possibility3);
                    }

                    List<Integer> wordsTried4 = new ArrayList<>();
                    int index4 = 0;
                    for (String word4 : allWordsToCheck) {
                        wordsTried4.add(index4);
                        if (wordsTried4.contains(index4)) {
                            index4++;
                            continue;
                        }
                        index4++;

                        boolean isValid4 = checkWordToOtherWord(usedLetters3, word4);
                        if (!isValid4) {
                            continue;
                        }

                        List<Character> usedLetters4 = sortString(word + word2 + word3 + word4);

                        List<String> possibility4 = new ArrayList<>(possibility3);
                        possibility4.add(word4);

                        if (possibility4.size() >= longestRowForWord.size()) {
                            longestRowForWord = new ArrayList<>(possibility4);
                        }

                        int index5 = 0;
                        for (String word5 : allWordsToCheck) {
                            if (wordsTried4.contains(index5)) {
                                index5++;
                                continue;
                            }
                            index5++;

                            boolean isValid5 = checkWordToOtherWord(usedLetters4, word5);
                            if (!isValid5) {
                                continue;
                            }

                            if (possibility4.size() + 1 > longestRowForWord.size()) {
                                longestRowForWord = new ArrayList<>(possibility4);
                                longestRowForWord.add(word5);
                            }
                        }
                    }
                }

                if (possibility.size() >= longestRowForWord.size()) {
                    longestRowForWord = new ArrayList<>(possibility);
                }
                if (longestRowForWord.size() >= longestRow.size()) {
                    longestRow = new ArrayList<>(longestRowForWord);
                }
            }
            index++;
            if (index % CHECKING_STEP == 0) {
                System.out.println("Tested " + index + " words.");
                System.out.println(longestRow);
            }
        }
        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        System.out.println("Execution time: " + duration + " milliseconds");
    }

    public static List<Character> sortString(String word) {
        char[] chars = word.toCharArray();
        Arrays.sort(chars);
        List<Character> sortedLetters = new ArrayList<>();
        for (char letter : chars) {
            sortedLetters.add(letter);
        }
        return sortedLetters;
    }
}
