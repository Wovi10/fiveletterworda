using System.Collections;
using Microsoft.VisualBasic;

namespace FiveLetterWordCSharp;

internal static class Program
{
    private const int WordLength = 5;
    private const int CheckingStep = 1000;

    private static readonly char[] CustomOrder2 = ['e', 's', 'i', 'a', 'r', 'n', 't', 'o', 'l', 'c', 'd', 'u', 'g', 'p', 'm', 
        'h', 'b', 'y', 'f', 'v', 'k', 'w', 'z', 'x', 'j', 'q'];
    private static readonly char[] CustomOrder = ['q', 'j', 'x', 'z', 'w', 'k', 'v', 'f', 'y', 'b', 'h', 'm', 'p', 'g', 'u', 
        'd', 'c', 'l', 'o', 't', 'n', 'r', 'a', 'i', 's', 'e'];

    private const int MaxNumWords = 26 / WordLength;

    private static List<string>? _allWords;
    private static readonly List<List<string>> AllCombinations = new();

    private static void Main()
    {
        GetWords();
        MakeAllCombinations();
        foreach (var combination in AllCombinations)
        {
            Console.WriteLine(string.Join(", ", combination));
        }

        Console.WriteLine($"====== Finished running. ======");
    }

    private static void GetWords()
    {
        var filteringStartTime = DateTime.Now;
        var filePath = Path.Combine("../../..", "Files/words_alpha.txt");
        var fullPath = Path.Combine(Directory.GetCurrentDirectory(), filePath);
        var allWordsInList = File.ReadAllLines(fullPath);

        Console.WriteLine($"There are {allWordsInList.Length} words in total.");

        var correctWords = new List<string>();
        var sortedWords = new List<string>();
        foreach (var wordToCheck in allWordsInList)
        {
            if (wordToCheck.Length != WordLength)
                continue;

            var isValid = CheckWord(wordToCheck);
            if (!isValid)
                continue;

            var sortedWord = SortString(wordToCheck);
            if (sortedWords.Contains(sortedWord))
                continue;

            sortedWords.Add(sortedWord);
            correctWords.Add(wordToCheck);
        }

        Console.WriteLine($"There are {correctWords.Count} words that are the correct length, " +
                          "no anagram and do not have any repeating letters.");

        var sortedList = correctWords.OrderBy(word => word, new CustomOrderComparer()).ToList();
        Console.WriteLine("Sorted according to custom order");
        Console.WriteLine($"Created word list in {CalculateTimePassed(filteringStartTime, DateTime.Now)}");
        _allWords = sortedList;
    }

    static bool CheckWord(string word)
    {
        var tempUsedLetter = new List<char>();
        foreach (var letter in word.OrderBy(c => c))
        {
            if (tempUsedLetter.Contains(letter))
                return false;
            tempUsedLetter.Add(letter);
        }
        return true;
    }

    private static bool CheckWordToOtherWord(string usedLetters, string word)
    {
        var sortedWord = new string(word.OrderBy(character => CustomOrder.ToList().IndexOf(character)).ToArray());
        var sortedUsedLetters = new string(usedLetters.OrderBy(c => CustomOrder.ToList().IndexOf(c)).ToArray());
        return sortedWord.All(letter => !sortedUsedLetters.Contains(letter));
    }

    private static void MakeAllCombinations()
    {
        WordLoop("", [], []);
    }

    private static List<string> WordLoop(string previousTriedGroups, List<string> previousWords, List<string> possibility, int depth = 1, int counter = 0)
    {
        if (_allWords == null) return possibility;
        var groups = _allWords.GroupBy(x => x[0]);
        var triedGroups = "";
        foreach (var group in groups)
        {
            var currentLetter = group.Key;
            triedGroups += currentLetter;
            if (depth == 1 && currentLetter != 'f')
                continue;
            if (previousTriedGroups.Contains(currentLetter))
                continue;

            var groupList = group.ToList();
            foreach (var word in groupList)
            {
                if ((depth == 1 && word != "fjord") || (depth == 2 && word != "gucks") || (depth == 3 && word != "nymph") || (depth == 4 && word != "vibex"))
                    continue;
                if (previousWords.Count == depth)
                {
                    previousWords.RemoveAt(previousWords.Count - 1);
                }
                if (depth == 1)
                {
                    possibility.Clear();
                    previousWords.Clear();
                }
                var (usedLetters, newPossibility) = DefaultLoopActions(word, previousWords, possibility);
                possibility = newPossibility;
                if (usedLetters == "")
                {
                    continue;
                }
                previousWords.Add(word);
                var words = new List<string>(previousWords);
                if (depth == 4 && word == "vibex")
                {
                    Console.WriteLine();
                }
                if (words.Count == MaxNumWords)
                {
                    Console.WriteLine("WOOHOOOOOW");
                    Console.WriteLine(string.Join(", ", words));
                    AllCombinations.Add([..words]);
                    return possibility;
                }
                possibility = WordLoop(triedGroups, words, possibility, depth + 1, counter);
                if (depth != 1) continue;
                counter++;
                if (counter % CheckingStep == 0)
                {
                    Console.WriteLine($"Found {counter - CheckingStep}-{counter} in " +
                                      $"{(DateTime.Now - DateTime.Today.AddHours(counter))}");
                }
            }
        }

        return possibility;
    }

    private static (string, List<string>) DefaultLoopActions(string wordInLoop, List<string> previousWords, List<string> possibility)
    {
        var usedLetters = string.Join("", previousWords);
        if (previousWords.Contains(wordInLoop))
        {
            return ("", possibility);
        }
        var isValid = CheckWordToOtherWord(usedLetters, wordInLoop);
        if (!isValid)
        {
            return ("", possibility);
        }
        possibility = [..previousWords, wordInLoop];
        return (string.Join("", possibility), possibility);
    }

    private static string CalculateTimePassed(DateTime startTime, DateTime endTime)
    {
        var totalTime = endTime - startTime;
        var totalHours = totalTime.Hours;
        var totalMinutes = totalTime.Minutes;
        var totalSeconds = totalTime.Seconds;

        return $"{totalHours}h:{totalMinutes}m:{totalSeconds}s";
    }

    private static string SortString(string input)
    {
        char[] customOrder = ['q', 'j', 'x', 'z', 'w', 'k', 'v', 'f', 'y', 'b', 'h', 'm', 'p', 'g', 'u', 
            'd', 'c', 'l', 'o', 't', 'n', 'r', 'a', 'i', 's', 'e'];
        var chars = input.ToCharArray()
            .OrderBy(c => Array.IndexOf(customOrder, c))
            .ToArray();
        
        return new string(chars);
    }

    private class CustomOrderComparer : IComparer<string>
    {
        private readonly Dictionary<char, int> _orderDictionary;

        public CustomOrderComparer()
        {
            _orderDictionary = CustomOrder.Select((c, i) => new {Char = c, Index = i}).ToDictionary(x => x.Char, x => x.Index);
        }

        public int Compare(string x, string y)
        {
            var orderComparisonX = _orderDictionary[x[0]];
            var orderComparisonY = _orderDictionary[y[0]];
            return orderComparisonX.CompareTo(orderComparisonY);
        }
    }
}