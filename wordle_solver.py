"""
### HOW TO USE ###
On the command line, you'd run
`python3 wordle_solver.py`
and it'll prompt you:
`Guess a five letter word:`
and
`Results:`.

For help, type "h" or "help" at any point.
"""

from collections import defaultdict

def help():
  print("Welcome to Wordle Solver! What step do you need help with?")
  print("For results, X denotes not in word, I denotes in word but wrong place, and O denotes letter in correct spot.")
  print("For 5 words that gives 25 unique letters: fjord chunk vibex gymps waltz")

def isvalidguess(guess):
  if len(guess) != 5:
    return False
  return True

def isvalidresult(result):
  if len(result) != 5 and result != "O" and result != "X":
    return False
  for letter in result:
    if letter != 'X' and letter != 'I' and letter != 'O':
      return False
  return True

def showbestremainingwords(mode, words, foundwords, knownletters):
  for k in range(mode):
    if foundwords[k]:
      print("Game " + str(k + 1) + " words remaining: " + str(words[k]) + " COMPLETE")
      continue

    words[k] = [word.strip() for word in words[k]]
    if len(words[k]) < 13:
      print("Game " + str(k + 1) + " words remaining: " + str(words[k]))
      continue

    letterfrequencydict = {}
    for word in words[k]:
      word = word.strip()
      for i in range(len(word)):
        if knownletters[k][i] != "":
          # we only care to optimize for letter frequencies on parts of the word that is yet to be solved.
          continue
        letter = word[i]
        if letter in letterfrequencydict:
          letterfrequencydict[letter] += 1
        else:
          letterfrequencydict[letter] = 1

    remainingwordswithscores = []
    for word in words[k]:
      word = word.strip()
      alreadyusedletters = set()
      score = 0

      # Get the "score" of the word based on how frequently its letters are used in remaining valid words
      for i in range(len(word)):
        letter = word[i]
        if knownletters[k][i] != "" or letter in alreadyusedletters:
          # we only care to optimize for letter frequencies on parts of the word that is yet to be solved and is unique.
          continue
        else:
          alreadyusedletters.add(letter)
          score += letterfrequencydict[letter]

      # Fetch the 12 most valuable words to use to print to the user
      if len(remainingwordswithscores) < 12:
        remainingwordswithscores.append([word, score])
      else:
        remainingwordswithscores.sort(key = lambda x: x[1], reverse = True)
        if score > remainingwordswithscores[-1][1]:
          remainingwordswithscores.pop()
          remainingwordswithscores.append([word, score])

    print("Game " + str(k + 1) + " words remaining: " + str(remainingwordswithscores))
  print("\n")
  return

def filterwords(words, knownletters, knownwrongplacements, inword, notinword, multiletters):
  # filter first on correct letter position words
  for j in range(len(knownletters)):
    if knownletters[j] != '':
      words = [word for word in words if word[j] == knownletters[j]]

  # then filter on having correct letters
  for letter in inword:
    words = [word for word in words if letter in word]

  # then filter on not having incorrect letters
  for letter in notinword:
    words = [word for word in words if letter not in word]

  # then filter on not having right letters in wrong placements
  for j in range(len(knownwrongplacements)):
    if knownwrongplacements[j]:
      for wrongplacement in knownwrongplacements[j]:
        words = [word for word in words if word[j] != wrongplacement]

  # then, if a letter is known to appear at least twice but isn't mapped yet, then filter
  for key, value in multiletters.items():
    words = [word for word in words if word.count(key) >= value]

  return words

def submitresults(mode, foundwords):
  results = []
  for i in range(mode):
    if foundwords[i] == True:
      results.append("OOOOO")
      continue
    result = input("Results for Game " + str(i + 1) + ": ")
    while not isvalidresult(result):
      if result == "help" or result == "h":
        help()
      result = input("Results should only be made up of X/I/O and be 5 characters long: ")

    if result == "O":
      result = "OOOOO"
    elif result == "X":
      result = "XXXXX"
    results.append(result)
  return results

def takeguess():
  guess = input("Guess a five letter word: ")
  while not isvalidguess(guess):
    if guess == "help" or guess == "h":
      help()
    guess = input("Please guess a word with five letters: ")

  return guess

def playgame(words, mode):
  remainingwords = [words.copy() for _ in range(mode)]
  notinword = [set() for _ in range(mode)]
  inword = [set() for _ in range(mode)]
  knownletters = [['' for _ in range(5)] for _ in range(mode)]
  knownwrongplacements = [[[] for _ in range(5)] for _ in range(mode)]

  originalnumwords = len(words)
  validwordscount = [originalnumwords for _ in range(mode)]
  foundwords = [False for _ in range(mode)]

  numturns = 0

  while foundwords.count(True) < mode:
    tempvalidwordscount = [0 for _ in range(mode)]

    # Have user take guess, and record results
    guess = takeguess()
    guess_results = submitresults(mode, foundwords)
    numturns += 1
    for i in range(mode):
      if foundwords[i]:
        continue

      guess_result = guess_results[i]
      if guess_result == "OOOOO":
        foundwords[i] = True
        if guess in remainingwords[i]:
          remainingwords[i] = [guess]
        continue

      # Gather information based on results on letter placement, and if each letter is in the word or not
      potentiallynotinword = []

      guessletterfreq = defaultdict(int)
      yellowletters = set()
      for j in range(5):
        letter = guess[j]
        if guess_result[j] == "X":
          potentiallynotinword.append(letter)
        else:
          inword[i].add(letter)
          guessletterfreq[letter] += 1
          if guess_result[j] == "I":
            knownwrongplacements[i][j].append(letter)
            yellowletters.add(letter)
          elif guess_result[j] == "O":
            knownletters[i][j] = letter

      # get any letter that shows up at least twice but with at least one yellow
      multiletters = {}
      for key, value in guessletterfreq.items():
        if value >= 2 and key in yellowletters:
          multiletters[key] = value

      for letter in potentiallynotinword:
        if letter not in inword[i]:
          notinword[i].add(letter)

      # Filters down the list of words that can possibly remain to guess.
      remainingwords[i] = filterwords(remainingwords[i], knownletters[i], knownwrongplacements[i], inword[i], notinword[i], multiletters)

      tempvalidwordscount[i] = len(remainingwords[i])

    print("Number of possible words reduced from " + str(validwordscount) + " down to " + str(tempvalidwordscount) + ".")
    validwordscount = tempvalidwordscount

    showbestremainingwords(mode, remainingwords, foundwords, knownletters)

  print("Congrats! You've won in " + str(numturns) + " turns.")

def choosegamemode():
  print("Welcome to Wordle Solver!")
  print("What version of Wordle are you playing today?")
  print("[1] Wordle\n[2] Duordle\n[4] Quordle\n[8] Octordle")
  mode = input("Game mode: ")
  while mode != "1" and mode != "2" and mode != "4" and mode != "8":
    if mode == "help" or mode == "h":
      help()
    mode = input("Please select a valid game mode: ")

  return int(mode)

def readindictionaryofwords():
  all_words_file = open('all_words.txt', 'r')
  words = all_words_file.readlines()
  all_words_file.close

  for word in words:
    word = word.strip()

  return words

def main():
  # Reads in the list of 5 letter words available to us.
  words = readindictionaryofwords()

  # Prompts the user for their guess and the corresponding result
  mode = choosegamemode()

  playgame(words, mode)


if __name__ == '__main__':
  main()
