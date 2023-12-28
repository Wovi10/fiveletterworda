namespace FiveLetterWordCSharp;

internal static class Program
{
    private const int WordLength = 5;
    private const int CheckingStep = 1000;

    // private static readonly char[] CustomOrder2 = {'e', 's', 'i', 'a', 'r', 'n', 't', 'o', 'l', 'c', 'd', 'u', 'g', 'p', 'm', 
    //     'h', 'b', 'y', 'f', 'v', 'k', 'w', 'z', 'x', 'j', 'q'};
    private static readonly char[] CustomOrder = {'q', 'j', 'x', 'z', 'w', 'k', 'v', 'f', 'y', 'b', 'h', 'm', 'p', 'g', 'u', 
        'd', 'c', 'l', 'o', 't', 'n', 'r', 'a', 'i', 's', 'e'};

    private const int MaxNumWords = 26 / WordLength;

    private static List<string>? _allWords;
    private static readonly List<List<string>> AllCombinations = new();

    private static void Main()
    {
        var startTime = DateTime.Now;
        _allWords = GetWords();
        MakeAllCombinations();
        Console.WriteLine("All possible combinations we found.");
        foreach (var combination in AllCombinations)
        {
            Console.WriteLine(string.Join(", ", combination));
        }

        Console.WriteLine("====== Finished running. ======");
        Console.WriteLine($"This run took {CalculateTimePassed(startTime, DateTime.Now)}");
    }

    private static List<string> GetWords()
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

            var hasRepeatingLetter = HasRepeatingLetter(wordToCheck);
            if (!hasRepeatingLetter)
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

        return sortedList;
    }

    private static bool HasRepeatingLetter(string word)
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
        return word.All(letter => !usedLetters.Contains(letter));
    }

    private static void MakeAllCombinations()
    {
        WordLoop(string.Empty, new List<string>(), new List<string>(), _allWords!.GroupBy(x => x[0]));
    }

    private static List<string> WordLoop(string previousTriedGroups, List<string> previousWords, List<string> possibility, IEnumerable<IGrouping<char, string>> allGroups, int depth = 1, int counter = 0)
    {
        if (_allWords == null) 
            return possibility;

        var groups = _allWords.GroupBy(x => x[0]).Where(group => !previousTriedGroups.Contains(group.Key));
        var triedGroups = string.Empty;

        foreach (var group in allGroups)
        {
            var currentLetter = group.Key;
            triedGroups += currentLetter;
            if (previousTriedGroups.Contains(currentLetter) || string.Join("", previousWords).Distinct().Contains(currentLetter))
                continue;

            var groupList = group.ToList();
            foreach (var word in groupList)
            {
                if (depth == 1)
                {
                    possibility.Clear();
                    previousWords.Clear();
                }

                if (previousWords.Count == depth) 
                    previousWords.RemoveAt(previousWords.Count - 1);

                var (usedLetters, newPossibility) = DefaultLoopActions(word, previousWords, possibility);
                possibility = newPossibility;
                if (usedLetters == string.Empty)
                    continue;

                previousWords.Add(word);
                var words = new List<string>(previousWords);
                if (words.Count == MaxNumWords)
                {
                    Console.WriteLine("Found one");
                    AllCombinations.Add(words);
                    return possibility;
                }
                possibility = WordLoop(triedGroups, words, possibility, groups.Where(thingy => thingy.Key != currentLetter), depth + 1, counter);
                if (depth != 1) 
                    continue;

                counter++;
                if (counter % CheckingStep == 0)
                    Console.WriteLine($"Found {counter - CheckingStep}-{counter} in " +
                                      $"{(DateTime.Now - DateTime.Today.AddHours(counter))}");
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

        possibility = previousWords.Append(wordInLoop).ToList();
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
        var chars = input.ToCharArray();
        Array.Sort(chars, (a,b) => Array.IndexOf(CustomOrder, a).CompareTo(Array.IndexOf(CustomOrder, b)));
        
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